"""Tests for PDF generation."""

import pytest
from pathlib import Path
from src.pdf_generator.pdf_service import PDFGenerator


def test_generate_markdown():
    """Test markdown generation from articles."""
    generator = PDFGenerator(output_dir="/tmp/test_output")
    
    articles = [
        {
            "title": "Test Article 1",
            "source": "Test Source",
            "author": "Test Author",
            "published_date": "2024-01-18",
            "url": "https://example.com/1",
            "content": "Test content 1"
        },
        {
            "title": "Test Article 2",
            "source": "Test Source 2",
            "author": "Test Author 2",
            "published_date": "2024-01-18",
            "url": "https://example.com/2",
            "content": "Test content 2"
        }
    ]
    
    markdown = generator.generate_markdown(articles, "Test Title")
    
    assert "Test Title" in markdown
    assert "Test Article 1" in markdown
    assert "Test Article 2" in markdown
    assert "Test Source" in markdown
    assert "Total Articles: 2" in markdown


def test_generate_html():
    """Test HTML generation from markdown."""
    generator = PDFGenerator(output_dir="/tmp/test_output")
    
    markdown_content = "# Test Title\n\n## Article 1\n\nContent here."
    html = generator.generate_html(markdown_content)
    
    assert "<!DOCTYPE html>" in html
    assert "<html>" in html
    assert "Test Title" in html
    assert "Article 1" in html
