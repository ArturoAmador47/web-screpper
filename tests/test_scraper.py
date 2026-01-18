"""Tests for the news scraper."""

import pytest
from src.scraper.news_scraper import NewsScraper, Article


@pytest.mark.asyncio
async def test_scrape_rss_feed():
    """Test RSS feed scraping."""
    scraper = NewsScraper()
    # Using a reliable RSS feed for testing
    articles = await scraper.scrape_rss_feed("https://techcrunch.com/feed/")
    
    assert isinstance(articles, list)
    # Should get at least some articles (might be 0 if feed is down)
    if len(articles) > 0:
        article = articles[0]
        assert isinstance(article, Article)
        assert article.title
        assert article.url


@pytest.mark.asyncio
async def test_article_to_dict():
    """Test article dictionary conversion."""
    from datetime import datetime
    
    article = Article(
        title="Test Article",
        content="Test content",
        url="https://example.com",
        source="Test Source",
        published_date=datetime.now(),
        author="Test Author"
    )
    
    article_dict = article.to_dict()
    
    assert article_dict["title"] == "Test Article"
    assert article_dict["content"] == "Test content"
    assert article_dict["url"] == "https://example.com"
    assert article_dict["source"] == "Test Source"
    assert article_dict["author"] == "Test Author"
    assert "published_date" in article_dict
