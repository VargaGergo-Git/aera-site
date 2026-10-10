#!/usr/bin/env python3
"""Trackable outreach links: hi/<channel>/<lang>/ and get/<channel>/<lang>/.

    python3 scripts/build_outreach_links.py

Letters, club posts and directory listings link to these paths instead of the bare
homepage or store, so Cloudflare Web Analytics (which drops query strings and sees no
referrer from mail apps) counts each channel as its own path. Channels live in
scripts/outreach_links.json. Both page kinds wait for the beacon like get/<place>/.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from build_home import COPY, CF_BEACON, ROOT, get_page  # noqa: E402

HOME = {"en": "/", "hu": "/hu.html", "de": "/de.html"}


def hi_page(lang, url):
    beacon = ('<script defer src="https://static.cloudflareinsights.com/beacon.min.js" '
              "data-cf-beacon='{\"token\": \"%s\"}'></script>" % CF_BEACON) if CF_BEACON else ""
    return """<!doctype html>
<html lang="%(lang)s"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Aera</title>
<meta http-equiv="refresh" content="2; url=%(url)s">
<script>
// Let the Cloudflare beacon count this path first; go anyway at 1.5 s.
(function () {
  var go = function () { location.replace(%(js)s); };
  addEventListener('load', function () { setTimeout(go, 400); });
  setTimeout(go, 1500);
})();
</script>
<style>body{margin:0;min-height:100vh;display:grid;place-items:center;font:17px/1.4 -apple-system,system-ui,sans-serif;background:#f6f4ef;color:#1c1c1e}@media (prefers-color-scheme:dark){body{background:#0b0b0c;color:#f2f2f2}}a{color:inherit}</style>
%(beacon)s
</head><body><p><a href="%(url)s">Aera</a></p></body></html>
""" % {"lang": lang, "url": url, "js": json.dumps(url), "beacon": beacon}


def main():
    channels = json.load(open(os.path.join(ROOT, "scripts", "outreach_links.json")))["channels"]
    n = 0
    for ch in channels:
        if not re.fullmatch(r"[a-z0-9-]+", ch):
            raise SystemExit("bad channel name: %r" % ch)
        for c in COPY.values():
            lang = c["lang"]
            for kind, body in (("hi", hi_page(lang, HOME[lang])), ("get", get_page(c["store"], lang, ch))):
                d = os.path.join(ROOT, kind, ch, lang)
                os.makedirs(d, exist_ok=True)
                with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
                    f.write(body)
                n += 1
    print(n, "pages for", len(channels), "channels")


if __name__ == "__main__":
    main()
