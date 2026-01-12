#!/usr/bin/env python3
"""
AI News Fetcher - Production Version for Cicadas
自动获取和更新AI新闻数据

使用方法：
python ai_news_fetcher.py

设置环境变量：
NEWS_API_KEY=your_api_key_here
"""

import os
import sys
import json
import requests
import feedparser
from datetime import datetime, timedelta
from dotenv import load_dotenv
import re

class CicadasAINews:
    def __init__(self):
        # 加载环境变量
        load_dotenv()
        
        self.news_api_key = os.getenv('NEWS_API_KEY')
        self.max_articles = int(os.getenv('MAX_ARTICLES', 15))
        self.debug = os.getenv('DEBUG_MODE', 'false').lower() == 'true'
        
        # RSS feeds from major AI companies
        self.rss_sources = [
            {
                'url': 'https://openai.com/blog/rss/',
                'name': 'OpenAI Blog',
                'category': 'research'
            },
            {
                'url': 'https://blog.anthropic.com/rss',
                'name': 'Anthropic',
                'category': 'research'
            },
            {
                'url': 'https://ai.meta.com/blog/feed/',
                'name': 'Meta AI',
                'category': 'research'
            }
        ]
        
        # AI keywords for NewsAPI
        self.ai_keywords = [
            'artificial intelligence OR AI',
            'machine learning',
            'GPT OR ChatGPT',
            'OpenAI',
            'Google AI OR DeepMind',
            'large language model OR LLM'
        ]
        
        self.log(f"🤖 AI News Fetcher initialized")
        self.log(f"📊 Max articles: {self.max_articles}")
    
    def log(self, message):
        """日志输出"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"[{timestamp}] {message}")
        
        if self.debug:
            with open('ai_news_debug.log', 'a', encoding='utf-8') as f:
                f.write(f"{datetime.now().isoformat()} - {message}\n")
    
    def fetch_rss_news(self):
        """从RSS feeds获取新闻"""
        self.log("📡 Fetching RSS feeds...")
        all_news = []
        
        for source in self.rss_sources:
            try:
                self.log(f"  📰 Fetching: {source['name']}")
                feed = feedparser.parse(source['url'])
                
                for entry in feed.entries[:5]:  # 每个源取5条最新
                    # 过滤最近7天的新闻
                    pub_date = self.parse_date(entry.get('published', ''))
                    if pub_date and (datetime.now() - datetime.fromisoformat(pub_date)).days > 7:
                        continue
                    
                    news_item = {
                        'id': self.generate_id(entry.title),
                        'title': self.clean_text(entry.title),
                        'summary': self.clean_text(entry.get('summary', '')[:300]),
                        'source': source['name'],
                        'author': self.extract_author(entry),
                        'url': entry.link,
                        'publishDate': pub_date or datetime.now().strftime('%Y-%m-%d'),
                        'category': source['category'],
                        'tags': self.extract_tags(entry.title + ' ' + entry.get('summary', '')),
                        'readTime': self.estimate_read_time(entry.get('summary', '')),
                        'featured': self.is_featured_news(entry.title),
                        'language': 'en'
                    }
                    all_news.append(news_item)
                    
                self.log(f"  ✅ Got {len([n for n in all_news if n['source'] == source['name']])} articles from {source['name']}")
                
            except Exception as e:
                self.log(f"  ❌ Error fetching {source['name']}: {e}")
        
        return all_news
    
    def fetch_news_api(self):
        """使用NewsAPI获取新闻"""
        if not self.news_api_key:
            self.log("⚠️  NewsAPI key not found, skipping NewsAPI")
            return []
        
        self.log("🔍 Fetching from NewsAPI...")
        all_news = []
        
        for keyword in self.ai_keywords:
            try:
                self.log(f"  🔎 Searching: {keyword}")
                
                url = "https://newsapi.org/v2/everything"
                params = {
                    'q': keyword,
                    'language': 'en',
                    'sortBy': 'publishedAt',
                    'pageSize': 10,
                    'apiKey': self.news_api_key,
                    'from': (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d'),
                    'domains': 'techcrunch.com,arstechnica.com,theverge.com,venturebeat.com,thenextweb.com'
                }
                
                response = requests.get(url, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                if 'articles' in data:
                    for article in data['articles']:
                        if not article['title'] or 'removed' in article['title'].lower():
                            continue
                            
                        news_item = {
                            'id': self.generate_id(article['title']),
                            'title': self.clean_text(article['title']),
                            'summary': self.clean_text(article['description'] or ''),
                            'source': article['source']['name'],
                            'author': article.get('author', 'AI News Team'),
                            'url': article['url'],
                            'publishDate': article['publishedAt'][:10],
                            'category': self.categorize_news(article['title']),
                            'tags': self.extract_tags(article['title'] + ' ' + (article['description'] or '')),
                            'readTime': self.estimate_read_time(article['description'] or ''),
                            'featured': self.is_featured_news(article['title']),
                            'language': 'en'
                        }
                        all_news.append(news_item)
                
                self.log(f"  ✅ Got {len([n for n in all_news if keyword.split()[0].lower() in n['title'].lower()])} articles for '{keyword}'")
                
            except Exception as e:
                self.log(f"  ❌ Error with keyword '{keyword}': {e}")
        
        return all_news
    
    def translate_to_spanish(self, news_list):
        """将新闻翻译成西班牙语（简单版本）"""
        self.log("🌐 Translating to Spanish...")
        
        # 简单的关键词翻译映射
        translations = {
            'artificial intelligence': 'inteligencia artificial',
            'machine learning': 'aprendizaje automático',
            'deep learning': 'aprendizaje profundo',
            'neural network': 'red neuronal',
            'chatbot': 'chatbot',
            'breakthrough': 'avance',
            'research': 'investigación',
            'announces': 'anuncia',
            'launches': 'lanza',
            'develops': 'desarrolla',
            'AI': 'IA'
        }
        
        for news in news_list:
            if news['language'] == 'en':
                # 简单翻译标题中的关键词
                spanish_title = news['title']
                for en, es in translations.items():
                    spanish_title = re.sub(f'\\b{en}\\b', es, spanish_title, flags=re.IGNORECASE)
                
                # 如果标题有明显变化，创建西班牙语版本
                if spanish_title != news['title']:
                    news['title_es'] = spanish_title
                    news['language'] = 'multilingual'
        
        return news_list
    
    def clean_text(self, text):
        """清理文本"""
        if not text:
            return ''
        
        # 移除HTML标签
        text = re.sub(r'<[^>]+>', '', text)
        # 标准化空格
        text = re.sub(r'\s+', ' ', text).strip()
        # 移除特殊字符
        text = re.sub(r'[^\w\s\-.,!?;:()\[\]\'\"áéíóúñ]', '', text)
        
        return text
    
    def categorize_news(self, title):
        """新闻分类"""
        title_lower = title.lower()
        
        if any(word in title_lower for word in ['research', 'study', 'paper', 'breakthrough', 'discovery']):
            return 'research'
        elif any(word in title_lower for word in ['company', 'business', 'enterprise', 'market', 'stock']):
            return 'industry'
        elif any(word in title_lower for word in ['tool', 'app', 'software', 'platform', 'api']):
            return 'tools'
        elif any(word in title_lower for word in ['ethics', 'bias', 'safety', 'regulation', 'policy']):
            return 'ethics'
        elif any(word in title_lower for word in ['startup', 'funding', 'investment', 'vc']):
            return 'startups'
        else:
            return 'research'
    
    def extract_tags(self, text):
        """提取标签"""
        tags = []
        text_upper = text.upper()
        
        # 预定义标签
        tag_patterns = {
            'GPT': ['GPT', 'CHATGPT'],
            'OpenAI': ['OPENAI'],
            'Google': ['GOOGLE', 'DEEPMIND', 'BARD'],
            'Microsoft': ['MICROSOFT', 'COPILOT'],
            'Meta': ['META', 'FACEBOOK'],
            'Anthropic': ['ANTHROPIC', 'CLAUDE'],
            'Machine Learning': ['MACHINE LEARNING', 'ML'],
            'Deep Learning': ['DEEP LEARNING', 'NEURAL NETWORK'],
            'Computer Vision': ['COMPUTER VISION', 'IMAGE RECOGNITION'],
            'NLP': ['NATURAL LANGUAGE', 'NLP', 'TEXT'],
            'Robotics': ['ROBOT', 'ROBOTICS'],
            'AI Safety': ['AI SAFETY', 'BIAS', 'ETHICS'],
            'LLM': ['LARGE LANGUAGE MODEL', 'LLM']
        }
        
        for tag, patterns in tag_patterns.items():
            if any(pattern in text_upper for pattern in patterns):
                tags.append(tag)
        
        return tags[:5]  # 最多5个标签
    
    def extract_author(self, entry):
        """提取作者信息"""
        author = entry.get('author', '')
        if not author and 'authors' in entry:
            authors = entry.get('authors', [])
            if authors:
                author = authors[0].get('name', '')
        
        return author or 'AI News Team'
    
    def estimate_read_time(self, text):
        """估算阅读时间"""
        if not text:
            return '2 min'
        
        words = len(text.split())
        minutes = max(1, round(words / 200))  # 假设每分钟200词
        return f'{minutes} min'
    
    def is_featured_news(self, title):
        """判断是否为重点新闻"""
        featured_keywords = [
            'breakthrough', 'launches', 'announces', 'releases', 'unveils',
            'gpt-5', 'gpt-4', 'agi', 'artificial general intelligence',
            'billion', 'million', 'funding', 'acquisition'
        ]
        
        title_lower = title.lower()
        return any(keyword in title_lower for keyword in featured_keywords)
    
    def parse_date(self, date_str):
        """解析日期"""
        if not date_str:
            return None
            
        try:
            # 尝试多种日期格式
            formats = [
                '%a, %d %b %Y %H:%M:%S %Z',
                '%Y-%m-%dT%H:%M:%S%z',
                '%Y-%m-%d %H:%M:%S',
                '%Y-%m-%d'
            ]
            
            for fmt in formats:
                try:
                    dt = datetime.strptime(date_str.replace('GMT', '+0000'), fmt)
                    return dt.strftime('%Y-%m-%d')
                except:
                    continue
                    
        except Exception:
            pass
        
        return None
    
    def generate_id(self, title):
        """生成新闻ID"""
        import hashlib
        return hashlib.md5(title.encode()).hexdigest()[:8]
    
    def deduplicate_news(self, news_list):
        """去重新闻"""
        seen_titles = set()
        unique_news = []
        
        for news in news_list:
            title_key = news['title'].lower().strip()
            if title_key not in seen_titles:
                seen_titles.add(title_key)
                unique_news.append(news)
        
        return unique_news
    
    def get_latest_news(self):
        """获取最新新闻"""
        self.log("🚀 Starting AI news fetch...")
        
        # 获取新闻
        rss_news = self.fetch_rss_news()
        api_news = self.fetch_news_api()
        
        # 合并新闻
        all_news = rss_news + api_news
        self.log(f"📊 Total articles fetched: {len(all_news)}")
        
        # 去重
        unique_news = self.deduplicate_news(all_news)
        self.log(f"📊 Unique articles: {len(unique_news)}")
        
        # 翻译
        unique_news = self.translate_to_spanish(unique_news)
        
        # 按日期和重要性排序
        unique_news.sort(key=lambda x: (x['featured'], x['publishDate']), reverse=True)
        
        # 限制数量
        latest_news = unique_news[:self.max_articles]
        
        self.log(f"✅ Final articles selected: {len(latest_news)}")
        self.log(f"⭐ Featured articles: {len([n for n in latest_news if n['featured']])}")
        
        return latest_news
    
    def save_for_website(self, news_data):
        """保存为网站格式"""
        self.log("💾 Saving news data for website...")
        
        # 添加元数据
        output_data = {
            'lastUpdated': datetime.now().isoformat(),
            'totalArticles': len(news_data),
            'featuredCount': len([n for n in news_data if n['featured']]),
            'categories': list(set(n['category'] for n in news_data)),
            'sources': list(set(n['source'] for n in news_data)),
            'news': news_data
        }
        
        # 保存JSON数据
        json_path = 'ai_news_data.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        self.log(f"📄 JSON data saved to: {json_path}")
        
        # 生成JavaScript格式
        js_content = f"""// AI News Data - Auto-generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}
// Last updated: {output_data['lastUpdated']}
// Total articles: {output_data['totalArticles']}

const aiNewsData = {json.dumps(output_data, indent=2, ensure_ascii=False)};

// For backward compatibility
const mockNews = aiNewsData.news;

// Export for modules
if (typeof module !== 'undefined' && module.exports) {{
    module.exports = aiNewsData;
}}
"""
        
        js_path = 'ai_news_data.js'
        with open(js_path, 'w', encoding='utf-8') as f:
            f.write(js_content)
        
        self.log(f"📄 JavaScript data saved to: {js_path}")
        
        return output_data

def main():
    """主函数"""
    try:
        fetcher = CicadasAINews()
        
        # 检查API密钥
        if not fetcher.news_api_key:
            print("❌ ERROR: NEWS_API_KEY not found!")
            print("Please set your NewsAPI key in the .env file")
            print("Create .env file with: NEWS_API_KEY=your_api_key_here")
            sys.exit(1)
        
        # 获取新闻
        latest_news = fetcher.get_latest_news()
        
        # 保存数据
        saved_data = fetcher.save_for_website(latest_news)
        
        # 输出摘要
        print("\n" + "="*60)
        print(f"🎉 AI News Update Complete!")
        print(f"📅 Updated: {saved_data['lastUpdated']}")
        print(f"📊 Articles: {saved_data['totalArticles']}")
        print(f"⭐ Featured: {saved_data['featuredCount']}")
        print(f"📂 Categories: {', '.join(saved_data['categories'])}")
        print(f"📰 Sources: {', '.join(saved_data['sources'])}")
        print("="*60)
        
        # 显示前几条新闻标题
        print("\n📋 Latest Headlines:")
        for i, news in enumerate(latest_news[:5], 1):
            status = "⭐" if news['featured'] else "📰"
            print(f"{i}. {status} {news['title']} ({news['source']})")
        
        print(f"\n💾 Files saved:")
        print(f"  - ai_news_data.json")
        print(f"  - ai_news_data.js")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        if fetcher.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()