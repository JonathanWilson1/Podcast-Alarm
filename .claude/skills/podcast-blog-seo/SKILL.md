---
name: podcast-blog-seo
description: Use when working on PodcastAlarm blog - creating podcast list posts, rewriting meta titles/descriptions, analysing GSC/GA4 data, or fetching podcast artwork. Also use when user mentions podcastalarm.app blog, CTR optimisation, or podcast list posts.
---

# Podcast Blog SEO

Create, update and optimise blog posts on podcastalarm.app (Jekyll + GitHub Pages).

## Key IDs

- GA4 property: `249905482` (PodcastAlarm.app)
- GSC property: `sc-domain:podcastalarm.app`
- Site repo: `/Users/jonathanwilson/Developer/PodcastAlarm-site` (Jekyll, master branch, GitHub Pages)
- Listen Notes API key: in `/Users/jonathanwilson/Developer/PodcastAlarm/PodcastAlarm/Services/PodcastAPI.swift` (grep for `apiKey`)
- Image script: `PodcastAlarm-site/scripts/fetch-podcast-images.py`

## Creating a New Blog Post

### Step 1: Write the post

File: `_posts/YYYY-MM-DD-slug.markdown`

```markdown
---
layout: post
title: "POST TITLE (2026)"
categories: Podcast
featured-image: "/images/blog/charts/100UK2020/kelly-sikkema-1KfV102FCcQ-unsplash.jpg"
featured-image-alt: "Description"
description: "UNDER 160 CHARS. Include 2-3 podcast names. Never mention Podcast Alarm."
permalink: /blog/slug-here
author: "Jonathan Wilson"
authorImage: "/images/blog/me.png"
---

<p>Intro paragraph.</p>

{% include callToActionRow.html %}

<br>

<h3><a class="text-info" href="https://podcasts.apple.com/gb/search?term=Podcast+Name">1. Podcast Name</a></h3>
<img src="/images/blog/charts/NEWDIR/filename.jpg" alt="Podcast Name podcast artwork" width="100" style="border-radius:12px;float:left;margin:0 15px 15px 0;">
<p>2-3 sentences. What makes it good, who hosts it, why listen.</p>
<br style="clear:both;">

<h3><a class="text-info" href="https://podcasts.apple.com/gb/search?term=Podcast+Name+2">2. Podcast Name 2</a></h3>
<img src="/images/blog/charts/NEWDIR/filename2.jpg" alt="Podcast Name 2 podcast artwork" width="100" style="border-radius:12px;float:left;margin:0 15px 15px 0;">
<p>Description.</p>
<br style="clear:both;">
```

**CRITICAL: Every entry MUST have:**
1. Apple Podcasts search link on the `<h3>`
2. `<img>` tag with the podcast artwork image
3. `<br style="clear:both;">` after the `<p>`

**Never write `<h3>` + `<p>` without the image** — the inline artwork is a core part of every post's design. After fetching images, immediately wire them into the post before deploying.

### Step 2: Fetch images

Read the API key from PodcastAPI.swift, then write a JSON file and run the script:

```bash
cd /Users/jonathanwilson/Developer/PodcastAlarm-site
export LISTEN_NOTES_API_KEY="THE_KEY"
python3 scripts/fetch-podcast-images.py --podcasts-file podcasts.json --output-dir images/blog/charts/NEWDIR
```

The `podcasts.json` format:
```json
[
  ["Search query for podcast", "explicit-filename.jpg"],
  ["Another Podcast Host Name", "another-podcast.jpg"]
]
```

**Always use explicit filenames** — similar names like "The Rest Is Politics" / "The Rest Is History" collide when auto-slugified.

### Step 3: Check the script output

The script reports NOT FOUND and WRONG MATCH separately. For every NOT FOUND or WRONG MATCH:
- **Swap that podcast for a different one that has an image**
- Re-run the script
- Repeat until zero failures

### Step 4: Verify before deploying

```bash
# Must return nothing (only the featured-image line in frontmatter is OK):
grep "kelly-sikkema" _posts/YOUR-POST.markdown | grep -v "featured-image"

# Must return nothing (no placeholder references):
grep "100UK2020" _posts/YOUR-POST.markdown | grep -v "featured-image"
```

### Step 5: Commit and push

```bash
git add _posts/ images/
git commit -m "Add new blog post: TITLE"
git push origin master
```

Live in 1-2 minutes on GitHub Pages.

## Post Formats

### Article post (`layout: post`)

Use `<h3>` + `<p>` for each entry. Best for SEO — more text content.

### Chart/list post (`layout: chart`)

For large lists (50-100 items). Top 10 get full cards, rest go in image grids.

**Top entries:** `blogPostListItem.html` — takes `title`, `content`, `link`, `image`
```
{% include blogPostListItem.html
  title="1) Podcast Name"
  content="Description here."
  link="https://podcasts.apple.com/gb/podcast/..."
  image="/images/blog/charts/DIR/filename.jpg"
%}
```

**Grid entries:** `blogPostTopChartListItem.html` in rows of 3
```html
<div class="row">
  <div class="col-md-4">
  {% include blogPostTopChartListItem.html
    title="11) Short Name"
    content=""
    link="#"
    image="/images/blog/charts/DIR/filename.jpg"
  %}
  </div>
  <div class="col-md-4">
    {% include blogPostTopChartListItem.html
      title="12) Short Name"
      content=""
      link="#"
      image="/images/blog/charts/DIR/filename.jpg"
    %}
  </div>
  <div class="col-md-4">
    {% include blogPostTopChartListItem.html
      title="13) Short Name"
      content=""
      link="#"
      image="/images/blog/charts/DIR/filename.jpg"
    %}
  </div>
</div>
```

**Grid title max: 22 characters** after the number prefix. Strip "The", host names, "Podcast", "Show":
- "On Purpose with Jay Shetty" → "On Purpose"
- "The Totally Football Show" → "Totally Football"

**Cross-link** between posts:
```html
<p>⭐️Featured in <a class="text-info" href="/blog/other-post">Other Post Title</a></p>
```

## Meta Title & Description Rules

| Rule | Why |
|------|-----|
| Include 2-3 podcast names in description | Searchers recognise brands, increases CTR |
| Never mention "Podcast Alarm" or "alarm" | Searchers don't know the brand |
| Add `(2026)` to titles | Freshness signal |
| Titles under 60 characters | Google truncates longer |
| Descriptions 150-160 characters | Full SERP display |
| Lead with the keyword | Google bolds matching terms |

## Replacing an Existing Post

1. New file with today's date and new slug
2. `permalink: /blog/new-slug` (evergreen, no year in URL)
3. `redirect_from: /blog/old-slug` for 301 redirect
4. Change old post's `permalink` (append `-old`) to avoid conflict

## Analysing SEO Data

Pull GA4 and GSC in parallel:

```
GA4:  run_report on property 249905482
      - 30 days vs previous 30: totalUsers, sessions, screenPageViews, engagementRate
      - by channel: sessionDefaultChannelGroup
      - by page: pagePath

GSC:  get_performance_overview for sc-domain:podcastalarm.app
      get_search_analytics by query (top 20)
      get_search_analytics by page (top 15)
```

**Quick wins** = high impressions + low CTR + good position (< 10). Meta rewrites, not content changes.

## Image Sourcing Caveats

1. **Listen Notes doesn't have every podcast.** BBC Radio 4, niche UK shows often missing. Swap the podcast, don't use a placeholder.
2. **First result is often wrong.** Script validates but check the WRONG MATCH report. "The Bunker" returned a paintball podcast.
3. **Never deploy placeholder images.** If image can't be sourced, change the podcast.
4. **Verify every image** exists, is > 5KB, and is the correct podcast before pushing.

## Writing Style

- Write like recommending shows to a friend — not a listicle robot
- No filler ("In today's world...", "It's no secret that...")
- Short paragraphs: 2-3 sentences per entry
- Every entry needs: podcast name, host, what makes it worth listening to
