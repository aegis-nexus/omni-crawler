# Project: Omni-Crawler - Hot Ranking Feasibility Analysis (2025/2026)

This document analyzes the technical feasibility of building a cross-platform hot ranking crawler.

## 1. Target Platforms & Feasibility

| Platform | Feasibility | Technical Approach | Difficulty | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Weibo (微博)** | **High** | Mobile API / Real-time search page | Medium | Frequent UI/API updates; requires header rotation. |
| **Zhihu (知乎)** | **High** | Public API () | Low | Relatively stable JSON endpoints. |
| **Douyin (抖音)** | **Medium** | Mobile API / Web-rendering (Selenium) | High | Strong anti-crawling; may require JS execution. |
| **Baidu (百度)** | **High** | Web Scraping (Top search page) | Low | Simple HTML structure; easy to parse. |
| **X (Twitter)** | **Medium** | Official API / Web Scraping | High | API is costly; scraping is strictly monitored. |
| **Reddit** | **High** | Official API / RSS /  endpoints | Low | Very developer-friendly. |
| **Google Trends** | **Medium** | Unofficial APIs / PyTrends | Medium | Rate-limiting is aggressive. |

## 2. Technical Architecture Proposal

- **Collector (Python/Node.js):**
  - Use  for API-based targets.
  - Use  for JS-heavy targets (Douyin/X).
- **Scheduler (GitHub Actions):**
  - Trigger every 30-60 minutes.
- **Storage:**
  - Git-as-Database (storing JSON snapshots in the repo).
- **Interface:**
  - Inject data into the  frontend for real-time display.

## 3. Risk Assessment

1. **Anti-Crawling:** Major platforms (especially domestic) use dynamic JS and IP blocking.
2. **Account Risks:** Scraping X or Douyin may require login session cookies, which rotate.
3. **Legal/TOS:** Automated scraping must respect  and platform rate limits.

## 4. Next Steps

1. Prototype the **Zhihu** and **Weibo** collectors (highest ROI).
2. Establish a data schema for unified ranking (Source, Title, Rank, Trend, URL).
3. Setup GitHub Actions workflow for persistence.

---
*Drafted by Aegis // Verified by Lsland*
