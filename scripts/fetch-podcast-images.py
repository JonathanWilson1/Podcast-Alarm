#!/usr/bin/env python3
"""
Fetch podcast artwork from Listen Notes API for blog posts.

Usage:
  python3 scripts/fetch-podcast-images.py [--output-dir DIR] [--podcasts-file FILE]

If no --podcasts-file is given, reads PODCASTS list from this script.
API key is read from the iOS app's PodcastAPI.swift automatically.

Caveats learned the hard way:
  - First search result is often WRONG. Script verifies title matches.
  - Similar names (e.g. "The Rest Is Politics" / "The Rest Is History")
    produce duplicate slugs. Script uses full name for filenames.
  - Some podcasts aren't on Listen Notes at all. Script reports these
    clearly so you can swap them for podcasts that DO have images.
  - Always check the final report for WRONG MATCH and NOT FOUND entries.
"""

import os
import sys
import re
import time
import json
import argparse
import requests
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
SITE_DIR = SCRIPT_DIR.parent
DEFAULT_OUTPUT = SITE_DIR / "images" / "blog" / "charts" / "ukpodcasts2026"


def find_api_key():
    """Get Listen Notes API key from environment."""
    key = os.environ.get("LISTEN_NOTES_API_KEY")
    if not key:
        print("Set LISTEN_NOTES_API_KEY environment variable first.")
        print("Key is in PodcastAlarm/PodcastAlarm/Services/PodcastAPI.swift")
        sys.exit(1)
    return key


def slugify(name):
    """Convert podcast name to a unique, safe filename."""
    slug = name.lower()
    # Remove common prefixes/suffixes that waste space
    for remove in ["'", "\u2019", '"']:
        slug = slug.replace(remove, "")
    for char, replacement in [("&", "and"), (" ", "-"), (".", ""), (",", ""), (":", ""), ("?", ""), ("!", ""), ("*", "")]:
        slug = slug.replace(char, replacement)
    # Remove duplicate hyphens
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug[:80]


def title_matches(search_query, result_title):
    """Check if the search result is actually the podcast we wanted."""
    query_words = set(search_query.lower().split()[:3])  # First 3 words of query
    title_words = set(result_title.lower().split())

    # At least 2 of the first 3 query words should appear in the result title
    overlap = query_words & title_words
    return len(overlap) >= min(2, len(query_words))


def search_podcast(query, headers):
    """Search Listen Notes and return the best matching result."""
    resp = requests.get(
        "https://listen-api.listennotes.com/api/v2/search",
        headers=headers,
        params={"q": query, "type": "podcast", "len_min": 1},
    )
    resp.raise_for_status()
    data = resp.json()

    # Check all results, not just the first, for a title match
    for result in data.get("results", [])[:10]:
        if title_matches(query, result.get("title_original", "")):
            return result, True  # matched

    # If no match found, return first result flagged as unverified
    if data.get("results"):
        return data["results"][0], False
    return None, False


def download_image(url, filepath):
    """Download an image and verify it's valid."""
    resp = requests.get(url, stream=True, timeout=30)
    resp.raise_for_status()
    with open(filepath, "wb") as f:
        for chunk in resp.iter_content(8192):
            f.write(chunk)

    # Verify file is a real image (not an error page)
    size = filepath.stat().st_size
    if size < 5000:
        filepath.unlink()
        return False
    return True


# Default podcast list — edit this or pass --podcasts-file
PODCASTS = [
    # Format: ("Search query", "output-filename.jpg")
    # Use specific filenames to avoid slug collisions
    ("The Rest Is Politics", "rest-is-politics.jpg"),
    ("The Diary of a CEO Steven Bartlett", "diary-of-a-ceo.jpg"),
    ("Off Menu James Acaster Ed Gamble", "off-menu.jpg"),
    ("The News Agents Emily Maitlis", "the-news-agents.jpg"),
    ("Shagged Married Annoyed Chris Ramsey", "shagged-married-annoyed.jpg"),
    ("The Rest Is History Tom Holland Dominic Sandbrook", "rest-is-history.jpg"),
    ("No Such Thing As A Fish QI", "no-such-thing.jpg"),
    ("Desert Island Discs BBC", "desert-island-discs.jpg"),
    ("Parenting Hell Rob Beckett", "parenting-hell.jpg"),
    ("The High Performance Podcast Jake Humphrey", "high-performance.jpg"),
]


def main():
    parser = argparse.ArgumentParser(description="Fetch podcast artwork from Listen Notes")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT, help="Image output directory")
    parser.add_argument("--podcasts-file", type=Path, help="JSON file with podcast list: [[query, filename], ...]")
    parser.add_argument("--force", action="store_true", help="Re-download existing images")
    args = parser.parse_args()

    api_key = find_api_key()
    headers = {"X-ListenAPI-Key": api_key}
    args.output_dir.mkdir(parents=True, exist_ok=True)

    # Load podcast list
    if args.podcasts_file:
        with open(args.podcasts_file) as f:
            podcasts = json.load(f)
    else:
        podcasts = PODCASTS

    results = {"downloaded": [], "skipped": [], "not_found": [], "wrong_match": []}
    total = len(podcasts)

    for i, entry in enumerate(podcasts, 1):
        if isinstance(entry, (list, tuple)):
            query, filename = entry[0], entry[1]
        else:
            query = entry
            filename = slugify(query) + ".jpg"

        filepath = args.output_dir / filename

        if filepath.exists() and not args.force:
            print(f"[{i}/{total}] SKIP (exists): {filename}")
            results["skipped"].append(filename)
            continue

        print(f"[{i}/{total}] Searching: {query}...", end=" ", flush=True)

        try:
            result, verified = search_podcast(query, headers)

            if result and result.get("image"):
                actual_title = result.get("title_original", "Unknown")

                if not verified:
                    print(f"WRONG MATCH: got '{actual_title}'")
                    results["wrong_match"].append((query, actual_title, filename))
                    continue

                ok = download_image(result["image"], filepath)
                if ok:
                    print(f"OK -> {filename} ({actual_title})")
                    results["downloaded"].append(filename)
                else:
                    print(f"BAD IMAGE (too small)")
                    results["not_found"].append(query)
            else:
                print("NOT FOUND")
                results["not_found"].append(query)
        except Exception as e:
            print(f"ERROR: {e}")
            results["not_found"].append(query)

        time.sleep(0.3)  # Rate limit: 5 req/sec on free tier

    # Save mapping
    mapping_path = args.output_dir / "image-mapping.json"
    with open(mapping_path, "w") as f:
        json.dump(results, f, indent=2)

    # Report
    print(f"\n{'='*60}")
    print(f"Downloaded: {len(results['downloaded'])}")
    print(f"Skipped (existed): {len(results['skipped'])}")
    print(f"Not found: {len(results['not_found'])}")
    print(f"Wrong match: {len(results['wrong_match'])}")

    if results["not_found"]:
        print(f"\nMISSING — swap these podcasts for ones with images:")
        for q in results["not_found"]:
            print(f"  - {q}")

    if results["wrong_match"]:
        print(f"\nWRONG MATCH — verify or swap:")
        for query, got, filename in results["wrong_match"]:
            print(f"  - Searched: '{query}' -> Got: '{got}' ({filename})")

    print(f"\nResults saved to {mapping_path}")


if __name__ == "__main__":
    main()
