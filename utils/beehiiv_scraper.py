# utils/beehiiv_scraper.py
from playwright.sync_api import sync_playwright, TimeoutError
from typing import Dict, Optional, Callable, List
from datetime import datetime
import time
import os
import json

class BeehiivScraper:
    def __init__(self, cache_dir: str = 'newsletter_cache'):
        """Initialize scraper with caching directory"""
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def _get_cache_filename(self, url: str) -> str:
        """Convert URL to a valid filename for caching"""
        # Take the last part of the URL and sanitize it
        safe_name = url.split('/')[-1].replace('-', '_')
        return os.path.join(self.cache_dir, f"{safe_name}.json")
    
    def _load_from_cache(self, url: str) -> Optional[Dict]:
        """Try to load newsletter data from cache"""
        cache_file = self._get_cache_filename(url)
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Check if cache is less than 24 hours old
                    cache_time = datetime.fromisoformat(data['scraped_at'])
                    if (datetime.now() - cache_time).days < 1:
                        print(f"Loading from cache: {url}")
                        return data
            except Exception as e:
                print(f"Cache read error: {str(e)}")
        return None
    
    def _save_to_cache(self, url: str, data: Dict):
        """Save newsletter data to cache"""
        cache_file = self._get_cache_filename(url)
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Saved to cache: {url}")
        except Exception as e:
            print(f"Cache write error: {str(e)}")

    def scrape_newsletter(self, url: str) -> Optional[Dict]:
        # Try to load from cache first
        cached_data = self._load_from_cache(url)
        if cached_data:
            return cached_data
            
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context(
                    viewport={'width': 1920, 'height': 1080},
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                )
                page = context.new_page()
                page.set_default_timeout(60000)
                
                print(f"\nScraping new content: {url}")
                page.goto(url, wait_until='networkidle')
                page.wait_for_load_state('domcontentloaded')
                time.sleep(2)
                
                print("Looking for main content...")
                main_element = page.wait_for_selector('main', timeout=30000)
                if not main_element:
                    raise Exception("Main content not found")
                
                newsletter_data = {
                    'url': url,
                    'title': page.evaluate('() => document.querySelector("h1")?.innerText || ""'),
                    'date': page.evaluate('() => document.querySelector("time")?.getAttribute("datetime") || ""'),
                    'content': page.evaluate('() => document.querySelector("main")?.innerText || ""'),
                    'author': page.evaluate('() => document.querySelector(".post-author, .author")?.innerText || ""'),
                    'scraped_at': datetime.now().isoformat()
                }
                
                browser.close()
                
                if not newsletter_data['content']:
                    raise ValueError("No content extracted")
                
                # Save to cache before returning
                self._save_to_cache(url, newsletter_data)
                print(f"Successfully scraped: {newsletter_data['title']}")
                return newsletter_data
                
        except Exception as e:
            print(f"Error scraping {url}: {str(e)}")
            return None

    def process_multiple_urls(self, urls: List[str], progress_callback: Callable = None) -> List[Dict]:
        newsletters = []
        total_urls = len(urls)
        
        for i, url in enumerate(urls, 1):
            print(f"\nProcessing URL {i}/{total_urls}")
            newsletter_data = self.scrape_newsletter(url)
            
            if newsletter_data:
                newsletters.append(newsletter_data)
                print(f"Successfully scraped: {newsletter_data['title']}")
            else:
                print(f"Failed to scrape URL {i}")
            
            if progress_callback:
                progress_callback(i, total_urls)
            
            if i < total_urls:
                time.sleep(1)
                
        print(f"\nCompleted scraping {len(newsletters)}/{total_urls} newsletters")
        return newsletters