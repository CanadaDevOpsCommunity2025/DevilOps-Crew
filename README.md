# DevilOps Crew
Canada DevOps Community of Practice - Toronto Hackathon Series - Team 13

Project Name - DevilOps Crew

Team Mentor -

Participant Names - 

     Team Lead - Francis Sujai Arokiaraj
     Team Members - Derek Xu, Francis Sujai Arokiaraj, Saurabh Kamboj, Shujuan (Susan) Jia

# TV Channel Research & Reporting Tool

A specialized CrewAI-powered tool for TV channels to research and report on trending topics, breaking news, and content opportunities.

## 🎬 Overview

This tool uses AI agents to:
- **Research specific topics** in-depth for special segments and documentaries
- **Monitor trending topics** across social media, news, and entertainment platforms
- **Aggregate breaking news** from multiple credible sources
- **Analyze content potential** for TV segments and programming
- **Generate production-ready reports** with story angles, sources, and recommendations

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- OpenAI API key (or other LLM provider)

### Setup

1. **Navigate to the project directory**:
```bash
cd tv-channel-research
```

2. **Configure environment**:
```bash
cp .env.example .env
# Edit .env and add your API keys
```

3. **Build and run all services**:
```bash
docker compose up --build
```

4. **Access the application**:
   - **Web UI**: http://localhost:8501
   - **API Documentation**: http://localhost:8000/docs
   - **API Health Check**: http://localhost:8000/health

### Research Specific Topics

To research a specific topic instead of trending topics:

**Option 1: Environment Variable**
```bash
# Set in .env file
RESEARCH_TOPIC="Artificial Intelligence in Healthcare"

# Then run
docker compose up --build
```

**Option 2: Command Line Arguments**
```bash
# Pass topic as command line argument
docker compose run --rm tv-crew python -m tv_research.main "Climate Change"
```

**Option 3: Using Examples**
```bash
# Use the existing topic research example
docker compose run --rm tv-crew python examples/topic_research.py
```

When no topic is specified, the tool performs general trending topics research.

## 📋 Features

### Multi-Agent Research System
- **Trend Researcher**: Identifies viral topics and emerging trends
- **News Aggregator**: Gathers and verifies breaking news from multiple sources
- **Content Strategist**: Develops story angles and production recommendations
- **Reporting Analyst**: Compiles comprehensive broadcast-ready reports

### Specialized Tools
- **Social Media Trends Monitor**: Tracks trending topics on Twitter, Reddit, etc.
- **News API Integration**: Aggregates breaking news from major outlets
- **Content Analyzer**: Evaluates stories for TV broadcast potential
- **Report Generator**: Creates structured reports for producers

### Output Formats
- Comprehensive research reports (Markdown)
- Quick briefing summaries
- Topic rankings with engagement metrics
- Story angle recommendations with visual elements

### Web Interface & API
- **Interactive Web UI**: Easy-to-use interface for starting research and viewing results
- **REST API**: Programmatic access to all research functionality
- **Result Persistence**: Database storage of all research results
- **Background Processing**: Asynchronous research execution
- **Real-time Status Updates**: Live progress tracking

## 🎯 Use Cases

### Daily News Research
```bash
docker compose run --rm tv-crew python examples/daily_news_brief.py
```
Generates morning/evening news briefings with top stories and trends.

### Topic Deep Dive
```bash
docker compose run --rm tv-crew python examples/topic_research.py --topic "AI Technology"
```
Comprehensive research on specific topics for special segments.

### Weekly Trending Report
```bash
docker compose run --rm tv-crew python examples/weekly_trends.py
```
Weekly roundup of trending topics perfect for weekend programming.

### Breaking News Analysis
```bash
docker compose run --rm tv-crew python examples/breaking_news.py
```
Rapid analysis of breaking news with broadcast angles.

## 📂 Project Structure

```
tv-channel-research/
├── src/
│   └── tv_research/
│       ├── __init__.py
│       ├── main.py                    # Main entry point
│       ├── crew.py                    # Crew definition
│       ├── api.py                     # FastAPI backend
│       ├── ui.py                      # Streamlit web interface
│       ├── models.py                  # Database models
│       ├── config/
│       │   ├── agents.yaml           # Agent configurations
│       │   └── tasks.yaml            # Task definitions
│       └── tools/
│           ├── __init__.py
│           ├── trend_monitor.py      # Social media trends
│           ├── news_aggregator.py    # News gathering
│           └── content_analyzer.py   # Content evaluation
├── examples/
│   ├── daily_news_brief.py           # Daily briefing example
│   ├── topic_research.py             # Deep dive research
│   ├── weekly_trends.py              # Weekly trends report
│   └── breaking_news.py              # Breaking news analysis
├── reports/                           # Generated reports
├── data/
│   └── tv_research.db                 # SQLite database (created automatically)
├── docker-compose.yml                 # Docker Compose config
├── Dockerfile                         # Container definition
├── pyproject.toml                     # Dependencies
├── .env.example                       # Environment template
└── README.md                          # This file
```

## 🏗️ Scalable Architecture

The application now uses a **distributed, queue-based architecture** for maximum scalability:

### Architecture Overview

```
┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐
│   Web UI        │────│   FastAPI    │────│    Redis Queue  │
│   (Streamlit)   │    │   (Router)   │    │   (Message Bus) │
└─────────────────┘    └──────────────┘    └─────────────────┘
                                │                    │
                                │                    │
                       ┌────────▼────────┐    ┌────▼────────────────┐
                       │   Database      │    │   Worker Services   │
                       │ (SQLite/PostgreSQL)│    │                   │
                       └─────────────────┘    │ • Trend Research    │
                                              │ • News Aggregation  │
                                              │ • Content Strategy  │
                                              │ • Final Reporting   │
                                              └─────────────────────┘
```

### Key Components

- **Redis Queue**: Message broker for task distribution
- **Worker Services**: Specialized containers for each agent type
- **API Router**: Enqueues tasks and manages workflow
- **Database**: Stores results and task status
- **Web UI**: User interface for task submission and monitoring

### Worker Services

Each agent runs in its own scalable container:

- **worker-trend** (2 replicas): Trend research and analysis
- **worker-news** (2 replicas): News aggregation and verification
- **worker-content** (1 replica): Content strategy development
- **worker-reporting** (1 replica): Final report generation

### Scaling Benefits

- **Horizontal Scaling**: Add more worker instances as needed
- **Fault Tolerance**: Workers can fail independently
- **Load Distribution**: Tasks automatically distributed across workers
- **Resource Efficiency**: Scale specific components based on load
- **Cloud Ready**: Perfect for Kubernetes/Docker Swarm deployment

## 🌐 Web Interface & API

### Web Interface (Streamlit)

Access the web interface at http://localhost:8501 after running `docker compose up`.

**Features:**
- **New Research Tab**: Start research on specific topics or trending topics
- **Research History Tab**: View all previous research results with status tracking
- **Real-time Updates**: Live progress tracking during research execution
- **Result Management**: View, expand, and delete research results

**Usage:**
1. Navigate to the "New Research" tab
2. Enter a topic (optional) or leave blank for trending topics
3. Click "Start Research" to begin
4. Monitor progress in real-time
5. View results when complete

### REST API

The API provides programmatic access to all research functionality.

**Base URL:** http://localhost:8000
**Documentation:** http://localhost:8000/docs (Swagger UI)

**Endpoints:**

#### Start Research
```http
POST /research
Content-Type: application/json

{
  "topic": "optional topic name"
}
```

**Response:**
```json
{
  "id": 1,
  "topic": "optional topic name",
  "status": "queued",
  "created_at": "2025-11-02T12:33:35.000Z",
  "completed_at": null,
  "result_content": null,
  "error_message": null,
  "execution_time": null
}
```

#### Get Research Result
```http
GET /research/{result_id}
```

#### List All Research Results
```http
GET /research?limit=50&offset=0
```

#### Delete Research Result
```http
DELETE /research/{result_id}
```

#### Health Check
```http
GET /health
```

**Python Example:**
```python
import requests

# Start research
response = requests.post("http://localhost:8000/research",
                        json={"topic": "Climate Change"})
result = response.json()
research_id = result["id"]

# Check status - now shows detailed workflow progress
while True:
    status = requests.get(f"http://localhost:8000/research/{research_id}").json()
    print(f"Status: {status['status']}")  # Shows: queued, running, trend_research_completed, etc.

    if status["status"] == "completed":
        print("Research complete!")
        print(status["result_content"])
        break
    elif status["status"] == "failed":
        print(f"Research failed: {status['error_message']}")
        break
    time.sleep(5)
```

### Docker Services

The application now runs as multiple scalable services:

**Core Services:**
- **redis**: Redis message queue (port 6379)
- **api**: FastAPI backend/router (port 8000)
- **ui**: Streamlit web interface (port 8501)

**Worker Services:**
- **worker-trend**: Trend research workers (2 replicas)
- **worker-news**: News aggregation workers (2 replicas)
- **worker-content**: Content strategy worker (1 replica)
- **worker-reporting**: Final reporting worker (1 replica)

**Legacy Service:**
- **tv-crew**: CLI service (for backward compatibility)

**Start all services:**
```bash
docker compose up --build
```

**Start only core services:**
```bash
docker compose up redis api ui --build
```

**Scale specific workers:**
```bash
# Scale trend research workers
docker compose up --scale worker-trend=5

# Scale news aggregation workers
docker compose up --scale worker-news=3
```

**Run CLI research (legacy):**
```bash
docker compose run --rm tv-crew python -m tv_research.main "Your Topic"
```

### Worker Management

Use the worker management script for local development:

```bash
# Check queue status
python src/tv_research/manage_workers.py status

# Start all workers
python src/tv_research/manage_workers.py start

# Start specific queue workers
python src/tv_research/manage_workers.py start --queue trend_research --workers 3
```

## 🔧 Configuration

### Agent Customization

Edit `src/tv_research/config/agents.yaml` to customize agent behavior:
- Adjust research depth and focus areas
- Modify tone and reporting style
- Add domain-specific expertise

### Task Workflows

Edit `src/tv_research/config/tasks.yaml` to:
- Change research parameters
- Adjust output formats
- Customize report structure

### Tool Integration

Add new tools in `src/tv_research/tools/`:
- Custom API integrations
- Specialized analyzers
- Export formatters

## 📊 Sample Outputs

### Daily News Brief
```markdown
# TV Channel Daily News Brief - [Date]

## Top Trending Topics
1. **[Topic Name]** - Engagement Score: 95/100
   - Sources: [List]
   - Story Angle: [Recommendation]
   - Visual Elements: [Suggestions]

## Breaking News
- **[Headline]** - [Source]
  - Impact: High/Medium/Low
  - Coverage Recommendation: [Details]
...
```

### Topic Research Report
```markdown
# In-Depth Research: [Topic Name]

## Executive Summary
[Overview and key findings]

## Trend Analysis
[Detailed trend data and patterns]

## Story Angles
1. [Angle 1]: [Description and rationale]
2. [Angle 2]: [Description and rationale]

## Interview Subjects
- [Expert 1]: [Credentials and contact]
- [Expert 2]: [Credentials and contact]

## Visual Elements
[Recommendations for graphics, footage, etc.]

## Production Notes
[Timing, resources, and technical requirements]
```

## 🧪 Testing & Validation

### Container Validation

Use the validation script to test all containers:

```bash
# Validate all running containers
python scripts/validate_containers.py

# Wait for services to start before validating
python scripts/validate_containers.py --wait 60

# Test against different base URL
python scripts/validate_containers.py --url http://your-server.com
```

### API Testing

Run comprehensive API tests:

```bash
# Run all API tests (requires running containers)
python tests/test_api.py

# Run only basic endpoint tests
python tests/test_api.py --skip-integration

# Test against different API URL
python tests/test_api.py --url http://your-api-server:8000
```

### Worker Management

Manage worker processes:

```bash
# Check queue status
python src/tv_research/manage_workers.py status

# Start all workers locally
python src/tv_research/manage_workers.py start

# Start specific worker type
python src/tv_research/manage_workers.py start --queue trend_research --workers 3
```

## 🚀 CI/CD Pipeline

The project includes a comprehensive GitHub Actions CI/CD pipeline:

### Pipeline Stages:
1. **Test**: Code linting and basic import tests
2. **Build & Test Containers**: Docker build, container validation, API tests
3. **Security Scan**: Vulnerability scanning with Trivy
4. **Deploy**: Automated deployment to staging/production

### Running Tests Locally:

```bash
# Run the same tests as CI/CD
docker compose up -d --build
sleep 60  # Wait for services
python scripts/validate_containers.py --wait 10
python tests/test_api.py --skip-integration
docker compose down -v
```

## 🎬 Development Commands

All commands run inside Docker containers:

```bash
# Run daily news brief
docker compose run --rm tv-crew python examples/daily_news_brief.py

# Research specific topic
docker compose run --rm tv-crew python examples/topic_research.py

# Interactive Python shell
docker compose run --rm tv-crew python

# Shell access for debugging
docker compose run --rm tv-crew bash

# Run custom research
docker compose run --rm tv-crew python -c "
from src.tv_research.crew import TVResearchCrew
crew = TVResearchCrew().crew()
result = crew.kickoff(inputs={
    'topic': 'Climate Change',
    'depth': 'comprehensive',
    'format': 'broadcast'
})
"
```

## 🔐 Environment Variables

Required variables in `.env`:

```env
# LLM Configuration
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4  # or gpt-3.5-turbo

# Optional: News API
NEWS_API_KEY=your_news_api_key

# Optional: Social Media APIs
TWITTER_BEARER_TOKEN=your_token
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_secret

# Report Configuration
REPORT_OUTPUT_DIR=/app/reports
DEFAULT_RESEARCH_DEPTH=comprehensive

# Research Topic (optional - leave empty for trending topics research)
# RESEARCH_TOPIC=Artificial Intelligence in Healthcare
```

## 📈 Adding New Features

### New Research Source

1. Create tool in `src/tv_research/tools/`:
```python
from crewai.tools import BaseTool

class YourNewTool(BaseTool):
    name: str = "Your Tool Name"
    description: str = "What it does"

    def _run(self, query: str) -> str:
        # Implementation
        return results
```

2. Add to agent in `crew.py`:
```python
@agent
def researcher(self) -> Agent:
    return Agent(
        config=self.agents_config['trend_researcher'],
        tools=[YourNewTool()],
        verbose=True
    )
```

3. Rebuild container:
```bash
docker compose build
```

### New Report Format

1. Add task in `config/tasks.yaml`
2. Create corresponding task in `crew.py`
3. Test with `docker compose run`

## 🎯 Best Practices

1. **API Rate Limits**: Configure delays and caching for external APIs
2. **Data Freshness**: Schedule regular runs for up-to-date information
3. **Source Verification**: Always cross-reference multiple sources
4. **Report Archiving**: Save reports with timestamps for historical reference
5. **Customization**: Adjust agents and tasks for your specific channel's needs

## 🤝 Support & Contribution

For issues, improvements, or custom features:
- Report bugs and request features via issues
- Contribute custom tools and examples
- Share successful configurations

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

```
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

---

**Built for TV professionals who need fast, accurate, and actionable research.** 🎬📺
