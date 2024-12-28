# test_scraper.py
from utils.beehiiv_scraper import BeehiivScraper
import json

def test_single_url():
    url = "https://lootbag.beehiiv.com/p/closer-look-feds-2-inflation-target"
    scraper = BeehiivScraper()
    
    print("\n=== Starting Scraper Test ===")
    result = scraper.scrape_newsletter(url)
    
    if result:
        print("\n=== Scraping Successful ===")
        # Save full results to a file
        with open('scraped_content.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print("\nFull results saved to 'scraped_content.json'")
        
        # Print preview of each field
        for key, value in result.items():
            if isinstance(value, str) and len(value) > 100:
                print(f"\n{key} (preview): {value[:100]}...")
            else:
                print(f"\n{key}: {value}")
    else:
        print("\n=== Scraping Failed! ===")

if __name__ == "__main__":
    test_single_url()