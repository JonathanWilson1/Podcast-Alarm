#!/usr/bin/env python3
"""
Fetch podcast artwork from Listen Notes API for the UK podcasts blog post.

Usage:
  export LISTEN_NOTES_API_KEY="your_key_here"
  python3 scripts/fetch-podcast-images.py

Get a free API key at: https://www.listennotes.com/api/
Free tier: 5 req/sec, 300 req/month
"""

import os
import sys
import time
import json
import requests
from pathlib import Path

API_KEY = os.environ.get("LISTEN_NOTES_API_KEY")
if not API_KEY:
    print("Set LISTEN_NOTES_API_KEY environment variable first.")
    print("Get a free key at: https://www.listennotes.com/api/")
    sys.exit(1)

HEADERS = {"X-ListenAPI-Key": API_KEY}
BASE_URL = "https://listen-api.listennotes.com/api/v2"
IMG_DIR = Path(__file__).parent.parent / "images" / "blog" / "charts" / "ukpodcasts2026"
IMG_DIR.mkdir(parents=True, exist_ok=True)

# Podcast names from the blog post — search term : filename
PODCASTS = [
    "The Rest Is Politics",
    "The Diary of a CEO Steven Bartlett",
    "Off Menu James Acaster Ed Gamble",
    "The News Agents Emily Maitlis",
    "Shagged Married Annoyed Chris Ramsey",
    "The Rest Is History Tom Holland Dominic Sandbrook",
    "No Such Thing As A Fish QI",
    "Desert Island Discs BBC",
    "Parenting Hell Rob Beckett",
    "The High Performance Podcast Jake Humphrey",
    "My Dad Wrote a Porno",
    "The Receipts Podcast",
    "Table Manners Jessie Ware",
    "Out to Lunch Jay Rayner",
    "The Adam Buxton Podcast",
    "Grounded with Louis Theroux",
    "The Rest Is Entertainment Richard Osman",
    "That Peter Crouch Podcast",
    "Athletico Mince Bob Mortimer",
    "Have You Heard George's Podcast",
    "The Guilty Feminist",
    "Walking the Dog Emily Dean",
    "Howie Mandel Does Stuff",
    "Films to Be Buried With Brett Goldstein",
    "Nobody Panic Tessa Coates",
    "Newscast BBC",
    "Political Currency Ed Balls George Osborne",
    "Leading Alastair Campbell",
    "Americast BBC",
    "The Political Party Matt Forde",
    "More or Less BBC Radio 4",
    "The Today Podcast BBC",
    "FT News Briefing Financial Times",
    "Pod Save the UK",
    "Tortoise Slow News",
    "Uncanny Danny Robins BBC",
    "They Walk Among Us",
    "Casefile True Crime",
    "British Scandal Wondery",
    "Swindled podcast",
    "You're Wrong About",
    "Red Handed true crime podcast",
    "Crime Junkie Ashley Flowers",
    "Serial podcast",
    "In Our Time BBC Melvyn Bragg",
    "You're Dead to Me BBC Greg Jenner",
    "Infinite Monkey Cage BBC Brian Cox",
    "Science Vs Gimlet Wendy Zukerman",
    "Huberman Lab Andrew Huberman",
    "Stuff You Should Know",
    "Dan Snow History Hit",
    "Lex Fridman Podcast",
    "Radiolab",
    "The Moth podcast",
    "Happy Place Fearne Cotton",
    "How I Built This Guy Raz",
    "The Tim Ferriss Show",
    "My Therapist Ghosted Me Vogue Williams",
    "Feel Better Live More Dr Rangan Chatterjee",
    "On Purpose Jay Shetty",
    "Deep Dive Ali Abdaal",
    "Ctrl Alt Delete Emma Gannon",
    "Money Clinic Financial Times",
    "The Property Podcast Rob Bence",
    "Tailenders BBC Greg James Jimmy Anderson",
    "The Totally Football Show",
    "Griefcast Cariad Lloyd",
    "How to Fail Elizabeth Day",
    "Kermode and Mayo",
    "The Allusionist Helen Zaltzman",
    "Three Bean Salad podcast",
]


def slugify(name):
    """Convert podcast name to a safe filename."""
    return (
        name.lower()
        .replace("'", "")
        .replace("'", "")
        .replace("&", "and")
        .replace(" ", "-")
        .replace(".", "")
        .replace(",", "")
        .replace(":", "")
    )[:60]


def search_podcast(query):
    """Search Listen Notes for a podcast and return the first result."""
    resp = requests.get(
        f"{BASE_URL}/search",
        headers=HEADERS,
        params={"q": query, "type": "podcast", "len_min": 1},
    )
    resp.raise_for_status()
    data = resp.json()
    if data.get("results"):
        return data["results"][0]
    return None


def download_image(url, filepath):
    """Download an image from a URL."""
    resp = requests.get(url, stream=True)
    resp.raise_for_status()
    with open(filepath, "wb") as f:
        for chunk in resp.iter_content(8192):
            f.write(chunk)


def main():
    results = {}
    total = len(PODCASTS)

    for i, podcast_name in enumerate(PODCASTS, 1):
        slug = slugify(podcast_name.split()[0] + " " + " ".join(podcast_name.split()[1:3]))
        img_path = IMG_DIR / f"{slug}.jpg"

        if img_path.exists():
            print(f"[{i}/{total}] SKIP (exists): {podcast_name}")
            results[podcast_name] = str(img_path)
            continue

        print(f"[{i}/{total}] Searching: {podcast_name}...", end=" ", flush=True)

        try:
            result = search_podcast(podcast_name)
            if result and result.get("image"):
                img_url = result["image"]
                download_image(img_url, img_path)
                results[podcast_name] = str(img_path)
                print(f"OK -> {slug}.jpg")
            else:
                print("NOT FOUND")
        except Exception as e:
            print(f"ERROR: {e}")

        # Respect rate limit (free tier: 5 req/sec)
        time.sleep(0.3)

    # Save mapping for reference
    mapping_path = IMG_DIR / "image-mapping.json"
    with open(mapping_path, "w") as f:
        json.dump(results, f, indent=2)

    found = len(results)
    print(f"\nDone! {found}/{total} images downloaded to {IMG_DIR}")
    print(f"Mapping saved to {mapping_path}")


if __name__ == "__main__":
    main()
