import json
import logging
import os
from datetime import datetime
import config
from crawlers import zhihu, weibo, baidu, reddit, github, bilibili, toutiao, hackernews, v2ex, kr36, ithome

logging.basicConfig(
    level=config.LOG_LEVEL,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(config.LOG_DIR, f"crawler_{datetime.now().strftime('%Y-%m-%d')}.log"), encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("OmniCrawler")

def save_data(platform, data):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    filename = os.path.join(config.DATA_DIR, f"{platform}_{timestamp}.json")
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"Saved {len(data)} items for {platform}")
    except Exception as e:
        logger.error(f"Failed to save {platform}: {e}")

def main():
    logger.info("--- Starting Omni-Crawler Session ---")
    platforms = [
        {"name": "zhihu", "module": zhihu},
        {"name": "weibo", "module": weibo},
        {"name": "baidu", "module": baidu},
        {"name": "reddit", "module": reddit},
        {"name": "github", "module": github},
        {"name": "bilibili", "module": bilibili},
        {"name": "toutiao", "module": toutiao},
        {"name": "hackernews", "module": hackernews},
        {"name": "v2ex", "module": v2ex},
        {"name": "36kr", "module": kr36},
        {"name": "ithome", "module": ithome}
    ]
    for platform in platforms:
        try:
            data = platform["module"].fetch()
            if data:
                save_data(platform["name"], data)
        except Exception as e:
            logger.error(f"Platform {platform['name']} failed: {e}")
    logger.info("--- Session Complete ---")

if __name__ == "__main__":
    main()
