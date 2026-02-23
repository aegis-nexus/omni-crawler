import requests
import logging
from bs4 import BeautifulSoup

logger = logging.getLogger("OmniCrawler.GitHub")

def fetch():
    """Fetches GitHub Trending repositories."""
    url = "https://github.com/trending"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        articles = soup.select('article.Box-row')
        results = []
        
        for article in articles:
            title_el = article.select_one('h2 a')
            desc_el = article.select_one('p.col-9')
            
            if title_el:
                repo_path = title_el.get('href', '').strip('/')
                footer_el = article.select_one('div.f6.color-fg-muted')
                # Fixed: Use double backslash for literal newline character in replace
                raw_score = footer_el.text.strip() if footer_el else "N/A"
                score_text = " ".join(raw_score.split())
                results.append({
                    "title": repo_path,
                    "url": f"https://github.com/{repo_path}",
                    "hot_score": score_text,
                    "excerpt": desc_el.text.strip() if desc_el else ""
                })
                
        logger.info(f"Retrieved {len(results)} items from GitHub Trending")
        return results
    except Exception as e:
        logger.error(f"Error fetching GitHub: {e}")
        return []
