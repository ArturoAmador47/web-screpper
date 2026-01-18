"""PDF generation module using WeasyPrint."""

import logging
from typing import List, Dict, Any
from datetime import datetime
from pathlib import Path
import markdown
from weasyprint import HTML, CSS

from src.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PDFGenerator:
    """Generate PDF reports from news articles."""
    
    def __init__(self, output_dir: str = None):
        self.output_dir = Path(output_dir or settings.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_markdown(
        self,
        articles: List[Dict[str, Any]],
        title: str = None
    ) -> str:
        """Generate markdown content from articles."""
        title = title or settings.pdf_title
        
        md_content = f"# {title}\n\n"
        md_content += f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"
        md_content += f"---\n\n"
        md_content += f"**Total Articles: {len(articles)}**\n\n"
        md_content += "---\n\n"
        
        for idx, article in enumerate(articles, 1):
            md_content += f"## {idx}. {article.get('title', 'No Title')}\n\n"
            
            # Metadata
            source = article.get('source', 'Unknown')
            author = article.get('author', 'Unknown')
            date = article.get('published_date', 'N/A')
            url = article.get('url', '#')
            
            md_content += f"**Source:** {source}  \n"
            md_content += f"**Author:** {author}  \n"
            md_content += f"**Published:** {date}  \n"
            md_content += f"**URL:** [{url}]({url})  \n\n"
            
            # Content
            content = article.get('content', 'No content available.')
            md_content += f"{content}\n\n"
            md_content += "---\n\n"
        
        return md_content
    
    def generate_html(self, markdown_content: str) -> str:
        """Convert markdown to HTML with styling."""
        # Convert markdown to HTML
        html_body = markdown.markdown(
            markdown_content,
            extensions=['extra', 'codehilite', 'tables']
        )
        
        # Create full HTML document with CSS
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{settings.pdf_title}</title>
    <style>
        @page {{
            size: A4;
            margin: 2cm;
        }}
        
        body {{
            font-family: 'Helvetica', 'Arial', sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
        }}
        
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-top: 0;
        }}
        
        h2 {{
            color: #34495e;
            margin-top: 30px;
            border-bottom: 1px solid #bdc3c7;
            padding-bottom: 5px;
        }}
        
        a {{
            color: #3498db;
            text-decoration: none;
        }}
        
        a:hover {{
            text-decoration: underline;
        }}
        
        hr {{
            border: none;
            border-top: 1px solid #ecf0f1;
            margin: 30px 0;
        }}
        
        strong {{
            color: #2c3e50;
        }}
        
        em {{
            color: #7f8c8d;
        }}
        
        code {{
            background-color: #f8f9fa;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }}
        
        pre {{
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }}
        
        blockquote {{
            border-left: 4px solid #3498db;
            padding-left: 20px;
            margin-left: 0;
            color: #555;
            font-style: italic;
        }}
    </style>
</head>
<body>
    {html_body}
</body>
</html>
"""
        return html
    
    def generate_pdf(
        self,
        articles: List[Dict[str, Any]],
        filename: str = None,
        title: str = None
    ) -> Path:
        """Generate PDF from articles."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"tech_news_digest_{timestamp}.pdf"
        
        output_path = self.output_dir / filename
        
        try:
            # Generate markdown
            markdown_content = self.generate_markdown(articles, title)
            
            # Convert to HTML
            html_content = self.generate_html(markdown_content)
            
            # Generate PDF
            HTML(string=html_content).write_pdf(output_path)
            
            logger.info(f"PDF generated successfully: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error generating PDF: {e}")
            raise
    
    def generate_pdf_from_markdown(
        self,
        markdown_content: str,
        filename: str = None
    ) -> Path:
        """Generate PDF directly from markdown content."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"report_{timestamp}.pdf"
        
        output_path = self.output_dir / filename
        
        try:
            html_content = self.generate_html(markdown_content)
            HTML(string=html_content).write_pdf(output_path)
            
            logger.info(f"PDF generated from markdown: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error generating PDF from markdown: {e}")
            raise


def main():
    """Test PDF generation."""
    generator = PDFGenerator()
    
    # Sample articles
    sample_articles = [
        {
            "title": "AI Breakthrough: New Model Achieves Human-Level Performance",
            "source": "TechCrunch",
            "author": "John Doe",
            "published_date": "2024-01-18",
            "url": "https://example.com/article1",
            "content": "A new artificial intelligence model has achieved human-level performance on a wide range of tasks. The model, developed by researchers at a leading tech company, demonstrates unprecedented capabilities in natural language understanding and generation."
        },
        {
            "title": "Quantum Computing Makes Major Leap Forward",
            "source": "The Verge",
            "author": "Jane Smith",
            "published_date": "2024-01-17",
            "url": "https://example.com/article2",
            "content": "Scientists have announced a major breakthrough in quantum computing, successfully running complex algorithms on a 1000-qubit processor. This achievement brings us closer to practical quantum computers that can solve real-world problems."
        }
    ]
    
    output_path = generator.generate_pdf(sample_articles, "test_report.pdf")
    print(f"Test PDF generated at: {output_path}")


if __name__ == "__main__":
    main()
