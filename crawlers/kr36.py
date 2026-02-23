import requests
import logging
import json
import re

logger = logging.getLogger("OmniCrawler.36Kr")

def fetch():
    url = "https://36kr.com/newsflashes"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        match = re.search(r'window.initialState=(.*?)</script>', response.text)
        if not match: return []
        
        json_str = match.group(1).strip()
        if json_str.endswith(';'): json_str = json_str[:-1]
        state = json.loads(json_str)
        
        # 2026 Path extraction
        items = []
        try:
            # Path can vary, trying common nested structures
            raw_list = state.get('newsflashCatalogData', {}).get('data', {}).get('newsflashList', {}).get('data', {}).get('itemList', [])
            if not raw_list:
                raw_list = state.get('newsflashCatalogData', {}).get('newsflashList', {}).get('itemList', [])
            
            for item in raw_list:
                m = item.get('templateMaterial', {})
                items.append({
                    "title": m.get('widgetTitle'),
                    "url": f"https://36kr.com/newsflashes/{item.get('itemId')}",
                    "hot_score": "Recent",
                    "excerpt": m.get('widgetContent', '')[:200]
                })
        except: pass
        return items
    except Exception as e:
        logger.error(f"36Kr Error: {e}")
        return []
