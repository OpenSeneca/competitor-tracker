# Competitor Tracker v1.0.0

Tracks AI company product launches, features, and announcements for competitive intelligence.

## Features

- **Multi-source tracking**: Reads from multiple news/blog sources
- **Structured storage**: Stores announcements in JSON format with metadata
- **Digest generation**: Produces weekly summaries for blog posts
- **Deduplication**: Avoids duplicate entries across sources
- **Company filtering**: Focus on specific AI companies of interest

## Installation

```bash
pip install -e .
```

## Usage

### Scan for new announcements

```bash
competitor-tracker scan
```

Scan specific sources:
```bash
competitor-tracker scan --source techcrunch --source venturebeat
```

### Generate weekly digest

```bash
competitor-tracker digest
```

For a specific date range:
```bash
competitor-tracker digest --from 2026-05-09 --to 2026-05-16
```

### List all tracked announcements

```bash
competitor-tracker list
```

Filter by company:
```bash
competitor-tracker list --company OpenAI --company Anthropic
```

### Add manual announcement

```bash
competitor-tracker add \
  --company "OpenAI" \
  --title "GPT-5 Released" \
  --url "https://openai.com/gpt5" \
  --date 2026-05-15
```

## Data Storage

Announcements are stored in:
- `~/.openclaw/workspace/competitor-tracker/data/announcements.json`
- `~/.openclaw/workspace/outputs/competitor-digest-YYYY-MM-DD.md`

## Supported Sources

- TechCrunch (AI section)
- VentureBeat (AI section)
- The Verge (AI section)
- Hacker News (AI-related)
- Custom RSS feeds (configurable)

## Configuration

Edit `config.yaml` to add sources or companies:

```yaml
companies:
  - OpenAI
  - Anthropic
  - Google DeepMind
  - Meta AI
  - Microsoft AI

sources:
  - name: techcrunch
    url: https://techcrunch.com/category/artificial-intelligence/feed/
    type: rss

  - name: custom
    url: https://example.com/feed
    type: rss
```

## Weekly Digest Format

Digests include:
- Summary of all announcements by company
- Trending topics
- Product launches vs. features
- Links to original articles

## Automation

Add to crontab for weekly scanning:

```cron
# Scan for new announcements every Monday at 9 AM UTC
0 9 * * 1 /home/exedev/.openclaw/workspace/tools/competitor-tracker/competitor-tracker.sh scan

# Generate digest every Monday at 10 AM UTC
0 10 * * 1 /home/exedev/.openclaw/workspace/tools/competitor-tracker/competitor-tracker.sh digest
```

## License

MIT
