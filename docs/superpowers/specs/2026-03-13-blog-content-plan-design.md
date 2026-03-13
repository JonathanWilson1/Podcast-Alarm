# Blog Content Plan — 25 New Posts

**Date:** 2026-03-13
**Goal:** Drive app downloads via organic search traffic
**Target audience:** Worldwide podcast listeners

## Context

The PodcastAlarm blog has 28 existing posts. The best-performing format is "best X podcasts" list posts targeting `[topic] podcasts` keywords. Top pages by GSC impressions (last 28 days): science (4,935), women-hosted (3,400), commute (3,199), make you smarter (2,211), true crime (1,800).

There are significant podcast niches with no coverage. This plan fills those gaps with 25 new posts.

## Post Format

All posts follow the proven pattern from recent posts (e.g. `best-podcasts-to-fall-asleep-to`):

- 8-12 podcast recommendations per post
- Each entry: `<h3>N. Podcast Name</h3>` + `<p>2-3 sentence description</p>`
- `{% include callToActionRow.html %}` after intro paragraph
- Closing `<h2>` section tying back to the app with App Store link

### Front Matter Template

```yaml
layout: post
title: "Best X Podcasts (2026)"          # under 60 chars, lead with keyword
categories: Podcast
featured-image: "/images/blog/charts/DIR/stock-image.jpg"  # reuse existing stock image
featured-image-alt: "Description of image"
description: "120-160 chars. Include 2-3 podcast names. Never mention Podcast Alarm."
permalink: /blog/slug-here               # no year in URL, evergreen
author: "Jonathan Wilson"
authorImage: "/images/blog/me.png"
```

### File Naming

Files use `YYYY-MM-DD-slug.markdown` (`.markdown` extension, not `.md`). Use publication date.

### Title Format

Use `Best X Podcasts (2026)` consistently — no counts, no clickbait hooks, no "in 2026". Keep it clean and under 60 chars.

## Image Pipeline

Each post requires podcast artwork fetched via `scripts/fetch-podcast-images.py`:

1. Write `podcasts.json` with `["Search query", "explicit-filename.jpg"]` pairs
2. Run script with Listen Notes API key from `PodcastAPI.swift`
3. Output directory per post: `images/blog/charts/<slug>/` (e.g. `images/blog/charts/best-history-podcasts/`)
4. Swap any NOT FOUND / WRONG MATCH podcasts and re-run until zero failures
5. Verify no placeholder image references in post

## Meta SEO Rules

- Title: under 60 chars, include (2026), lead with keyword
- Description: 120-160 chars, include 2-3 podcast names, never mention Podcast Alarm
- Permalink: `/blog/slug-here` (no year, evergreen URL)

## Posts to Create

### Genre Posts (15)

| # | Title | Slug |
|---|-------|------|
| 1 | Best History Podcasts (2026) | `/blog/best-history-podcasts` |
| 2 | Best Comedy Podcasts (2026) | `/blog/best-comedy-podcasts` |
| 3 | Best Business Podcasts (2026) | `/blog/best-business-podcasts` |
| 4 | Best Sports Podcasts (2026) | `/blog/best-sports-podcasts` |
| 5 | Best Mental Health Podcasts (2026) | `/blog/best-mental-health-podcasts` |
| 6 | Best Technology Podcasts (2026) | `/blog/best-technology-podcasts` |
| 7 | Best News & Politics Podcasts (2026) | `/blog/best-news-politics-podcasts` |
| 8 | Best Horror & Scary Podcasts (2026) | `/blog/best-horror-podcasts` |
| 9 | Best Philosophy Podcasts (2026) | `/blog/best-philosophy-podcasts` |
| 10 | Best Parenting Podcasts (2026) | `/blog/best-parenting-podcasts` |
| 11 | Best Health & Fitness Podcasts (2026) | `/blog/best-health-fitness-podcasts` |
| 12 | Best Documentary Podcasts (2026) | `/blog/best-documentary-podcasts` |
| 13 | Best Music Podcasts (2026) | `/blog/best-music-podcasts` |
| 14 | Best Economics Podcasts (2026) | `/blog/best-economics-podcasts` |
| 15 | Best Language Learning Podcasts (2026) | `/blog/best-language-learning-podcasts` |

### Use-Case Posts (10)

| # | Title | Slug |
|---|-------|------|
| 16 | Best Podcasts for Running (2026) | `/blog/best-podcasts-for-running` |
| 17 | Best Short Podcasts Under 20 Minutes (2026) | `/blog/best-short-podcasts` |
| 18 | Best Podcasts for Road Trips (2026) | `/blog/best-podcasts-for-road-trips` |
| 19 | Best Podcasts for the Gym (2026) | `/blog/best-podcasts-for-the-gym` |
| 20 | Best Podcasts for Walking (2026) | `/blog/best-podcasts-for-walking` |
| 21 | Best Podcasts for Cooking (2026) | `/blog/best-podcasts-for-cooking` |
| 22 | Best Podcasts for Teenagers (2026) | `/blog/best-podcasts-for-teenagers` |
| 23 | Best Podcasts for Couples (2026) | `/blog/best-podcasts-for-couples` |
| 24 | Best Podcasts for Long Flights (2026) | `/blog/best-podcasts-for-long-flights` |
| 25 | Best Podcasts for Anxiety & Stress Relief (2026) | `/blog/best-podcasts-for-anxiety-stress-relief` |

## Production Process Per Post

1. Write the post content (8-12 podcasts, intro, CTA, closing)
2. Create `podcasts.json` with search queries and explicit filenames
3. Run `fetch-podcast-images.py` to download artwork
4. Swap any podcasts with missing/wrong images and re-run
5. Verify no placeholder references (`grep` checks)
6. Commit post + images and push

## Success Criteria

- All 25 posts live on podcastalarm.app
- Each post has correct podcast artwork (no placeholders)
- Meta titles under 60 chars, descriptions 150-160 chars
- Posts begin ranking in GSC within 2-4 weeks
- Monitor for impressions and clicks; refresh meta if CTR is low

## Decisions Made

- **Raw HTML over components:** Podcast entries use `<h3>` + `<p>` directly, not a Jekyll include. Simpler, and find-and-replace handles bulk changes.
- **No geo-targeting:** All posts target worldwide audience.
- **New posts only:** No refreshing existing posts in this batch.
- **Genre + use-case mix:** Genre posts for search volume, use-case posts for higher-intent listeners closer to the app's value prop.

## Topic Overlap Notes

- **Mental Health (#5) vs Anxiety (#25):** Mental health post covers broad topics (therapy, self-improvement, emotional wellbeing). Anxiety post focuses specifically on calming/stress-relief shows. Zero podcast overlap between the two.
- **Health & Fitness (#11) vs Running (#16) / Gym (#19):** Health & Fitness focuses on nutrition, wellness, and general health education. Exclude exercise-specific shows covered in the running and gym posts.
- **Economics (#14) vs existing Investment post:** Economics covers macroeconomics, policy, and economic thinking. Avoid personal finance/investing shows already in the investment post.

## Internal Linking

Cross-link related posts where natural (e.g. running post links to gym post, mental health links to anxiety post). Use the existing format: `<a class="text-info" href="/blog/slug">Title</a>`.
