# agents/research_agent.py
from crewai import Agent
from config import get_llm

class ResearchAgent:
    @staticmethod
    def create():
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