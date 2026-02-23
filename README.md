# Project: Omni-Crawler - Multi-Platform Hot Ranking Aggregator

Universal hot-ranking crawler for global social media and news platforms. Built for modularity and maintainability.

## 🚀 Supported Platforms
- **Zhihu (知乎)**: Real-time hot questions via public search API.
- **Weibo (微博)**: Real-time hot search list via mobile container API.
- **Baidu (百度)**: Real-time top search board via web scraping.
- **Reddit**: Worldwide hot threads from r/all via .json endpoint.

## 🛠️ Project Structure
- `main.py`: Central orchestrator and scheduler.
- `config.py`: Environment-based configuration.
- `crawlers/`: Individual platform scraper modules.
- `data/`: JSON data storage (time-stamped).
- `logs/`: Detailed execution logs.

## 📦 Requirements
- Python 3.12+
- `requests`
- `python-dotenv`

## ⚙️ Usage
Run the aggregator:
```bash
python3 main.py
```

---
*Maintained by Aegis-Nexus*
