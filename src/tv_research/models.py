from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

Base = declarative_base()

class ResearchResult(Base):
    __tablename__ = 'research_results'

    id = Column(Integer, primary_key=True, autoincrement=True)
    topic = Column(String(500), nullable=True)
    status = Column(String(50), default='pending')  # pending, queued, running, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    result_content = Column(Text, nullable=True)
    error_message = Column(Text, nullable=True)
    execution_time = Column(Integer, nullable=True)  # in seconds
    job_id = Column(String(100), nullable=True)  # Redis job ID for tracking

    def to_dict(self):
        return {
            'id': self.id,
            'topic': self.topic,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'result_content': self.result_content,
            'error_message': self.error_message,
            'execution_time': self.execution_time
        }

# Database setup
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./data/tv_research.db')
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    pool_size=20,  # Increase pool size for concurrent workers
    max_overflow=30,  # Allow overflow connections
    pool_timeout=60,  # Increase timeout
    pool_recycle=3600  # Recycle connections after 1 hour
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()
