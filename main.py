import json
import logging
import os
from datetime import datetime
import config
from crawlers import zhihu, weibo, baidu, reddit, github, bilibili, toutiao, hackernews

# Setup Logging
log_filename = os.path.join(config.LOG_DIR, f"crawler_{datetime.now().strftime('%Y-%m-%d')}.log")
logging.basicConfig(
    level=config.LOG_LEVEL,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler(log_filename, encoding='utf-8'),
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
        logger.info(f"Successfully saved {len(data)} items for {platform} to {filename}")
    except Exception as e:
        logger.error(f"Failed to save data for {platform}: {e}")

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
        {"name": "hackernews", "module": hackernews}
    ]
    
    for platform in platforms:
        name = platform["name"]
        module = platform["module"]
        
        logger.info(f"Executing crawler for: {name}")
        try:
            data = module.fetch()
            if data:
                save_data(name, data)
                logger.info(f"Top entry for {name}: {data[0]['title']}")
            else:
                logger.warning(f"No data retrieved for {name}")
        except Exception as e:
            logger.error(f"Critical error in {name} crawler: {e}")
            
    logger.info("--- Omni-Crawler Session Complete ---")

if __name__ == "__main__":
    main()
