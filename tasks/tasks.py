# tasks/tasks.py
from crewai import Task

class NewsletterTasks:
    """A class containing static methods for newsletter-related tasks.
    This class provides functionality for analyzing newsletter styles
    and generating new newsletters based on established style guides.
    Methods
    analyze_style(agent, newsletters)
        Analyzes newsletters to create a comprehensive style guide by examining
        writing patterns, tone, structure, and other stylistic elements.
    write_newsletter(agent, style_guide, topic)
        Generates a new newsletter following a provided style guide and covering
        a specified topic.
    >>> tasks = NewsletterTasks()
    >>> style_guide = tasks.analyze_style(agent, existing_newsletters)
    >>> new_newsletter = tasks.write_newsletter(agent, style_guide, "Market Update")
    """
    @staticmethod
    def analyze_style(agent, newsletters):
        """Analyzes newsletters to create a comprehensive style guide.
        This function creates a Task object that instructs an AI agent to analyze provided newsletters
        and generate a detailed style guide focusing on various writing elements.
        Parameters:
            agent: The AI agent responsible for executing the analysis task
            newsletters (list or str): Collection of newsletters to be analyzed
        Returns:
            Task: A Task object containing the style analysis instructions and expected output
        The analysis covers:
            - Writing tone and voice
            - Common phrases and expressions
            - Article structure
            - Financial concept explanations
            - Examples and metaphors usage
            - Paragraph formatting
            - Section transitions
            - Hooks and conclusions
        Expected output format is a comprehensive style guide document detailing all analyzed elements.
        """
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
        """Generate a financial newsletter task based on provided style guide and topic.
        This function creates a Task object that instructs an AI agent to write a newsletter
        following specific style requirements and covering a given topic.
        Parameters
        ----------
        agent : Agent
            The AI agent that will execute the newsletter writing task
        style_guide : str
            Guidelines defining the writing style, tone, and formatting to follow
        topic : str
            The main subject matter to be covered in the newsletter
        Returns
        -------
        Task
            A Task object containing the newsletter writing instructions and requirements
        Example
        -------
        >>> style_guide = "Use conversational tone, 3-4 sentence paragraphs..."
        >>> topic = "Q3 Market Analysis"
        >>> task = write_newsletter(agent, style_guide, topic)
        """
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