#!/usr/bin/env python3
"""
Simple file watcher that monitors a directory for changes.
Runs continuously, logging any file modifications.
"""

import os
import time
import hashlib
from pathlib import Path

WATCH_DIR = os.environ.get("WATCH_DIR", "/tmp/watched")
POLL_INTERVAL = int(os.environ.get("POLL_INTERVAL", "2"))


def get_file_hash(filepath: str) -> str:
    """Get MD5 hash of file contents."""
    try:
        with open(filepath, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()
    except (IOError, OSError):
        return ""


def get_directory_state(directory: str) -> dict[str, str]:
    """Get current state of all files in directory."""
    state = {}
    path = Path(directory)
    if path.exists():
        for file in path.rglob("*"):
            if file.is_file():
                state[str(file)] = get_file_hash(str(file))
    return state


def main():
    print(f"File Watcher started")
    print(f"Watching: {WATCH_DIR}")
    print(f"Poll interval: {POLL_INTERVAL}s")

    # Ensure watch directory exists
    Path(WATCH_DIR).mkdir(parents=True, exist_ok=True)

    previous_state = get_directory_state(WATCH_DIR)
    print(f"Initial files: {len(previous_state)}")

    while True:
        time.sleep(POLL_INTERVAL)
        current_state = get_directory_state(WATCH_DIR)

        # Check for new files
        for filepath in current_state:
            if filepath not in previous_state:
                print(f"[CREATED] {filepath}")
            elif current_state[filepath] != previous_state[filepath]:
                print(f"[MODIFIED] {filepath}")

        # Check for deleted files
        for filepath in previous_state:
            if filepath not in current_state:
                print(f"[DELETED] {filepath}")

        previous_state = current_state


if __name__ == "__main__":
    main()
