import requests
import logging

logger = logging.getLogger("OmniCrawler.Zhihu")

def fetch():
    url = "https://www.zhihu.com/api/v4/search/top_search/tabs/hot/items"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.zhihu.com/hot"
    }
    
    try:
        logger.debug(f"Requesting Zhihu hot items from {url}")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        results = []
        for item in data.get('data', []):
            query = item.get('query_display')
            results.append({
                "title": query,
                "url": f"https://www.zhihu.com/search?q={query}&type=content",
                "hot_score": "N/A",
                "excerpt": item.get('query_description', '')
            })
        logger.info(f"Retrieved {len(results)} items from Zhihu")
        return results
    except Exception as e:
        logger.error(f"Error fetching Zhihu: {e}")
        return []
