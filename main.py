import logging
import os
from datetime import datetime
import config
import storage
from crawlers import zhihu, weibo, baidu, reddit, github, bilibili, toutiao, hackernews, v2ex, kr36, ithome

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
    
    stats = {"success": 0, "skipped": 0, "failed": 0}
    
    for platform in platforms:
        name = platform["name"]
        logger.info(f"Fetching: {name}")
        try:
            data = platform["module"].fetch()
            if data:
                is_new = storage.save_platform_data(name, data)
                if is_new: stats["success"] += 1
                else: stats["skipped"] += 1
            else:
                logger.warning(f"No data for {name}")
                stats["failed"] += 1
        except Exception as e:
            logger.error(f"Critical error in {name}: {e}")
            stats["failed"] += 1
            
    logger.info(f"--- Session Complete | Success: {stats['success']} | Skipped: {stats['skipped']} | Failed: {stats['failed']} ---")

if __name__ == "__main__":
    main()
