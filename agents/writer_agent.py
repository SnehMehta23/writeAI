# agents/writer_agent.py
from crewai import Agent
from config import get_llm

class WriterAgent:
    @staticmethod
    def create():
        return Agent(
            role='Financial Newsletter Writer',
            goal='Write engaging financial newsletters matching the established style',
            backstory="""You are a skilled financial writer with expertise in creating
            newsletters that maintain consistency with an established voice and style.
            You excel at breaking down complex financial concepts while maintaining
            the original author's tone and approach.""",
            verbose=True,
            allow_delegation=False,
            llm=get_llm()
        )