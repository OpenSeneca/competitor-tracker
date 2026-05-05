# Competitor Tracker CLI

Tracks what AI companies ship (products, features, papers, etc.). Useful for blog posts and competitive analysis.

## Why This Tool Exists

When writing blog posts or doing competitive analysis, Justin needs to quickly reference what AI companies have shipped. This tool provides a structured database of competitive intelligence that's easy to query and export.

## Features

- **Add entries**: Track products, features, papers, and other releases
- **List recent entries**: See what happened in the last N days
- **Search**: Find entries by company, product, or keywords
- **Export**: Export data to JSON, CSV, or Markdown
- **Statistics**: See which companies are most active

## Quick Start

```bash
cd ~/.openclaw/workspace/tools/competitor-tracker
python3 main.py --help
```

## Usage Examples

### Add a new entry

```bash
# Product launch
python3 main.py add \
  --company "OpenAI" \
  --item "GPT-5" \
  --date "2026-05-04" \
  --url "https://openai.com/gpt5" \
  --notes "Major upgrade, 10x faster" \
  --category product

# Research paper
python3 main.py add \
  --company "Anthropic" \
  --item "Constitutional AI v3" \
  --date "2026-05-03" \
  --url "https://arxiv.org/abs/..." \
  --category paper

# Feature release
python3 main.py add \
  --company "Google" \
  --item "Gemini Code Assist for Python" \
  --category feature
```

### List recent entries

```bash
# Last 7 days (default)
python3 main.py list

# Last 30 days
python3 main.py list --days 30

# Filter by company
python3 main.py list --company "OpenAI"

# Filter by category
python3 main.py list --category paper
```

### Search entries

```bash
# Search by keyword
python3 main.py search --query "GPT"

# Search by company
python3 main.py search --query "Anthropic"
```

### Export data

```bash
# Export to JSON (default)
python3 main.py export --format json --output competitors.json

# Export to CSV for spreadsheets
python3 main.py export --format csv --output competitors.csv

# Export to Markdown for blog posts
python3 main.py export --format markdown --output competitors.md
```

### Show statistics

```bash
python3 main.py stats
```

Output:
```
📈 Competitor Tracker Statistics
================================================================================
Total entries: 42
Date range: 2026-04-01 to 2026-05-04
Companies tracked: 8

By company:
  • OpenAI: 15 entries
  • Anthropic: 10 entries
  • Google: 8 entries
  • Meta: 5 entries
  • ...

By category:
  • product: 20 entries
  • feature: 12 entries
  • paper: 8 entries
  • other: 2 entries
```

## Data Storage

Entries are stored in `~/.openclaw/workspace/data/competitor-tracker.json` as JSON.

```json
[
  {
    "id": 1,
    "company": "OpenAI",
    "item": "GPT-5",
    "date": "2026-05-04",
    "url": "https://openai.com/gpt5",
    "notes": "Major upgrade, 10x faster",
    "category": "product",
    "added_at": "2026-05-04T05:45:00.000000"
  }
]
```

## Categories

- **product**: Full product launches (GPT-5, Claude 4, etc.)
- **feature**: New features or updates (API additions, integrations, etc.)
- **paper**: Research papers (arXiv, blog posts, technical reports)
- **other**: Announcements, acquisitions, partnerships

## Use Cases

### Blog Post Research

When writing about a topic, export relevant entries:

```bash
# Export all OpenAI products to markdown
python3 main.py list --company "OpenAI" --category product > openai-products.md
```

### Competitive Intelligence

Get weekly summary of what competitors shipped:

```bash
# Show last 7 days of activity
python3 main.py list --days 7 > weekly-competitor-update.md
```

### Historical Analysis

Track company activity over time:

```bash
# Export to CSV for charts
python3 main.py export --format csv --output competitor-activity.csv
```

## Integration with Squad Tools

This tool complements other squad tools:
- **Content Pipeline**: Use tracker data in blog angles
- **Blog Assistant**: Reference competitor releases in outlines
- **Squad Activity Digest**: Include competitive intel in daily summary

## Automation

Add entries automatically from cron:

```bash
# Daily cron to add items from RSS feeds (future feature)
0 9 * * * cd ~/.openclaw/workspace/tools/competitor-tracker && python3 auto-ingest.py
```

## Requirements

- Python 3.6+
- No external dependencies

## Future Enhancements

- Auto-import from RSS feeds / blogs
- Web UI for easier browsing
- Integration with news APIs for automatic detection
- Trend analysis and activity graphs

## License

MIT

---

**Built by Archimedes** for the OpenSeneca squad.
