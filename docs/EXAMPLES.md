# Usage Examples

Practical examples of using the Tech News Aggregator.

## Quick Start Example

### 1. Basic Scraping (No API Keys Required)

Test the scraper with public RSS feeds:

```bash
python scripts/test_scraping.py
```

### 2. Full Pipeline (Requires API Keys)

Set up your environment first:

```bash
# Create .env file
cat > .env << EOF
OPENAI_API_KEY=sk-your-key-here
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-key-here
NEWS_SOURCES=https://techcrunch.com/feed/,https://www.theverge.com/rss/index.xml
EOF

# Run the aggregator
python -m src.aggregator
```

## Component Examples

### Scraping Only

```python
import asyncio
from src.scraper.news_scraper import NewsScraper

async def scrape_news():
    scraper = NewsScraper()
    
    # Scrape a single feed
    articles = await scraper.scrape_rss_feed("https://techcrunch.com/feed/")
    
    for article in articles:
        print(f"Title: {article.title}")
        print(f"URL: {article.url}")
        print(f"Source: {article.source}")
        print("-" * 50)

asyncio.run(scrape_news())
```

### Generate Embeddings

```python
import asyncio
from src.embeddings.embeddings_service import EmbeddingsService

async def generate_embeddings():
    service = EmbeddingsService()
    
    texts = [
        "OpenAI releases GPT-5",
        "Google announces new AI model",
    ]
    
    embeddings = await service.generate_embeddings_batch(texts)
    
    # Check similarity
    similarity = service.cosine_similarity(embeddings[0], embeddings[1])
    print(f"Similarity: {similarity:.4f}")

asyncio.run(generate_embeddings())
```

### Deduplication

```python
from src.embeddings.embeddings_service import EmbeddingsService

service = EmbeddingsService()

# Sample embeddings (in real use, these come from OpenAI)
embeddings = [
    [1.0, 0.0, 0.0],
    [0.99, 0.01, 0.0],  # Very similar to first
    [0.0, 1.0, 0.0],    # Different
]

duplicates = service.find_duplicates(embeddings, threshold=0.9)
print(f"Found {len(duplicates)} duplicate groups")
```

### PDF Generation

```python
from src.pdf_generator.pdf_service import PDFGenerator

generator = PDFGenerator()

articles = [
    {
        "title": "Tech News Article",
        "source": "TechCrunch",
        "author": "John Doe",
        "published_date": "2024-01-18",
        "url": "https://example.com",
        "content": "Article content here..."
    }
]

# Generate PDF
pdf_path = generator.generate_pdf(articles, "my_digest.pdf")
print(f"PDF saved to: {pdf_path}")
```

## API Examples

### Using curl

```bash
# Scrape news with custom sources
curl -X POST http://localhost:8000/scrape \
  -H "Content-Type: application/json" \
  -d '{
    "sources": [
      "https://techcrunch.com/feed/",
      "https://www.theverge.com/rss/index.xml",
      "https://feeds.arstechnica.com/arstechnica/index"
    ],
    "deduplicate": true,
    "store": true,
    "generate_pdf": true
  }'

# Get recent articles
curl "http://localhost:8000/articles?limit=5"

# List PDFs
curl http://localhost:8000/pdfs
```

### Using Python Requests

```python
import requests
import json

# Start scraping
response = requests.post(
    "http://localhost:8000/scrape",
    json={
        "deduplicate": True,
        "store": True,
        "generate_pdf": True
    }
)

if response.status_code == 200:
    result = response.json()
    print(f"Success! Processed {result['articles_processed']} articles")
    print(f"Time taken: {result['elapsed_time']:.2f}s")
    
    # Download the PDF
    if result['pdf_path']:
        pdf_filename = result['pdf_path'].split('/')[-1]
        pdf_response = requests.get(
            f"http://localhost:8000/pdf/{pdf_filename}"
        )
        
        with open("news_digest.pdf", "wb") as f:
            f.write(pdf_response.content)
        print("PDF downloaded!")
```

### Using JavaScript/Fetch

```javascript
async function scrapeNews() {
  const response = await fetch('http://localhost:8000/scrape', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      deduplicate: true,
      store: true,
      generate_pdf: true
    })
  });
  
  const result = await response.json();
  console.log(`Processed ${result.articles_processed} articles`);
  
  // Download PDF
  if (result.pdf_path) {
    const pdfFilename = result.pdf_path.split('/').pop();
    const pdfUrl = `http://localhost:8000/pdf/${pdfFilename}`;
    window.open(pdfUrl, '_blank');
  }
}

scrapeNews();
```

## n8n Workflow Examples

### Daily Digest via Email

1. Import `n8n_workflows/daily_news_aggregator.json`
2. Update email settings
3. Activate the workflow

The workflow will:
- Run daily at your scheduled time
- Scrape configured news sources
- Generate PDF digest
- Email you the results

### Webhook-Triggered Scraping

1. Import `n8n_workflows/webhook_trigger.json`
2. Get your webhook URL from n8n
3. Trigger it programmatically:

```bash
curl -X POST https://your-n8n.com/webhook/tech-news-webhook \
  -H "Content-Type: application/json" \
  -d '{
    "sources": ["https://techcrunch.com/feed/"],
    "deduplicate": true
  }'
```

## Advanced Use Cases

### Custom News Source

```python
import asyncio
from src.scraper.news_scraper import NewsScraper, Article
from datetime import datetime

async def scrape_custom_source():
    scraper = NewsScraper()
    
    # Scrape your custom RSS feed
    articles = await scraper.scrape_rss_feed(
        "https://your-blog.com/feed.xml"
    )
    
    # Filter articles
    recent_articles = [
        a for a in articles 
        if a.published_date.date() == datetime.now().date()
    ]
    
    print(f"Found {len(recent_articles)} articles from today")
    return recent_articles

asyncio.run(scrape_custom_source())
```

### Batch Processing Multiple Feeds

```python
import asyncio
from src.aggregator import NewsAggregator

async def process_multiple_sources():
    aggregator = NewsAggregator()
    
    tech_sources = [
        "https://techcrunch.com/feed/",
        "https://www.theverge.com/rss/index.xml",
        "https://feeds.arstechnica.com/arstechnica/index",
    ]
    
    result = await aggregator.run_full_pipeline(
        sources=tech_sources,
        deduplicate=True,
        store=True,
        generate_pdf=True
    )
    
    print(f"Articles scraped: {result['articles_scraped']}")
    print(f"After deduplication: {result['articles_processed']}")
    print(f"PDF: {result['pdf_path']}")

asyncio.run(process_multiple_sources())
```

### Custom PDF Title and Styling

```python
from src.pdf_generator.pdf_service import PDFGenerator

generator = PDFGenerator(output_dir="./custom_output")

# Generate with custom title
pdf_path = generator.generate_pdf(
    articles=articles,
    filename="weekly_digest.pdf",
    title="Weekly Tech News - January 2024"
)
```

### Similarity Threshold Tuning

```python
from src.config import settings

# Adjust similarity threshold for deduplication
# Higher = more strict (0.0 to 1.0)
settings.similarity_threshold = 0.90

# Now run the aggregator
# It will use the new threshold
```

## Docker Example

```bash
# Build image
docker build -t tech-news-aggregator .

# Run container
docker run -d \
  -p 8000:8000 \
  -e OPENAI_API_KEY=your_key \
  -e SUPABASE_URL=your_url \
  -e SUPABASE_KEY=your_key \
  -e NEWS_SOURCES="https://techcrunch.com/feed/" \
  -v $(pwd)/output:/app/output \
  tech-news-aggregator

# Test the API
curl http://localhost:8000/health
```

## Scheduled Execution (Cron)

```bash
# Add to crontab for daily execution at 8 AM
0 8 * * * cd /path/to/web-screpper && /usr/bin/python3 -m src.aggregator
```

## Monitoring and Logging

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('news_aggregator.log'),
        logging.StreamHandler()
    ]
)

# Now run the aggregator - all logs will be captured
```

## Error Handling

```python
import asyncio
from src.aggregator import NewsAggregator

async def robust_scraping():
    aggregator = NewsAggregator()
    
    try:
        result = await aggregator.run_full_pipeline()
        
        if result['success']:
            print(f"Success! Processed {result['articles_processed']} articles")
        else:
            print(f"Failed: {result.get('message', 'Unknown error')}")
            
    except Exception as e:
        print(f"Error during scraping: {e}")
        # Implement retry logic, notifications, etc.

asyncio.run(robust_scraping())
```

## Testing Without OpenAI

For development/testing without API keys:

```python
# Mock embeddings service for testing
from unittest.mock import Mock, AsyncMock

mock_service = Mock()
mock_service.generate_embeddings_batch = AsyncMock(
    return_value=[[1.0, 0.0, 0.0]] * 10
)

# Use in your tests
```

## Performance Optimization

```python
# Process large batches efficiently
async def process_large_batch():
    aggregator = NewsAggregator()
    
    # Scrape more sources
    sources = [...]  # 50+ sources
    
    # Process in chunks to avoid memory issues
    chunk_size = 10
    for i in range(0, len(sources), chunk_size):
        chunk = sources[i:i + chunk_size]
        await aggregator.run_full_pipeline(
            sources=chunk,
            deduplicate=True
        )
```
