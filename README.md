# Tech News Aggregator

An automated tech news aggregator that scrapes multiple sources daily, processes content with AI embeddings for deduplication, and generates PDF digests.

## Features

- 🔄 **Automated Scraping**: RSS feed parsing and web scraping with Crawl4AI
- 🤖 **AI-Powered Deduplication**: Uses OpenAI embeddings to identify and remove duplicate articles
- 🗄️ **Vector Storage**: Stores articles with embeddings in Supabase with pgvector
- 📄 **PDF Generation**: Creates beautifully formatted PDF digests using WeasyPrint
- 🚀 **FastAPI**: High-performance async API for integration
- 🔗 **n8n Integration**: Ready-to-use workflows for automation

## Tech Stack

- **Orchestration**: n8n (self-hosted)
- **Scraping**: Python 3.11+ with Crawl4AI, Feedparser, Requests
- **API**: FastAPI with async support
- **Embeddings**: OpenAI text-embedding-ada-002
- **Vector Store**: Supabase with pgvector extension
- **Output**: Markdown to PDF (WeasyPrint)

## Quick Start

### Prerequisites

- Python 3.11 or higher
- OpenAI API key
- Supabase account (optional, for storage)
- n8n instance (optional, for automation)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/ArturoAmador47/web-screpper.git
cd web-screpper
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables:**
```bash
cp .env.example .env
# Edit .env with your configuration
```

Required environment variables:
```env
OPENAI_API_KEY=your_openai_api_key_here
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_key_here
NEWS_SOURCES=https://techcrunch.com/feed/,https://www.theverge.com/rss/index.xml
```

4. **Set up Supabase (optional):**

Run the SQL from `src/storage/supabase_storage.py` in your Supabase SQL editor:
```bash
python -m src.storage.supabase_storage
```

This will print the SQL needed to create the articles table and vector search function.

### Usage

#### Run the API Server

```bash
python -m src.api.main
```

The API will be available at `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

#### Run the Aggregator Directly

```bash
python -m src.aggregator
```

#### API Endpoints

- `POST /scrape` - Trigger news scraping and processing
- `GET /articles` - Retrieve stored articles
- `GET /pdfs` - List generated PDFs
- `GET /pdf/{filename}` - Download a specific PDF
- `POST /webhook/n8n` - n8n webhook endpoint

Example API call:
```bash
curl -X POST http://localhost:8000/scrape \
  -H "Content-Type: application/json" \
  -d '{
    "deduplicate": true,
    "store": true,
    "generate_pdf": true
  }'
```

#### n8n Integration

Import the workflows from `n8n_workflows/`:

1. **Daily Aggregator**: Automated daily news digest with email delivery
2. **Webhook Trigger**: On-demand scraping via webhook

See [n8n_workflows/README.md](n8n_workflows/README.md) for detailed setup instructions.

## Architecture

```
┌─────────────┐
│   n8n       │  Orchestration & Scheduling
│  Workflows  │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────────────┐
│              FastAPI Server                      │
│  ┌─────────────────────────────────────────┐   │
│  │         News Aggregator                  │   │
│  │  ┌───────────┐  ┌──────────────┐        │   │
│  │  │  Scraper  │  │  Embeddings  │        │   │
│  │  │ (Crawl4AI)│  │   (OpenAI)   │        │   │
│  │  └─────┬─────┘  └──────┬───────┘        │   │
│  │        │                │                │   │
│  │        └────────┬───────┘                │   │
│  │                 ▼                        │   │
│  │        ┌─────────────────┐              │   │
│  │        │  Deduplication  │              │   │
│  │        └────────┬────────┘              │   │
│  │                 │                        │   │
│  │        ┌────────┴────────┐              │   │
│  │        ▼                 ▼              │   │
│  │  ┌──────────┐    ┌──────────────┐      │   │
│  │  │ Supabase │    │     PDF      │      │   │
│  │  │ (pgvector)│    │  Generator   │      │   │
│  │  └──────────┘    └──────────────┘      │   │
│  └─────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```

## Project Structure

```
web-screpper/
├── src/
│   ├── api/
│   │   └── main.py              # FastAPI application
│   ├── scraper/
│   │   └── news_scraper.py      # RSS and web scraping
│   ├── embeddings/
│   │   └── embeddings_service.py # OpenAI embeddings
│   ├── storage/
│   │   └── supabase_storage.py  # Database operations
│   ├── pdf_generator/
│   │   └── pdf_service.py       # PDF generation
│   ├── aggregator.py            # Main orchestration
│   └── config.py                # Configuration management
├── n8n_workflows/
│   ├── daily_news_aggregator.json
│   ├── webhook_trigger.json
│   └── README.md
├── tests/                       # Test files
├── output/                      # Generated PDFs
├── requirements.txt
├── pyproject.toml
├── .env.example
└── README.md
```

## Configuration

All configuration is managed through environment variables in `.env`:

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | Required |
| `SUPABASE_URL` | Supabase project URL | Required |
| `SUPABASE_KEY` | Supabase API key | Required |
| `NEWS_SOURCES` | Comma-separated RSS feed URLs | "" |
| `EMBEDDING_MODEL` | OpenAI embedding model | text-embedding-ada-002 |
| `SIMILARITY_THRESHOLD` | Duplicate detection threshold | 0.85 |
| `API_HOST` | API server host | 0.0.0.0 |
| `API_PORT` | API server port | 8000 |
| `OUTPUT_DIR` | PDF output directory | ./output |

## How It Works

1. **Scraping**: The scraper fetches articles from configured RSS feeds using Feedparser. For full article content, it can use Crawl4AI for intelligent web scraping.

2. **Embedding Generation**: Each article's title and content are combined and sent to OpenAI's embedding API to generate a 1536-dimensional vector representation.

3. **Deduplication**: Articles are compared using cosine similarity of their embeddings. Articles above the similarity threshold are considered duplicates, and only one is kept.

4. **Storage**: Unique articles and their embeddings are stored in Supabase with pgvector, enabling fast similarity searches.

5. **PDF Generation**: Articles are formatted into a styled PDF document using WeasyPrint, with markdown rendering for rich formatting.

6. **Automation**: n8n workflows can trigger the pipeline on a schedule or via webhooks, with results delivered via email or other channels.

## Development

### Running Tests

```bash
pytest tests/
```

### Code Style

The project follows PEP 8 style guidelines. Format code with:
```bash
black src/
```

## API Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Troubleshooting

### Common Issues

1. **ImportError for Crawl4AI**: Crawl4AI is optional. If not installed, the scraper falls back to using requests for web scraping.

2. **Supabase connection errors**: Ensure your Supabase URL and key are correct and the database schema is set up.

3. **OpenAI rate limits**: The embeddings service processes articles in batches to avoid rate limits. Adjust batch size if needed.

4. **WeasyPrint dependencies**: WeasyPrint requires system libraries. On Linux:
   ```bash
   sudo apt-get install python3-dev python3-pip python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0
   ```

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Roadmap

- [ ] Support for more news sources and formats
- [ ] Advanced deduplication using semantic analysis
- [ ] Multi-language support
- [ ] Custom PDF templates
- [ ] Article categorization and tagging
- [ ] Real-time streaming API
- [ ] Web dashboard for monitoring
- [ ] Docker containerization

## Support

For issues and questions:
- GitHub Issues: [Create an issue](https://github.com/ArturoAmador47/web-screpper/issues)
- Documentation: See inline code documentation

---

Built with ❤️ using Python, FastAPI, and modern AI tools.
