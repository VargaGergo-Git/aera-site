"""Tag every App Store link on the static pages with Apple's campaign fields.

The home pages and their get/ forwarding pages are tagged by build_home.py.
This does the rest (guides, tools, the Flyover page, press, the s/ share
pages): each store link in an href, a meta refresh or a location.replace
gets ?pt=<APPSTORE_PT>&ct=<page>&mt=8, so App Store Connect > App Analytics
> Campaigns shows which page sent the install. Structured data (downloadUrl,
sameAs) stays untagged. Idempotent; re-run after adding or rebuilding a page.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from build_home import APPSTORE_PT, ROOT  # noqa: E402

HOME = {"index.html", "hu.html", "de.html"}
SKIP_DIRS = {".git", "get", "scenes", "shots", "assets", "img", "scripts"}
LINK = re.compile(r'(href="|url=|replace\(")(https://apps\.apple\.com/(?:[a-z]{2}/)?app/id6762456252)(\?[^"\s<]*)?')


def short(prefix, slug):
    """prefix-slug in at most 40 characters, cut at a word."""
    out = prefix
    for w in slug.split("-"):
        if len(out) + 1 + len(w) > 40:
            break
        out += "-" + w
    return out


def ct_for(rel):
    parts = rel[:-5].split("/")  # drop .html
    if parts[0] == "guides":
        return short("guide", parts[1])
    if parts[0] == "tools":
        return short("tool", parts[1])
    if parts[0] == "s":
        return short("share", parts[1])
    if parts[0] == "press":
        return "press-kit"
    return short("page", "-".join(p for p in parts if p != "index"))


def main():
    seen, changed = {}, 0
    for d, dirs, files in os.walk(ROOT):
        dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
        for f in files:
            if not f.endswith(".html") or (d == ROOT and f in HOME):
                continue
            path = os.path.join(d, f)
            s = open(path, encoding="utf-8").read()
            if not LINK.search(s):
                continue
            rel = os.path.relpath(path, ROOT)
            ct = ct_for(rel)
            assert re.fullmatch(r"[a-z0-9-]{1,40}", ct), (rel, ct)
            assert seen.setdefault(ct, rel) == rel, ("ct used twice", ct, seen[ct], rel)

            def tag(m):
                if not APPSTORE_PT:
                    return m.group(1) + m.group(2)
                amp = "&" if m.group(1).startswith("replace") else "&amp;"
                return m.group(1) + m.group(2) + "?pt=%s%sct=%s%smt=8" % (APPSTORE_PT, amp, ct, amp)
            new = LINK.sub(tag, s)
            if new != s:
                open(path, "w", encoding="utf-8").write(new)
                changed += 1
    for ct, rel in sorted(seen.items()):
        print("%-42s %s" % (ct, rel))
    print("tagged %d pages" % changed)


if __name__ == "__main__":
    main()
