# Competitor Tracker

Tracks AI company shipping activity (product launches, features, announcements) for reference in blog posts.

## What It Does

- Accepts new shipping entries via CLI
- Stores entries in structured JSON format
- Generates weekly/monthly summary reports
- Filters by company, date range, category
- Outputs clean markdown for easy reference

## Companies Tracked

- Anthropic (Claude, safety research)
- OpenAI (ChatGPT, GPT models, API)
- Google DeepMind (Gemini, AlphaFold, research)
- Meta (Llama models, research, products)
- Microsoft (Copilot, Azure AI, research)
- Stability AI (image/video generation)
- Midjourney (image generation)
- Perplexity (search/AI assistant)
- Mistral (language models, API)
- Custom companies as needed

## Installation

```bash
cd ~/.openclaw/workspace/tools/competitor-tracker
pip install -e .
```

## Usage

### Add a new shipping entry

```bash
# Basic entry
competitor-track add "OpenAI" "Launched ChatGPT 4o" "New model with voice and vision"

# With category
competitor-track add "Anthropic" "Claude 3.5 Sonnet" "New flagship model" --category model

# With links
competitor-track add "Google" "Gemini 1.5 Pro" "2M context window" --link https://blog.google/technology/ai/

# With impact rating (1-5)
competitor-track add "Meta" "Llama 3.1" "405B parameter model" --impact 5
```

### Generate reports

```bash
# List all entries
competitor-track list

# Filter by company
competitor-track list --company OpenAI

# Filter by date range (last 7 days)
competitor-track list --days 7

# Filter by category
competitor-track list --category model

# Generate markdown report
competitor-track report --output ~/reports/ai-shipping-weekly.md
```

### Manage data

```bash
# Show data location
competitor-track info

# Export to JSON
competitor-track export --format json --output ai-shipping.json

# Import from JSON
competitor-track import --format json --input ai-shipping.json
```

## Data Structure

Entries are stored in `~/.openclaw/workspace/data/competitor-tracker/entries.json`:

```json
{
  "entries": [
    {
      "id": "uuid",
      "timestamp": "2026-05-06T19:00:00Z",
      "company": "OpenAI",
      "name": "ChatGPT 4o",
      "description": "New model with voice and vision",
      "category": "model",
      "links": ["https://openai.com/blog/chatgpt-4o"],
      "impact": 5,
      "notes": "Available in free tier"
    }
  ]
}
```

## Categories

- `model` - New language model or foundation model
- `feature` - New feature or capability
- `api` - API change, pricing, or availability
- `product` - New product or service
- `research` - Research paper or breakthrough
- `safety` - Safety, alignment, or security announcement
- `other` - Everything else

## Impact Rating

1 - Minor update, niche interest
2 - Notable change, some users affected
3 - Significant feature, broad interest
4 - Major launch, industry attention
5 - Breakthrough, redefines category

## Reports

The `report` command generates a markdown summary:

```markdown
# AI Shipping Report - Week of May 6, 2026

## High Impact (5)
- **OpenAI**: ChatGPT 4o - New model with voice and vision
- **Meta**: Llama 3.1 - 405B parameter model

## Models
- Anthropic: Claude 3.5 Sonnet
- Google: Gemini 1.5 Pro
- Mistral: Mistral Large 2

## Features
- OpenAI: Advanced voice mode
- Anthropic: Artifacts feature

## Summary
This week: 8 launches across 5 companies
Top impact: OpenAI (3), Meta (2), Anthropic (2), Google (1)
```

## Integration

This tool is useful for:
- Justin: Reference when writing blog posts about AI developments
- Marcus: Track research breakthroughs for AI/ML research
- Seneca: Generate weekly shipping digests for team updates

## License

MIT
