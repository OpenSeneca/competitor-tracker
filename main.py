#!/usr/bin/env python3
"""
Competitor Tracker CLI
Tracks what AI companies ship (products, features, papers, etc.)
Useful for blog posts and competitive analysis.

Usage:
    python3 main.py add --company "OpenAI" --item "GPT-5" --date "2026-05-04" --url "https://openai.com/gpt5"
    python3 main.py list [--days 7]
    python3 main.py search --query "GPT"
    python3 main.py export --format json
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Data directory
DATA_DIR = Path.home() / ".openclaw" / "workspace" / "data"
DATA_FILE = DATA_DIR / "competitor-tracker.json"

# Ensure data directory exists
DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_entries():
    """Load all entries from data file."""
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)


def save_entries(entries):
    """Save entries to data file."""
    with open(DATA_FILE, 'w') as f:
        json.dump(entries, f, indent=2)


def add_entry(company, item, date=None, url="", notes="", category="product"):
    """Add a new competitor entry."""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    entries = load_entries()
    entry = {
        "id": len(entries) + 1,
        "company": company,
        "item": item,
        "date": date,
        "url": url,
        "notes": notes,
        "category": category,
        "added_at": datetime.now().isoformat()
    }
    entries.append(entry)

    # Sort by date (newest first)
    entries.sort(key=lambda x: x["date"], reverse=True)

    save_entries(entries)
    print(f"✅ Added: {company} - {item} ({date})")
    return entry


def list_entries(days=7, company=None, category=None):
    """List recent entries."""
    entries = load_entries()

    # Filter by date
    if days:
        cutoff = datetime.now() - timedelta(days=days)
        entries = [e for e in entries if datetime.fromisoformat(e["added_at"]) >= cutoff]

    # Filter by company
    if company:
        entries = [e for e in entries if e["company"].lower() == company.lower()]

    # Filter by category
    if category:
        entries = [e for e in entries if e["category"].lower() == category.lower()]

    if not entries:
        print("No entries found.")
        return

    # Display
    print(f"📊 Competitor Tracker ({days} days)")
    print("=" * 80)

    for entry in entries:
        cat_icon = {"product": "🚀", "feature": "✨", "paper": "📄", "other": "📌"}.get(entry["category"], "📌")
        print(f"{cat_icon} {entry['company']} - {entry['item']}")
        print(f"   📅 {entry['date']} | 🏷️  {entry['category']}")
        if entry['url']:
            print(f"   🔗 {entry['url']}")
        if entry['notes']:
            print(f"   📝 {entry['notes']}")
        print()

    print(f"Total: {len(entries)} entries")


def search_entries(query):
    """Search entries by query."""
    entries = load_entries()
    query = query.lower()

    results = [
        e for e in entries
        if query in e["company"].lower()
        or query in e["item"].lower()
        or query in e["notes"].lower()
    ]

    if not results:
        print(f"No results for '{query}'")
        return

    print(f"🔍 Search results for '{query}'")
    print("=" * 80)

    for entry in results:
        print(f"• {entry['company']} - {entry['item']} ({entry['date']})")
        if entry['url']:
            print(f"  {entry['url']}")
        if entry['notes']:
            print(f"  {entry['notes']}")
        print()

    print(f"Total: {len(results)} results")


def export_entries(format="json", output_file=None):
    """Export entries to specified format."""
    entries = load_entries()

    if format == "json":
        output = json.dumps(entries, indent=2)
    elif format == "csv":
        import csv
        import io

        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=["company", "item", "date", "url", "notes", "category"])
        writer.writeheader()
        for entry in entries:
            writer.writerow({k: v for k, v in entry.items() if k not in ["id", "added_at"]})
        output = output.getvalue()
    elif format == "markdown":
        output = "# Competitor Tracker\n\n"
        for entry in entries:
            output += f"- **{entry['company']}** - {entry['item']} ({entry['date']})\n"
            if entry['url']:
                output += f"  - {entry['url']}\n"
            if entry['notes']:
                output += f"  - {entry['notes']}\n"
    else:
        print(f"Unknown format: {format}")
        return

    if output_file:
        with open(output_file, 'w') as f:
            f.write(output)
        print(f"✅ Exported {len(entries)} entries to {output_file}")
    else:
        print(output)


def stats():
    """Show statistics about tracked competitors."""
    entries = load_entries()

    if not entries:
        print("No entries tracked yet.")
        return

    # Count by company
    companies = {}
    for entry in entries:
        companies[entry["company"]] = companies.get(entry["company"], 0) + 1

    # Count by category
    categories = {}
    for entry in entries:
        categories[entry["category"]] = categories.get(entry["category"], 0) + 1

    # Date range
    dates = [e["date"] for e in entries]
    min_date = min(dates)
    max_date = max(dates)

    print("📈 Competitor Tracker Statistics")
    print("=" * 80)
    print(f"Total entries: {len(entries)}")
    print(f"Date range: {min_date} to {max_date}")
    print(f"Companies tracked: {len(companies)}")
    print()
    print("By company:")
    for company, count in sorted(companies.items(), key=lambda x: x[1], reverse=True):
        print(f"  • {company}: {count} entries")
    print()
    print("By category:")
    for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        print(f"  • {category}: {count} entries")


def main():
    parser = argparse.ArgumentParser(description="Competitor Tracker CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new entry")
    add_parser.add_argument("--company", required=True, help="Company name")
    add_parser.add_argument("--item", required=True, help="What was shipped")
    add_parser.add_argument("--date", help="Date (YYYY-MM-DD, defaults to today)")
    add_parser.add_argument("--url", default="", help="Reference URL")
    add_parser.add_argument("--notes", default="", help="Additional notes")
    add_parser.add_argument("--category", default="product",
                           choices=["product", "feature", "paper", "other"],
                           help="Category of the entry")

    # List command
    list_parser = subparsers.add_parser("list", help="List recent entries")
    list_parser.add_argument("--days", type=int, default=7, help="Number of days to show")
    list_parser.add_argument("--company", help="Filter by company")
    list_parser.add_argument("--category", help="Filter by category")

    # Search command
    search_parser = subparsers.add_parser("search", help="Search entries")
    search_parser.add_argument("--query", required=True, help="Search query")

    # Export command
    export_parser = subparsers.add_parser("export", help="Export entries")
    export_parser.add_argument("--format", default="json",
                               choices=["json", "csv", "markdown"],
                               help="Output format")
    export_parser.add_argument("--output", help="Output file (default: stdout)")

    # Stats command
    subparsers.add_parser("stats", help="Show statistics")

    args = parser.parse_args()

    if args.command == "add":
        add_entry(args.company, args.item, args.date, args.url, args.notes, args.category)
    elif args.command == "list":
        list_entries(args.days, args.company, args.category)
    elif args.command == "search":
        search_entries(args.query)
    elif args.command == "export":
        export_entries(args.format, args.output)
    elif args.command == "stats":
        stats()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
