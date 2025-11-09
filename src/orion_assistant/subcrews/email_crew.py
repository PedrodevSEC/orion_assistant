from crewai import Agent, Crew, Task, Process, LLM
from config.config import Config

llm = LLM(model=Config.MODEL, api_key=Config.GOOGLE_API_KEY)

class EmailCrew:
    def __init__(self):
        self.email_agent = Agent(
            role="Assistente de E-mails",
            goal="Gerar e-mails claros, educados e coerentes com o tom do usuário.",
            backstory="Especialista em escrita de comunicação profissional.",
            llm=llm
        )

        self.email_task = Task(
            description="Escrever um e-mail de acordo com o pedido do usuário, que é: {user_input}",
            expected_output="Um e-mail formatado corretamente, com saudação e assinatura. Apenas o texto do email.",
            agent=self.email_agent
        )

    def crew(self):
        return Crew(
            agents=[self.email_agent],
            tasks=[self.email_task],
            process=Process.sequential,
            verbose=True
        )
