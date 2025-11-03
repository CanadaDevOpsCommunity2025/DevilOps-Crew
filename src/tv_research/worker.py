import os
import redis
from rq import Worker, Queue
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from .models import ResearchResult, init_db, engine
from .crew import TVResearchCrew
from crewai import Agent, Task

# Redis connection
redis_conn = redis.from_url(os.getenv('REDIS_URL', 'redis://localhost:6379'))

# Database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

def update_task_status(task_id: int, status: str, result_content: str = None, error_message: str = None, execution_time: int = None):
    """Update task status in database"""
    db = get_db()
    try:
        task = db.query(ResearchResult).filter(ResearchResult.id == task_id).first()
        if task:
            task.status = status
            if result_content:
                task.result_content = result_content
                task.completed_at = datetime.utcnow()
                # Calculate execution time if not provided
                if execution_time is None and task.created_at:
                    execution_time = int((datetime.utcnow() - task.created_at).total_seconds())
                if execution_time is not None:
                    task.execution_time = execution_time
            if error_message:
                task.error_message = error_message
                task.completed_at = datetime.utcnow()
                # Calculate execution time for failed tasks too
                if execution_time is None and task.created_at:
                    execution_time = int((datetime.utcnow() - task.created_at).total_seconds())
                if execution_time is not None:
                    task.execution_time = execution_time
            db.commit()
    except Exception as e:
        print(f"Database error updating task {task_id}: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def run_trend_research(task_id: int, inputs: dict):
    """Worker function for trend research agent"""
    try:
        update_task_status(task_id, 'running')

        # Create trend researcher agent
        crew = TVResearchCrew()
        trend_agent = crew.trend_researcher()
        trend_task = crew.trend_research_task()

        # Run trend research
        result = trend_agent.execute_task(trend_task, inputs)

        # Store intermediate result
        update_task_status(task_id, 'trend_research_completed', str(result))

        # Enqueue next job: news aggregation
        news_queue.enqueue(run_news_aggregation, task_id, inputs, str(result))

        return result

    except Exception as e:
        update_task_status(task_id, 'failed', error_message=str(e))
        raise

def run_news_aggregation(task_id: int, inputs: dict, trend_result: str):
    """Worker function for news aggregation agent"""
    try:
        update_task_status(task_id, 'news_aggregation_running')

        # Create news aggregator agent
        crew = TVResearchCrew()
        news_agent = crew.news_aggregator()
        news_task = crew.news_aggregation_task()

        # Update inputs with trend research results
        inputs['trend_analysis'] = trend_result

        # Run news aggregation
        result = news_agent.execute_task(news_task, inputs)

        # Store intermediate result
        update_task_status(task_id, 'news_aggregation_completed', str(result))

        # Enqueue next job: content strategy
        content_queue.enqueue(run_content_strategy, task_id, inputs, str(result))

        return result

    except Exception as e:
        update_task_status(task_id, 'failed', error_message=str(e))
        raise

def run_content_strategy(task_id: int, inputs: dict, news_result: str):
    """Worker function for content strategy agent"""
    try:
        update_task_status(task_id, 'content_strategy_running')

        # Create content strategist agent
        crew = TVResearchCrew()
        content_agent = crew.content_strategist()
        content_task = crew.content_strategy_task()

        # Update inputs with previous results
        inputs['news_analysis'] = news_result

        # Run content strategy
        result = content_agent.execute_task(content_task, inputs)

        # Store intermediate result
        update_task_status(task_id, 'content_strategy_completed', str(result))

        # Enqueue next job: final reporting
        reporting_queue.enqueue(run_final_reporting, task_id, inputs, str(result))

        return result

    except Exception as e:
        update_task_status(task_id, 'failed', error_message=str(e))
        raise

def run_final_reporting(task_id: int, inputs: dict, content_result: str):
    """Worker function for final reporting agent"""
    try:
        update_task_status(task_id, 'final_reporting_running')

        # Create reporting analyst agent
        crew = TVResearchCrew()
        reporting_agent = crew.reporting_analyst()

        # Create final reporting task with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'reports/tv_research_report_{timestamp}.md'

        from crewai import Task
        reporting_task = Task(
            config=crew.tasks_config['reporting_task'],
            output_file=output_file
        )

        # Update inputs with all previous results
        inputs['content_strategy'] = content_result

        # Run final reporting
        result = reporting_agent.execute_task(reporting_task, inputs)

        # Store final result
        update_task_status(task_id, 'completed', str(result))

        return result

    except Exception as e:
        update_task_status(task_id, 'failed', error_message=str(e))
        raise

# Worker queues
trend_queue = Queue('trend_research', connection=redis_conn)
news_queue = Queue('news_aggregation', connection=redis_conn)
content_queue = Queue('content_strategy', connection=redis_conn)
reporting_queue = Queue('final_reporting', connection=redis_conn)

def run_worker(queue_name: str):
    """Run worker for specific queue"""
    worker = Worker(queue_name, connection=redis_conn)
    worker.work()

if __name__ == '__main__':
    # Initialize database
    init_db()

    # Run worker based on environment variable
    queue_name = os.getenv('WORKER_QUEUE', 'trend_research')
    run_worker(queue_name)
