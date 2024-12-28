# newsletter_ai.py
from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from utils.beehiiv_scraper import BeehiivScraper
import json

class NewsletterAI:
    def __init__(self):
        self.llm = Ollama(
            model="llama3.2",
            temperature=0.7,
            base_url="http://localhost:11434"
        )
        
    def analyze_style(self, newsletters):
        """Analyze the writing style of the newsletters"""
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
        
        style_chain = LLMChain(
            llm=self.llm,
            prompt=style_analysis_prompt,
            verbose=True
        )
        
        return style_chain.run(newsletters=newsletters)
    
    def write_newsletter(self, style_guide, topic):
        """Write a new newsletter following the style guide"""
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
        
        writing_chain = LLMChain(
            llm=self.llm,
            prompt=writing_prompt,
            verbose=True
        )
        
        return writing_chain.run(style_guide=style_guide, topic=topic)

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
    # Initialize the AI and scraper
    newsletter_ai = NewsletterAI()
    scraper = BeehiivScraper(cache_dir='newsletter_cache')
    
    # Load newsletters
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
    print(result)