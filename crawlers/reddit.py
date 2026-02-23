import requests
import logging

logger = logging.getLogger("OmniCrawler.Reddit")

def fetch():
    """Fetches Reddit r/all hot posts."""
    url = "https://www.reddit.com/r/all/hot.json?limit=25"
    headers = {
        "User-Agent": "AegisNexusBot/1.0 (managed by Lsland)"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        items = data.get('data', {}).get('children', [])
        results = []
        for item in items:
            post = item.get('data', {})
            results.append({
                "title": post.get('title'),
                "url": f"https://www.reddit.com{post.get('permalink')}",
                "hot_score": f"{post.get('ups')} ups",
                "excerpt": post.get('selftext')[:200] if post.get('selftext') else ""
            })
            
        logger.info(f"Retrieved {len(results)} items from Reddit")
        return results
    except Exception as e:
        logger.error(f"Error fetching Reddit: {e}")
        return []
