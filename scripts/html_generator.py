# -*- coding: utf-8 -*-
"""
AI Daily HTML 生成器
读取 articles_YYYY-MM-DD.json，生成美观的日报网页
"""

import json
import datetime
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

# 标签对应的颜色
TAG_COLORS = {
    "AI & Tech":      ("#E6F1FB", "#185FA5"),   # 蓝底蓝字
    "Startup":        ("#EAF3DE", "#3B6D11"),   # 绿底绿字
    "AI Tools":       ("#EEEDFE", "#534AB7"),   # 紫底紫字
    "AI News":        ("#FBEAF0", "#993556"),   # 粉底粉字
    "AI Paper":       ("#FAEEDA", "#854F0B"),   # 橙底橙字
    "AI Education":   ("#E1F5EE", "#0F6E56"),   # 青底青字
    "AI Interview":  ("#F1EFE8", "#5F5E5A"),   # 灰底灰字
}


def make_card(article, index):
    """生成单篇文章的 HTML 卡片"""
    title = article.get("title", "")
    link = article.get("link", "#")
    summary = article.get("summary", "")
    source = article.get("source", "")
    tag = article.get("tag", "AI & Tech")
    published = article.get("published", "")

    bg, color = TAG_COLORS.get(tag, ("#F1EFE8", "#5F5E5A"))

    return f"""
  <article class="card">
    <div class="card-header">
      <span class="tag" style="background:{bg};color:{color}">{tag}</span>
      <span class="source">{source}</span>
    </div>
    <h2 class="card-title">
      <a href="{link}" target="_blank">{title}</a>
    </h2>
    <p class="card-summary">{summary}</p>
    <div class="card-footer">
      {f'<span class="date">{published}</span>' if published else ''}
      <a href="{link}" class="read-more" target="_blank">阅读原文 ↗</a>
    </div>
  </article>"""


def generate_html(articles_json_path, output_html_path=None):
    """将 JSON 数据渲染为完整 HTML 页面"""

    # 读取文章数据
    with open(articles_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    date_str = data.get("date", datetime.date.today().strftime("%Y-%m-%d"))
    articles = data.get("articles", [])

    # 按 tag 分组
    groups = {}
    for a in articles:
        tag = a.get("tag", "其他")
        groups.setdefault(tag, []).append(a)

    # 生成卡片 HTML
    all_cards_html = "\n".join(
        make_card(a, i) for i, a in enumerate(articles)
    )

    # 按 tag 分区块的 HTML
    tag_blocks_html = ""
    for tag, arts in groups.items():
        bg, color = TAG_COLORS.get(tag, ("#F1EFE8", "#5F5E5A"))
        cards = "\n".join(make_card(a, i) for i, a in enumerate(arts))
        tag_blocks_html += f"""
    <section class="tag-section">
      <div class="tag-section-header" style="border-left: 3px solid {color}">
        <span class="tag-label" style="color:{color}">{tag}</span>
        <span class="tag-count">{len(arts)} 条</span>
      </div>
      <div class="card-grid">
        {cards}
      </div>
    </section>"""

    # 星期几
    weekday = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][
        datetime.datetime.strptime(date_str, "%Y-%m-%d").weekday()
    ]

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AI Daily · {date_str} · {weekday}</title>
  <style>
    :root {{
      --bg: #F8F9FA;
      --card-bg: #FFFFFF;
      --border: #E8E8E8;
      --text-primary: #1A1A1A;
      --text-secondary: #666666;
      --text-muted: #999999;
      --accent: #185FA5;
      --font: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
      font-family: var(--font);
      background: var(--bg);
      color: var(--text-primary);
      line-height: 1.6;
      min-height: 100vh;
    }}

    /* 顶部标题区 */
    .hero {{
      background: linear-gradient(135deg, #1A1A2E 0%, #16213E 50%, #0F3460 100%);
      color: white;
      padding: 3rem 2rem 2.5rem;
      text-align: center;
    }}
    .hero-eyebrow {{
      font-size: 12px;
      letter-spacing: 2px;
      text-transform: uppercase;
      color: rgba(255,255,255,0.5);
      margin-bottom: 8px;
    }}
    .hero h1 {{
      font-size: 2.2rem;
      font-weight: 700;
      letter-spacing: -0.5px;
      margin-bottom: 4px;
    }}
    .hero-date {{
      font-size: 14px;
      color: rgba(255,255,255,0.6);
    }}
    .hero-stats {{
      display: flex;
      justify-content: center;
      gap: 2rem;
      margin-top: 1.5rem;
    }}
    .hero-stat {{
      text-align: center;
    }}
    .hero-stat-num {{
      font-size: 1.8rem;
      font-weight: 700;
      color: #5BC8F5;
    }}
    .hero-stat-label {{
      font-size: 12px;
      color: rgba(255,255,255,0.5);
    }}

    /* 内容区 */
    .container {{
      max-width: 1100px;
      margin: 0 auto;
      padding: 2rem 1.5rem 4rem;
    }}

    /* 分区标题 */
    .tag-section {{
      margin-bottom: 3rem;
    }}
    .tag-section-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0.5rem 0 0.75rem;
      margin-bottom: 1rem;
      border-bottom: 1px solid var(--border);
    }}
    .tag-label {{
      font-size: 15px;
      font-weight: 600;
      letter-spacing: 0.5px;
    }}
    .tag-count {{
      font-size: 12px;
      color: var(--text-muted);
    }}

    /* 卡片网格 */
    .card-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
      gap: 1rem;
    }}

    /* 文章卡片 */
    .card {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 1.1rem 1.2rem;
      transition: box-shadow 0.2s, transform 0.2s;
      display: flex;
      flex-direction: column;
    }}
    .card:hover {{
      box-shadow: 0 4px 16px rgba(0,0,0,0.08);
      transform: translateY(-2px);
    }}
    .card-header {{
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 8px;
    }}
    .tag {{
      font-size: 11px;
      font-weight: 600;
      padding: 2px 8px;
      border-radius: 4px;
      white-space: nowrap;
    }}
    .source {{
      font-size: 12px;
      color: var(--text-muted);
    }}
    .card-title {{
      font-size: 14px;
      font-weight: 600;
      line-height: 1.5;
      margin-bottom: 8px;
      flex: 1;
    }}
    .card-title a {{
      color: var(--text-primary);
      text-decoration: none;
    }}
    .card-title a:hover {{
      color: var(--accent);
    }}
    .card-summary {{
      font-size: 13px;
      color: var(--text-secondary);
      line-height: 1.7;
      margin-bottom: 10px;
      flex: 1;
    }}
    .card-footer {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-top: auto;
      padding-top: 8px;
      border-top: 1px solid var(--border);
    }}
    .date {{
      font-size: 11px;
      color: var(--text-muted);
    }}
    .read-more {{
      font-size: 12px;
      color: var(--accent);
      text-decoration: none;
      font-weight: 500;
    }}
    .read-more:hover {{
      text-decoration: underline;
    }}

    /* 底部 */
    .footer {{
      text-align: center;
      padding: 2rem;
      font-size: 12px;
      color: var(--text-muted);
      border-top: 1px solid var(--border);
    }}
    .footer a {{
      color: var(--accent);
      text-decoration: none;
    }}

    /* 响应式 */
    @media (max-width: 640px) {{
      .hero {{ padding: 2rem 1rem 1.5rem; }}
      .hero h1 {{ font-size: 1.6rem; }}
      .container {{ padding: 1.5rem 1rem 3rem; }}
      .card-grid {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>

  <header class="hero">
    <p class="hero-eyebrow">AI Daily</p>
    <h1>今日 AI & 创业资讯</h1>
    <p class="hero-date">{date_str} · {weekday}</p>
    <div class="hero-stats">
      <div class="hero-stat">
        <div class="hero-stat-num">{len(articles)}</div>
        <div class="hero-stat-label">篇精选文章</div>
      </div>
      <div class="hero-stat">
        <div class="hero-stat-num">{len(groups)}</div>
        <div class="hero-stat-label">个分类</div>
      </div>
      <div class="hero-stat">
        <div class="hero-stat-num">{len(set(a.get('source','') for a in articles))}</div>
        <div class="hero-stat-label">个来源</div>
      </div>
    </div>
  </header>

  <main class="container">
    {tag_blocks_html}
  </main>

  <footer class="footer">
    <p>由 AI Daily 自动抓取生成 · <a href="https://github.com" target="_blank">开源项目</a></p>
  </footer>

</body>
</html>"""

    # 写入文件
    if output_html_path is None:
        output_html_path = articles_json_path.replace("articles_", "daily_").replace(".json", ".html")
    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(html)

    # 同时写一份 index.html（供 GitHub Pages 根路径使用）
    index_path = os.path.join(os.path.dirname(output_html_path), "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ HTML 日报已生成: {output_html_path}")
    return output_html_path


def main():
    # 默认读取今天日期的 JSON
    today = datetime.date.today().strftime("%Y-%m-%d")
    default_json = os.path.join(
        os.path.dirname(__file__), "..", "output", f"articles_{today}.json"
    )
    json_path = os.path.abspath(default_json)

    if len(sys.argv) > 1:
        json_path = sys.argv[1]

    if not os.path.exists(json_path):
        print(f"❌ 文件不存在: {json_path}")
        print("请先运行 rss_fetcher.py 抓取文章")
        return

    output_path = generate_html(json_path)
    print(f"\n📄 打开方式：直接在浏览器打开这个文件即可预览：\n   {output_path}")


if __name__ == "__main__":
    main()
