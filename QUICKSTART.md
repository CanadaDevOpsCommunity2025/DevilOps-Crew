# TV Channel Research Tool - Quick Start Guide

Get up and running in 5 minutes! 🚀

## Prerequisites

- Docker and Docker Compose installed
- OpenAI API key (or compatible LLM provider)
- Optional: SerperDev API key for enhanced web search

## Step 1: Setup Environment

```bash
# Navigate to the project directory
cd tv-channel-research

# Copy environment template
cp .env.example .env

# Edit .env and add your API keys
# Required: OPENAI_API_KEY
# Optional but recommended: SERPER_API_KEY
```

**Get API Keys:**
- OpenAI: https://platform.openai.com/account/api-keys
- SerperDev: https://serper.dev/ (free tier available)

## Step 2: Build and Run

```bash
# Build the Docker container
docker compose build

# Run the default research (generates trending topics report)
docker compose up
```

That's it! Your first report will be generated in the `reports/` directory.

## Quick Examples

### Daily News Brief
```bash
docker compose run --rm tv-crew python examples/daily_news_brief.py
```

### Topic Research
```bash
docker compose run --rm tv-crew python examples/topic_research.py
```

### Weekly Trends
```bash
docker compose run --rm tv-crew python examples/weekly_trends.py
```

### Custom Topic Research
```bash
docker compose run --rm tv-crew python -c "
from examples.topic_research import research_topic
research_topic('Your Custom Topic Here')
"
```

## Output

All reports are saved to `tv-channel-research/reports/` with timestamps:
- Format: `tv_research_report_YYYYMMDD_HHMMSS.md`
- Markdown format for easy reading and sharing
- Includes comprehensive research, sources, and recommendations

## Customization

### Modify Research Parameters

Edit `src/tv_research/main.py` to change default parameters:
- `channel_type`: Type of TV programming
- `time_slot`: Target broadcast time
- `audience_demographic`: Target audience
- `production_timeline`: Available production time

### Customize Agents

Edit `src/tv_research/config/agents.yaml` to adjust:
- Agent personalities and expertise
- Research depth and focus areas
- Tone and reporting style

### Customize Tasks

Edit `src/tv_research/config/tasks.yaml` to modify:
- Research scope and requirements
- Output format and structure
- Analysis depth and priorities

## Troubleshooting

### "No API key found"
Make sure you've copied `.env.example` to `.env` and added your API keys.

### "Module not found"
Rebuild the container: `docker compose build`

### "Permission denied"
On Linux/Mac, you may need to fix permissions:
```bash
chmod -R 755 reports/
```

### Reports not generating
Check that the `reports/` directory exists and is writable inside the container.

## Need Help?

1. Check the main [README.md](README.md) for detailed documentation
2. Review example scripts in `examples/` directory
3. Examine agent and task configurations in `src/tv_research/config/`

## Next Steps

- Review your generated reports in `reports/`
- Customize agents and tasks for your specific channel
- Create scheduled runs for daily/weekly reports
- Integrate with your production workflow
- Add custom tools for specialized research needs

---

**Happy researching!** 🎬📺
