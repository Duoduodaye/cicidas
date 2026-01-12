#!/usr/bin/env python3
"""
Daily AI News - Simple Version for Cicadas Website
Fetches AI news and generates a simple daily summary

Usage: python daily_ai_news.py
"""

import requests
import json
from datetime import datetime, timedelta
import re

def get_ai_news_simple():
    """
    Get AI news using a simple approach with mock data
    In production, you could integrate with:
    - News APIs (NewsAPI, Bing News API)
    - RSS feeds from AI companies
    - Twitter/X API for trending topics
    - Reddit API for r/MachineLearning, r/artificial
    """
    
    # Mock recent AI news (in real implementation, this would be fetched from APIs)
    recent_news = [
        {
            "title": "OpenAI Announces GPT-4 Turbo with Enhanced Reasoning",
            "summary": "OpenAI has released an updated version of GPT-4 with improved reasoning capabilities and reduced hallucination rates.",
            "source": "OpenAI Blog",
            "date": datetime.now().strftime('%Y-%m-%d'),
            "category": "research",
            "tags": ["GPT-4", "OpenAI", "Reasoning"],
            "featured": True
        },
        {
            "title": "Google's Gemini Ultra Achieves Human-Level Performance on MMLU",
            "summary": "Google DeepMind reports that Gemini Ultra has achieved 90.0% on MMLU benchmark, matching human expert performance.",
            "source": "Google AI",
            "date": datetime.now().strftime('%Y-%m-%d'),
            "category": "research", 
            "tags": ["Gemini", "Google", "Benchmark"],
            "featured": True
        },
        {
            "title": "Microsoft Copilot Studio Launches for Enterprise",
            "summary": "Microsoft introduces Copilot Studio, allowing enterprises to create custom AI assistants for their specific workflows.",
            "source": "Microsoft News",
            "date": (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'),
            "category": "industry",
            "tags": ["Microsoft", "Copilot", "Enterprise"],
            "featured": False
        },
        {
            "title": "Anthropic Releases Constitutional AI Paper",
            "summary": "Anthropic publishes research on Constitutional AI, a method for training helpful, harmless AI systems.",
            "source": "Anthropic",
            "date": (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'),
            "category": "ethics",
            "tags": ["Anthropic", "Constitutional AI", "Safety"],
            "featured": False
        },
        {
            "title": "Meta Open Sources Code Llama 2",
            "summary": "Meta releases Code Llama 2, an improved version of their code generation model, now with better Python support.",
            "source": "Meta AI",
            "date": (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d'),
            "category": "tools",
            "tags": ["Meta", "Code Llama", "Open Source"],
            "featured": False
        }
    ]
    
    return recent_news

def generate_html_summary(news_items):
    """Generate an HTML summary for embedding in the website"""
    
    html = f"""
    <!-- AI News Daily Update - Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')} -->
    <div class="ai-news-daily-update">
        <h3>🤖 Daily AI News Update</h3>
        <p class="last-updated">Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
        
        <div class="featured-news">
            <h4>⭐ Featured Stories</h4>
    """
    
    # Add featured news
    featured = [item for item in news_items if item.get('featured', False)]
    for item in featured:
        html += f"""
            <div class="news-item featured">
                <h5>{item['title']}</h5>
                <p class="summary">{item['summary']}</p>
                <div class="meta">
                    <span class="source">{item['source']}</span> • 
                    <span class="date">{item['date']}</span> • 
                    <span class="category">{item['category'].title()}</span>
                </div>
                <div class="tags">
                    {' '.join([f'<span class="tag">#{tag}</span>' for tag in item['tags']])}
                </div>
            </div>
        """
    
    html += """
        </div>
        
        <div class="other-news">
            <h4>📰 Other Stories</h4>
    """
    
    # Add other news
    other = [item for item in news_items if not item.get('featured', False)]
    for item in other:
        html += f"""
            <div class="news-item">
                <h6>{item['title']}</h6>
                <p class="summary">{item['summary']}</p>
                <div class="meta">
                    <span class="source">{item['source']}</span> • 
                    <span class="date">{item['date']}</span>
                </div>
            </div>
        """
    
    html += """
        </div>
        
        <div class="news-stats">
            <p>📊 Today's Summary:</p>
            <ul>
                <li>Total articles: """ + str(len(news_items)) + """</li>
                <li>Featured stories: """ + str(len(featured)) + """</li>
                <li>Categories covered: """ + str(len(set(item['category'] for item in news_items))) + """</li>
            </ul>
        </div>
        
        <style>
        .ai-news-daily-update {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }
        
        .ai-news-daily-update h3 {
            color: #2c3e50;
            margin-bottom: 10px;
        }
        
        .last-updated {
            color: #7f8c8d;
            font-size: 0.9em;
            margin-bottom: 20px;
        }
        
        .news-item {
            background: white;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .news-item.featured {
            border-left: 4px solid #3498db;
            background: linear-gradient(135deg, #fff 0%, #f8f9ff 100%);
        }
        
        .news-item h5, .news-item h6 {
            margin: 0 0 10px 0;
            color: #2c3e50;
        }
        
        .summary {
            color: #34495e;
            line-height: 1.4;
            margin: 10px 0;
        }
        
        .meta {
            font-size: 0.85em;
            color: #7f8c8d;
            margin: 10px 0;
        }
        
        .tags {
            margin-top: 10px;
        }
        
        .tag {
            background: #3498db;
            color: white;
            padding: 2px 6px;
            border-radius: 12px;
            font-size: 0.75em;
            margin-right: 5px;
        }
        
        .news-stats {
            background: rgba(255,255,255,0.7);
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
        }
        
        .news-stats ul {
            margin: 10px 0 0 20px;
        }
        </style>
    </div>
    <!-- End AI News Daily Update -->
    """
    
    return html

def save_for_website(news_items):
    """Save news data in format suitable for your Cicadas website"""
    
    # Generate HTML snippet
    html_snippet = generate_html_summary(news_items)
    
    # Save HTML snippet
    with open('daily_ai_news.html', 'w', encoding='utf-8') as f:
        f.write(html_snippet)
    
    # Save JSON data
    news_data = {
        "last_updated": datetime.now().isoformat(),
        "news": news_items,
        "summary": {
            "total_articles": len(news_items),
            "featured_count": len([item for item in news_items if item.get('featured', False)]),
            "categories": list(set(item['category'] for item in news_items))
        }
    }
    
    with open('daily_ai_news.json', 'w', encoding='utf-8') as f:
        json.dump(news_data, f, indent=2, ensure_ascii=False)
    
    print("✅ Files generated:")
    print("📁 daily_ai_news.html - HTML snippet for your website")
    print("📁 daily_ai_news.json - JSON data for API integration")

def print_summary(news_items):
    """Print a console summary"""
    print(f"\n📰 AI News Summary for {datetime.now().strftime('%Y-%m-%d')}")
    print("=" * 60)
    
    featured = [item for item in news_items if item.get('featured', False)]
    if featured:
        print("\n⭐ FEATURED STORIES:")
        for item in featured:
            print(f"• {item['title']}")
            print(f"  {item['summary'][:100]}...")
            print(f"  Source: {item['source']} | Tags: {', '.join(item['tags'])}\n")
    
    other = [item for item in news_items if not item.get('featured', False)]
    if other:
        print("📰 OTHER STORIES:")
        for item in other:
            print(f"• {item['title']} ({item['source']})")
    
    print(f"\n📊 Total: {len(news_items)} articles | Featured: {len(featured)} | Categories: {len(set(item['category'] for item in news_items))}")
    print("=" * 60)

def main():
    print("🤖 Starting Daily AI News Fetcher...")
    
    # Get news data
    news_items = get_ai_news_simple()
    
    # Print summary to console
    print_summary(news_items)
    
    # Save files for website integration
    save_for_website(news_items)
    
    print("\n🎉 Daily AI news update complete!")
    print("💡 Next steps:")
    print("   1. Copy daily_ai_news.html content to your AI news page")
    print("   2. Set up a daily cron job to run this script")
    print("   3. Integrate with real news APIs for live data")

if __name__ == "__main__":
    main()