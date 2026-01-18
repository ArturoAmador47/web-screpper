"""Scraper module for fetching tech news from various sources."""

import asyncio
import feedparser
import requests
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

try:
    from crawl4ai import AsyncWebCrawler
    CRAWL4AI_AVAILABLE = True
except ImportError:
    CRAWL4AI_AVAILABLE = False

from src.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Article:
    """Represents a news article."""
    
    def __init__(
        self,
        title: str,
        content: str,
        url: str,
        source: str,
        published_date: Optional[datetime] = None,
        author: Optional[str] = None
    ):
        self.title = title
        self.content = content
        self.url = url
        self.source = source
        self.published_date = published_date or datetime.now()
        self.author = author
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert article to dictionary."""
        return {
            "title": self.title,
            "content": self.content,
            "url": self.url,
            "source": self.source,
            "published_date": self.published_date.isoformat(),
            "author": self.author
        }


class NewsScraper:
    """Scraper for tech news from RSS feeds and web pages."""
    
    def __init__(self):
        self.headers = {
            "User-Agent": settings.user_agent
        }
        self.timeout = settings.request_timeout
    
    async def scrape_rss_feed(self, feed_url: str) -> List[Article]:
        """Scrape articles from an RSS feed."""
        logger.info(f"Scraping RSS feed: {feed_url}")
        articles = []
        
        try:
            feed = feedparser.parse(feed_url)
            
            for entry in feed.entries[:10]:  # Limit to 10 recent articles
                title = entry.get("title", "No Title")
                link = entry.get("link", "")
                
                # Get content
                content = ""
                if hasattr(entry, "summary"):
                    content = entry.summary
                elif hasattr(entry, "description"):
                    content = entry.description
                elif hasattr(entry, "content"):
                    content = entry.content[0].value if entry.content else ""
                
                # Get published date
                published_date = None
                if hasattr(entry, "published_parsed") and entry.published_parsed:
                    published_date = datetime(*entry.published_parsed[:6])
                
                # Get author
                author = entry.get("author", None)
                
                # Determine source
                source = feed.feed.get("title", feed_url)
                
                article = Article(
                    title=title,
                    content=content,
                    url=link,
                    source=source,
                    published_date=published_date,
                    author=author
                )
                articles.append(article)
                
        except Exception as e:
            logger.error(f"Error scraping RSS feed {feed_url}: {e}")
        
        logger.info(f"Scraped {len(articles)} articles from {feed_url}")
        return articles
    
    async def scrape_webpage(self, url: str) -> Optional[str]:
        """Scrape content from a webpage using Crawl4AI or fallback to requests."""
        logger.info(f"Scraping webpage: {url}")
        
        try:
            if CRAWL4AI_AVAILABLE:
                async with AsyncWebCrawler() as crawler:
                    result = await crawler.arun(url=url)
                    if result.success:
                        return result.markdown
            
            # Fallback to requests
            response = requests.get(
                url, 
                headers=self.headers, 
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.text
            
        except Exception as e:
            logger.error(f"Error scraping webpage {url}: {e}")
            return None
    
    async def scrape_all_sources(self, sources: Optional[List[str]] = None) -> List[Article]:
        """Scrape all configured news sources."""
        if sources is None:
            sources = settings.get_news_sources()
        
        if not sources:
            logger.warning("No news sources configured")
            return []
        
        logger.info(f"Scraping {len(sources)} news sources")
        
        all_articles = []
        tasks = [self.scrape_rss_feed(source) for source in sources]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, list):
                all_articles.extend(result)
            elif isinstance(result, Exception):
                logger.error(f"Error in scraping task: {result}")
        
        logger.info(f"Total articles scraped: {len(all_articles)}")
        return all_articles


async def main():
    """Test the scraper."""
    scraper = NewsScraper()
    articles = await scraper.scrape_all_sources()
    for article in articles[:5]:
        print(f"\nTitle: {article.title}")
        print(f"Source: {article.source}")
        print(f"URL: {article.url}")
        print(f"Date: {article.published_date}")
        print(f"Content preview: {article.content[:100]}...")


if __name__ == "__main__":
    asyncio.run(main())
