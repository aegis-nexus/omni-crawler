import requests
import logging
import json

logger = logging.getLogger("OmniCrawler.ITHome")

def fetch():
    """Uses a more stable third-party or mobile-mimic interface for ITHome."""
    # IT之家 PC 首页现在异步加载较多，尝试一个更直接的 API 节点（聚合 API 往往更稳）
    url = "https://api.98dou.cn/api/hotlist/ithome"
    headers = {"User-Agent": "AegisNexus/1.0"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Standard aggregation API format: {code: 200, data: [...]}
        raw_items = data.get('data', [])
        results = []
        for item in raw_items:
            results.append({
                "title": item.get('title'),
                "url": item.get('url'),
                "hot_score": item.get('hot_score', 'Hot'),
                "excerpt": ""
            })
        return results
    except Exception as e:
        logger.error(f"ITHome Error: {e}")
        return []
