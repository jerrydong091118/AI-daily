# -*- coding: utf-8 -*-
"""
AI Daily 入口脚本
运行方式: python main.py
功能: 1. 抓取 RSS → 2. 生成 HTML 日报
"""
import subprocess
import sys
import os

PYTHON = "python"  # Windows/Mac/Linux 均兼容

def run(script_path, desc):
    print(f"\n{'='*50}")
    print(f">>> {desc}")
    print(f"{'='*50}")
    result = subprocess.run(
        [PYTHON, script_path],
        capture_output=False
    )
    if result.returncode != 0:
        print(f"❌ {desc} 失败，退出码: {result.returncode}")
        sys.exit(1)
    print(f"✅ {desc} 完成")

if __name__ == "__main__":
    base = os.path.dirname(os.path.abspath(__file__))

    # Step 1: 抓取文章
    run(os.path.join(base, "fetcher", "rss_fetcher.py"), "Step 1: 抓取 RSS 资讯")

    # Step 2: 生成 HTML
    run(os.path.join(base, "scripts", "html_generator.py"), "Step 2: 生成日报网页")

    print("\n" + "🎉"*10)
    print("今日日报生成完毕！")
    print("打开 output/daily_YYYY-MM-DD.html 即可预览")
