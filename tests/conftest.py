"""Tests configuration."""

import pytest


@pytest.fixture
def sample_article():
    """Sample article for testing."""
    return {
        "title": "Test Article",
        "content": "This is test content for an article.",
        "url": "https://example.com/article",
        "source": "Test Source",
        "published_date": "2024-01-18T12:00:00",
        "author": "Test Author"
    }


@pytest.fixture
def sample_articles():
    """Sample articles list for testing."""
    return [
        {
            "title": "Article 1",
            "content": "Content 1",
            "url": "https://example.com/1",
            "source": "Source 1",
            "published_date": "2024-01-18T12:00:00",
            "author": "Author 1"
        },
        {
            "title": "Article 2",
            "content": "Content 2",
            "url": "https://example.com/2",
            "source": "Source 2",
            "published_date": "2024-01-18T13:00:00",
            "author": "Author 2"
        }
    ]
