#!/usr/bin/env python3
"""
Competitor Tracker - Track AI company shipping activity

Usage:
  competitor-track add <company> <name> <description> [--category CATEGORY] [--link LINK] [--impact 1-5]
  competitor-track list [--company COMPANY] [--days N] [--category CATEGORY]
  competitor-track report [--output FILE] [--days N]
  competitor-track export --format json --output FILE
  competitor-track import --format json --input FILE
  competitor-track info
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
import uuid

# Configuration
DATA_DIR = Path.home() / ".openclaw" / "workspace" / "data" / "competitor-tracker"
ENTRIES_FILE = DATA_DIR / "entries.json"
OUTPUT_DIR = Path.home() / ".openclaw" / "workspace" / "outputs"

# Valid companies and categories
COMPANIES = [
    "Anthropic", "OpenAI", "Google DeepMind", "Google", "Meta",
    "Microsoft", "Stability AI", "Midjourney", "Perplexity", "Mistral"
]

CATEGORIES = ["model", "feature", "api", "product", "research", "safety", "other"]

def ensure_data_dir() -> None:
    """Ensure data directory exists."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

def load_entries() -> Dict[str, Any]:
    """Load entries from JSON file."""
    ensure_data_dir()
    if not ENTRIES_FILE.exists():
        return {"entries": []}
    try:
        with open(ENTRIES_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {"entries": []}

def save_entries(data: Dict[str, Any]) -> None:
    """Save entries to JSON file."""
    ensure_data_dir()
    with open(ENTRIES_FILE, "w") as f:
        json.dump(data, f, indent=2)

def add_entry(company: str, name: str, description: str,
              category: Optional[str] = None,
              link: Optional[str] = None,
              impact: Optional[int] = None,
              notes: Optional[str] = None) -> str:
    """Add a new shipping entry."""
    data = load_entries()

    # Validate impact
    if impact is not None and (impact < 1 or impact > 5):
        print("Error: Impact must be between 1 and 5", file=sys.stderr)
        sys.exit(1)

    entry = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "company": company,
        "name": name,
        "description": description,
    }

    if category:
        entry["category"] = category
    if link:
        entry["links"] = [link]
    if impact is not None:
        entry["impact"] = impact
    if notes:
        entry["notes"] = notes

    data["entries"].append(entry)
    save_entries(data)

    return entry["id"]

def list_entries(company: Optional[str] = None,
                 days: Optional[int] = None,
                 category: Optional[str] = None) -> List[Dict[str, Any]]:
    """List entries with optional filters."""
    data = load_entries()
    entries = data["entries"]

    # Sort by timestamp (newest first)
    entries = sorted(entries, key=lambda x: x["timestamp"], reverse=True)

    # Filter by company
    if company:
        entries = [e for e in entries if e["company"].lower() == company.lower()]

    # Filter by days
    if days:
        cutoff = (datetime.utcnow() - timedelta(days=days)).isoformat() + "Z"
        entries = [e for e in entries if e["timestamp"] >= cutoff]

    # Filter by category
    if category:
        entries = [e for e in entries if e.get("category") == category]

    return entries

def format_entry(entry: Dict[str, Any], show_id: bool = False) -> str:
    """Format a single entry for display."""
    parts = []

    if show_id:
        parts.append(f"[{entry['id'][:8]}]")

    timestamp = datetime.fromisoformat(entry["timestamp"].replace("Z", "+00:00"))
    date_str = timestamp.strftime("%Y-%m-%d %H:%M UTC")

    parts.append(f"{date_str} - **{entry['company']}**: {entry['name']}")

    if entry.get("description"):
        parts.append(f"  {entry['description']}")

    if entry.get("category"):
        parts.append(f"  Category: {entry['category']}")

    if entry.get("impact"):
        stars = "⭐" * entry["impact"]
        parts.append(f"  Impact: {stars} ({entry['impact']}/5)")

    if entry.get("links"):
        parts.append(f"  Links: {', '.join(entry['links'])}")

    if entry.get("notes"):
        parts.append(f"  Notes: {entry['notes']}")

    return "\n".join(parts)

def generate_report(days: Optional[int] = None) -> str:
    """Generate a markdown report."""
    entries = list_entries(days=days)

    if not entries:
        return "# No entries found for the specified period."

    # Group by impact
    by_impact = {i: [] for i in range(5, 0, -1)}
    by_category = {}

    for entry in entries:
        impact = entry.get("impact", 2)
        if impact in by_impact:
            by_impact[impact].append(entry)

        category = entry.get("category", "other")
        if category not in by_category:
            by_category[category] = []
        by_category[category].append(entry)

    # Calculate stats
    companies_count = {}
    for entry in entries:
        company = entry["company"]
        companies_count[company] = companies_count.get(company, 0) + 1

    # Build report
    lines = []

    period = f"Last {days} days" if days else "All time"
    lines.append(f"# AI Shipping Report - {period}")
    lines.append(f"")
    lines.append(f"**Generated:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append(f"")

    # High impact section
    lines.append(f"## High Impact (5)")
    for entry in by_impact[5]:
        lines.append(f"- **{entry['company']}**: {entry['name']} - {entry.get('description', '')}")
    lines.append(f"")

    # By category
    lines.append(f"## By Category")
    for category in sorted(by_category.keys()):
        lines.append(f"")
        lines.append(f"### {category.capitalize()}")
        for entry in by_category[category]:
            lines.append(f"- {entry['company']}: {entry['name']}")

    # Stats
    lines.append(f"")
    lines.append(f"## Summary")
    lines.append(f"")
    lines.append(f"**This week:** {len(entries)} launches across {len(companies_count)} companies")

    if companies_count:
        lines.append(f"")
        lines.append(f"**By company:**")
        sorted_companies = sorted(companies_count.items(), key=lambda x: x[1], reverse=True)
        for company, count in sorted_companies:
            lines.append(f"- {company}: {count}")

    return "\n".join(lines)

def export_entries(output_file: str) -> None:
    """Export entries to JSON file."""
    data = load_entries()
    output_path = Path(output_file)

    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Exported {len(data['entries'])} entries to {output_path}")

def import_entries(input_file: str) -> None:
    """Import entries from JSON file."""
    input_path = Path(input_file)

    if not input_path.exists():
        print(f"Error: File not found: {input_file}", file=sys.stderr)
        sys.exit(1)

    with open(input_path, "r") as f:
        imported_data = json.load(f)

    if "entries" not in imported_data:
        print("Error: Invalid import file - missing 'entries' key", file=sys.stderr)
        sys.exit(1)

    data = load_entries()

    # Check for duplicates by ID
    existing_ids = {e["id"] for e in data["entries"]}
    new_entries = [e for e in imported_data["entries"] if e["id"] not in existing_ids]

    data["entries"].extend(new_entries)
    save_entries(data)

    print(f"Imported {len(new_entries)} entries from {input_file}")

def generate_weekly_digest() -> str:
    """Generate a weekly digest report."""
    # Get entries from the last 7 days
    entries = list_entries(days=7)
    now = datetime.utcnow()
    week_number = now.isocalendar()[1]
    year = now.year

    if not entries:
        return f"# AI Shipping Digest - Week {week_number} ({year})\n\nNo entries found this week."

    # Calculate stats
    companies_count = {}
    impact_count = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    category_count = {}

    for entry in entries:
        company = entry["company"]
        companies_count[company] = companies_count.get(company, 0) + 1

        impact = entry.get("impact", 2)
        impact_count[impact] += 1

        category = entry.get("category", "other")
        category_count[category] = category_count.get(category, 0) + 1

    # Build digest
    lines = []
    lines.append(f"# AI Shipping Digest - Week {week_number} ({year})")
    lines.append("")
    lines.append(f"**Generated:** {now.strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append(f"**Period:** {now - timedelta(days=7).strftime('%Y-%m-%d')} to {now.strftime('%Y-%m-%d')}")
    lines.append("")
    lines.append(f"## 📊 This Week")
    lines.append(f"")
    lines.append(f"- **Total entries:** {len(entries)}")
    lines.append(f"- **Companies tracked:** {len(companies_count)}")
    lines.append(f"- **High impact (5):** {impact_count[5]}")
    lines.append("")

    # Top companies
    lines.append(f"## 🏢 Top Companies")
    sorted_companies = sorted(companies_count.items(), key=lambda x: x[1], reverse=True)
    for company, count in sorted_companies:
        lines.append(f"- {company}: {count} shipping(s)")
    lines.append("")

    # High impact entries
    high_impact = [e for e in entries if e.get("impact", 0) >= 4]
    if high_impact:
        lines.append(f"## 🔥 High Impact (4-5 stars)")
        for entry in high_impact:
            timestamp = datetime.fromisoformat(entry["timestamp"].replace("Z", "+00:00"))
            date_str = timestamp.strftime("%m-%d")
            stars = "⭐" * entry.get("impact", 2)
            lines.append(f"- [{date_str}] **{entry['company']}**: {entry['name']}")
            if entry.get("description"):
                lines.append(f"  {entry['description']} {stars}")
            if entry.get("links"):
                lines.append(f"  🔗 {', '.join(entry['links'])}")
        lines.append("")

    # By category
    lines.append(f"## 📦 By Category")
    sorted_categories = sorted(category_count.items(), key=lambda x: x[1], reverse=True)
    for category, count in sorted_categories:
        lines.append(f"- {category.capitalize()}: {count}")
    lines.append("")

    # All entries
    lines.append(f"## 📋 All Entries")
    for entry in entries:
        timestamp = datetime.fromisoformat(entry["timestamp"].replace("Z", "+00:00"))
        date_str = timestamp.strftime("%Y-%m-%d")
        stars = "⭐" * entry.get("impact", 2)
        lines.append(f"**[{date_str}] {entry['company']}: {entry['name']}** {stars}")
        if entry.get("description"):
            lines.append(f"{entry['description']}")
        if entry.get("category"):
            lines.append(f"*Category: {entry['category']}*")
        lines.append("")

    return "\n".join(lines)


def show_info() -> None:
    """Show data location and stats."""
    data = load_entries()
    print(f"Data directory: {DATA_DIR}")
    print(f"Entries file: {ENTRIES_FILE}")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Total entries: {len(data['entries'])}")

    if data["entries"]:
        # Find most recent entry
        latest = max(data["entries"], key=lambda x: x["timestamp"])
        print(f"Latest entry: {latest['company']} - {latest['name']}")
        print(f"  Date: {latest['timestamp']}")

def main() -> None:
    parser = argparse.ArgumentParser(description="Track AI company shipping activity")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new shipping entry")
    add_parser.add_argument("company", help="Company name")
    add_parser.add_argument("name", help="Product/feature name")
    add_parser.add_argument("description", help="Description")
    add_parser.add_argument("--category", choices=CATEGORIES, help="Category")
    add_parser.add_argument("--link", help="Link URL")
    add_parser.add_argument("--impact", type=int, choices=range(1, 6), help="Impact rating (1-5)")
    add_parser.add_argument("--notes", help="Additional notes")

    # List command
    list_parser = subparsers.add_parser("list", help="List entries")
    list_parser.add_argument("--company", help="Filter by company")
    list_parser.add_argument("--days", type=int, help="Filter by last N days")
    list_parser.add_argument("--category", choices=CATEGORIES, help="Filter by category")

    # Report command
    report_parser = subparsers.add_parser("report", help="Generate markdown report")
    report_parser.add_argument("--output", "-o", help="Output file path")
    report_parser.add_argument("--days", type=int, help="Report for last N days")

    # Export command
    export_parser = subparsers.add_parser("export", help="Export entries to JSON")
    export_parser.add_argument("--format", choices=["json"], default="json", help="Export format")
    export_parser.add_argument("--output", "-o", required=True, help="Output file path")

    # Import command
    import_parser = subparsers.add_parser("import", help="Import entries from JSON")
    import_parser.add_argument("--format", choices=["json"], default="json", help="Import format")
    import_parser.add_argument("--input", "-i", required=True, help="Input file path")

    # Info command
    subparsers.add_parser("info", help="Show data location and stats")

    # Digest command
    digest_parser = subparsers.add_parser("digest", help="Generate weekly digest")
    digest_parser.add_argument("--output", "-o", help="Output file path (default: outputs/competitor-digest-YYYY-Www.md)")
    digest_parser.add_argument("--save", action="store_true", help="Save digest to outputs directory")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "add":
        entry_id = add_entry(
            args.company,
            args.name,
            args.description,
            category=args.category,
            link=args.link,
            impact=args.impact,
            notes=args.notes
        )
        print(f"Entry added: {entry_id}")

    elif args.command == "list":
        entries = list_entries(company=args.company, days=args.days, category=args.category)

        if not entries:
            print("No entries found.")
        else:
            for entry in entries:
                print("")
                print(format_entry(entry))
                print("-" * 60)

    elif args.command == "report":
        report = generate_report(days=args.days)

        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w") as f:
                f.write(report)
            print(f"Report saved to: {output_path}")
        else:
            print(report)

    elif args.command == "export":
        export_entries(args.output)

    elif args.command == "import":
        import_entries(args.input)

    elif args.command == "info":
        show_info()

    elif args.command == "digest":
        digest = generate_weekly_digest()

        if args.save:
            now = datetime.utcnow()
            week_number = now.isocalendar()[1]
            filename = f"competitor-digest-{now.year}-W{week_number:02d}.md"
            output_path = OUTPUT_DIR / filename
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w") as f:
                f.write(digest)
            print(f"Digest saved to: {output_path}")
        elif args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w") as f:
                f.write(digest)
            print(f"Digest saved to: {output_path}")
        else:
            print(digest)

if __name__ == "__main__":
    main()
