# tasks/tasks.py
from crewai import Task

class NewsletterTasks:
    @staticmethod
    def analyze_style(agent, newsletters):
        return Task(
            description=f"""
            Analyze the provided newsletters to create a comprehensive style guide.
            
            Newsletters to analyze:
            {newsletters}
            
            Focus on identifying:
            1. Writing tone and voice
            2. Common phrases and expressions
            3. Typical article structure
            4. How complex financial concepts are explained
            5. Use of examples and metaphors
            6. Paragraph length and formatting patterns
            7. Transition styles between sections
            8. Types of hooks and conclusions used
            
            Create a detailed style guide that captures all these elements.
            """,
            agent=agent,
            expected_output="A comprehensive style guide document detailing the writing patterns, tone, structure, and stylistic elements found in the analyzed newsletters."
        )

    @staticmethod
    def write_newsletter(agent, style_guide, topic):
        return Task(
            description=f"""
            Write a new financial newsletter following the provided style guide.
            
            Style Guide:
            {style_guide}
            
            Topic to cover: {topic}
            
            Requirements:
            1. Match the established tone and voice perfectly
            2. Follow the same structural patterns
            3. Explain concepts using similar approaches
            4. Maintain consistent paragraph length and formatting
            5. Use similar transition styles
            6. Create hooks and conclusions in the same style
            
            The final output should be indistinguishable from the original author's writing.
            """,
            agent=agent,
            expected_output="A complete newsletter article written in the style defined by the style guide, covering the specified topic."
        )