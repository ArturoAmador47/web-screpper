#!/usr/bin/env python3
"""
Quick test script to verify the setup.
This will test scraping without requiring API keys.
"""

import asyncio
from src.scraper.news_scraper import NewsScraper, Article


async def test_scraping():
    """Test scraping functionality."""
    print("Testing News Scraper...")
    print("-" * 80)
    
    scraper = NewsScraper()
    
    # Test with TechCrunch RSS feed
    test_feed = "https://techcrunch.com/feed/"
    print(f"\nScraping: {test_feed}")
    
    articles = await scraper.scrape_rss_feed(test_feed)
    
    print(f"\nFound {len(articles)} articles\n")
    
    if articles:
        print("Sample Articles:")
        print("-" * 80)
        for i, article in enumerate(articles[:3], 1):
            print(f"\n{i}. {article.title}")
            print(f"   Source: {article.source}")
            print(f"   URL: {article.url}")
            print(f"   Date: {article.published_date}")
            print(f"   Content preview: {article.content[:100]}...")
    else:
        print("No articles found. This might be due to network issues.")
    
    print("\n" + "=" * 80)
    print("Scraping test completed!")


def main():
    """Run the test."""
    asyncio.run(test_scraping())


if __name__ == "__main__":
    main()
