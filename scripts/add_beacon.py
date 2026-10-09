"""Put the Cloudflare Web Analytics beacon on every static page of the site.

The home pages (index, hu, de) get it from build_home.py. This adds the same
tag before </head> on every other .html page (privacy, support, terms, notes,
guides, tools), once. Re-run after adding a page. With CF_BEACON empty it
removes the tag instead, so analytics can be switched off in one place.
Cookieless: no banner needed, no personal data stored.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from build_home import CF_BEACON, ROOT  # noqa: E402

HOME = {"index.html", "hu.html", "de.html"}
SKIP_DIRS = {".git", "scenes", "shots", "assets", "img", "scripts"}
TAG = re.compile(r'\n?<script defer src="https://static\.cloudflareinsights\.com/beacon\.min\.js"[^>]*></script>')


def beacon():
    return ('<script defer src="https://static.cloudflareinsights.com/beacon.min.js" '
            "data-cf-beacon='{\"token\": \"%s\"}'></script>" % CF_BEACON)


def main():
    changed = 0
    for d, dirs, files in os.walk(ROOT):
        dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
        for f in files:
            if not f.endswith(".html") or (d == ROOT and f in HOME):
                continue
            path = os.path.join(d, f)
            s = open(path, encoding="utf-8").read()
            if "</head>" not in s:
                continue
            new = TAG.sub("", s)
            if CF_BEACON:
                new = new.replace("</head>", beacon() + "\n</head>", 1)
            if new != s:
                open(path, "w", encoding="utf-8").write(new)
                changed += 1
    print("beacon %s on %d pages" % ("set" if CF_BEACON else "removed", changed))


if __name__ == "__main__":
    main()
