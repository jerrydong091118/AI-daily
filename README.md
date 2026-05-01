# 🤖 AI Daily - 每日 AI & 创业资讯日报

自动从多个优质 RSS 源抓取资讯，每天生成一份可分享的日报网页。

## 📁 项目结构

```
ai-daily/
├── main.py                      # 一键运行入口（抓取 + 生成）
├── fetcher/
│   └── rss_fetcher.py          # RSS 抓取脚本
├── scripts/
│   └── html_generator.py       # HTML 日报生成器
├── output/
│   ├── articles_YYYY-MM-DD.json # 原始文章数据
│   └── daily_YYYY-MM-DD.html    # 生成的日报网页
├── requirements.txt             # Python 依赖
└── .github/workflows/daily.yml   # GitHub Actions 自动部署配置
```

## 🚀 本地运行

**第一步：安装依赖**
```bash
pip install -r requirements.txt
```

**第二步：一键生成今日日报**
```bash
python main.py
```

**第三步：预览日报**
打开 `output/daily_YYYY-MM-DD.html`，在浏览器中查看效果。

## ☁️ 部署到云端（自动运行）

项目配置了 GitHub Actions，部署后**每天北京时间 08:00 自动运行**，无需手动操作。

### 部署步骤

**1. 在 GitHub 创建新仓库**
- 访问 github.com → New repository
- 仓库名：`ai-daily`（随意）
- 设为 Private 或 Public 均可

**2. 把本地代码上传到 GitHub**
```bash
cd D:\ai-daily
git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/你的用户名/ai-daily.git
git push -u origin main
```

**3. 开启 GitHub Pages**
- 进入仓库 → Settings → Pages
- Source 选 **GitHub Actions**
- 保存

**4. 确认 Actions 在运行**
- 进入仓库 → Actions 标签页
- 看到 "AI Daily - 自动生成日报" 工作流在跑
- 等 1~2 分钟，日报链接会出现在页面顶部

## 📡 抓取的资讯源

| 来源 | 语言 | 分类 |
|------|------|------|
| TechCrunch | 英文 | 创业 & 科技 |
| Ars Technica | 英文 | AI & 科技 |
| The Verge | 英文 | AI & 科技 |
| MIT Tech Review | 英文 | AI & 科技 |
| 爱范儿 | 中文 | AI & 科技 |
| 36氪 | 中文 | 创业 |
| 少数派 | 中文 | AI & 科技 |
| 极客公园 | 中文 | 创业 |
| 品玩 | 中文 | AI & 科技 |
| 动点科技 | 中文 | 创业 |

> 注：少数源在国内可能超时（如虎嗅、机器之心），脚本会自动跳过，不影响整体运行。

## ⚙️ 自定义修改

**修改抓取的来源**
编辑 `fetcher/rss_fetcher.py` 中的 `FEEDS` 列表，添加/删除 RSS 地址。

**修改日报样式**
编辑 `scripts/html_generator.py` 中的 CSS 样式部分。

**修改自动运行时间**
编辑 `.github/workflows/daily.yml` 中的 `cron: "0 0 * * *"`
- 格式为 [分][时][日][月][周]
- 0 0 * * * = 每天 00:00 UTC = **北京时间 08:00**
