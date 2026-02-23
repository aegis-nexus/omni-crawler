import requests
import logging
from bs4 import BeautifulSoup

logger = logging.getLogger("OmniCrawler.Baidu")

def fetch():
    """Fetches Baidu hot search list via direct HTML scraping with fixed URL extraction."""
    url = "https://top.baidu.com/board?tab=realtime"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Current Baidu PC structure
        items = soup.select('.category-wrap_iQLoo')
        
        results = []
        for item in items:
            # Fix: Baidu titles are inside a div with specific class
            title_el = item.select_one('.c-single-text-ellipsis')
            # Fix: URLs are in the <a> tags with class content_1YWBm or similar
            link_el = item.select_one('a.content_1YWBm') or item.select_one('a')
            score_el = item.select_one('.hot-index_1Bl1a') or item.select_one('.hot-index_1_I_F')
            desc_el = item.select_one('.hot-desc_1m_jR') or item.select_one('.hot-desc_1m_Bq')
            
            if title_el:
                results.append({
                    "title": title_el.text.strip(),
                    "url": link_el.get('href', '') if link_el else "",
                    "hot_score": score_el.text.strip() if score_el else "N/A",
                    "excerpt": desc_el.text.strip().replace('查看更多>', '') if desc_el else ""
                })
        
        logger.info(f"Retrieved {len(results)} items from Baidu")
        return results
    except Exception as e:
        logger.error(f"Error fetching Baidu: {e}")
        return []
