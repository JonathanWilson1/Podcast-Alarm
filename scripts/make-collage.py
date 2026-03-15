#!/usr/bin/env python3
"""
Create a collage banner from podcast artwork images for each blog post.
Small tiles in a tight grid, randomly ordered, filling the entire banner.
"""

import random
from pathlib import Path
from PIL import Image

SITE_DIR = Path(__file__).parent.parent
CHARTS_DIR = SITE_DIR / "images" / "blog" / "charts"

BANNER_WIDTH = 1200
BANNER_HEIGHT = 500
TILE_SIZE = 100


def make_collage(image_dir, output_path):
    """Fill banner with a grid of small randomly-ordered artwork tiles."""
    source_files = sorted([
        f for f in image_dir.iterdir()
        if f.suffix.lower() in ('.jpg', '.png')
        and f.name != 'collage-banner.jpg'
        and f.stat().st_size > 5000
    ])

    if not source_files:
        print(f"  No images found in {image_dir.name}, skipping")
        return False

    # Load and resize all artwork to small squares
    tiles = []
    for f in source_files:
        try:
            img = Image.open(f).convert('RGB')
            w, h = img.size
            side = min(w, h)
            left = (w - side) // 2
            top = (h - side) // 2
            img = img.crop((left, top, left + side, top + side))
            img = img.resize((TILE_SIZE, TILE_SIZE), Image.LANCZOS)
            tiles.append(img)
        except Exception as e:
            print(f"  Error with {f.name}: {e}")

    if not tiles:
        return False

    cols = BANNER_WIDTH // TILE_SIZE
    rows = BANNER_HEIGHT // TILE_SIZE

    # Canvas sized exactly to grid
    canvas_w = cols * TILE_SIZE
    canvas_h = rows * TILE_SIZE
    canvas = Image.new('RGB', (canvas_w, canvas_h))

    # Build list of tiles to fill every cell, shuffled
    total_cells = cols * rows
    rng = random.Random(42)
    fill = []
    while len(fill) < total_cells:
        batch = list(tiles)
        rng.shuffle(batch)
        fill.extend(batch)
    fill = fill[:total_cells]

    for i, tile in enumerate(fill):
        row = i // cols
        col = i % cols
        canvas.paste(tile, (col * TILE_SIZE, row * TILE_SIZE))

    # Resize to exact banner dimensions
    canvas = canvas.resize((BANNER_WIDTH, BANNER_HEIGHT), Image.LANCZOS)
    canvas.save(output_path, 'JPEG', quality=85)
    return True


def main():
    for img_dir in sorted(CHARTS_DIR.iterdir()):
        if not img_dir.is_dir():
            continue
        if not (img_dir.name.startswith('best-') or img_dir.name == '100UK2020'):
            continue

        output = img_dir / "collage-banner.jpg"
        print(f"Creating collage for {img_dir.name}...")
        if make_collage(img_dir, output):
            src = len([f for f in img_dir.iterdir() if f.suffix.lower() in ('.jpg', '.png') and f.name != 'collage-banner.jpg'])
            print(f"  -> {output.name} ({src} source images)")


if __name__ == "__main__":
    main()
