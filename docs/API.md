# API Reference

Complete API documentation for the Tech News Aggregator.

## Base URL

```
http://localhost:8000
```

## Endpoints

### Health Check

**GET** `/health`

Check if the API is running.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-18T12:00:00.000Z"
}
```

---

### Scrape News

**POST** `/scrape`

Trigger the news aggregation pipeline.

**Request Body:**
```json
{
  "sources": ["https://techcrunch.com/feed/"],  // Optional
  "deduplicate": true,                          // Optional, default: true
  "store": true,                                // Optional, default: true
  "generate_pdf": true                          // Optional, default: true
}
```

**Response:**
```json
{
  "success": true,
  "articles_scraped": 50,
  "articles_processed": 45,
  "articles_stored": 45,
  "pdf_path": "/app/output/tech_news_digest_20240118_120000.pdf",
  "elapsed_time": 15.5
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/scrape \
  -H "Content-Type: application/json" \
  -d '{
    "deduplicate": true,
    "store": true,
    "generate_pdf": true
  }'
```

---

### Get Articles

**GET** `/articles`

Retrieve stored articles from the database.

**Query Parameters:**
- `limit` (int, default: 100): Maximum number of articles
- `source` (string, optional): Filter by source name

**Response:**
```json
[
  {
    "title": "AI Breakthrough: GPT-5 Released",
    "content": "OpenAI has released...",
    "url": "https://example.com/article",
    "source": "TechCrunch",
    "published_date": "2024-01-18T12:00:00",
    "author": "John Doe"
  }
]
```

**Example:**
```bash
curl "http://localhost:8000/articles?limit=10&source=TechCrunch"
```

---

### List PDFs

**GET** `/pdfs`

List all generated PDF files.

**Response:**
```json
{
  "count": 5,
  "files": [
    {
      "filename": "tech_news_digest_20240118_120000.pdf",
      "size_bytes": 524288,
      "created_at": "2024-01-18T12:00:00",
      "download_url": "/pdf/tech_news_digest_20240118_120000.pdf"
    }
  ]
}
```

**Example:**
```bash
curl http://localhost:8000/pdfs
```

---

### Download PDF

**GET** `/pdf/{filename}`

Download a specific PDF file.

**Parameters:**
- `filename` (path): Name of the PDF file

**Response:** PDF file download

**Example:**
```bash
curl http://localhost:8000/pdf/tech_news_digest_20240118_120000.pdf \
  --output digest.pdf
```

---

### n8n Webhook

**POST** `/webhook/n8n`

Webhook endpoint for n8n workflows.

**Request Body:**
```json
{
  "sources": ["https://techcrunch.com/feed/"],
  "deduplicate": true,
  "store": true,
  "generate_pdf": true
}
```

**Response:** Same as `/scrape` endpoint

**Example:**
```bash
curl -X POST http://localhost:8000/webhook/n8n \
  -H "Content-Type: application/json" \
  -d '{
    "sources": [
      "https://techcrunch.com/feed/",
      "https://www.theverge.com/rss/index.xml"
    ],
    "deduplicate": true
  }'
```

---

### Get Configuration

**GET** `/config`

Get current configuration (excluding sensitive data).

**Response:**
```json
{
  "embedding_model": "text-embedding-ada-002",
  "similarity_threshold": 0.85,
  "news_sources": [
    "https://techcrunch.com/feed/",
    "https://www.theverge.com/rss/index.xml"
  ],
  "output_dir": "./output",
  "pdf_title": "Tech News Digest"
}
```

**Example:**
```bash
curl http://localhost:8000/config
```

---

## Error Responses

All endpoints may return error responses in the following format:

**4xx Client Errors:**
```json
{
  "detail": "Error message describing what went wrong"
}
```

**5xx Server Errors:**
```json
{
  "detail": "Internal server error message"
}
```

Common HTTP status codes:
- `200 OK`: Successful request
- `400 Bad Request`: Invalid request parameters
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server-side error

---

## Interactive Documentation

Visit these URLs when the API is running:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

These provide interactive API documentation where you can test endpoints directly from your browser.

---

## Rate Limiting

Be aware of rate limits from external services:

- **OpenAI API**: Depends on your plan (typically 3,500 requests/min for embeddings)
- **RSS Feeds**: Most feeds allow frequent polling, but be respectful
- **Supabase**: Depends on your plan

---

## Best Practices

1. **Batch Processing**: Use the `/scrape` endpoint with `deduplicate=true` to minimize API calls
2. **Caching**: Store results in Supabase to avoid re-scraping
3. **Scheduling**: Use n8n workflows for scheduled execution
4. **Error Handling**: Implement retry logic with exponential backoff
5. **Monitoring**: Check `/health` endpoint regularly

---

## Authentication

Currently, the API does not require authentication. For production deployments, consider adding:

- API keys
- OAuth 2.0
- JWT tokens
- IP whitelisting

---

## Examples

### Complete Workflow

```bash
# 1. Check health
curl http://localhost:8000/health

# 2. Scrape and process news
curl -X POST http://localhost:8000/scrape \
  -H "Content-Type: application/json" \
  -d '{"deduplicate": true, "generate_pdf": true}'

# 3. List available PDFs
curl http://localhost:8000/pdfs

# 4. Download latest PDF
curl http://localhost:8000/pdf/tech_news_digest_20240118_120000.pdf \
  -o latest_digest.pdf

# 5. Get stored articles
curl "http://localhost:8000/articles?limit=5"
```

### Python Client

```python
import requests

# Scrape news
response = requests.post(
    "http://localhost:8000/scrape",
    json={
        "sources": [
            "https://techcrunch.com/feed/",
            "https://www.theverge.com/rss/index.xml"
        ],
        "deduplicate": True,
        "store": True,
        "generate_pdf": True
    }
)

result = response.json()
print(f"Scraped {result['articles_scraped']} articles")
print(f"PDF: {result['pdf_path']}")

# Get articles
articles = requests.get(
    "http://localhost:8000/articles",
    params={"limit": 10}
).json()

for article in articles:
    print(f"- {article['title']}")
```

### JavaScript/Node.js Client

```javascript
const axios = require('axios');

async function scrapeNews() {
  const response = await axios.post('http://localhost:8000/scrape', {
    deduplicate: true,
    store: true,
    generate_pdf: true
  });
  
  console.log(`Scraped ${response.data.articles_scraped} articles`);
  console.log(`PDF: ${response.data.pdf_path}`);
}

scrapeNews();
```
