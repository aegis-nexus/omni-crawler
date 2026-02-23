import argparse
import logging
import os
import sys
from datetime import datetime
import config
import storage
import status_manager

# Mapping platforms to their modules
PLATFORMS = {}
try:
    from crawlers import zhihu, weibo, baidu, reddit, github, bilibili, toutiao, hackernews, v2ex, kr36, ithome
    PLATFORMS = {
        "zhihu": zhihu, "weibo": weibo, "baidu": baidu, "reddit": reddit,
        "github": github, "bilibili": bilibili, "toutiao": toutiao,
        "hackernews": hackernews, "v2ex": v2ex, "36kr": kr36, "ithome": ithome
    }
except ImportError as e:
    print(f"Import Error: {e}")

# Setup Logging
log_filename = os.path.join(config.LOG_DIR, f"crawler_{datetime.now().strftime('%Y-%m-%d')}.log")
logging.basicConfig(
    level=config.LOG_LEVEL,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.FileHandler(log_filename, encoding='utf-8'), logging.StreamHandler()]
)
logger = logging.getLogger("OmniCrawler")

def run_crawler(name):
    module = PLATFORMS.get(name)
    if not module:
        logger.error(f"Platform {name} not found.")
        return
    
    logger.info(f"--- Executing: {name} ---")
    try:
        data = module.fetch()
        # Data Quality Check: Fail if data is empty or URL missing rate > 50%
        if not data:
            raise ValueError("Empty data retrieved")
        
        missing_urls = sum(1 for item in data if not item.get('url'))
        if missing_urls / len(data) > 0.5:
            raise ValueError(f"High URL missing rate: {missing_urls}/{len(data)}")
            
        success = storage.save_platform_data(name, data)
        status_manager.update_platform_status(name, True)
        logger.info(f"--- Success: {name} ---")
    except Exception as e:
        logger.error(f"--- Failed: {name} | Error: {e} ---")
        status_manager.update_platform_status(name, False, str(e))

def main():
    parser = argparse.ArgumentParser(description="Omni-Crawler CLI Manager")
    parser.add_argument("--platform", type=str, help="Specific platform to crawl")
    parser.add_argument("--all", action="store_true", help="Crawl all supported platforms")
    parser.add_argument("--reset", type=str, help="Reset status for a specific platform")
    parser.add_argument("--status", action="store_true", help="Show health status of all platforms")
    
    args = parser.parse_args()
    
    if args.status:
        status = status_manager.load_status()
        print("
--- Omni-Crawler Health Report ---")
        for p, info in status.items():
            color = "OK" if info['status'] == 'HEALTHY' else "!!"
            print(f"[{color}] {p:12} | Status: {info['status']:8} | Fails: {info['consecutive_failures']} | Last: {info['last_run']}")
        return

    if args.reset:
        if status_manager.reset_platform(args.reset):
            print(f"Status for {args.reset} has been reset to HEALTHY.")
        else:
            print(f"Platform {args.reset} not found in status registry.")
        return

    if args.platform:
        run_crawler(args.platform)
    elif args.all:
        for name in PLATFORMS.keys():
            run_crawler(name)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
