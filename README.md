[English](README.md) | [简体中文](README_ZH.md)
# Omni-Crawler: Global Hot-Ranking Aggregator

A professional-grade, CLI-driven crawler system designed for multi-platform hot ranking aggregation. Built with a focus on long-term data persistence, robust health management, and seamless external integration.

## 🚀 Supported Platforms (11)
- **General News**: Weibo (微博), Baidu (百度), Toutiao (今日头条), 36Kr (36氪)
- **Tech & Geek**: GitHub Trending, Hacker News, V2EX, ITHome (IT之家)
- **Community & Video**: Bilibili (哔哩哔哩), Reddit (Global), Zhihu (知乎)

## 🏗️ Technical Architecture

### 1. Unified JSON Interface
The system is designed to be called by external schedulers (e.g., Cron, Custom Managers). It outputs a pure JSON response to `stdout`:
- **code**: 0 (Success), 1 (Quality/Logic Failure), 2 (Script Error).
- **message**: Descriptive status or error details.
- **data**: The captured hot-list items (array of objects with `title`, `url`, `hot_score`, `excerpt`).

### 2. Industrial Storage Layer
- **Monthly Rotation**: Automatically creates a new SQLite database file for each month (e.g., `data/db/2026-02.sqlite`).
- **Atomic De-duplication**: Uses MD5 hashing of platform+title+url to ensure unique records while tracking trend changes.

### 3. Health & Status Management
- **5-Fail Threshold**: Automatically marks a platform as `FAILED` only after 5 consecutive failed attempts, preventing false alarms from network jitters.
- **Self-Healing**: Automatically reverts to `HEALTHY` upon the first successful capture.
- **CLI Management**: Inspect system health via `--status` or manually fix states via `--reset`.

## 📦 Project Structure
- `main.py`: The central CLI orchestrator.
- `storage.py`: SQLite persistence and de-duplication engine.
- `status_manager.py`: Health tracking and persistence.
- `crawlers/`: Independent modules for each platform.
- `data/db/`: SQLite monthly archives.

## ⚙️ Usage Guide

### Installation
```bash
pip install requests beautifulsoup4 python-dotenv
```

### Execution
Pass the platform slug to the `--platform` argument.

#### Available Platforms
| Slug | Platform Name | Category |
| :--- | :--- | :--- |
| `baidu` | Baidu (百度) | General News |
| `weibo` | Weibo (微博) | Social Media |
| `toutiao` | Toutiao (今日头条) | General News |
| `zhihu` | Zhihu (知乎) | Q&A Community |
| `36kr` | 36Kr (36氪) | Business/Tech |
| `ithome` | ITHome (IT之家) | Tech News |
| `bilibili` | Bilibili (哔哩哔哩) | Video/ACG |
| `v2ex` | V2EX | Tech Community |
| `github` | GitHub Trending | Open Source |
| `hackernews` | Hacker News | Tech/Startup |
| `reddit` | Reddit (r/all) | Global Hot |

#### Commands
```bash
# Run a specific platform (e.g., Baidu)
python3 main.py --platform baidu

# Run all platforms at once
python3 main.py --all

# Inspect system health and error counts
python3 main.py --status

# Reset a platform status after manual fix
python3 main.py --reset baidu
```

---
*Maintained by Aegis-Nexus // Engineering Authority: Lsland*
