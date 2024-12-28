# main.py
from crewai import Crew
from agents.research_agent import ResearchAgent
from agents.writer_agent import WriterAgent
from tasks.tasks import NewsletterTasks
from utils.beehiiv_scraper import BeehiivScraper

def progress_callback(current, total):
    """Simple progress indicator"""
    print(f"Progress: {current}/{total} newsletters processed")

def load_newsletter_urls():
    """Return list of your Beehiiv newsletter URLs"""
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

def load_example_newsletters():
    """Load newsletters from Beehiiv URLs with progress tracking"""
    print("\nStarting newsletter scraping process...")
    
    urls = load_newsletter_urls()
    scraper = BeehiivScraper(cache_dir='newsletter_cache')
    newsletters = scraper.process_multiple_urls(urls, progress_callback)
    
    if not newsletters:
        raise Exception("No newsletters were successfully scraped!")
    
    print(f"\nSuccessfully scraped {len(newsletters)} newsletters")
    
    # Format the newsletters for the research agent
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
    
    return "\n".join(formatted_content)

def main():
    try:
        # Initialize agents
        print("Initializing agents...")
        research_agent = ResearchAgent.create()
        writer_agent = WriterAgent.create()
        
        # Load previous newsletters
        print("Loading newsletters...")
        newsletters = load_example_newsletters()
        
        print("Creating tasks...")
        # Create tasks
        analyze_task = NewsletterTasks.analyze_style(
            agent=research_agent,
            newsletters=newsletters
        )
        
        write_task = NewsletterTasks.write_newsletter(
            agent=writer_agent,
            style_guide="Will be provided by research agent",
            topic="Current Market Analysis"  # Can be dynamically set
        )
        
        # Create crew
        print("Starting CrewAI process...")
        crew = Crew(
            agents=[research_agent, writer_agent],
            tasks=[analyze_task, write_task],
            verbose=True
        )
        
        # Execute tasks
        result = crew.kickoff()
        
        return result
        
    except Exception as e:
        print(f"Error in main process: {str(e)}")
        raise

if __name__ == "__main__":
    result = main()
    print("\nFinal Result:")
    print(result)