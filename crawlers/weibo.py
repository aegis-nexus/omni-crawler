import requests
import logging
from bs4 import BeautifulSoup

logger = logging.getLogger("OmniCrawler.Weibo")

def fetch():
    """Fetches Weibo hot search list via PC web scraping (s.weibo.com)."""
    url = "https://s.weibo.com/top/summary?cate=realtimehot"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://weibo.com/",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "SUB=_2AkMSY_pAf8NxqwFRmP8SyW_mbY12zwnEieKkqInJJRMxHRl-yT9kqm8StRB6O_Z_X_vX_Z_X_vX_Z_X_vX_Z;" # Placeholder/Minimal Cookie
    }
    
    try:
        # Using a session to better manage headers
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Weibo uses a table structure for hot topics
        table = soup.select_one('section.list table tbody')
        if not table:
            # Fallback to direct tbody if section not found
            table = soup.select_one('tbody')
            
        if not table:
            logger.error("Could not find Weibo hot list table")
            return []

        rows = table.find_all('tr')
        results = []
        
        for row in rows:
            td_rank = row.select_one('.td-01')
            td_content = row.select_one('.td-02')
            
            if not td_rank or not td_content:
                continue
                
            rank = td_rank.text.strip()
            link_el = td_content.select_one('a')
            score_el = td_content.select_one('span')
            
            # Skip the 'top' ad or fixed items that don't have a numerical rank
            if not rank.isdigit() and rank != "":
                continue
                
            if link_el:
                title = link_el.text.strip()
                href = link_el.get('href', '')
                url = f"https://s.weibo.com{href}" if href.startswith('/') else href
                
                results.append({
                    "title": title,
                    "url": url,
                    "hot_score": score_el.text.strip() if score_el else "N/A",
                    "excerpt": ""
                })
        
        logger.info(f"Retrieved {len(results)} items from Weibo")
        return results
    except Exception as e:
        logger.error(f"Error fetching Weibo: {e}")
        return []
