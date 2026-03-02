#!/usr/bin/env python3
"""
黑猫的AI每日报 - 自动生成脚本
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path

OUTPUT_DIR = Path("/root/.openclaw/workspace/web/ai-vibe-coding-daily")

def get_today_date():
    return datetime.now()

def format_date_cn(date):
    weekdays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
    return f"{date.year}年{date.month}月{date.day}日 {weekdays[date.weekday()]}"

def generate_html(date, news_items, summary):
    date_str = date.strftime("%Y-%m-%d")
    date_cn = format_date_cn(date)
    
    news_cards = []
    for news in news_items:
        card = f"""<article class="news-card"><div class="card-glow"></div><img src="{news.get('image', '')}" alt="{news.get('title', '')}" class="news-image"><div class="news-content"><span class="news-tag tag-{news.get('tag_class', 'default')}">{news.get('tag', '资讯')}</span><h3 class="news-title">{news.get('title', '')}</h3><p class="news-summary">{news.get('summary', '')}</p><div class="news-meta"><span class="meta-source">{news.get('source', '')}</span><span class="meta-date">{news.get('date', '')}</span><a href="{news.get('url', '#')}" target="_blank" class="news-link"><span>阅读全文</span> →</a></div></div></article>"""
        news_cards.append(card)
    
    cards_html = "".join(news_cards)
    
    return f"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>黑猫的AI每日报 | {date_str}</title><style>@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Noto+Sans+SC:wght@300;400;500;700&display=swap');:root{{--neon-blue:#00f5ff;--neon-pink:#ff6b9d;--neon-purple:#b829dd;--dark-bg:#0a0a0f;--card-bg:rgba(20,20,35,0.8);}}*{{margin:0;padding:0;box-sizing:border-box;}}body{{font-family:'Noto Sans SC',sans-serif;background:var(--dark-bg);min-height:100vh;padding:40px 20px;}}body::before{{content:'';position:fixed;top:0;left:0;right:0;bottom:0;background:linear-gradient(90deg,rgba(0,245,255,0.03) 1px,transparent 1px),linear-gradient(rgba(0,245,255,0.03) 1px,transparent 1px);background-size:50px 50px;pointer-events:none;z-index:-1;}}.container{{max-width:900px;margin:0 auto;}}.nav{{text-align:center;margin-bottom:30px;}}.nav a{{color:var(--neon-blue);text-decoration:none;font-family:'Orbitron',monospace;font-size:0.9rem;letter-spacing:2px;opacity:0.8;transition:all 0.3s;}}.nav a:hover{{opacity:1;text-shadow:0 0 20px var(--neon-blue);}}.header{{text-align:center;margin-bottom:50px;position:relative;}}.header::before{{content:'';position:absolute;top:-20px;left:50%;transform:translateX(-50%);width:200px;height:2px;background:linear-gradient(90deg,transparent,var(--neon-blue),transparent);}}.cat-avatar{{width:120px;height:120px;margin:0 auto 20px;border-radius:50%;border:3px solid var(--neon-blue);box-shadow:0 0 30px rgba(0,245,255,0.4);animation:catGlow 3s ease-in-out infinite;object-fit:cover;}}@keyframes catGlow{{0%,100%{{box-shadow:0 0 30px rgba(0,245,255,0.4);}}50%{{box-shadow:0 0 50px rgba(0,245,255,0.7);}}}}.header h1{{font-family:'Orbitron','Noto Sans SC',sans-serif;font-size:2.5rem;font-weight:900;background:linear-gradient(135deg,var(--neon-blue) 0%,var(--neon-pink) 50%,var(--neon-purple) 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;letter-spacing:4px;margin-bottom:15px;}}.header .date{{font-family:'Orbitron',monospace;font-size:1rem;color:var(--neon-blue);opacity:0.8;letter-spacing:3px;}}.summary-box{{background:var(--card-bg);border:1px solid rgba(0,245,255,0.3);border-radius:16px;padding:28px;margin-bottom:40px;box-shadow:0 0 40px rgba(0,245,255,0.1),inset 0 0 20px rgba(0,245,255,0.05);position:relative;overflow:hidden;}}.summary-box::before{{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent,var(--neon-blue),transparent);}}.summary-box h2{{color:var(--neon-blue);font-family:'Orbitron',sans-serif;font-size:1rem;margin-bottom:15px;letter-spacing:2px;text-transform:uppercase;}}.summary-box p{{color:#ccc;line-height:1.8;font-size:1.1rem;}}.news-grid{{display:grid;gap:30px;}}.news-card{{background:var(--card-bg);border:1px solid rgba(0,245,255,0.2);border-radius:20px;overflow:hidden;position:relative;transition:all 0.4s cubic-bezier(0.4,0,0.2,1);}}.news-card:hover{{transform:translateY(-8px);border-color:var(--neon-blue);box-shadow:0 20px 60px rgba(0,245,255,0.2);}}.card-glow{{position:absolute;top:0;left:0;right:0;bottom:0;background:linear-gradient(135deg,rgba(0,245,255,0.1) 0%,transparent 50%,rgba(255,107,157,0.1) 100%);opacity:0;transition:opacity 0.4s;pointer-events:none;}}.news-card:hover .card-glow{{opacity:1;}}.news-image{{width:100%;height:220px;object-fit:cover;border-bottom:1px solid rgba(0,245,255,0.1);}}.news-content{{padding:28px;}}.news-tag{{display:inline-block;padding:6px 16px;border-radius:20px;font-size:0.75rem;font-weight:600;text-transform:uppercase;margin-bottom:15px;letter-spacing:1px;border:1px solid;}}.tag-crisis{{background:rgba(255,0,0,0.1);color:#ff4444;border-color:rgba(255,0,0,0.3);}}.tag-security{{background:rgba(255,0,0,0.1);color:#ff4444;border-color:rgba(255,0,0,0.3);}}.tag-update{{background:rgba(0,245,255,0.1);color:var(--neon-blue);border-color:rgba(0,245,255,0.3);}}.tag-trend{{background:rgba(0,255,136,0.1);color:#00ff88;border-color:rgba(0,255,136,0.3);}}.tag-strategy{{background:rgba(255,107,157,0.1);color:var(--neon-pink);border-color:rgba(255,107,157,0.3);}}.tag-default{{background:rgba(255,255,255,0.05);color:#888;border-color:rgba(255,255,255,0.2);}}.news-title{{font-size:1.3rem;color:#fff;margin-bottom:15px;line-height:1.5;font-weight:600;}}.news-summary{{color:#aaa;line-height:1.8;margin-bottom:20px;font-size:0.95rem;}}.news-meta{{display:flex;justify-content:space-between;align-items:center;font-size:0.85rem;color:#666;padding-top:15px;border-top:1px solid rgba(255,255,255,0.1);}}.meta-source{{color:var(--neon-pink);}}.meta-date{{color:#666;}}.news-link{{color:var(--neon-blue);text-decoration:none;font-weight:500;display:flex;align-items:center;gap:6px;transition:all 0.3s;}}.news-link:hover{{color:var(--neon-pink);gap:10px;}}.footer{{text-align:center;margin-top:60px;color:#666;font-size:0.9rem;font-family:'Orbitron',monospace;letter-spacing:2px;}}.footer span{{color:var(--neon-blue);}}@media (max-width:600px){{.header h1{{font-size:1.8rem;letter-spacing:2px;}}.news-title{{font-size:1.1rem;}}.cat-avatar{{width:80px;height:80px;font-size:48px;}}}}</style></head><body><div class="container"><div class="nav"><a href="index.html">← 返回首页</a></div><header class="header"><img src="black-cat-avatar.jpg" alt="黑猫" class="cat-avatar"><h1>黑猫的AI每日报</h1><p class="date">{date_cn}</p></header><div class="summary-box"><h2>◆ 每日摘要</h2><p>{summary}</p></div><div class="news-grid">{cards_html}</div><footer class="footer"><p>黑猫的AI每日报 · 每日更新</p></footer></div></body></html>"""

def save_html(date, html_content):
    date_str = date.strftime("%Y-%m-%d")
    output_file = OUTPUT_DIR / f"{date_str}.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    return output_file

def git_commit_and_push(date_str):
    try:
        result = subprocess.run(['git', 'rev-parse', '--git-dir'], cwd=OUTPUT_DIR, capture_output=True, text=True)
        if result.returncode != 0:
            print("警告：当前目录不是 git 仓库，跳过提交")
            return False
        subprocess.run(['git', 'add', '-A'], cwd=OUTPUT_DIR, check=True)
        result = subprocess.run(['git', 'diff', '--cached', '--quiet'], cwd=OUTPUT_DIR)
        if result.returncode == 0:
            print("没有更改需要提交")
            return True
        commit_msg = f"Add daily report for {date_str}"
        subprocess.run(['git', 'commit', '-m', commit_msg], cwd=OUTPUT_DIR, check=True)
        print(f"已提交: {commit_msg}")
        subprocess.run(['git', 'push', 'origin', 'main'], cwd=OUTPUT_DIR, check=True)
        print("已推送到 GitHub")
        return True
    except Exception as e:
        print(f"Git 操作失败: {e}")
        return False

def update_index():
    html_files = sorted(OUTPUT_DIR.glob("*.html"))
    html_files = [f for f in html_files if f.name not in ["index.html", "template.html"]]
    links = []
    for f in reversed(html_files):
        date_str = f.stem
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
            date_cn = format_date_cn(date)
            links.append(f'<li><a href="{f.name}">{date_cn}</a></li>')
        except:
            continue
    
    links_html = "".join(links) if links else '<li style="color:#666;padding:20px 0;text-align:center;">暂无文章</li>'
    
    index_html = f"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>黑猫的AI每日报 - 历史归档</title><style>@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Noto+Sans+SC:wght@300;400;500;700&display=swap');:root{{--neon-blue:#00f5ff;--neon-pink:#ff6b9d;--neon-purple:#b829dd;--dark-bg:#0a0a0f;--card-bg:rgba(20,20,35,0.8);}}*{{margin:0;padding:0;box-sizing:border-box;}}body{{font-family:'Noto Sans SC',sans-serif;background:var(--dark-bg);min-height:100vh;padding:40px 20px;}}body::before{{content:'';position:fixed;top:0;left:0;right:0;bottom:0;background:linear-gradient(90deg,rgba(0,245,255,0.03) 1px,transparent 1px),linear-gradient(rgba(0,245,255,0.03) 1px,transparent 1px);background-size:50px 50px;pointer-events:none;z-index:-1;}}.container{{max-width:700px;margin:0 auto;}}.header{{text-align:center;margin-bottom:50px;position:relative;}}.header::before{{content:'';position:absolute;top:-20px;left:50%;transform:translateX(-50%);width:200px;height:2px;background:linear-gradient(90deg,transparent,var(--neon-blue),transparent);}}.cat-avatar{{width:80px;height:80px;margin:0 auto 20px;border-radius:50%;background:linear-gradient(135deg,#2d2d2d 0%,#1a1a2e 100%);border:3px solid var(--neon-blue);box-shadow:0 0 30px rgba(0,245,255,0.4);display:flex;align-items:center;justify-content:center;font-size:48px;animation:catGlow 3s ease-in-out infinite;}}@keyframes catGlow{{0%,100%{{box-shadow:0 0 30px rgba(0,245,255,0.4);}}50%{{box-shadow:0 0 50px rgba(0,245,255,0.7);}}}}.header h1{{font-family:'Orbitron','Noto Sans SC',sans-serif;font-size:2rem;font-weight:900;background:linear-gradient(135deg,var(--neon-blue) 0%,var(--neon-pink) 50%,var(--neon-purple) 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;letter-spacing:3px;margin-bottom:10px;}}.header p{{color:#666;font-family:'Orbitron',monospace;letter-spacing:2px;}}.archive{{background:var(--card-bg);border:1px solid rgba(0,245,255,0.2);border-radius:20px;padding:30px;box-shadow:0 0 40px rgba(0,245,255,0.1);}}.archive h2{{color:var(--neon-blue);margin-bottom:25px;font-size:1.1rem;font-family:'Orbitron',sans-serif;letter-spacing:2px;text-transform:uppercase;display:flex;align-items:center;gap:10px;}}.archive ul{{list-style:none;}}.archive li{{border-bottom:1px solid rgba(255,255,255,0.1);transition:all 0.3s;}}.archive li:last-child{{border-bottom:none;}}.archive a{{display:flex;justify-content:space-between;align-items:center;padding:18px 0;color:#ccc;text-decoration:none;font-size:1.05rem;transition:all 0.3s;}}.archive a:hover{{color:var(--neon-blue);padding-left:10px;}}.archive a::after{{content:'→';color:var(--neon-pink);opacity:0;transition:all 0.3s;}}.archive a:hover::after{{opacity:1;transform:translateX(5px);}}.footer{{text-align:center;margin-top:50px;color:#666;font-size:0.85rem;font-family:'Orbitron',monospace;letter-spacing:2px;}}.footer span{{color:var(--neon-blue);}}</style></head><body><div class="container"><header class="header"><img src="black-cat-avatar.jpg" alt="黑猫" class="cat-avatar"><h1>黑猫的AI每日报</h1><p>每日 AI 资讯自动归档</p></header><div class="archive"><h2>◆ 历史文章</h2><ul>{links_html}</ul></div><footer class="footer"><p>由 <span>OpenClaw AI</span> 自动生成</p></footer></div></body></html>"""
    
    with open(OUTPUT_DIR / "index.html", 'w', encoding='utf-8') as f:
        f.write(index_html)

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    today = get_today_date()
    date_str = today.strftime("%Y-%m-%d")
    print(f"生成早报: {date_str}")
    
    news_data = os.environ.get('DAILY_NEWS_DATA', '')
    summary = os.environ.get('DAILY_SUMMARY', 'AI领域今日无重大更新。')
    
    if news_data:
        try:
            news_items = json.loads(news_data)
        except:
            news_items = []
    else:
        news_items = [{'title': '今日 AI 资讯', 'summary': '请运行搜索任务获取最新资讯。', 'source': 'OpenClaw AI', 'date': date_str, 'url': '#', 'tag': '提示', 'tag_class': 'default', 'image': 'https://images.unsplash.com/photo-1518770660439-4636190af475?w=800&h=400&fit=crop'}]
    
    html_content = generate_html(today, news_items, summary)
    output_file = save_html(today, html_content)
    print(f"已保存: {output_file}")
    
    update_index()
    print("索引页已更新")
    
    git_commit_and_push(date_str)

if __name__ == '__main__':
    main()