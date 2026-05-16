#!/bin/bash
# Competitor Tracker shell wrapper

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$SCRIPT_DIR/competitor_tracker.py" "$@"
