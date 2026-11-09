# Automatic posting to Instagram, Facebook and Threads

Posts Aera's short videos through Meta's official APIs (Instagram Content Publishing, Facebook Reels Publishing, Threads API). No browser bots and no third-party tools.

- Job: `.github/workflows/social-post.yml` runs every 15 minutes, posts whatever is due, and saves a log. It does nothing until the `META_TOKEN` secret exists.
- Script: `scripts/social/meta_post.py` (Python standard library only).
- Data: the **`social-media` branch** (kept off `main`, so videos never reach the website or bloat its history). The job creates it on its first run.
- Each week's videos and captions arrive as a **pull request into `social-media`**. That pull request is the preview: nothing posts until it is merged.

## The `social-media` branch
```
queue.json        the posts (Claude writes it each week)
media/<file>.mp4  the videos (9:16, H.264, under 20 MB so Threads can fetch them)
posted.json       written by the job: links, failures, missed posts
comments/<date>.md  daily digest of new comments and replies (08:00 Budapest)
```

A post in `queue.json`:
```json
{
  "id": "2026-11-24-b1",
  "at": "2026-11-24T18:30:00+01:00",
  "video": "2026-11-24-b1.mp4",
  "instagram_caption": "English caption, hashtags at the end",
  "facebook_caption": "Magyar szöveg",
  "threads_caption": "Short English text, at most 500 characters",
  "platforms": ["instagram", "facebook", "threads"],
  "cover_ms": 1500,
  "hold": false
}
```
- `caption` is used for any platform without its own caption. `platforms` defaults to all three.
- `hold: true` keeps a post from going out. Gergő can ask for that any time before the slot.
- A post more than 6 hours late is marked `missed`, not posted late.
- A failed platform is retried on the next two runs, then left as `failed` in `posted.json`. A post that already went out to a platform is never posted there again.

## Copy checks before every post
The job refuses a caption with the word "AI", "Flyover", "companion", an exclamation mark, an em dash or a price, or one over the platform's length limit. The run fails once per version of the post, so GitHub emails us, and the post waits until the queue is fixed.

## Running it by hand
GitHub › Actions › "Social posts" › Run workflow:
- `check`: tests both tokens, finds the Page and Instagram ids, shows the Instagram quota and validates the queue. Posts nothing. Run this after setup.
- `post` with dry run on: lists what would go out now.
- `post` with dry run off and `only` set to an id: posts that one now, ignoring its time.
- `comments`, `threads-token`: the daily and weekly jobs.

## Secrets (Settings › Secrets and variables › Actions)
- `META_TOKEN`: a never-expiring system user token from Meta Business settings, with `instagram_basic`, `instagram_content_publish`, `instagram_manage_comments`, `pages_show_list`, `pages_read_engagement`, `pages_manage_posts` and `pages_read_user_content`.
- `THREADS_TOKEN`: the Threads long-lived token (`threads_basic`, `threads_content_publish`, `threads_read_replies`). It lasts 60 days. The Monday job extends it and fails when 10 days or fewer are left, or if Meta hands out a new token that has to be saved.
- Optional variable `META_PAGE_ID` if the Page can't be found by name.

The one-time setup prompt for Claude in Chrome is in the project files: `reports/distribution/meta-accounts-2026-11-09/CHROME-PROMPT-API-SETUP.md`.

## Limits
Instagram allows 100 API posts a day and Threads 250. Facebook Reels has its own cap, around 30 a day by third-party reports. We post 4 a week.

YouTube Shorts stay manual: uploads from an un-audited YouTube API project can be locked to private.
