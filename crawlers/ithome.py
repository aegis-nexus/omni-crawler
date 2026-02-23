import requests
import logging

logger = logging.getLogger("OmniCrawler.ITHome")

def fetch():
    """Fetches ITHome hot news using a verified aggregation endpoint with proper URL mapping."""
    # IT之家官方 Web 路由已失效，改用稳定的聚合 API
    url = "https://api.98dou.cn/api/hotlist/ithome"
    headers = {"User-Agent": "AegisNexus/1.0"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Expected API format: {"data": [{"title": "...", "url": "...", "hot": "..."}]}
        raw_items = data.get('data', [])
        results = []
        for item in raw_items:
            # Handle potential variation in key names (url vs link)
            target_url = item.get('url') or item.get('link')
            if target_url:
                results.append({
                    "title": item.get('title', ''),
                    "url": target_url,
                    "hot_score": item.get('hot') or item.get('hot_score', 'Hot'),
                    "excerpt": ""
                })
        
        if not results:
            logger.warning("ITHome API returned empty results or invalid schema")
            
        logger.info(f"Retrieved {len(results)} items from ITHome")
        return results
    except Exception as e:
        logger.error(f"Error fetching ITHome: {e}")
        return []
