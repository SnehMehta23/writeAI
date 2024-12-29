# utils/beehiiv_scraper.py
from playwright.sync_api import sync_playwright, TimeoutError
from typing import Dict, Optional, Callable, List
from datetime import datetime
import time
import os
import json

class BeehiivScraper:
    def __init__(self, cache_dir: str = 'newsletter_cache', verbose: bool = False):
        """Initialize scraper with caching directory and verbosity setting"""
        self.cache_dir = cache_dir
        self.verbose = verbose
        os.makedirs(cache_dir, exist_ok=True)
    
    def _get_cache_filename(self, url: str) -> str:
        """Convert a URL into a valid filename for caching.

        This method takes a URL and converts it into a safe filename that can be used
        for caching the scraped content. It replaces hyphens with underscores and 
        appends .json extension.

        Args:
            url (str): The URL to convert into a filename

        Returns:
            str: The sanitized filename path within the cache directory

        Example:
            >>> _get_cache_filename("https://example.com/page-name")
            "/cache/dir/page_name.json"
        """
        # Take the last part of the URL and sanitize it
        safe_name = url.split('/')[-1].replace('-', '_')
        return os.path.join(self.cache_dir, f"{safe_name}.json")
    
    def _load_from_cache(self, url: str) -> Optional[Dict]:
        cache_file = self._get_cache_filename(url)
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    cache_time = datetime.fromisoformat(data['scraped_at'])
                    if (datetime.now() - cache_time).days < 1:
                        if self.verbose:  # Move behind verbose flag
                            print(f"Loading from cache: {url}")
                        return data
            except Exception as e:
                if self.verbose:  # Move behind verbose flag
                    print(f"Cache read error: {str(e)}")
        return None

    
    def _save_to_cache(self, url: str, data: Dict):
        cache_file = self._get_cache_filename(url)
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            if self.verbose:
                print(f"Saved to cache: {url}")
        except Exception as e:
            print(f"Cache write error: {str(e)}")

    def scrape_newsletter(self, url: str) -> Optional[Dict]:
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
                
                if self.verbose:  # Move behind verbose flag
                    print(f"\nScraping new content: {url}")
                    
                page.goto(url, wait_until='networkidle')
                page.wait_for_load_state('domcontentloaded')
                time.sleep(2)
                
                if self.verbose:  # Move behind verbose flag
                    print("Looking for main content...")
                main_element = page.wait_for_selector('main', timeout=30000)
                
                newsletter_data = {
                    'url': url,
                    'title': page.evaluate('() => document.querySelector("h1")?.innerText || ""'),
                    'date': page.evaluate('() => document.querySelector("time")?.getAttribute("datetime") || ""'),
                    'content': page.evaluate('() => document.querySelector("main")?.innerText || ""'),
                    'author': page.evaluate('() => document.querySelector(".post-author, .author")?.innerText || ""'),
                    'scraped_at': datetime.now().isoformat()
                }
                
                browser.close()
                # Save to cache before returning
                self._save_to_cache(url, newsletter_data)
                return newsletter_data
                
        except Exception as e:
            if self.verbose:  # Move behind verbose flag
                print(f"Error scraping {url}: {str(e)}")
            return None

    def process_multiple_urls(self, urls: List[str], progress_callback: Callable = None) -> List[Dict]:
        """
        Process multiple newsletter URLs and scrape their content.
        This method iterates through a list of URLs, scrapes each newsletter's content,
        and provides progress updates during the process. It includes a delay between
        requests to prevent overwhelming the server.
        Args:
            urls (List[str]): A list of newsletter URLs to process.
            progress_callback (Callable, optional): A callback function to report progress.
                The callback should accept two parameters: current count and total count.
        Returns:
            List[Dict]: A list of dictionaries containing scraped newsletter data.
                Returns empty list if no newsletters could be scraped.
                Each dictionary contains newsletter details like title, content, etc.
        Example:
            >>> scraper = BeehiivScraper()
            >>> urls = ["url1", "url2"]
            >>> newsletters = scraper.process_multiple_urls(urls)
        """
        newsletters = []
        total_urls = len(urls)
        print(f"Starting to process {total_urls} newsletters...")  # Keep this
        
        for i, url in enumerate(urls, 1):
            newsletter_data = self.scrape_newsletter(url)
            
            if newsletter_data:
                newsletters.append(newsletter_data)
                print(f"[{i}/{total_urls}] ✓ Processed: {url}")  # Just print URL instead of content
            else:
                print(f"[{i}/{total_urls}] ✗ Failed to process: {url}")
            
            if progress_callback:
                progress_callback(i, total_urls)
            
            if i < total_urls:
                time.sleep(1)
        
        print(f"\nCompleted: {len(newsletters)}/{total_urls} newsletters processed")
        return newsletters