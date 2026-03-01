#!/usr/bin/env python3
"""
AI Vibe Coding 早报自动生成脚本
用法: python3 generate_daily.py
"""

import os
import sys
import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

# 配置
OUTPUT_DIR = Path("/root/.openclaw/workspace/web/ai-vibe-coding-daily")
TEMPLATE_FILE = OUTPUT_DIR / "template.html"

def get_today_date():
    """获取今天日期"""
    return datetime.now()

def format_date_cn(date):
    """格式化中文日期"""
    weekdays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
    return f"{date.year}年{date.month}月{date.day}日 {weekdays[date.weekday()]}"

def search_news():
    """搜索 AI Vibe Coding 相关新闻"""
    # 这里调用 kimi_search 或其他搜索工具
    # 由于是在子代理中执行，实际搜索由外部调用传入
    return []

def generate_html(date, news_items, summary):
    """生成 HTML 页面"""
    
    date_str = date.strftime("%Y-%m-%d")
    date_cn = format_date_cn(date)
    
    # 构建新闻卡片 HTML
    news_cards = []
    for i, news in enumerate(news_items, 1):
        card = f'''
            <article class="news-card">
                <img src="{news.get('image', 'https://images.unsplash.com/photo-1518770660439-4636190af475?w=800&h=400&fit=crop')}" 
                     alt="{news.get('title', 'News')}" class="news-image">
                <div class="news-content">
                    <span class="news-tag tag-{news.get('tag_class', 'default')}">{news.get('tag', '资讯')}</span>
                    <h3 class="news-title">{news.get('title', '')}</h3>
                    <p class="news-summary">{news.get('summary', '')}</p>
                    <div class="news-meta">
                        <span>{news.get('source', '')} · {news.get('date', '')}</span>
                        <a href="{news.get('url', '#')}" target="_blank" class="news-link">阅读全文 →</a>
                    </div>
                </div>
            </article>
        '''
        news_cards.append(card)
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Vibe Coding 早报 | {date_str}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }}
        .container {{ max-width: 800px; margin: 0 auto; }}
        .header {{ text-align: center; margin-bottom: 40px; color: white; }}
        .header h1 {{ font-size: 2.5rem; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.2); }}
        .header .date {{ font-size: 1.1rem; opacity: 0.9; }}
        .summary-box {{
            background: rgba(255,255,255,0.95);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        }}
        .summary-box h2 {{ color: #667eea; font-size: 1.2rem; margin-bottom: 12px; display: flex; align-items: center; gap: 8px; }}
        .summary-box p {{ color: #444; line-height: 1.7; font-size: 1rem; }}
        .news-grid {{ display: grid; gap: 24px; }}
        .news-card {{
            background: white;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            transition: transform 0.3s, box-shadow 0.3s;
        }}
        .news-card:hover {{ transform: translateY(-4px); box-shadow: 0 8px 30px rgba(0,0,0,0.15); }}
        .news-image {{ width: 100%; height: 200px; object-fit: cover; background: linear-gradient(45deg, #f0f0f0, #e0e0e0); }}
        .news-content {{ padding: 24px; }}
        .news-tag {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            margin-bottom: 12px;
        }}
        .tag-crisis {{ background: #fee; color: #c33; }}
        .tag-security {{ background: #ffe8e8; color: #d32f2f; }}
        .tag-update {{ background: #e3f2fd; color: #1976d2; }}
        .tag-trend {{ background: #e8f5e9; color: #388e3c; }}
        .tag-strategy {{ background: #fff3e0; color: #f57c00; }}
        .tag-default {{ background: #f5f5f5; color: #666; }}
        .news-title {{ font-size: 1.3rem; color: #222; margin-bottom: 12px; line-height: 1.4; }}
        .news-summary {{ color: #666; line-height: 1.7; margin-bottom: 16px; }}
        .news-meta {{ display: flex; justify-content: space-between; align-items: center; font-size: 0.85rem; color: #999; }}
        .news-link {{ color: #667eea; text-decoration: none; font-weight: 500; }}
        .news-link:hover {{ text-decoration: underline; }}
        .footer {{ text-align: center; margin-top: 40px; color: white; opacity: 0.8; font-size: 0.9rem; }}
        .nav {{ text-align: center; margin-bottom: 20px; }}
        .nav a {{ color: white; text-decoration: none; opacity: 0.8; }}
        .nav a:hover {{ opacity: 1; }}
        @media (max-width: 600px) {{
            .header h1 {{ font-size: 1.8rem; }}
            .news-title {{ font-size: 1.1rem; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="nav">
            <a href="index.html">← 返回首页</a>
        </div>
        
        <header class="header">
            <h1>🤖 AI Vibe Coding 早报</h1>
            <p class="date">{date_cn}</p>
        </header>
        
        <div class="summary-box">
            <h2>📌 一句话总结</h2>
            <p>{summary}</p>
        </div>
        
        <div class="news-grid">
            {''.join(news_cards)}
        </div>
        
        <footer class="footer">
            <p>由 OpenClaw AI 自动生成 · 每日更新</p>
        </footer>
    </div>
</body>
</html>'''
    
    return html

def save_html(date, html_content):
    """保存 HTML 文件"""
    date_str = date.strftime("%Y-%m-%d")
    output_file = OUTPUT_DIR / f"{date_str}.html"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return output_file

def update_index():
    """更新索引页"""
    html_files = sorted(OUTPUT_DIR.glob("*.html"))
    html_files = [f for f in html_files if f.name != "index.html" and f.name != "template.html"]
    
    links = []
    for f in reversed(html_files):  # 最新的在前
        date_str = f.stem
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
            date_cn = format_date_cn(date)
            links.append(f'<li><a href="{f.name}">{date_cn}</a></li>')
        except:
            continue
    
    index_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Vibe Coding 早报 - 历史归档</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }}
        .container {{ max-width: 600px; margin: 0 auto; }}
        .header {{ text-align: center; margin-bottom: 40px; color: white; }}
        .header h1 {{ font-size: 2rem; margin-bottom: 10px; }}
        .header p {{ opacity: 0.9; }}
        .archive {{
            background: white;
            border-radius: 16px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        }}
        .archive h2 {{ color: #667eea; margin-bottom: 20px; font-size: 1.3rem; }}
        .archive ul {{ list-style: none; }}
        .archive li {{ border-bottom: 1px solid #eee; }}
        .archive li:last-child {{ border-bottom: none; }}
        .archive a {{
            display: block;
            padding: 16px 0;
            color: #333;
            text-decoration: none;
            font-size: 1.1rem;
            transition: color 0.2s;
        }}
        .archive a:hover {{ color: #667eea; }}
        .footer {{ text-align: center; margin-top: 40px; color: white; opacity: 0.8; font-size: 0.9rem; }}
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>🤖 AI Vibe Coding 早报</h1>
            <p>每日 AI 编程资讯自动归档</p>
        </header>
        
        <div class="archive">
            <h2>📚 历史文章</h2>
            <ul>
                {''.join(links) if links else '<li style="color: #999; padding: 16px 0;">暂无文章</li>'}
            </ul>
        </div>
        
        <footer class="footer">
            <p>由 OpenClaw AI 自动生成</p>
        </footer>
    </div>
</body>
</html>'''
    
    with open(OUTPUT_DIR / "index.html", 'w', encoding='utf-8') as f:
        f.write(index_html)

def main():
    """主函数"""
    # 确保输出目录存在
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # 获取今天日期
    today = get_today_date()
    date_str = today.strftime("%Y-%m-%d")
    
    print(f"生成早报: {date_str}")
    
    # 从环境变量或参数获取新闻数据
    # 实际使用时，这些数据由调用者（AI Agent）搜索整理后传入
    news_data = os.environ.get('DAILY_NEWS_DATA', '')
    summary = os.environ.get('DAILY_SUMMARY', 'AI氛围编码领域今日无重大更新。')
    
    if news_data:
        try:
            news_items = json.loads(news_data)
        except:
            news_items = []
    else:
        # 默认示例数据
        news_items = [
            {
                'title': '今日 AI Vibe Coding 资讯',
                'summary': '请运行搜索任务获取最新资讯。',
                'source': 'OpenClaw AI',
                'date': date_str,
                'url': '#',
                'tag': '提示',
                'tag_class': 'default',
                'image': 'https://images.unsplash.com/photo-1518770660439-4636190af475?w=800&h=400&fit=crop'
            }
        ]
    
    # 生成 HTML
    html_content = generate_html(today, news_items, summary)
    
    # 保存文件
    output_file = save_html(today, html_content)
    print(f"已保存: {output_file}")
    
    # 更新索引
    update_index()
    print("索引页已更新")

if __name__ == '__main__':
    main()
