# -*- coding: utf-8 -*-
"""
AI Daily Fetcher
从多个 RSS 源抓取 AI / 创业 / 科技资讯
"""

import feedparser
import requests
import json
import datetime
import time
import sys
import os

# 让控制台输出支持中文
sys.stdout.reconfigure(encoding='utf-8')

# RSS 源配置列表
# name: 显示名称 | url: RSS 地址 | tag: 内容分类
# 说明：优先选择国内可访问的优质源，少数外媒（TechCrunch/Ars/The Verge）已验证可访问
FEEDS = [
    # 优质外媒（已验证可访问）
    {"name": "TechCrunch", "url": "https://techcrunch.com/feed/", "tag": "Startup"},
    {"name": "Ars Technica", "url": "https://feeds.arstechnica.com/arstechnica/index", "tag": "AI & Tech"},
    {"name": "The Verge", "url": "https://www.theverge.com/rss/index.xml", "tag": "AI & Tech"},
    # AI / 科技中文源
    {"name": "爱范儿", "url": "https://www.ifanr.com/feed", "tag": "AI & Tech"},
    {"name": "36氪", "url": "https://36kr.com/feed", "tag": "Startup"},
    {"name": "机器之心", "url": "https://jiqizhixin.m.alauda.cn/rss", "tag": "AI & Tech"},
    {"name": "少数派", "url": "https://sspai.com/feed", "tag": "AI & Tech"},
    # 创业 / 商业中文源
    {"name": "极客公园", "url": "https://www.geekpark.net/rss", "tag": "Startup"},
    {"name": "虎嗅", "url": "https://www.huxiu.com/rss/0.xml", "tag": "Startup"},
    # 英文 AI 新闻（备用）
    {"name": "MIT Tech Review", "url": "https://www.technologyreview.com/feed/", "tag": "AI & Tech"},
    # 备用中文源（机器之心/虎嗅超时时代替）
    {"name": "品玩", "url": "https://www.pingwest.com/feed", "tag": "AI & Tech"},
    {"name": "动点科技", "url": "https://cn.technode.com/feed/", "tag": "Startup"},
]

def fetch_rss(feed_info, max_articles=8):
    """抓取单个 RSS 源，返回文章列表"""
    articles = []
    try:
        print(f"  抓取中: {feed_info['name']}...", end=" ", flush=True)
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; AI-Daily/1.0)"
        }
        resp = requests.get(feed_info["url"], headers=headers, timeout=15)
        resp.raise_for_status()
        feed = feedparser.parse(resp.text)

        for i, entry in enumerate(feed.entries[:max_articles]):
            # 提取标题和链接
            title = entry.get("title", "").strip()
            link = entry.get("link", "") or entry.get("id", "")

            # 提取摘要（先尝试 summary，没有就用 title）
            summary = ""
            if hasattr(entry, "summary"):
                summary = entry.summary
            elif hasattr(entry, "description"):
                summary = entry.description
            # 清理 HTML 标签，只保留纯文字
            import re
            summary = re.sub(r'<[^>]+>', '', summary)
            summary = summary.strip()[:300]  # 截取前300字

            # 发布时间
            published = ""
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                try:
                    dt = datetime.datetime(*entry.published_parsed[:6])
                    published = dt.strftime("%Y-%m-%d")
                except Exception:
                    pass

            articles.append({
                "title": title,
                "link": link,
                "summary": summary,
                "published": published,
                "source": feed_info["name"],
                "tag": feed_info["tag"],
            })

        print(f"✓ 拿到 {len(articles)} 条")
    except Exception as e:
        print(f"✗ 失败: {e}")

    # 每请求之间暂停 1 秒，防止被限流
    time.sleep(1)
    return articles


def fetch_youtube():
    """通过 RSSHub 将 YouTube 频道转为 RSS 抓取"""
    articles = []
    for ch in YOUTUBE_CHANNELS:
        feed_url = f"https://rsshub.app/youtube/channel/{ch['id']}"
        try:
            print(f"  抓取中: YouTube - {ch['name']}...", end=" ", flush=True)
            headers = {"User-Agent": "Mozilla/5.0 (compatible; AI-Daily/1.0)"}
            resp = requests.get(feed_url, headers=headers, timeout=15)
            resp.raise_for_status()
            feed = feedparser.parse(resp.text)
            count = 0
            for entry in feed.entries[:3]:
                import re
                summary = ""
                if hasattr(entry, "summary"):
                    summary = re.sub(r'<[^>]+>', '', entry.summary)
                articles.append({
                    "title": entry.get("title", "").strip(),
                    "link": entry.get("link", "") or entry.get("id", ""),
                    "summary": summary.strip()[:300],
                    "published": "",
                    "source": f"YouTube: {ch['name']}",
                    "tag": ch["tag"],
                })
                count += 1
            print(f"✓ 拿到 {count} 条")
        except Exception as e:
            print(f"✗ 失败: {e}")
        time.sleep(1)
    return articles


def main():
    today = datetime.date.today().strftime("%Y-%m-%d")
    print(f"\n{'='*50}")
    print(f"🤖 AI Daily 抓取任务开始 - {today}")
    print(f"{'='*50}\n")

    all_articles = []

    # 抓 RSS
    for feed in FEEDS:
        articles = fetch_rss(feed)
        all_articles.extend(articles)

    # 抓 YouTube（需要外网访问，国内可能超时，暂跳过）
    # 如需开启，取消注释下面两行，并安装 RSSHub 自建服务
    # print("\n--- YouTube 频道 ---")
    # yt_articles = fetch_youtube()  # noqa

    # 按时间排序（新到旧），无时间则排最后
    all_articles.sort(
        key=lambda x: x["published"] if x["published"] else "9999-99-99",
        reverse=True
    )

    # 保存为 JSON，供 HTML 生成器使用
    output_path = os.path.join(os.path.dirname(__file__), "..", "output", f"articles_{today}.json")
    output_path = os.path.abspath(output_path)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({
            "date": today,
            "total": len(all_articles),
            "articles": all_articles
        }, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 完成！共抓取 {len(all_articles)} 条，保存至:")
    print(f"   {output_path}")
    return output_path


if __name__ == "__main__":
    main()
