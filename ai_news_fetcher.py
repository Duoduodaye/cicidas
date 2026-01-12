#!/usr/bin/env python3
"""
AI News Fetcher for Cicadas Website
Auto-fetches and curates daily AI news content

Requirements:
pip install requests beautifulsoup4 feedparser python-dateutil

Usage:
python ai_news_fetcher.py
"""

import requests
import feedparser
import json
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging
from dataclasses import dataclass
from bs4 import BeautifulSoup
import time

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class NewsItem:
    """Structure for AI news items"""
    title: str
    summary: str
    content: str
    category: str
    source: str
    author: str
    publish_date: str
    read_time: str
    tags: List[str]
    url: str
    featured: bool = False

class AINewsFetcher:
    """Fetches AI news from multiple sources"""
    
    def __init__(self):
        # RSS feeds and sources for AI news
        self.sources = {
            'OpenAI Blog': 'https://openai.com/blog/rss.xml',
            'Google AI Blog': 'https://ai.googleblog.com/feeds/posts/default',
            'Microsoft AI Blog': 'https://blogs.microsoft.com/ai/feed/',
            'DeepMind Blog': 'https://deepmind.com/blog/feed/',
            'Anthropic News': 'https://www.anthropic.com/news/rss',
            'MIT Tech Review AI': 'https://www.technologyreview.com/topic/artificial-intelligence/feed/',
            'AI News': 'https://artificialintelligence-news.com/feed/',
            'Towards Data Science': 'https://towardsdatascience.com/feed'
        }
        
        # Keywords for categorization
        self.categories = {
            'research': ['research', 'paper', 'study', 'algorithm', 'model', 'neural network', 'breakthrough'],
            'industry': ['microsoft', 'google', 'apple', 'amazon', 'meta', 'enterprise', 'business'],
            'tools': ['open source', 'github', 'api', 'framework', 'library', 'tool', 'software'],
            'ethics': ['ethics', 'bias', 'fairness', 'responsible', 'governance', 'regulation'],
            'startups': ['funding', 'investment', 'startup', 'series', 'venture', 'raise']
        }
        
        # AI-related keywords for filtering
        self.ai_keywords = [
            'artificial intelligence', 'machine learning', 'deep learning', 'neural network',
            'AI', 'ML', 'LLM', 'GPT', 'transformer', 'chatbot', 'computer vision',
            'natural language', 'robotics', 'automation', 'algorithm'
        ]

    def is_ai_related(self, title: str, summary: str) -> bool:
        """Check if content is AI-related"""
        text = (title + ' ' + summary).lower()
        return any(keyword.lower() in text for keyword in self.ai_keywords)

    def categorize_news(self, title: str, summary: str) -> str:
        """Categorize news based on content"""
        text = (title + ' ' + summary).lower()
        
        for category, keywords in self.categories.items():
            if any(keyword in text for keyword in keywords):
                return category
        
        return 'research'  # Default category

    def estimate_read_time(self, content: str) -> str:
        """Estimate reading time based on word count"""
        word_count = len(content.split())
        minutes = max(1, round(word_count / 200))  # Average reading speed: 200 words/minute
        return f"{minutes} min"

    def extract_tags(self, title: str, summary: str) -> List[str]:
        """Extract relevant tags from content"""
        text = (title + ' ' + summary).lower()
        
        # Common AI-related tags
        potential_tags = [
            'OpenAI', 'GPT-4', 'GPT-5', 'ChatGPT', 'DALL-E',
            'Google', 'DeepMind', 'Bard', 'Gemini',
            'Microsoft', 'Copilot', 'Azure',
            'Meta', 'LLaMA',
            'Anthropic', 'Claude',
            'Machine Learning', 'Deep Learning', 'Neural Networks',
            'Computer Vision', 'NLP', 'Robotics',
            'Ethics', 'AI Safety', 'Bias',
            'Open Source', 'Research', 'Breakthrough'
        ]
        
        found_tags = []
        for tag in potential_tags:
            if tag.lower() in text:
                found_tags.append(tag)
                if len(found_tags) >= 4:  # Limit to 4 tags
                    break
        
        return found_tags or ['AI', 'Technology']

    def clean_text(self, text: str) -> str:
        """Clean and format text content"""
        if not text:
            return ""
        
        # Remove HTML tags
        soup = BeautifulSoup(text, 'html.parser')
        text = soup.get_text()
        
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Limit length
        if len(text) > 500:
            text = text[:497] + "..."
        
        return text

    def fetch_from_rss(self, source_name: str, url: str) -> List[NewsItem]:
        """Fetch news from RSS feed"""
        news_items = []
        
        try:
            logger.info(f"Fetching from {source_name}: {url}")
            feed = feedparser.parse(url)
            
            if feed.bozo:
                logger.warning(f"RSS feed may have issues: {source_name}")
            
            for entry in feed.entries[:5]:  # Limit to 5 latest items
                try:
                    title = self.clean_text(getattr(entry, 'title', ''))
                    summary = self.clean_text(getattr(entry, 'summary', ''))
                    
                    if not title or not self.is_ai_related(title, summary):
                        continue
                    
                    # Parse publication date
                    pub_date = getattr(entry, 'published_parsed', None)
                    if pub_date:
                        date_str = datetime(*pub_date[:6]).strftime('%Y-%m-%d')
                    else:
                        date_str = datetime.now().strftime('%Y-%m-%d')
                    
                    # Only include recent news (last 7 days)
                    pub_datetime = datetime.strptime(date_str, '%Y-%m-%d')
                    if pub_datetime < datetime.now() - timedelta(days=7):
                        continue
                    
                    news_item = NewsItem(
                        title=title,
                        summary=summary,
                        content=summary,  # For RSS, content is often same as summary
                        category=self.categorize_news(title, summary),
                        source=source_name,
                        author=getattr(entry, 'author', 'AI Team'),
                        publish_date=date_str,
                        read_time=self.estimate_read_time(summary),
                        tags=self.extract_tags(title, summary),
                        url=getattr(entry, 'link', ''),
                        featured=False  # Will be determined later
                    )
                    
                    news_items.append(news_item)
                    
                except Exception as e:
                    logger.error(f"Error processing entry from {source_name}: {e}")
                    continue
            
            logger.info(f"Successfully fetched {len(news_items)} items from {source_name}")
            
        except Exception as e:
            logger.error(f"Error fetching from {source_name}: {e}")
        
        return news_items

    def fetch_all_news(self) -> List[NewsItem]:
        """Fetch news from all sources"""
        all_news = []
        
        for source_name, url in self.sources.items():
            try:
                news_items = self.fetch_from_rss(source_name, url)
                all_news.extend(news_items)
                
                # Be respectful to servers
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Failed to fetch from {source_name}: {e}")
                continue
        
        return all_news

    def deduplicate_and_rank(self, news_items: List[NewsItem]) -> List[NewsItem]:
        """Remove duplicates and rank news items"""
        # Simple deduplication based on title similarity
        unique_news = []
        seen_titles = set()
        
        for item in news_items:
            # Create a normalized title for comparison
            normalized_title = re.sub(r'[^\w\s]', '', item.title.lower()).strip()
            
            if normalized_title not in seen_titles:
                seen_titles.add(normalized_title)
                unique_news.append(item)
        
        # Sort by date (newest first)
        unique_news.sort(key=lambda x: x.publish_date, reverse=True)
        
        # Mark top 2 as featured
        for i in range(min(2, len(unique_news))):
            unique_news[i].featured = True
        
        return unique_news

    def save_to_json(self, news_items: List[NewsItem], filename: str = 'ai_news_data.json'):
        """Save news data to JSON file"""
        try:
            data = {
                'last_updated': datetime.now().isoformat(),
                'total_items': len(news_items),
                'news': [
                    {
                        'id': str(i + 1),
                        'title': item.title,
                        'summary': item.summary,
                        'content': item.content,
                        'category': item.category,
                        'source': item.source,
                        'author': item.author,
                        'publishDate': item.publish_date,
                        'readTime': item.read_time,
                        'tags': item.tags,
                        'url': item.url,
                        'featured': item.featured
                    }
                    for i, item in enumerate(news_items)
                ]
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Saved {len(news_items)} news items to {filename}")
            
        except Exception as e:
            logger.error(f"Error saving to JSON: {e}")

    def generate_daily_summary(self, news_items: List[NewsItem]) -> str:
        """Generate a daily summary of AI news"""
        if not news_items:
            return "No AI news found for today."
        
        summary = f"📰 Daily AI News Summary ({datetime.now().strftime('%Y-%m-%d')})\n\n"
        summary += f"Total articles: {len(news_items)}\n\n"
        
        # Group by category
        by_category = {}
        for item in news_items:
            category = item.category
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(item)
        
        for category, items in by_category.items():
            summary += f"🔸 {category.upper()}: {len(items)} articles\n"
            for item in items[:3]:  # Top 3 per category
                summary += f"  • {item.title} ({item.source})\n"
            summary += "\n"
        
        return summary

def main():
    """Main function to fetch and process AI news"""
    logger.info("Starting AI News Fetcher...")
    
    fetcher = AINewsFetcher()
    
    # Fetch news from all sources
    logger.info("Fetching news from all sources...")
    all_news = fetcher.fetch_all_news()
    
    if not all_news:
        logger.warning("No news items found!")
        return
    
    # Deduplicate and rank
    logger.info("Processing and ranking news...")
    processed_news = fetcher.deduplicate_and_rank(all_news)
    
    # Save to JSON
    fetcher.save_to_json(processed_news)
    
    # Generate summary
    summary = fetcher.generate_daily_summary(processed_news)
    print("\n" + "="*60)
    print(summary)
    print("="*60)
    
    logger.info(f"✅ Successfully processed {len(processed_news)} unique news items")
    logger.info("📁 Data saved to 'ai_news_data.json'")
    logger.info("🌐 You can now integrate this data into your AI News Hub!")

if __name__ == "__main__":
    main()