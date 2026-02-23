import requests
import logging

logger = logging.getLogger("OmniCrawler.HackerNews")

def fetch():
    """Fetches Hacker News top stories."""
    # Using the official Firebase API
    top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    item_url_template = "https://hacker-news.firebaseio.com/v0/item/{}.json"
    
    try:
        # Get top 20 IDs
        response = requests.get(top_stories_url, timeout=10)
        response.raise_for_status()
        story_ids = response.json()[:20]
        
        results = []
        for sid in story_ids:
            try:
                story_res = requests.get(item_url_template.format(sid), timeout=5)
                story = story_res.json()
                if story:
                    results.append({
                        "title": story.get('title', ''),
                        "url": story.get('url') or f"https://news.ycombinator.com/item?id={sid}",
                        "hot_score": f"{story.get('score', 0)} points",
                        "excerpt": f"By {story.get('by')} | {story.get('descendants', 0)} comments"
                    })
            except Exception as item_e:
                logger.warning(f"Error fetching HN item {sid}: {item_e}")
                
        logger.info(f"Retrieved {len(results)} items from Hacker News")
        return results
    except Exception as e:
        logger.error(f"Error fetching Hacker News: {e}")
        return []
