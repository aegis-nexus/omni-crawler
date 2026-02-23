import requests
import logging
import re
import json

logger = logging.getLogger("OmniCrawler.Baidu")

def fetch():
    """Fetches Baidu hot search list via web scraping."""
    url = "https://top.baidu.com/board?tab=realtime"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        html = response.text
        
        # Baidu embeds data in a JSON string within the HTML
        pattern = re.compile(r'<!--s-data:(.*?)-->')
        match = pattern.search(html)
        
        if not match:
            logger.error("Could not find s-data in Baidu page")
            return []
            
        data = json.loads(match.group(1))
        cards = data.get('cards', [])
        
        # Find the card containing the list
        list_card = next((c for c in cards if c.get('content')), {})
        items = list_card.get('content', [])
        
        results = []
        for item in items:
            results.append({
                "title": item.get('word', ''),
                "url": item.get('rawUrl', ''),
                "hot_score": item.get('hotScore', 'N/A'),
                "excerpt": item.get('desc', '')
            })
            
        logger.info(f"Retrieved {len(results)} items from Baidu")
        return results
    except Exception as e:
        logger.error(f"Error fetching Baidu: {e}")
        return []
