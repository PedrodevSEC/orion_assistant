from crewai import Agent, Crew, Task, Process, LLM
from crewai.project import CrewBase, agent, task, crew
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from config.config import Config

llm = LLM(
    model=Config.MODEL,
    api_key=Config.GOOGLE_API_KEY,
    temperature=0.7
)

@CrewBase
class OrionCrew():
    """Crew principal que gerencia outras equipes"""
    
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def manager(self) -> Agent:
        return Agent(config=self.agents_config['manager'], llm=llm)

    def _load_subcrew(self, intent: str) -> Crew:
        """Carrega a sub-crew correspondente à intenção"""
        if intent == "email":
            from subcrews.email_crew import EmailCrew
            return EmailCrew().crew()
        # elif intent == "linkedin":
        #     from src.orion_assistant.subcrews.linkedin_crew import LinkedInCrew
        #     return LinkedInCrew().crew()
        # elif intent == "birthday":
        #     from src.orion_assistant.subcrews.birthday_crew import BirthdayCrew
        #     return BirthdayCrew().crew()
        # else:
        #     raise ValueError(f"Intenção '{intent}' não reconhecida.")

    def _get_intent(self, user_input: str) -> str:
        manager = self.manager()
        intent_task = Task(
            description=f"Analise o pedido e responda **APENAS COM UMA ÚNICA PALAVRA EM MINÚSCULA** que represente a intenção: email, linkedin ou aniversário. O pedido é: {user_input}",
            expected_output="Uma única palavra: email, linkedin ou aniversário.",
            agent=manager
        )
        crew = Crew(agents=[manager], tasks=[intent_task], process=Process.sequential)
        
        output = crew.kickoff()
        
       
        intent_text = output.raw if hasattr(output, "raw") else str(output)
        print(f"\n[DEBUG] Saída bruta da intenção: '{intent_text}'")
        
        return intent_text.strip().lower()

    def run(self, user_input: str):
        intent = self._get_intent(user_input)
        crew = self._load_subcrew(intent)
        return crew.kickoff(inputs={"user_input": user_input})
