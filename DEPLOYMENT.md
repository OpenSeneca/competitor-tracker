# Deployment Guide - Competitor Tracker CLI

## Installation

### Install from GitHub (Recommended)

```bash
# Install the latest version
pipx install git+https://github.com/OpenSeneca/competitor-tracker.git

# Or install with pip
pip install git+https://github.com/OpenSeneca/competitor-tracker.git
```

### Install from PyPI (when published)

```bash
# Install with pipx
pipx install squad-competitor-tracker

# Or install with pip
pip install squad-competitor-tracker
```

### Verify Installation

```bash
# Check version
competitor-tracker --version

# Show help
competitor-tracker --help
```

## First-Time Setup

### Create Data Directory

The tool stores data in `~/.openclaw/workspace/data/competitor-tracker.json`. This directory is created automatically.

### Add Your First Entry

```bash
competitor-tracker add \
  --company "OpenAI" \
  --item "GPT-5" \
  --date "2026-05-04" \
  --url "https://openai.com/gpt5" \
  --notes "Major upgrade, 10x faster" \
  --category product
```

## Configuration

No configuration file is required. All settings are command-line arguments.

## Automation

### Cron Job for Daily Summaries

```bash
# Add to crontab (crontab -e)
# Run daily at 9 AM to get weekly competitive update
0 9 * * * /usr/local/bin/competitor-tracker list --days 7 > /tmp/weekly-competitor-update.md
```

### Integration with Other Tools

```bash
# Export to markdown for content pipeline
competitor-tracker export --format markdown > /tmp/competitors.md

# Export to CSV for analysis
competitor-tracker export --format csv > /tmp/competitors.csv
```

## Data Management

### Backup Data

```bash
# Backup to archive
cp ~/.openclaw/workspace/data/competitor-tracker.json ~/backup/competitor-tracker-$(date +%Y%m%d).json
```

### Export All Data

```bash
# Full JSON export
competitor-tracker export --format json --output full-export.json
```

## Troubleshooting

### Command Not Found

If `competitor-tracker` is not in your PATH:

```bash
# Check installation
pipx list | grep competitor-tracker

# Reinstall with pipx
pipx install --force git+https://github.com/OpenSeneca/competitor-tracker.git
```

### Data File Issues

If the data file is corrupted:

```bash
# Remove and recreate
rm ~/.openclaw/workspace/data/competitor-tracker.json
competitor-tracker stats  # Will create new file
```

## Development

### Local Development

```bash
# Clone repo
git clone https://github.com/OpenSeneca/competitor-tracker.git
cd competitor-tracker

# Install in development mode
pip install -e .

# Run tests
python -m pytest

# Build package
python setup.py sdist bdist_wheel
```

### Creating a New Release

```bash
# Update version in setup.py
git commit -am "Bump version to X.Y.Z"
git tag vX.Y.Z
git push --tags
```

This triggers the GitHub Actions workflow to publish to PyPI.

## Requirements

- Python 3.6 or higher
- No external dependencies (uses Python standard library only)

## License

MIT License - see LICENSE file for details.

## Support

For issues or feature requests, please open an issue on GitHub:
https://github.com/OpenSeneca/competitor-tracker/issues
