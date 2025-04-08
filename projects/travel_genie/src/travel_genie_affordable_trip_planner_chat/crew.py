from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import ScrapeWebsiteTool
from crewai_tools import SeleniumScrapingTool
from crewai_tools import WebsiteSearchTool

@CrewBase
class TravelGenieAffordableTripPlannerChatCrew():
    """TravelGenieAffordableTripPlannerChat crew"""

    @agent
    def travel_data_integration(self) -> Agent:
        return Agent(
            config=self.agents_config['travel_data_integration'],
            tools=[ScrapeWebsiteTool(), SeleniumScrapingTool()],
        )

    @agent
    def itinerary_planner(self) -> Agent:
        return Agent(
            config=self.agents_config['itinerary_planner'],
            tools=[],
        )

    @agent
    def cost_optimizer(self) -> Agent:
        return Agent(
            config=self.agents_config['cost_optimizer'],
            tools=[],
        )

    @agent
    def map_integration(self) -> Agent:
        return Agent(
            config=self.agents_config['map_integration'],
            tools=[WebsiteSearchTool()],
        )

    @agent
    def personalization(self) -> Agent:
        return Agent(
            config=self.agents_config['personalization'],
            tools=[],
        )


    @task
    def data_retrieval(self) -> Task:
        return Task(
            config=self.tasks_config['data_retrieval'],
            tools=[ScrapeWebsiteTool(), SeleniumScrapingTool()],
        )

    @task
    def itinerary_construction(self) -> Task:
        return Task(
            config=self.tasks_config['itinerary_construction'],
            tools=[],
        )

    @task
    def cost_optimization(self) -> Task:
        return Task(
            config=self.tasks_config['cost_optimization'],
            tools=[],
        )

    @task
    def map_generation(self) -> Task:
        return Task(
            config=self.tasks_config['map_generation'],
            tools=[WebsiteSearchTool()],
        )

    @task
    def personalization_verification(self) -> Task:
        return Task(
            config=self.tasks_config['personalization_verification'],
            tools=[],
        )


    @crew
    def crew(self) -> Crew:
        """Creates the TravelGenieAffordableTripPlannerChat crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
