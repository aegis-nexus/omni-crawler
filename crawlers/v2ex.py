import requests
import logging

logger = logging.getLogger("OmniCrawler.V2EX")

def fetch():
    """Fetches V2EX hot topics."""
    url = "https://www.v2ex.com/api/topics/hot.json"
    headers = {
        "User-Agent": "AegisNexusBot/1.0"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        items = response.json()
        
        results = []
        for item in items:
            results.append({
                "title": item.get('title'),
                "url": item.get('url'),
                "hot_score": f"{item.get('replies')} replies",
                "excerpt": item.get('content_rendered')[:200] if item.get('content_rendered') else ""
            })
            
        logger.info(f"Retrieved {len(results)} items from V2EX")
        return results
    except Exception as e:
        logger.error(f"Error fetching V2EX: {e}")
        return []
