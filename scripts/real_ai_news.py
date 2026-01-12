#!/usr/bin/env python3
"""
Real AI News Fetcher - Production Version
获取真实的AI新闻数据

使用方法：
1. 注册API密钥
2. 配置环境变量
3. 运行脚本获取最新新闻
"""

import requests
import json
import os
from datetime import datetime, timedelta
import feedparser  # RSS feeds
import re

class AINewsAggregator:
    def __init__(self):
        self.news_api_key = os.environ.get('NEWS_API_KEY')  # newsapi.org
        self.sources = {
            'rss_feeds': [
                'https://openai.com/blog/rss/',
                'https://deepmind.google/blog/rss.xml',
                'https://blog.anthropic.com/rss/',
                'https://www.microsoft.com/en-us/research/feed/',
                'https://ai.meta.com/blog/feed/',
            ],
            'news_keywords': [
                'artificial intelligence',
                'machine learning', 
                'GPT',
                'ChatGPT',
                'OpenAI',
                'Google AI',
                'DeepMind'
            ]
        }
    
    def fetch_rss_news(self):
        """从RSS feeds获取新闻"""
        all_news = []
        
        for feed_url in self.sources['rss_feeds']:
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries[:5]:  # 取每个源最新5条
                    news_item = {
                        'title': entry.title,
                        'summary': self.clean_text(entry.summary if hasattr(entry, 'summary') else ''),
                        'source': feed.feed.title if hasattr(feed.feed, 'title') else 'AI Blog',
                        'url': entry.link,
                        'date': self.parse_date(entry.published if hasattr(entry, 'published') else ''),
                        'category': self.categorize_news(entry.title),
                        'tags': self.extract_tags(entry.title + ' ' + (entry.summary if hasattr(entry, 'summary') else '')),
                        'featured': 'GPT' in entry.title or 'breakthrough' in entry.title.lower()
                    }
                    all_news.append(news_item)
                    
            except Exception as e:
                print(f"Error fetching RSS from {feed_url}: {e}")
                
        return all_news
    
    def fetch_news_api(self):
        """使用NewsAPI获取新闻"""
        if not self.news_api_key:
            return []
            
        all_news = []
        
        for keyword in self.sources['news_keywords']:
            try:
                url = f"https://newsapi.org/v2/everything"
                params = {
                    'q': keyword,
                    'language': 'en',
                    'sortBy': 'publishedAt',
                    'pageSize': 10,
                    'apiKey': self.news_api_key,
                    'from': (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
                }
                
                response = requests.get(url, params=params)
                data = response.json()
                
                if 'articles' in data:
                    for article in data['articles']:
                        news_item = {
                            'title': article['title'],
                            'summary': self.clean_text(article['description'] or ''),
                            'source': article['source']['name'],
                            'url': article['url'],
                            'date': article['publishedAt'][:10],
                            'category': self.categorize_news(article['title']),
                            'tags': self.extract_tags(article['title'] + ' ' + (article['description'] or '')),
                            'featured': any(term in article['title'].lower() for term in ['breakthrough', 'launches', 'announces'])
                        }
                        all_news.append(news_item)
                        
            except Exception as e:
                print(f"Error fetching news for '{keyword}': {e}")
                
        return all_news
    
    def clean_text(self, text):
        """清理文本内容"""
        text = re.sub(r'<[^>]+>', '', text)  # 移除HTML标签
        text = re.sub(r'\s+', ' ', text).strip()  # 标准化空格
        return text[:200] + '...' if len(text) > 200 else text
    
    def categorize_news(self, title):
        """根据标题分类新闻"""
        title_lower = title.lower()
        
        if any(word in title_lower for word in ['research', 'study', 'paper', 'breakthrough']):
            return 'research'
        elif any(word in title_lower for word in ['company', 'business', 'enterprise', 'market']):
            return 'industry'
        elif any(word in title_lower for word in ['tool', 'app', 'software', 'platform']):
            return 'tools'
        elif any(word in title_lower for word in ['ethics', 'bias', 'safety', 'regulation']):
            return 'ethics'
        elif any(word in title_lower for word in ['startup', 'funding', 'investment']):
            return 'startups'
        else:
            return 'research'
    
    def extract_tags(self, text):
        """提取关键词标签"""
        common_tags = [
            'GPT', 'ChatGPT', 'OpenAI', 'Google', 'DeepMind', 'Anthropic',
            'Microsoft', 'Meta', 'AI Safety', 'Machine Learning', 'LLM',
            'Computer Vision', 'NLP', 'Robotics', 'AGI'
        ]
        
        found_tags = []
        text_upper = text.upper()
        
        for tag in common_tags:
            if tag.upper() in text_upper:
                found_tags.append(tag)
                
        return found_tags[:5]  # 最多5个标签
    
    def parse_date(self, date_str):
        """解析日期"""
        try:
            if date_str:
                return datetime.fromisoformat(date_str.replace('Z', '+00:00')).strftime('%Y-%m-%d')
        except:
            pass
        return datetime.now().strftime('%Y-%m-%d')
    
    def deduplicate_news(self, news_list):
        """去重新闻"""
        seen_titles = set()
        unique_news = []
        
        for news in news_list:
            if news['title'] not in seen_titles:
                seen_titles.add(news['title'])
                unique_news.append(news)
                
        return unique_news
    
    def get_latest_news(self):
        """获取最新新闻"""
        print("🤖 开始获取最新AI新闻...")
        
        # 从多个来源获取新闻
        rss_news = self.fetch_rss_news()
        api_news = self.fetch_news_api()
        
        # 合并并去重
        all_news = rss_news + api_news
        unique_news = self.deduplicate_news(all_news)
        
        # 按日期排序
        unique_news.sort(key=lambda x: x['date'], reverse=True)
        
        # 选择最新15条
        latest_news = unique_news[:15]
        
        print(f"📰 获取到 {len(latest_news)} 条最新AI新闻")
        
        return latest_news
    
    def save_to_website(self, news_data):
        """保存到网站格式"""
        # 生成JavaScript格式的数据
        js_data = f"""
// 自动生成的AI新闻数据 - {datetime.now().strftime('%Y-%m-%d %H:%M')}
const mockNews = {json.dumps(news_data, indent=2, ensure_ascii=False)};
        """
        
        # 保存到文件
        with open('ai_news_data.js', 'w', encoding='utf-8') as f:
            f.write(js_data)
            
        print("💾 新闻数据已保存到 ai_news_data.js")
        
        # 生成HTML片段
        html_content = self.generate_html_snippet(news_data)
        with open('ai_news_snippet.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        print("🌐 HTML片段已保存到 ai_news_snippet.html")
    
    def generate_html_snippet(self, news_data):
        """生成HTML片段"""
        featured_news = [n for n in news_data if n.get('featured', False)]
        regular_news = [n for n in news_data if not n.get('featured', False)]
        
        html = f"""
<div class="ai-news-update">
    <h3>🤖 最新AI新闻 - {datetime.now().strftime('%Y-%m-%d')}</h3>
    
    <div class="featured-news">
        <h4>⭐ 重点新闻</h4>
"""
        
        for news in featured_news[:3]:
            html += f"""
        <div class="news-item featured">
            <h5><a href="{news['url']}" target="_blank">{news['title']}</a></h5>
            <p>{news['summary']}</p>
            <div class="meta">{news['source']} • {news['date']}</div>
            <div class="tags">{''.join([f'<span class="tag">#{tag}</span>' for tag in news['tags']])}</div>
        </div>
"""
        
        html += """
    </div>
    <div class="other-news">
        <h4>📰 其他新闻</h4>
"""
        
        for news in regular_news[:8]:
            html += f"""
        <div class="news-item">
            <h6><a href="{news['url']}" target="_blank">{news['title']}</a></h6>
            <p>{news['summary']}</p>
            <div class="meta">{news['source']} • {news['date']}</div>
        </div>
"""
        
        html += """
    </div>
</div>
        """
        
        return html

def main():
    """主函数"""
    aggregator = AINewsAggregator()
    latest_news = aggregator.get_latest_news()
    aggregator.save_to_website(latest_news)
    
    print("✅ AI新闻更新完成！")
    print("📋 使用说明：")
    print("1. 将 ai_news_data.js 内容复制到你的网页中")
    print("2. 或直接使用 ai_news_snippet.html 片段")
    print("3. 设置定时任务每日自动运行此脚本")

if __name__ == "__main__":
    main()