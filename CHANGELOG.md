# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Intermediate Results in Reports**: Enhanced final reports to include complete intermediate results from all research stages
  - Added "INTERMEDIATE RESULTS SUMMARY" section showing trend research, news aggregation, and content strategy outputs
  - Modified `src/tv_research/config/tasks.yaml` to include intermediate results in the reporting task
  - Reports now provide full transparency into each stage of the research pipeline

### Fixed
- **Database Initialization Error**: Fixed worker crashes caused by attempting to create existing database tables
  - Modified `src/tv_research/models.py` to handle existing tables gracefully
  - Workers now restart properly without crashing on database initialization
- **Queue Processing**: Resolved stuck jobs in news aggregation queue
  - Fixed job chaining mechanism in RQ workers
  - Modified `src/tv_research/worker.py` to manually enqueue subsequent jobs when each phase completes
  - Updated `src/tv_research/api.py` to remove incorrect RQ dependency usage
  - Queue processing now works correctly through all stages (trend research → news aggregation → content strategy → final reporting)
- **Execution Time Tracking**: Fixed execution_time field returning null values
  - Modified `src/tv_research/worker.py` to calculate execution time based on task start/completion timestamps
  - Updated `src/tv_research/main.py` to track and store actual execution time for synchronous runs
  - API now returns accurate execution times for completed research tasks

## [1.0.0] - 2025-11-03

### Added
- **Initial Project Setup**: Complete TV Research application with AI-powered content analysis
  - Multi-stage research pipeline using CrewAI agents
  - Redis Queue (RQ) for distributed task processing
  - Docker containerization with docker-compose
  - FastAPI backend API
  - Streamlit web UI
  - SQLite database for result storage
  - Modular agent architecture:
    - Trend Researcher: Identifies trending topics
    - News Aggregator: Gathers breaking news
    - Content Strategist: Develops story angles
    - Reporting Analyst: Compiles final reports

### Added (Infrastructure)
- **Docker Configuration**:
  - Multi-service docker-compose setup
  - Separate containers for API, UI, workers, and Redis
  - Health checks and service dependencies
- **Worker Management**:
  - RQ-based queue system with multiple worker types
  - Scalable worker deployment (2 workers per queue type)
  - Environment-based queue assignment
- **Database Layer**:
  - SQLAlchemy ORM with SQLite backend
  - Research result tracking with status updates
  - Job ID mapping for queue monitoring

### Added (Core Features)
- **Research Pipeline**:
  - Automated trend analysis and news aggregation
  - Content strategy development
  - Professional report generation
  - Markdown report output with structured sections
- **API Endpoints**:
  - RESTful API for triggering research tasks
  - Result retrieval and status monitoring
- **Web Interface**:
  - Streamlit-based UI for easy interaction
  - Real-time status updates
- **Examples Folder**:
  - Added examples/weekly_trends.py with usage examples
  - Demonstrates how to use the TV research system programmatically

### Technical Details
- **Dependencies**: Python 3.12, CrewAI, Redis, RQ, FastAPI, SQLAlchemy
- **Architecture**: Microservices with container orchestration
- **Data Flow**: Input → Trend Research → News Aggregation → Content Strategy → Final Report
- **Queue Types**: trend_research, news_aggregation, content_strategy, final_reporting
