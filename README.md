# Omni-Crawler: Global Hot-Ranking Aggregator

A professional-grade, modular crawler system designed to track real-time hot rankings across 11 major global platforms. Built for long-term data persistence and analytical rigor.

## 🚀 Supported Platforms (11)
- **Comprehensive**: Weibo (微博), Baidu (百度), Toutiao (今日头条), 36Kr (36氪)
- **Tech/Geek**: GitHub Trending, Hacker News, V2EX, ITHome (IT之家)
- **Community/Video**: Bilibili (哔哩哔哩), Reddit (Global), Zhihu (知乎)

## 🛠️ Engineering Features
- **Modular Architecture**: Decoupled orchestrator (`main.py`) and platform scrapers (`crawlers/`).
- **Industrial Storage**: Monthly rotated **SQLite** databases for long-term stability.
- **Atomic De-duplication**: Per-item MD5 hashing to prevent redundant records while tracking trend fluctuations.
- **Bilingual Core**: Designed for both English and Chinese data processing.

## 📦 Project Structure
- `main.py`: Central orchestrator and scheduler.
- `storage.py`: SQLite persistence layer with de-duplication logic.
- `config.py`: Environment-based configuration (.env support).
- `crawlers/`: Individual platform scraper modules.
- `data/db/`: Monthly SQLite databases (`YYYY-MM.sqlite`).
- `logs/`: Standardized execution logs.

## ⚙️ Quick Start
1. Install dependencies: `pip install -r requirements.txt`
2. Run the aggregator: `python3 main.py`

---
*Maintained by Aegis-Nexus // Managed by Lsland*
