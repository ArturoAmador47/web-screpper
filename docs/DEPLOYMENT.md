# Deployment Guide

This guide covers deploying the Tech News Aggregator in various environments.

## Table of Contents

1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Cloud Deployment](#cloud-deployment)
4. [n8n Setup](#n8n-setup)
5. [Environment Variables](#environment-variables)
6. [Troubleshooting](#troubleshooting)

## Local Development

### Prerequisites

- Python 3.11+
- OpenAI API key
- Supabase account

### Setup Steps

1. **Clone and install:**
```bash
git clone https://github.com/ArturoAmador47/web-screpper.git
cd web-screpper
pip install -r requirements.txt
```

2. **Configure environment:**
```bash
cp .env.example .env
# Edit .env with your credentials
```

3. **Set up Supabase:**
```bash
python scripts/setup_supabase.py
# Copy the output SQL and run in Supabase SQL Editor
```

4. **Test scraping:**
```bash
python scripts/test_scraping.py
```

5. **Start the API:**
```bash
python -m src.api.main
```

Visit `http://localhost:8000/docs` for API documentation.

## Docker Deployment

### Build and Run

```bash
docker-compose up -d
```

## Cloud Deployment

### AWS EC2

1. **Launch EC2 instance** (Ubuntu 22.04 recommended)

2. **SSH into instance:**
```bash
ssh -i your-key.pem ubuntu@your-instance-ip
```

3. **Install dependencies:**
```bash
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3-pip
sudo apt install -y libcairo2 libpango-1.0-0 libpangocairo-1.0-0
```

4. **Clone and setup:**
```bash
git clone https://github.com/ArturoAmador47/web-screpper.git
cd web-screpper
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

5. **Configure environment:**
```bash
nano .env
# Add your credentials
```

6. **Run the service**

## n8n Setup

### Self-Hosted n8n

1. **Install n8n:**
```bash
npm install n8n -g
```

2. **Start n8n:**
```bash
n8n start
```

3. **Import workflows:**
- Open n8n interface at `http://localhost:5678`
- Go to Workflows → Import
- Upload files from `n8n_workflows/`

4. **Configure workflows:**
- Update API URLs to point to your deployment
- Configure email settings
- Set up credentials

## Environment Variables

### Required Variables

```env
OPENAI_API_KEY=sk-...
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=eyJ...
```

### Optional Variables

```env
NEWS_SOURCES=https://feed1.com,https://feed2.com
EMBEDDING_MODEL=text-embedding-ada-002
SIMILARITY_THRESHOLD=0.85
API_HOST=0.0.0.0
API_PORT=8000
OUTPUT_DIR=./output
PDF_TITLE=Tech News Digest
```

## Troubleshooting

### Common Issues

**WeasyPrint errors:**
```bash
# Install system dependencies
sudo apt-get install python3-dev libcairo2 libpango-1.0-0
```

**OpenAI rate limits:**
- Implement exponential backoff
- Reduce batch sizes
- Upgrade OpenAI tier

**Supabase connection issues:**
- Check firewall rules
- Verify API key permissions
- Monitor connection pool
