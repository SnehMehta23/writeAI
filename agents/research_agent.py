# agents/research_agent.py
from crewai import Agent
from config import get_llm

class ResearchAgent:
    """Research Agent Class for Newsletter Style Analysis
    This class provides functionality to create specialized agents focused on analyzing
    writing styles and patterns in newsletters, particularly financial content.
    The ResearchAgent is designed to identify and analyze unique writing patterns,
    tone, structure, and stylistic elements in financial newsletters.
    Attributes:
        None
    Methods:
        create(): Creates and returns a Style Analysis Agent instance configured with
                 specific role, goals, and capabilities for newsletter analysis.
    Example:
        agent = ResearchAgent.create()
    """
    @staticmethod
    def create():
        """Create and return a Style Analysis Agent instance.

        This function initializes a specialized agent focused on analyzing writing styles and patterns
        in newsletters, particularly financial content.

        Returns:
            Agent: An Agent instance configured with:
                - Role: Style Analysis Expert
                - Goal: Newsletter writing style analysis
                - Capabilities: Content analysis, pattern recognition, and stylistic evaluation
                - Delegation: Disabled
                - Verbose mode: Enabled
        """
        return Agent(
            role='Style Analysis Expert',
            goal='Analyze newsletters to understand writing style and patterns',
            backstory="""You are an expert in content analysis and writing style recognition.
            Your specialty is analyzing financial newsletters to identify unique writing patterns,
            tone, structure, and stylistic elements. You have a deep understanding of both
            financial writing and stylistic analysis.""",
            verbose=True,
            allow_delegation=False,
            llm=get_llm()
        )