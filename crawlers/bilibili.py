import requests
import logging

logger = logging.getLogger("OmniCrawler.Bilibili")

def fetch():
    """Fetches Bilibili popular videos."""
    url = "https://api.bilibili.com/x/web-interface/popular?ps=20&pn=1"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.bilibili.com/"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        items = data.get('data', {}).get('list', [])
        results = []
        
        for item in items:
            results.append({
                "title": item.get('title'),
                "url": f"https://www.bilibili.com/video/{item.get('bvid')}",
                "hot_score": f"View: {item.get('stat', {}).get('view')}",
                "excerpt": item.get('desc', '')
            })
            
        logger.info(f"Retrieved {len(results)} items from Bilibili")
        return results
    except Exception as e:
        logger.error(f"Error fetching Bilibili: {e}")
        return []
