#!/usr/bin/env python3
"""
Competitor Tracker - AI company announcement tracker for competitive intelligence.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import re
import subprocess


class CompetitorTracker:
    """Main tracker class for managing AI company announcements."""

    def __init__(self, data_dir: Path, output_dir: Path):
        self.data_dir = data_dir
        self.output_dir = output_dir
        self.announcements_file = data_dir / "announcements.json"
        self.config_file = data_dir / "config.yaml"

        # Create directories if they don't exist
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Load or initialize announcements
        self.announcements = self._load_announcements()

    def _load_announcements(self) -> List[Dict]:
        """Load announcements from JSON file."""
        if self.announcements_file.exists():
            with open(self.announcements_file, 'r') as f:
                return json.load(f)
        return []

    def _save_announcements(self) -> None:
        """Save announcements to JSON file."""
        with open(self.announcements_file, 'w') as f:
            json.dump(self.announcements, f, indent=2)

    def _is_duplicate(self, announcement: Dict) -> bool:
        """Check if announcement already exists (by URL or title+company)."""
        for existing in self.announcements:
            if (existing.get('url') == announcement.get('url') or
                (existing.get('title') == announcement.get('title') and
                 existing.get('company') == announcement.get('company'))):
                return True
        return False

    def add_announcement(
        self,
        company: str,
        title: str,
        url: str,
        date: str = None,
        summary: str = "",
        source: str = "manual"
    ) -> None:
        """Add a new announcement manually."""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        announcement = {
            "company": company,
            "title": title,
            "url": url,
            "date": date,
            "summary": summary,
            "source": source,
            "added_at": datetime.now().isoformat()
        }

        if not self._is_duplicate(announcement):
            self.announcements.append(announcement)
            self._save_announcements()
            print(f"✓ Added: {company} - {title}")
        else:
            print(f"⚠ Duplicate: {company} - {title}")

    def list_announcements(self, company: Optional[str] = None,
                          limit: Optional[int] = None) -> None:
        """List announcements, optionally filtered by company."""
        filtered = self.announcements
        if company:
            filtered = [a for a in filtered if a['company'].lower() == company.lower()]

        if limit:
            filtered = filtered[:limit]

        if not filtered:
            print("No announcements found.")
            return

        print(f"\n{'='*80}")
        print(f"Total: {len(filtered)} announcements")
        print(f"{'='*80}\n")

        for i, ann in enumerate(filtered, 1):
            print(f"{i}. {ann['company']} - {ann['title']}")
            print(f"   Date: {ann['date']}")
            print(f"   URL: {ann['url']}")
            print(f"   Source: {ann['source']}")
            if ann.get('summary'):
                print(f"   Summary: {ann['summary']}")
            print()

    def scan_sources(self, sources: List[str] = None) -> None:
        """
        Scan configured sources for new announcements.
        This is a placeholder implementation - actual RSS parsing would go here.
        """
        print("🔍 Scanning sources for new announcements...")

        # For now, add some sample data to demonstrate functionality
        sample_announcements = [
            {
                "company": "OpenAI",
                "title": "GPT-5 Released with Enhanced Reasoning",
                "url": "https://openai.com/gpt5",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "summary": "OpenAI releases GPT-5 with improved reasoning capabilities and multi-step problem solving.",
                "source": "techcrunch"
            },
            {
                "company": "Anthropic",
                "title": "Claude 4 with 1M Context Window",
                "url": "https://anthropic.com/claude4",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "summary": "Anthropic launches Claude 4 supporting 1 million token context window.",
                "source": "venturebeat"
            }
        ]

        for ann in sample_announcements:
            self.add_announcement(**ann)

        print(f"\n✓ Scan complete. Total announcements: {len(self.announcements)}")

    def generate_digest(self, from_date: str = None, to_date: str = None) -> None:
        """Generate a weekly digest of announcements."""
        if not self.announcements:
            print("No announcements to digest.")
            return

        # Filter by date range
        if from_date:
            from_dt = datetime.strptime(from_date, "%Y-%m-%d")
            filtered = [a for a in self.announcements
                       if datetime.strptime(a['date'], "%Y-%m-%d") >= from_dt]
        else:
            # Default to last 7 days
            week_ago = datetime.now() - timedelta(days=7)
            filtered = [a for a in self.announcements
                       if datetime.strptime(a['date'], "%Y-%m-%d") >= week_ago]

        if to_date:
            to_dt = datetime.strptime(to_date, "%Y-%m-%d")
            filtered = [a for a in filtered
                       if datetime.strptime(a['date'], "%Y-%m-%d") <= to_dt]

        if not filtered:
            print("No announcements found for the specified date range.")
            return

        # Generate digest
        output_file = self.output_dir / f"competitor-digest-{datetime.now().strftime('%Y-%m-%d')}.md"

        with open(output_file, 'w') as f:
            f.write(f"# Competitor Digest - {datetime.now().strftime('%Y-%m-%d')}\n\n")
            f.write(f"**Period**: {from_date or 'Last 7 days'} to {to_date or 'Today'}\n")
            f.write(f"**Total Announcements**: {len(filtered)}\n\n")

            # Group by company
            companies = {}
            for ann in filtered:
                if ann['company'] not in companies:
                    companies[ann['company']] = []
                companies[ann['company']].append(ann)

            # Write company sections
            for company, announcements in sorted(companies.items()):
                f.write(f"## {company}\n\n")
                for ann in announcements:
                    f.write(f"### {ann['title']}\n\n")
                    f.write(f"**Date**: {ann['date']}\n")
                    f.write(f"**Source**: {ann['source']}\n\n")
                    if ann.get('summary'):
                        f.write(f"{ann['summary']}\n\n")
                    f.write(f"[Read more]({ann['url']})\n\n")

            # Summary stats
            f.write("---\n\n")
            f.write("## Summary Stats\n\n")
            f.write(f"- Companies tracked: {len(companies)}\n")
            f.write(f"- Total announcements: {len(filtered)}\n")
            for company, announcements in sorted(companies.items()):
                f.write(f"- {company}: {len(announcements)}\n")

        print(f"✓ Digest generated: {output_file}")
        return output_file


def main():
    parser = argparse.ArgumentParser(description="Competitor Tracker - AI company announcement tracker")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add a manual announcement')
    add_parser.add_argument('--company', required=True, help='Company name')
    add_parser.add_argument('--title', required=True, help='Announcement title')
    add_parser.add_argument('--url', required=True, help='URL to announcement')
    add_parser.add_argument('--date', help='Date (YYYY-MM-DD, defaults to today)')
    add_parser.add_argument('--summary', default='', help='Brief summary')
    add_parser.add_argument('--source', default='manual', help='Source name')

    # List command
    list_parser = subparsers.add_parser('list', help='List announcements')
    list_parser.add_argument('--company', help='Filter by company')
    list_parser.add_argument('--limit', type=int, help='Limit number of results')

    # Scan command
    scan_parser = subparsers.add_parser('scan', help='Scan sources for new announcements')
    scan_parser.add_argument('--source', action='append', help='Specific sources to scan')

    # Digest command
    digest_parser = subparsers.add_parser('digest', help='Generate weekly digest')
    digest_parser.add_argument('--from', dest='from_date', help='Start date (YYYY-MM-DD)')
    digest_parser.add_argument('--to', dest='to_date', help='End date (YYYY-MM-DD)')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Initialize tracker
    data_dir = Path.home() / '.openclaw' / 'workspace' / 'competitor-tracker' / 'data'
    output_dir = Path.home() / '.openclaw' / 'workspace' / 'outputs'
    tracker = CompetitorTracker(data_dir, output_dir)

    # Execute command
    if args.command == 'add':
        tracker.add_announcement(
            company=args.company,
            title=args.title,
            url=args.url,
            date=args.date,
            summary=args.summary,
            source=args.source
        )
    elif args.command == 'list':
        tracker.list_announcements(company=args.company, limit=args.limit)
    elif args.command == 'scan':
        tracker.scan_sources(sources=args.source)
    elif args.command == 'digest':
        tracker.generate_digest(from_date=args.from_date, to_date=args.to_date)


if __name__ == '__main__':
    main()
