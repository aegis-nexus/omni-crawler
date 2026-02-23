import requests
import logging
from bs4 import BeautifulSoup

logger = logging.getLogger("OmniCrawler.ITHome")

def fetch():
    """Fetches ITHome hot news."""
    url = "https://www.ithome.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Target the 'hot news' list on the sidebar/content
        # Structure: <ul class="rank-list"> or similar
        items = soup.select('.lst-2 li') # Daily hot list class
        
        results = []
        for item in items:
            link_el = item.select_one('a')
            if link_el:
                results.append({
                    "title": link_el.text.strip(),
                    "url": link_el.get('href', ''),
                    "hot_score": "Hot",
                    "excerpt": ""
                })
                
        logger.info(f"Retrieved {len(results)} items from ITHome")
        return results
    except Exception as e:
        logger.error(f"Error fetching ITHome: {e}")
        return []
