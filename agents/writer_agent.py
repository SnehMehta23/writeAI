# agents/writer_agent.py
from crewai import Agent
from config import get_llm

class WriterAgent:
    """WriterAgent class for creating specialized financial newsletter writing agents.
    This class provides functionality to create an AI agent specifically configured
    for writing financial newsletters with consistent style and voice.
    Attributes:
        None
    Methods:
        create(): Creates and returns a Financial Newsletter Writer Agent instance.
    @staticmethod
    """
    def create():
        """Creates and returns a Financial Newsletter Writer Agent.

        This function instantiates an Agent object configured specifically for writing
        financial newsletters with a consistent style and voice.

        Returns:
            Agent: An Agent object initialized with:
                - Role: Financial Newsletter Writer
                - Goal: Write engaging newsletters matching established style
                - Backstory: Expert financial writer focused on maintaining consistent voice
                - Verbose mode enabled
                - Delegation disabled
                - Custom LLM configuration
        """
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