import requests
import logging
import json
import re

logger = logging.getLogger("OmniCrawler.36Kr")

def fetch():
    """Fetches 36Kr newsflashes (快讯)."""
    url = "https://36kr.com/newsflashes"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # 36Kr also embeds state in a window.initialState script tag
        pattern = re.compile(r'window.initialState=(.*?)</script>')
        match = pattern.search(response.text)
        
        if not match:
            logger.error("Could not find initialState in 36Kr")
            return []
            
        state = json.loads(match.group(1))
        # Navigate the nested state to find newsflashes
        # Path: newsflashCatalogData -> data -> newsflashList
        flashes = state.get('newsflashCatalogData', {}).get('data', {}).get('newsflashList', [])
        
        results = []
        for item in flashes:
            content_data = item.get('templateMaterial', {})
            results.append({
                "title": content_data.get('widgetTitle', ''),
                "url": f"https://36kr.com/newsflashes/{item.get('itemId')}",
                "hot_score": "Recent",
                "excerpt": content_data.get('widgetContent', '')[:200]
            })
            
        logger.info(f"Retrieved {len(results)} items from 36Kr")
        return results
    except Exception as e:
        logger.error(f"Error fetching 36Kr: {e}")
        return []
