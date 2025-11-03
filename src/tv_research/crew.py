from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from datetime import datetime


@CrewBase
class TVResearchCrew:
    """TV Channel Research and Reporting Crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self):
        # Initialize tools that will be shared across agents
        self.search_tool = SerperDevTool()
        self.scrape_tool = ScrapeWebsiteTool()

    @agent
    def trend_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['trend_researcher'],
            tools=[self.search_tool, self.scrape_tool],
            verbose=True,
            allow_delegation=False
        )

    @agent
    def news_aggregator(self) -> Agent:
        return Agent(
            config=self.agents_config['news_aggregator'],
            tools=[self.search_tool, self.scrape_tool],
            verbose=True,
            allow_delegation=False
        )

    @agent
    def content_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config['content_strategist'],
            verbose=True,
            allow_delegation=False
        )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['reporting_analyst'],
            verbose=True,
            allow_delegation=False
        )

    @task
    def trend_research_task(self) -> Task:
        return Task(
            config=self.tasks_config['trend_research_task'],
        )

    @task
    def news_aggregation_task(self) -> Task:
        return Task(
            config=self.tasks_config['news_aggregation_task'],
        )

    @task
    def content_strategy_task(self) -> Task:
        return Task(
            config=self.tasks_config['content_strategy_task'],
        )

    @task
    def reporting_task(self) -> Task:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'reports/tv_research_report_{timestamp}.md'

        return Task(
            config=self.tasks_config['reporting_task'],
            output_file=output_file
        )

    @crew
    def crew(self) -> Crew:
        """Creates the TV Research crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
