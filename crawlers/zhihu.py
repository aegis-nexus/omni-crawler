import requests
import logging

logger = logging.getLogger("OmniCrawler.Zhihu")

def fetch():
    """Fetches Zhihu hot topics. Tries to get the full list (up to 50 items)."""
    # Using the standard mobile hot list API which is more stable for general requests
    url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=50"
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        # If 401, fallback to the search-based hot API which is public
        if response.status_code == 401:
            logger.warning("Zhihu Main API requires auth, falling back to search API")
            url = "https://www.zhihu.com/api/v4/search/top_search/tabs/hot/items"
            response = requests.get(url, headers=headers, timeout=10)
            
        response.raise_for_status()
        data = response.json()
        
        results = []
        for item in data.get('data', []):
            # Parsing logic varies slightly between the two APIs
            target = item.get('target', {})
            title = target.get('title') or item.get('query_display')
            item_id = target.get('id')
            url = f"https://www.zhihu.com/question/{item_id}" if item_id else f"https://www.zhihu.com/search?q={title}"
            
            if title:
                results.append({
                    "title": title,
                    "url": url,
                    "hot_score": item.get('detail_text', 'N/A'),
                    "excerpt": target.get('excerpt', item.get('query_description', ''))
                })
        logger.info(f"Retrieved {len(results)} items from Zhihu")
        return results
    except Exception as e:
        logger.error(f"Error fetching Zhihu: {e}")
        return []
