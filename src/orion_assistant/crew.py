from crewai import Agent, Crew, Task, Process, LLM
from crewai.project import CrewBase, agent, task, crew, before_kickoff, after_kickoff
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from src.orion_assistant.config import Config

llm = LLM(
    model=Config.MODEL,
    api_key=Config.GOOGLE_API_KEY,
    temperature=0.7
)

@CrewBase
class OrionCrew():
    
    agents = List[BaseAgent]
    tasks = List[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            verbose=True,
        )
    
    @task
    def search_task(self) -> Agent:
        return Task(
            config=self.tasks_config['search_task']
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents, 
            tasks=self.tasks,   
            process=Process.sequential,
            verbose=True,
        )