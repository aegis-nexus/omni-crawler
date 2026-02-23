import argparse
import logging
import json
import sys
import os
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
    # This happens during early initialization if crawlers are missing
    pass

# Setup Logging - Redirect StreamHandler to sys.stderr to keep stdout clean for JSON response
log_filename = os.path.join(config.LOG_DIR, f"crawler_{datetime.now().strftime('%Y-%m-%d')}.log")
logging.basicConfig(
    level=config.LOG_LEVEL,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler(log_filename, encoding='utf-8'),
        logging.StreamHandler(sys.stderr) 
    ]
)
logger = logging.getLogger("OmniCrawler")

def respond(code, message, data=None):
    """Prints standardized JSON response to stdout and exits."""
    response = {
        "code": code,
        "message": message,
        "data": data if data is not None else []
    }
    # Ensure stdout only contains this JSON
    print(json.dumps(response, ensure_ascii=False))
    sys.exit(0) # Standard exit as requested, internal status handled in JSON

def run_crawler(name):
    module = PLATFORMS.get(name)
    if not module:
        respond(2, f"平台 {name} 不存在")
    
    try:
        data = module.fetch()
        
        if not data:
            status_manager.update_platform_status(name, False, "Empty data retrieved")
            respond(1, "数据获取失败: 结果为空", [])
        
        # Persistence
        storage.save_platform_data(name, data)
        status_manager.update_platform_status(name, True)
        
        respond(0, "获取成功", data)
        
    except Exception as e:
        error_info = str(e)
        status_manager.update_platform_status(name, False, error_info)
        respond(2, f"脚本内部错误: {error_info}", [])

def main():
    parser = argparse.ArgumentParser(description="Omni-Crawler CLI Manager")
    parser.add_argument("--platform", type=str, help="Specific platform to crawl")
    parser.add_argument("--all", action="store_true", help="Crawl all supported platforms (returns combined status)")
    parser.add_argument("--reset", type=str, help="Reset status for a specific platform")
    parser.add_argument("--status", action="store_true", help="Show health status of all platforms")
    
    args = parser.parse_args()
    
    # 1. Handle Status Check
    if args.status:
        status = status_manager.load_status()
        respond(0, "状态查询成功", status)

    # 2. Handle Manual Reset
    if args.reset:
        if status_manager.reset_platform(args.reset):
            respond(0, f"平台 {args.reset} 状态已手动重置", [])
        else:
            respond(2, f"未找到平台 {args.reset} 的记录", [])

    # 3. Handle Platform Execution
    if args.platform:
        run_crawler(args.platform)
    elif args.all:
        # For 'all', we return a summary response
        results = {}
        for name in sorted(PLATFORMS.keys()):
            module = PLATFORMS.get(name)
            try:
                data = module.fetch()
                if data:
                    storage.save_platform_data(name, data)
                    status_manager.update_platform_status(name, True)
                    results[name] = {"code": 0, "count": len(data)}
                else:
                    status_manager.update_platform_status(name, False, "No data")
                    results[name] = {"code": 1, "message": "No data"}
            except Exception as e:
                status_manager.update_platform_status(name, False, str(e))
                results[name] = {"code": 2, "message": str(e)}
        respond(0, "全量抓取任务完成", results)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
