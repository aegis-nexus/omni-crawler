[English](README.md) | [简体中文](README_ZH.md)
# Omni-Crawler: 全球热榜聚合抓取系统

一款工业级、由 CLI 驱动的爬虫系统，专为多平台热榜数据的自动化聚合而设计。本项目专注于长期数据持久化、健壮的健康管理以及无缝的外部系统集成。

## 🚀 支持平台 (11)
- **综合新闻**: 微博, 百度, 今日头条, 36Kr (36氪)
- **技术极客**: GitHub Trending, Hacker News, V2EX, ITHome (IT之家)
- **社区视频**: 哔哩哔哩, Reddit (Global), 知乎

## 🏗️ 核心架构

### 1. 统一 JSON 接口 (API Specification)
系统专为外部调度器（如 Cron、自动化脚本）设计。它向 `stdout`（标准输出）发送纯净的 JSON 响应，方便解析。

**响应结构:**
| 字段 | 类型 | 说明 |
| :--- | :--- | :--- |
| `code` | Integer | 状态码：0 (成功), 1 (质量/逻辑失败), 2 (脚本或环境错误) |
| `message` | String | 详细的状态描述或报错信息 |
| `data` | Array | 抓取到的热榜条目数组。每个条目包含 `title`, `url`, `hot_score`, `excerpt` |

**Message 输出示例:**
- `获取成功`: 抓取且持久化完成。
- `数据获取失败: 结果为空`: 抓取到的数据量为 0。
- `脚本内部错误: [错误详情]`: 抓取脚本执行时抛出异常。

**响应 JSON 示例:**
```json
{
  "code": 0,
  "message": "获取成功",
  "data": [
    {
      "title": "示例热搜标题",
      "url": "https://example.com/item/1",
      "hot_score": "125.4w",
      "excerpt": "这是关于该热点的简短摘要..."
    }
  ]
}
```

### 2. 工业级存储层
- **按月滚动**: 自动为每个月创建独立的 SQLite 数据库（例如 `data/db/2026-02.sqlite`），兼顾性能与可归档性。
- **原子级去重**: 对 `platform + title + url` 进行 MD5 哈希校验。只有当条目是新增或热度发生变化时才会记录，防止数据库冗余膨胀。

### 3. 健康与状态管理
- **5次失败判定**: 只有当某个平台连续失败达到 5 次时，其状态才会被标记为 `FAILED`，有效过滤网络波动。
- **自动自愈**: 任何一次成功的抓取都会立即重置错误计数并将状态恢复为 `HEALTHY`。

## 📦 项目结构
- `main.py`: CLI 核心调度器。
- `storage.py`: SQLite 持久化与去重引擎。
- `status_manager.py`: 健康追踪与状态持久化逻辑。
- `crawlers/`: 各平台独立的抓取模块。
- `data/db/`: SQLite 月度归档数据库。

## ⚙️ 使用指南

### 安装依赖
```bash
pip install requests beautifulsoup4 python-dotenv
```

### 执行命令
| Slug (参数名) | 平台名称 |
| :--- | :--- |
| `baidu` | 百度 | `weibo` | 微博 | `toutiao` | 今日头条 | `zhihu` | 知乎 |
| `36kr` | 36氪 | `ithome` | IT之家 | `bilibili` | B站 | `v2ex` | V2EX |
| `github` | GitHub Trending | `hackernews` | Hacker News | `reddit` | Reddit |

```bash
# 运行指定平台
python3 main.py --platform baidu

# 全量运行
python3 main.py --all

# 查看系统健康报告
python3 main.py --status

# 手动重置故障状态
python3 main.py --reset baidu
```

---
*由 Aegis-Nexus 维护 // 工程指导：Lsland*
