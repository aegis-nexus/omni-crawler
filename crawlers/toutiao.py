import requests
import logging

logger = logging.getLogger("OmniCrawler.Toutiao")

def fetch():
    """Fetches Toutiao hot board items."""
    # API endpoint for Toutiao hot board
    url = "https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.toutiao.com/"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        items = data.get('data', [])
        results = []
        
        for item in items:
            results.append({
                "title": item.get('Title', ''),
                "url": item.get('Url', ''),
                "hot_score": item.get('HotValue', 'N/A'),
                "excerpt": "" # Detail text usually not in this compact API
            })
            
        logger.info(f"Retrieved {len(results)} items from Toutiao")
        return results
    except Exception as e:
        logger.error(f"Error fetching Toutiao: {e}")
        return []
