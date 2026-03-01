#!/usr/bin/env python3
"""
AI Vibe Coding 早报自动更新脚本
每天往 daily.html 中追加新的早报内容
"""

import os
import re
from datetime import datetime

def get_today_info():
    """获取今天的日期信息"""
    today = datetime.now()
    weekdays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
    return {
        'date_str': today.strftime('%Y-%m-%d'),
        'date_cn': f"{today.year}年{today.month}月{today.day}日 {weekdays[today.weekday()]}",
        'year': today.year,
        'month': today.month,
        'day': today.day
    }

def update_daily_html(summary, news_items):
    """
    更新 daily.html 文件
    
    参数:
        summary: 一句话总结
        news_items: 新闻列表，每项包含 title, summary, source, url, tag, tag_class, image
    """
    
    file_path = '/root/.openclaw/workspace/web/ai-vibe-coding-daily/daily.html'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    today = get_today_info()
    
    # 1. 更新最新一期的日期和总结
    content = re.sub(
        r'（\d{4}年\d{1,2}月\d{1,2}日 [^）]+）',
        f"（{today['date_cn']}）",
        content
    )
    
    # 更新总结文字
    old_summary_pattern = r'(<div class="summary-box">.*?<p>).*?(</p>.*?</div>)'
    content = re.sub(
        old_summary_pattern,
        lambda m: f"{m.group(1)}{summary}{m.group(2)}",
        content,
        flags=re.DOTALL
    )
    
    # 2. 更新新闻内容（替换 news-grid 中的内容）
    news_html = ''
    for item in news_items:
        news_html += f'''                <article class="news-card">
                    <img src="{item['image']}" class="news-image">
                    <div class="news-content">
                        <span class="news-tag {item['tag_class']}">{item['tag']}</span>
                        <h3 class="news-title">{item['title']}</h3>
                        <p class="news-summary">{item['summary']}</p>
                        <div class="news-meta">
                            <span>{item['source']}</span>
                            <a href="{item['url']}" target="_blank" class="news-link">阅读全文 →</a>
                        </div>
                    </div>
                </article>
'''
    
    # 替换 news-grid 内容
    content = re.sub(
        r'(<div class="news-grid">).*?(</div>\s*</div>\s*<!-- 历史归档)',
        f"\\1\\n{news_html}            </div>\\n        </div>\\n\\n        <!-- 历史归档",
        content,
        flags=re.DOTALL
    )
    
    # 3. 在历史归档中添加新条目
    archive_entry = f'''                    <li>
                        <a href="#" onclick="showPage('latest'); return false;">
                            AI Vibe Coding 早报 
                            <span class="archive-date">{today['date_cn']}</span>
                        </a>
                    </li>
'''
    
    # 在 archive-list 开头插入新条目
    content = re.sub(
        r'(<ul class="archive-list">)',
        f"\\1\\n{archive_entry}",
        content
    )
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"已更新: {file_path}")
    return file_path

def create_new_daily(summary, news_items):
    """
    创建新的早报内容
    由定时任务调用
    """
    try:
        file_path = update_daily_html(summary, news_items)
        return {
            'success': True,
            'file': file_path,
            'date': get_today_info()['date_cn']
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

# 测试数据
if __name__ == '__main__':
    test_summary = "AI氛围编码正在从'快速原型'走向'工程化治理'，开源社区面临AI生成代码的质量危机。"
    
    test_news = [
        {
            'title': '测试新闻标题',
            'summary': '这是测试新闻的摘要内容，用于验证脚本是否正常工作。',
            'source': 'Test Source · 2026-02-28',
            'url': 'https://example.com',
            'tag': '测试',
            'tag_class': 'tag-update',
            'image': 'https://images.unsplash.com/photo-1518770660439-4636190af475?w=800&h=400&fit=crop'
        }
    ]
    
    result = create_new_daily(test_summary, test_news)
    print(result)
