#!/usr/bin/env python3
"""Post queued Aera videos to Instagram, the Facebook Page and Threads.

Meta's official APIs only. Runs on GitHub Actions (.github/workflows/social-post.yml).

Data lives on the `social-media` branch, checked out at --data (default ./social):
  queue.json      the posts to make (written by Claude each week)
  media/<file>    the videos
  posted.json     what went out, per post and platform (written by this script)
  comments/       daily comment digests (mode "comments")

Modes:
  post      publish every post that is due and not yet out
  check     verify tokens, find the Page and Instagram ids, validate the queue; posts nothing
  comments  write comments/<date>.md with new comments and replies from the last 14 days
  threads-token  refresh the Threads token's expiry and report days left

Secrets (environment): META_TOKEN (system user token), THREADS_TOKEN.
Optional: META_PAGE_ID, GRAPH_VERSION, MEDIA_BASE_URL.
"""
from __future__ import annotations

import argparse
import hashlib
import datetime as dt
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

GRAPH_VERSION = os.environ.get("GRAPH_VERSION", "v23.0")
GRAPH = f"https://graph.facebook.com/{GRAPH_VERSION}"
RUPLOAD = "https://rupload.facebook.com"
THREADS = "https://graph.threads.net/v1.0"
# Threads fetches the video from a public URL. jsDelivr serves the public social-media
# branch as video/mp4 (raw.githubusercontent says octet-stream), files up to 20 MB.
MEDIA_BASE_URL = os.environ.get(
    "MEDIA_BASE_URL",
    "https://cdn.jsdelivr.net/gh/VargaGergo-Git/aera-site@social-media/media/",
)
THREADS_MAX_BYTES = 20 * 1024 * 1024
PLATFORMS = ("instagram", "facebook", "threads")
MAX_TRIES = 3  # a failing platform is retried on the next runs, then left as failed
LATE_LIMIT = dt.timedelta(hours=6)  # a post more than 6 h late is marked missed, not posted
CAPTION_MAX = {"instagram": 2200, "facebook": 5000, "threads": 500}


class MetaError(RuntimeError):
    pass


class ProcessingFailed(MetaError):
    """Meta rejected the video itself: the post is not live, so it should be retried."""


# ---------- HTTP ----------

def _redact(text: str) -> str:
    for name in ("META_TOKEN", "THREADS_TOKEN", "PAGE_TOKEN"):
        value = os.environ.get(name)
        if value:
            text = text.replace(value, f"<{name}>")
    return re.sub(r"access_token=[^&\s\"']+", "access_token=<hidden>", text)


def request(method: str, url: str, params: dict | None = None, data: bytes | None = None,
            headers: dict | None = None, timeout: int = 300) -> dict:
    if params:
        encoded = urllib.parse.urlencode(params)
        if method == "GET" or data is not None:
            url = f"{url}?{encoded}"
        else:
            data = encoded.encode()
            headers = {**(headers or {}), "Content-Type": "application/x-www-form-urlencoded"}
    req = urllib.request.Request(url, data=data, method=method, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode() or "{}"
    except urllib.error.HTTPError as err:
        body = err.read().decode(errors="replace")
        raise MetaError(_redact(f"{method} {url.split('?')[0]} -> {err.code}: {body[:600]}")) from None
    except urllib.error.URLError as err:
        raise MetaError(_redact(f"{method} {url.split('?')[0]} -> {err.reason}")) from None
    try:
        return json.loads(body)
    except json.JSONDecodeError:
        return {"raw": body[:600]}


def best_effort(what: str, fetch, default):
    """A follow-up call after a post is already live: never let it fail the post."""
    try:
        return fetch()
    except ProcessingFailed:
        raise
    except (MetaError, KeyError) as err:
        print(f"  note: {what} failed after publishing ({_redact(str(err))[:200]})")
        return default


def wait_until(check, what: str, tries: int = 60, pause: float = 10.0) -> None:
    """Poll check() until it returns True; it raises on a hard failure."""
    for _ in range(tries):
        if check():
            return
        time.sleep(pause)
    raise MetaError(f"{what}: still processing after {int(tries * pause)} s")


# ---------- Accounts ----------

class Accounts:
    def __init__(self, meta_token: str | None, threads_token: str | None):
        self.meta_token = meta_token
        self.threads_token = threads_token
        self.page_id: str | None = None
        self.page_token: str | None = None
        self.ig_id: str | None = None

    def load_meta(self) -> None:
        if not self.meta_token:
            raise MetaError("META_TOKEN is not set")
        page_id = os.environ.get("META_PAGE_ID")
        if not page_id:
            pages = request("GET", f"{GRAPH}/me/accounts",
                            {"fields": "id,name,username", "access_token": self.meta_token}).get("data", [])
            match = [p for p in pages if p.get("username") == "aerahealthapp" or p.get("name") == "Aera Health"]
            if not match:
                names = ", ".join(p.get("name", "?") for p in pages) or "none"
                raise MetaError(f"Aera Health Page not visible to the token (Pages seen: {names})")
            page_id = match[0]["id"]
        page = request("GET", f"{GRAPH}/{page_id}",
                       {"fields": "name,access_token,instagram_business_account{id,username}",
                        "access_token": self.meta_token})
        self.page_id = page_id
        self.page_token = page.get("access_token") or self.meta_token
        os.environ["PAGE_TOKEN"] = self.page_token  # so errors redact it too
        ig = page.get("instagram_business_account") or {}
        self.ig_id = ig.get("id")
        if not self.ig_id:
            raise MetaError("The Page has no linked Instagram business account visible to the token")
        print(f"Page {page.get('name')} ({page_id}), Instagram @{ig.get('username')} ({self.ig_id})")


# ---------- Publishing ----------

def post_instagram(acc: Accounts, video: Path, caption: str, cover_ms: int | None) -> str:
    params = {"media_type": "REELS", "upload_type": "resumable", "caption": caption,
              "share_to_feed": "true", "access_token": acc.meta_token}
    if cover_ms is not None:
        params["thumb_offset"] = str(cover_ms)
    container = request("POST", f"{GRAPH}/{acc.ig_id}/media", params)
    cid = container["id"]
    upload_uri = container.get("uri") or f"{RUPLOAD}/ig-api-upload/{GRAPH_VERSION}/{cid}"
    data = video.read_bytes()
    request("POST", upload_uri, data=data, headers={
        "Authorization": f"OAuth {acc.meta_token}", "offset": "0", "file_size": str(len(data))})

    def ready() -> bool:
        status = request("GET", f"{GRAPH}/{cid}", {"fields": "status_code,status",
                                                   "access_token": acc.meta_token})
        code = status.get("status_code")
        if code in ("ERROR", "EXPIRED"):
            raise MetaError(f"Instagram processing {code}: {status.get('status')}")
        return code == "FINISHED"

    wait_until(ready, "Instagram")
    published = request("POST", f"{GRAPH}/{acc.ig_id}/media_publish",
                        {"creation_id": cid, "access_token": acc.meta_token})
    media_id = published["id"]
    # Live from here on. The permalink is a nicety; the post must be logged either way.
    return best_effort("Instagram permalink", lambda: request(
        "GET", f"{GRAPH}/{media_id}", {"fields": "permalink", "access_token": acc.meta_token}
    ).get("permalink") or media_id, media_id)


def post_facebook(acc: Accounts, video: Path, caption: str, title: str | None) -> str:
    start = request("POST", f"{GRAPH}/{acc.page_id}/video_reels",
                    {"upload_phase": "start", "access_token": acc.page_token})
    vid = start["video_id"]
    upload_url = start.get("upload_url") or f"{RUPLOAD}/video-upload/{GRAPH_VERSION}/{vid}"
    data = video.read_bytes()
    request("POST", upload_url, data=data, headers={
        "Authorization": f"OAuth {acc.page_token}", "offset": "0", "file_size": str(len(data))})
    finish = {"upload_phase": "finish", "video_id": vid, "video_state": "PUBLISHED",
              "description": caption, "access_token": acc.page_token}
    if title:
        finish["title"] = title
    request("POST", f"{GRAPH}/{acc.page_id}/video_reels", finish)

    def ready() -> bool:
        status = request("GET", f"{GRAPH}/{vid}", {"fields": "status", "access_token": acc.page_token})
        st = status.get("status", {})
        if st.get("video_status") == "error":
            raise ProcessingFailed(f"Facebook processing error: {json.dumps(st)[:300]}")
        publishing = (st.get("publishing_phase") or {}).get("status")
        return st.get("video_status") == "ready" or publishing == "complete"

    # The finish call publishes; waiting for processing only confirms it.
    best_effort("Facebook processing check", lambda: wait_until(ready, "Facebook"), None)
    return f"https://www.facebook.com/reel/{vid}"


def post_threads(acc: Accounts, video_name: str, text: str) -> str:
    if not acc.threads_token:
        raise MetaError("THREADS_TOKEN is not set")
    video_url = MEDIA_BASE_URL + urllib.parse.quote(video_name)
    container = request("POST", f"{THREADS}/me/threads",
                        {"media_type": "VIDEO", "video_url": video_url, "text": text,
                         "access_token": acc.threads_token})
    cid = container["id"]

    def ready() -> bool:
        status = request("GET", f"{THREADS}/{cid}", {"fields": "status,error_message",
                                                     "access_token": acc.threads_token})
        if status.get("status") in ("ERROR", "EXPIRED"):
            raise MetaError(f"Threads processing {status.get('status')}: {status.get('error_message')}")
        return status.get("status") == "FINISHED"

    wait_until(ready, "Threads")
    published = request("POST", f"{THREADS}/me/threads_publish",
                        {"creation_id": cid, "access_token": acc.threads_token})
    post_id = published["id"]
    return best_effort("Threads permalink", lambda: request(
        "GET", f"{THREADS}/{post_id}", {"fields": "permalink", "access_token": acc.threads_token}
    ).get("permalink") or post_id, post_id)


# ---------- Queue and copy rules ----------

RULES = [
    (re.compile(r"\bAI\b"), 'the word "AI"'),
    (re.compile(r"flyover", re.I), '"Flyover" (say "replay in 3D")'),
    (re.compile(r"!"), "an exclamation mark"),
    (re.compile("—"), "an em dash"),
    (re.compile(r"(\d[\d.,\s]*\s?(Ft|HUF|EUR|USD|€|\$))|([€$]\s?\d)", re.I), "a price"),
    (re.compile(r"companion", re.I), '"companion"'),
]


def caption_for(post: dict, platform: str) -> str:
    return (post.get(f"{platform}_caption") or post.get("caption") or "").strip()


def problems(post: dict, data_dir: Path) -> list[str]:
    found = []
    for key in ("id", "at", "video"):
        if not post.get(key):
            found.append(f"missing {key}")
    video = data_dir / "media" / post.get("video", "")
    if post.get("video") and not video.is_file():
        found.append(f"video media/{post['video']} not found")
    elif post.get("video") and "threads" in post.get("platforms", PLATFORMS) \
            and video.stat().st_size > THREADS_MAX_BYTES:
        found.append("video over 20 MB, too big for the Threads link (re-encode it)")
    try:
        when(post)
    except (KeyError, ValueError):
        found.append(f"bad time {post.get('at')!r} (use 2026-11-24T18:30:00+01:00)")
    for platform in post.get("platforms", PLATFORMS):
        if platform not in PLATFORMS:
            found.append(f"unknown platform {platform}")
            continue
        text = caption_for(post, platform)
        if not text:
            found.append(f"{platform}: empty caption")
        if len(text) > CAPTION_MAX[platform]:
            found.append(f"{platform}: caption {len(text)} chars, max {CAPTION_MAX[platform]}")
        for pattern, label in RULES:
            if pattern.search(text):
                found.append(f"{platform}: caption has {label}")
    return found


def when(post: dict) -> dt.datetime:
    moment = dt.datetime.fromisoformat(post["at"])
    if moment.tzinfo is None:
        raise ValueError("time zone missing")
    return moment


def load_json(path: Path, default):
    return json.loads(path.read_text()) if path.exists() else default


def save_json(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


# ---------- Modes ----------

def run_post(data_dir: Path, dry_run: bool, only: str | None) -> int:
    queue = load_json(data_dir / "queue.json", {"posts": []})["posts"]
    log_path = data_dir / "posted.json"
    log = load_json(log_path, {})
    now = dt.datetime.now(dt.timezone.utc)
    acc = Accounts(os.environ.get("META_TOKEN"), os.environ.get("THREADS_TOKEN"))
    failures = 0
    loaded = False
    for post in queue:
        if only and post.get("id") != only:
            continue
        if post.get("hold"):
            continue
        pid = post.get("id", "?")
        entry = log.setdefault(pid, {})
        todo = [p for p in post.get("platforms", PLATFORMS)
                if p not in entry or (entry[p].get("status") == "failed" and entry[p].get("tries", 0) < MAX_TRIES)]
        if not todo:
            continue
        issues = problems(post, data_dir)
        sig = hashlib.sha1(json.dumps(post, sort_keys=True).encode()).hexdigest()[:12]
        if issues:
            print(f"[{pid}] BLOCKED: " + "; ".join(issues))
            if entry.get("_blocked") != sig:  # report once per version of the post
                entry["_blocked"] = sig
                failures += 1
                if not dry_run:
                    save_json(log_path, log)
            continue
        entry.pop("_blocked", None)
        due = when(post)
        if not only and due > now:
            continue
        if not only and now - due > LATE_LIMIT:
            for platform in todo:
                entry[platform] = {"status": "missed", "at": now.isoformat(timespec="seconds")}
            print(f"[{pid}] missed (due {due.isoformat()}), not posting late")
            save_json(log_path, log)
            continue
        video = data_dir / "media" / post["video"]
        for platform in todo:
            if dry_run:
                print(f"[{pid}] would post to {platform}: {caption_for(post, platform)[:80]!r}")
                continue
            if not loaded and platform in ("instagram", "facebook"):
                acc.load_meta()
                loaded = True
            try:
                if platform == "instagram":
                    link = post_instagram(acc, video, caption_for(post, platform), post.get("cover_ms"))
                elif platform == "facebook":
                    link = post_facebook(acc, video, caption_for(post, platform), post.get("title"))
                else:
                    link = post_threads(acc, post["video"], caption_for(post, platform))
            except (MetaError, KeyError) as err:
                message = _redact(str(err))
                tries = entry.get(platform, {}).get("tries", 0) + 1
                entry[platform] = {"status": "failed", "tries": tries, "error": message[:300]}
                save_json(log_path, log)
                print(f"[{pid}] {platform} FAILED (try {tries} of {MAX_TRIES}): {message}")
                failures += 1
                continue
            entry[platform] = {"status": "posted", "link": link,
                               "at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")}
            save_json(log_path, log)  # after every platform, so a crash never double-posts
            print(f"[{pid}] {platform} posted: {link}")
    if not dry_run:
        save_json(log_path, {k: v for k, v in log.items() if v})
    return 1 if failures else 0


def run_check(data_dir: Path) -> int:
    ok = True
    acc = Accounts(os.environ.get("META_TOKEN"), os.environ.get("THREADS_TOKEN"))
    try:
        acc.load_meta()
        limit = request("GET", f"{GRAPH}/{acc.ig_id}/content_publishing_limit",
                        {"fields": "quota_usage,config", "access_token": acc.meta_token})
        print(f"Instagram publishing limit: {json.dumps(limit.get('data', limit))[:200]}")
    except MetaError as err:
        ok = False
        print(f"Facebook/Instagram: {err}")
    try:
        if not acc.threads_token:
            raise MetaError("THREADS_TOKEN is not set")
        me = request("GET", f"{THREADS}/me", {"fields": "id,username", "access_token": acc.threads_token})
        print(f"Threads @{me.get('username')} ({me.get('id')})")
    except MetaError as err:
        ok = False
        print(f"Threads: {err}")
    queue = load_json(data_dir / "queue.json", {"posts": []})["posts"]
    for post in queue:
        issues = problems(post, data_dir)
        print(f"[{post.get('id')}] {post.get('at')} " + ("OK" if not issues else "; ".join(issues)))
        ok = ok and not issues
    return 0 if ok else 1


def stamp_of(value: str | None) -> dt.datetime:
    """Meta times look like 2026-11-17T18:00:00+0000. A missing one counts as old."""
    if not value:
        return dt.datetime.min.replace(tzinfo=dt.timezone.utc)
    return dt.datetime.fromisoformat(re.sub(r"([+-]\d\d)(\d\d)$", r"\1:\2", value))


def run_comments(data_dir: Path) -> int:
    since = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=14)
    acc = Accounts(os.environ.get("META_TOKEN"), os.environ.get("THREADS_TOKEN"))
    acc.load_meta()
    seen_path = data_dir / "comments" / "seen.json"
    seen = set(load_json(seen_path, []))
    lines: list[str] = []

    def add(platform: str, link: str, who: str, text: str, cid: str) -> None:
        if cid in seen:
            return
        seen.add(cid)
        lines.append(f"- **{platform}** {who}: {text.strip()}  \n  on {link} (id {cid})")

    def safely(platform: str, fetch) -> None:
        try:
            fetch()
        except (MetaError, KeyError, ValueError) as err:
            lines.append(f"- **{platform}** could not be read: {_redact(str(err))[:200]}")

    def instagram() -> None:
        media = request("GET", f"{GRAPH}/{acc.ig_id}/media",
                        {"fields": "id,permalink,comments{id,username,text,timestamp}",
                         "limit": "25", "access_token": acc.meta_token}).get("data", [])
        for item in media:
            for c in (item.get("comments") or {}).get("data", []):
                if c.get("username") != "aerahealthapp" and stamp_of(c.get("timestamp")) > since:
                    add("Instagram", item.get("permalink", item["id"]), "@" + c.get("username", "?"),
                        c.get("text", ""), c["id"])

    def facebook() -> None:
        reels = request("GET", f"{GRAPH}/{acc.page_id}/video_reels",
                        {"fields": "id,permalink_url", "access_token": acc.page_token}).get("data", [])
        for item in reels[:25]:
            comments = request("GET", f"{GRAPH}/{item['id']}/comments",
                               {"fields": "id,from,message,created_time",
                                "access_token": acc.page_token}).get("data", [])
            for c in comments:
                who = (c.get("from") or {}).get("name", "someone")
                if who != "Aera Health" and stamp_of(c.get("created_time")) > since:
                    link = item.get("permalink_url") or item["id"]
                    if link.startswith("/"):
                        link = "https://www.facebook.com" + link
                    add("Facebook", link, who, c.get("message", ""), c["id"])

    def threads() -> None:
        posts = request("GET", f"{THREADS}/me/threads", {"fields": "id,permalink", "limit": "25",
                                                          "access_token": acc.threads_token}).get("data", [])
        for item in posts:
            replies = request("GET", f"{THREADS}/{item['id']}/replies",
                              {"fields": "id,username,text,timestamp",
                               "access_token": acc.threads_token}).get("data", [])
            for r in replies:
                if r.get("username") != "aerahealthapp" and stamp_of(r.get("timestamp")) > since:
                    add("Threads", item.get("permalink", item["id"]), "@" + r.get("username", "?"),
                        r.get("text", ""), r["id"])

    safely("Instagram", instagram)
    safely("Facebook", facebook)
    if acc.threads_token:
        safely("Threads", threads)
    out_dir = data_dir / "comments"
    out_dir.mkdir(exist_ok=True)
    save_json(seen_path, sorted(seen))
    if lines:
        day = dt.date.today().isoformat()
        path = out_dir / f"{day}.md"
        header = f"# New comments, {day}\n\n" if not path.exists() else "\n"
        with path.open("a") as fh:
            fh.write(header + "\n".join(lines) + "\n")
    print(f"{len(lines)} new comments")
    return 0


def run_threads_token() -> int:
    token = os.environ.get("THREADS_TOKEN")
    if not token:
        print("THREADS_TOKEN is not set")
        return 1
    fresh = request("GET", "https://graph.threads.net/refresh_access_token",
                    {"grant_type": "th_refresh_token", "access_token": token})
    days = int(fresh.get("expires_in", 0)) // 86400
    print(f"Threads token refreshed, {days} days left")
    if fresh.get("access_token") and fresh["access_token"] != token:
        print("Meta returned a NEW Threads token. Generate one in the app and save it as THREADS_TOKEN.")
        return 1
    return 0 if days > 10 else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("mode", choices=["post", "check", "comments", "threads-token"])
    parser.add_argument("--data", default="social", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--only", help="post this queue id now, ignoring its time")
    args = parser.parse_args()
    try:
        if args.mode == "post":
            return run_post(args.data, args.dry_run, args.only)
        if args.mode == "check":
            return run_check(args.data)
        if args.mode == "comments":
            return run_comments(args.data)
        return run_threads_token()
    except MetaError as err:
        print(_redact(str(err)))
        return 1


if __name__ == "__main__":
    sys.exit(main())
