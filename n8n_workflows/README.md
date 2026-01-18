# n8n Workflow Templates

This directory contains n8n workflow templates for automating the tech news aggregator.

## Available Workflows

### 1. Daily News Aggregator (`daily_news_aggregator.json`)

A scheduled workflow that runs daily to:
1. Scrape tech news from configured sources
2. Process and deduplicate articles using AI embeddings
3. Store articles in Supabase
4. Generate PDF digest
5. Send the digest via email

**Configuration:**
- Schedule: Every 24 hours (configurable)
- API endpoint: `http://localhost:8000/scrape`
- Email settings: Update sender and recipient emails

**Import Instructions:**
1. Open n8n interface
2. Go to Workflows → Import
3. Upload `daily_news_aggregator.json`
4. Update email configuration in "Send Email" node
5. Activate the workflow

### 2. Webhook Trigger (`webhook_trigger.json`)

A webhook-based workflow for on-demand news aggregation:
1. Receives webhook POST request
2. Forwards request to API
3. Returns results

**Usage:**
```bash
curl -X POST http://your-n8n-instance/webhook/tech-news-webhook \
  -H "Content-Type: application/json" \
  -d '{
    "sources": [
      "https://techcrunch.com/feed/",
      "https://www.theverge.com/rss/index.xml"
    ],
    "deduplicate": true,
    "store": true,
    "generate_pdf": true
  }'
```

## Setup Requirements

1. **n8n Instance**: Self-hosted or cloud instance
2. **API Server**: FastAPI server running at `http://localhost:8000`
3. **Email Configuration**: SMTP settings configured in n8n
4. **Network Access**: n8n must be able to reach the API server

## Customization

### Changing Schedule
Edit the "Schedule Daily" node in `daily_news_aggregator.json`:
```json
{
  "parameters": {
    "rule": {
      "interval": [
        {
          "field": "hours",
          "hoursInterval": 24  // Change this value
        }
      ]
    }
  }
}
```

### Adding Custom Processing
You can extend workflows by adding nodes for:
- Slack notifications
- Discord webhooks
- Database storage
- Custom analytics
- File uploads to cloud storage

## Troubleshooting

### Workflow Fails with Timeout
Increase timeout in HTTP Request nodes:
```json
{
  "options": {
    "timeout": 600000  // 10 minutes in milliseconds
  }
}
```

### Email Not Sending
1. Check SMTP configuration in n8n settings
2. Verify email credentials
3. Check spam folder

### API Connection Issues
1. Verify API server is running
2. Check network connectivity
3. Update API URL if different from localhost
