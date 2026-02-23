import requests
import logging

logger = logging.getLogger("OmniCrawler.Weibo")

def fetch():
    """Fetches Weibo hot search list via mobile API."""
    url = "https://m.weibo.cn/api/container/getIndex?containerid=106003type%3D25%26t%3D3%26disable_hot%3D1%26filter_type%3Drealtime"
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
        "Referer": "https://m.weibo.cn/p/index?containerid=106003type%3D25%26t%3D3%26disable_hot%3D1%26filter_type%3Drealtime"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Weibo API nested structure: data -> cards -> card_group
        cards = data.get('data', {}).get('cards', [])
        hot_card = next((c for c in cards if c.get('itemid') == 'hotword'), None)
        
        if not hot_card:
            # Fallback to general group parsing if itemid doesn't match
            group = cards[0].get('card_group', []) if cards else []
        else:
            group = hot_card.get('card_group', [])

        results = []
        for item in group:
            desc = item.get('desc', '')
            if not desc: continue
            
            results.append({
                "title": desc,
                "url": item.get('scheme', ''),
                "hot_score": item.get('desc_extr', 'N/A'),
                "excerpt": "" # Weibo API at this level doesn't provide excerpts
            })
        
        logger.info(f"Retrieved {len(results)} items from Weibo")
        return results
    except Exception as e:
        logger.error(f"Error fetching Weibo: {e}")
        return []
