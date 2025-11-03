from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
import time
from datetime import datetime
import redis
from rq import Queue
import os

from .models import ResearchResult, get_db, init_db
from .worker import (
    trend_queue, news_queue, content_queue, reporting_queue,
    run_trend_research, run_news_aggregation, run_content_strategy, run_final_reporting
)

app = FastAPI(title="TV Research API", description="API for TV Channel Research", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for API
class ResearchRequest(BaseModel):
    topic: Optional[str] = None

class ResearchResponse(BaseModel):
    id: int
    topic: Optional[str]
    status: str
    created_at: Optional[str]
    completed_at: Optional[str]
    result_content: Optional[str]
    error_message: Optional[str]
    execution_time: Optional[int]

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    init_db()

def enqueue_research_workflow(result_id: int, topic: Optional[str]):
    """Enqueue the complete research workflow"""
    # Prepare inputs for the research workflow
    if topic:
        inputs = {
            'channel_type': f'Special Report on {topic}',
            'time_slot': 'Prime Time Documentary/Special Segment',
            'audience_demographic': f'Educated general audience interested in {topic}',
            'production_timeline': '1-2 weeks for comprehensive coverage',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'research_focus': topic
        }
    else:
        inputs = {
            'channel_type': 'News and Entertainment',
            'time_slot': 'Prime Time',
            'audience_demographic': 'General audience aged 25-54',
            'production_timeline': '24-48 hours',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

    # Enqueue trend research first
    trend_job = trend_queue.enqueue(run_trend_research, result_id, inputs)

    # Chain the jobs: trend -> news -> content -> reporting
    news_job = news_queue.enqueue(run_news_aggregation, result_id, inputs,
                                  depends_on=trend_job)
    content_job = content_queue.enqueue(run_content_strategy, result_id, inputs,
                                        depends_on=news_job)
    reporting_job = reporting_queue.enqueue(run_final_reporting, result_id, inputs,
                                            depends_on=content_job)

    return trend_job.id

@app.post("/research", response_model=ResearchResponse)
async def start_research(request: ResearchRequest, db: Session = Depends(get_db)):
    """Start a new research task using Redis queues"""
    # Create new research result record
    result = ResearchResult(topic=request.topic, status='queued')
    db.add(result)
    db.commit()
    db.refresh(result)

    # Enqueue the research workflow
    try:
        job_id = enqueue_research_workflow(result.id, request.topic)
        # Store job ID for tracking (optional)
        result.job_id = job_id
        db.commit()
    except Exception as e:
        result.status = 'failed'
        result.error_message = f"Failed to enqueue job: {str(e)}"
        db.commit()

    return ResearchResponse(**result.to_dict())

@app.get("/research/{result_id}", response_model=ResearchResponse)
async def get_research_result(result_id: int, db: Session = Depends(get_db)):
    """Get a specific research result"""
    try:
        result = db.query(ResearchResult).filter(ResearchResult.id == result_id).first()
        if not result:
            raise HTTPException(status_code=404, detail="Research result not found")
        return ResearchResponse(**result.to_dict())
    except Exception as e:
        # Handle database connection issues
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/research", response_model=List[ResearchResponse])
async def list_research_results(limit: int = 50, offset: int = 0, db: Session = Depends(get_db)):
    """List all research results"""
    try:
        results = db.query(ResearchResult).order_by(ResearchResult.created_at.desc()).limit(limit).offset(offset).all()
        return [ResearchResponse(**result.to_dict()) for result in results]
    except Exception as e:
        # Handle database connection issues
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.delete("/research/{result_id}")
async def delete_research_result(result_id: int, db: Session = Depends(get_db)):
    """Delete a research result"""
    result = db.query(ResearchResult).filter(ResearchResult.id == result_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Research result not found")

    db.delete(result)
    db.commit()
    return {"message": "Research result deleted successfully"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.get("/metrics")
async def get_metrics():
    """Get system metrics and statistics"""
    try:
        # Get research statistics
        db = get_db()
        try:
            total_research = db.query(ResearchResult).count()
            completed_research = db.query(ResearchResult).filter(ResearchResult.status == 'completed').count()
            failed_research = db.query(ResearchResult).filter(ResearchResult.status == 'failed').count()
            active_research = db.query(ResearchResult).filter(
                ResearchResult.status.in_([
                    'running', 'queued', 'trend_research_completed',
                    'news_aggregation_completed', 'content_strategy_completed',
                    'final_reporting_running'
                ])
            ).count()

            # Calculate success rate
            success_rate = (completed_research / total_research * 100) if total_research > 0 else 0

            # Get recent activity (last 10)
            recent_research = db.query(ResearchResult).order_by(
                ResearchResult.created_at.desc()
            ).limit(10).all()

            recent_activity = []
            for research in recent_research:
                recent_activity.append({
                    'id': research.id,
                    'topic': research.topic,
                    'status': research.status,
                    'created_at': research.created_at.isoformat() if research.created_at else None,
                    'execution_time': research.execution_time
                })

            # Calculate performance metrics
            completed_times = [r.execution_time for r in db.query(ResearchResult).filter(
                ResearchResult.status == 'completed',
                ResearchResult.execution_time.isnot(None)
            ).all()]

            avg_execution_time = sum(completed_times) / len(completed_times) if completed_times else 0

            return {
                "research_stats": {
                    "total": total_research,
                    "completed": completed_research,
                    "failed": failed_research,
                    "active": active_research,
                    "success_rate": round(success_rate, 1)
                },
                "performance": {
                    "avg_execution_time": round(avg_execution_time, 1),
                    "execution_time_distribution": {
                        "fast": len([t for t in completed_times if t < 30]),
                        "medium": len([t for t in completed_times if 30 <= t < 120]),
                        "slow": len([t for t in completed_times if t >= 120])
                    }
                },
                "recent_activity": recent_activity,
                "system_status": {
                    "api": "healthy",
                    "database": "connected",
                    "timestamp": datetime.utcnow().isoformat()
                }
            }

        finally:
            db.close()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Metrics error: {str(e)}")

@app.get("/queue/status")
async def get_queue_status():
    """Get Redis queue status"""
    try:
        # Import here to avoid issues if Redis is not available
        from .worker import trend_queue, news_queue, content_queue, reporting_queue

        return {
            "queues": {
                "trend_research": trend_queue.count,
                "news_aggregation": news_queue.count,
                "content_strategy": content_queue.count,
                "final_reporting": reporting_queue.count
            },
            "timestamp": datetime.utcnow().isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Queue status error: {str(e)}")
