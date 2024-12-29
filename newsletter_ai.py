# newsletter_ai.py
"""A script that uses AI to analyze and generate financial newsletters in the style of existing ones.
The script uses LangChain and Ollama to analyze writing patterns from scraped Beehiiv newsletters
and generate new newsletters that match the identified style. It leverages web scraping, natural
language processing, and AI text generation.
Classes:
    NewsletterAI: Handles AI analysis and generation of newsletters
Functions:
    load_newsletter_urls(): Returns list of Beehiiv newsletter URLs to analyze
    main(): Orchestrates the newsletter analysis and generation workflow
Usage:
    Run the script directly to analyze newsletters and generate a new one:
    $ python newsletter_ai.py
    - langchain
    - ollama
    - Custom BeehiivScraper utility
    - Local Ollama instance running on port 11434
Output Files:
    - style_guide.txt: Analysis of writing style from source newsletters
    - generated_newsletter.txt: The newly generated newsletter content
    >>> python newsletter_ai.py
    Starting newsletter scraping process...
    Analyzing newsletter style...
    Style guide saved to style_guide.txt
    Writing new newsletter...
    New newsletter saved to generated_newsletter.txt"""
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnableSequence
from langchain.chains import LLMChain
from utils.beehiiv_scraper import BeehiivScraper
import json

class NewsletterAI:
    """A class that uses AI to analyze and generate financial newsletters.
    This class leverages the Ollama language model to analyze the writing style of existing newsletters
    and generate new ones that match the identified style patterns.
    Attributes:
        llm (Ollama): The language model instance configured with specific parameters.
    Methods:
        analyze_style(newsletters): Analyzes writing style of given newsletters and creates a style guide.
        write_newsletter(style_guide, topic): Generates a new newsletter following a given style guide.
    Example:
        >>> ai = NewsletterAI()
        >>> style_guide = ai.analyze_style(existing_newsletters)
        >>> new_newsletter = ai.write_newsletter(style_guide, "Market Trends 2024")
    """
    def __init__(self):
        self.llm = OllamaLLM(
            model="llama3.2",
            temperature=0.7,
            base_url="http://localhost:11434"
        )
        
    def analyze_style(self, newsletters):
        """Analyzes newsletters to create a comprehensive style guide."""
        style_analysis_prompt = PromptTemplate(
            input_variables=["newsletters"],
            template="""
            Analyze the following newsletters and create a comprehensive style guide.
            
            Newsletters:
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
            
            Provide a detailed style guide that captures all these elements.
            """
        )
        
        # New syntax using RunnableSequence
        chain = style_analysis_prompt | self.llm
        
        # Use invoke instead of run
        return chain.invoke({"newsletters": newsletters})
    
    def write_newsletter(self, style_guide, topic):
        """Write a new newsletter following a specified style guide and topic."""
        writing_prompt = PromptTemplate(
            input_variables=["style_guide", "topic"],
            template="""
            Write a financial newsletter following this style guide:
            
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
            """
        )
        
        # New syntax using RunnableSequence
        chain = writing_prompt | self.llm
        
        # Use invoke instead of run
        return chain.invoke({
            "style_guide": style_guide,
            "topic": topic
        })

def load_newsletter_urls():
    return [
        "https://lootbag.beehiiv.com/p/closer-look-feds-2-inflation-target",
        "https://lootbag.beehiiv.com/p/landlord-artificial-intelligence",
        "https://lootbag.beehiiv.com/p/connecting-dots-economic-projections-trail-mix-portfolio",
        "https://lootbag.beehiiv.com/p/stock-picking-alive-well",
        "https://lootbag.beehiiv.com/p/orange-coin",
        "https://lootbag.beehiiv.com/p/treasury-bonds-shaken-not-stirred",
        "https://lootbag.beehiiv.com/p/market-momentum",
        "https://lootbag.beehiiv.com/p/made-india",
        "https://lootbag.beehiiv.com/p/chips-ahoy",
        "https://lootbag.beehiiv.com/p/retail-resurgence"
    ]

def main():
    """Main execution function for the newsletter generation process.
    This function orchestrates the entire newsletter generation workflow:
    1. Initializes the AI and web scraper components
    2. Scrapes newsletters from provided URLs
    3. Formats the scraped content
    4. Analyzes the writing style
    5. Generates a new newsletter based on the analyzed style
    Raises:
        Exception: If no newsletters were successfully scraped
    Returns:
        str: The generated newsletter content
    Files created:
        - style_guide.txt: Contains the analyzed writing style guide
        - generated_newsletter.txt: Contains the newly generated newsletter"""
    # Initialize the AI and scraper
    newsletter_ai = NewsletterAI()
    scraper = BeehiivScraper(cache_dir='newsletter_cache', verbose=False)
    
    print("\nStarting newsletter scraping process...")
    urls = load_newsletter_urls()
    newsletters = scraper.process_multiple_urls(urls)
    
    if not newsletters:
        raise Exception("No newsletters were successfully scraped!")
    
    # Format newsletters for analysis
    formatted_content = []
    for newsletter in newsletters:
        formatted_content.append(
            f"""
            Title: {newsletter['title']}
            Date: {newsletter['date']}
            Author: {newsletter['author']}
            
            Content:
            {newsletter['content']}
            
            -------------------
            """
        )
    
    newsletter_text = "\n".join(formatted_content)
    
    # Analyze style
    print("\nAnalyzing newsletter style...")
    style_guide = newsletter_ai.analyze_style(newsletter_text)
    
    # Save style guide
    with open('style_guide.txt', 'w', encoding='utf-8') as f:
        f.write(style_guide)
        print("\nStyle guide saved to style_guide.txt")
    
    # Write new newsletter
    print("\nWriting new newsletter...")
    new_newsletter = newsletter_ai.write_newsletter(
        style_guide=style_guide,
        topic="Margin Expansion and Earnings Per Share Growth"
    )
    
    # Save new newsletter
    with open('generated_newsletter.txt', 'w', encoding='utf-8') as f:
        f.write(new_newsletter)
        print("\nNew newsletter saved to generated_newsletter.txt")
    
    return new_newsletter

if __name__ == "__main__":
    result = main()
    print("\nFinal Result:")
    # print(result)