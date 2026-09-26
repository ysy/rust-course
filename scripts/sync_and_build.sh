#!/usr/bin/env bash
# Bash wrapper to sync upstream and rebuild ebooks
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$SCRIPT_DIR/sync_and_build.py" "$@"
