#!/usr/bin/env python3
"""Give every page the one Aera header, closing band and footer (scripts/chrome.py).

The home pages take them straight from build_home3.py. This does every other
page: guides, the Field Guide, support, privacy, what's new, press, the tools,
the route planner. For each page it

- replaces the old top bar with the shared header. Its three language links go
  to the page's own translations (its <link rel="alternate" hreflang> tags),
  or to that language's home page when there is none;
- replaces the old footer with the closing band (slogan, App Store badge, a code
  to scan on a computer) and the shared footer. Legal pages get the footer only,
  and the route planner, a full-screen map, gets none;
- puts the saved light or dark choice in <head> before the first paint, and the
  small script for the footer's look switch and the language card before </body>;
- makes sure the page links styles.css (guides link article.css on top of it),
  each with ?v=<hash> so a deploy never shows new pages with an old sheet.

It also copies the shared CSS from chrome.py into styles.css, between the two
chrome markers.

Everything sits between <!--chrome:x--> markers and is rebuilt on each run, so
it is safe to run again and again. Run it after any generator that writes
pages (build_articles.py, build_guides_index.py, build_whats_new.py,
build_requests.py), and before add_campaign.py, which tags the store links it
adds. It replaces the old add_lang.py.
"""
import hashlib
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
import chrome  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {".git", "scenes", "shots", "assets", "img", "scripts", "get", "hi", "media", "h", "worker",
             "s", "oauth", "integrations"}
HOME = {"index.html", "hu.html", "de.html"}
# Footer only: nobody wants a download band under a contract or on top of a map.
PLAIN = {"privacy.html", "terms.html", "adatvedelem.html", "felhasznalasi-feltetelek.html"}
# The route planner is a full-screen map: no footer under it, and no language card over it.
NO_FOOT = {"plan/index.html"}
NO_HINT = {"plan/index.html"}

ALT = re.compile(r'<link rel="alternate" hreflang="(en|hu|de)" href="https://aerahealth\.app([^"]*)">')
OLD_LSW = re.compile(r"<!--lsw-->.*?<!--/lsw-->\n?", re.S)
OLD_BAR = re.compile(r'<div class="topbar">\s*<div class="wrap(?:-wide)?">.*?</nav>\s*</div>\s*</div>', re.S)
OLD_FOOT = re.compile(r"<footer\b.*?</footer>", re.S)
SHEET = re.compile(r'(<link rel="stylesheet" href=")((?:\.\./)*)(styles|article)\.css(?:\?v=[0-9a-f]+)?(">)')


def block(name, inner):
    return "<!--chrome:%s-->%s<!--/chrome:%s-->" % (name, inner, name)


def find(name):
    return re.compile(r"<!--chrome:%s-->.*?<!--/chrome:%s-->" % (name, name), re.S)


def sync_css():
    """Copy the shared CSS into styles.css; return {sheet name: short hash}."""
    path = os.path.join(ROOT, "styles.css")
    s = open(path, encoding="utf-8").read()
    a, b = s.index("/* chrome:start */"), s.index("/* chrome:end */")
    new = s[:a] + "/* chrome:start */" + chrome.CSS + s[b:]
    if new != s:
        open(path, "w", encoding="utf-8").write(new)
    out = {}
    for name in ("styles", "article"):
        data = open(os.path.join(ROOT, name + ".css"), "rb").read()
        out[name] = hashlib.sha1(data).hexdigest()[:8]
    return out


def current_for(rel, lang):
    if rel.startswith("guides/"):
        return "/guides/"
    return "/" + rel


def process(path, rel, ver):
    s = open(path, encoding="utf-8").read()
    m = re.search(r'<html[^>]*\blang="(en|hu|de)"', s)
    if not m or "</head>" not in s or "</body>" not in s:
        return None
    lang = m.group(1)
    new = OLD_LSW.sub("", s)
    alts = dict(ALT.findall(new))
    head = block("header", chrome.header(lang, alts, chrome.STORE, current=current_for(rel, lang),
                                         has_alt=bool(alts), hint=rel not in NO_HINT))
    foot = block("footer", ("" if rel in PLAIN else chrome.closing(lang, chrome.STORE)) + chrome.footer(lang, alts))

    if find("header").search(new):
        new = find("header").sub(lambda _: head, new, 1)
    elif OLD_BAR.search(new):
        new = OLD_BAR.sub(lambda _: head, new, 1)
    else:
        return None  # not a page with the site's header: leave it alone
    if rel in NO_FOOT:
        new = find("footer").sub("", new)
    elif find("footer").search(new):
        new = find("footer").sub(lambda _: foot, new, 1)
    else:
        feet = list(OLD_FOOT.finditer(new))
        if feet:
            last = feet[-1]
            new = new[:last.start()] + foot + new[last.end():]
        else:
            b = new.rfind("</body>")
            new = new[:b] + foot + "\n" + new[b:]

    # <head>: the saved look before the first paint, and the sheets with their hash.
    new = re.sub(r"<!--chrome:head-->.*?<!--/chrome:head-->\n?", "", new, flags=re.S)
    depth = "../" * rel.count("/")
    if not re.search(r'href="(?:\.\./)*styles\.css', new):
        new = re.sub(r'(<link rel="stylesheet" href="(?:\.\./)*article\.css)',
                     '<link rel="stylesheet" href="%sstyles.css">\n\\1' % depth, new, count=1)
    new = SHEET.sub(lambda k: "%s%s%s.css?v=%s%s" % (k.group(1), k.group(2), k.group(3), ver[k.group(3)], k.group(4)), new)
    first = re.search(r'<link rel="stylesheet"', new)
    if not first:
        return None
    new = new[:first.start()] + block("head", chrome.LOOK_HEAD_JS) + "\n" + new[first.start():]

    new = re.sub(r"<!--chrome:js-->.*?<!--/chrome:js-->\n?", "", new, flags=re.S)
    b = new.rfind("</body>")
    new = new[:b] + block("js", chrome.JS) + "\n" + new[b:]

    # Older pages set dark text on the old amber button in their own <style>.
    new = re.sub(r"color:\s*#17120a", "color:var(--btn-ink)", new)
    if new != s:
        open(path, "w", encoding="utf-8").write(new)
        return True
    return False


def main():
    ver = sync_css()
    done = changed = 0
    left = []
    for d, dirs, files in os.walk(ROOT):
        dirs[:] = sorted(x for x in dirs if x not in SKIP_DIRS)
        for f in sorted(files):
            if not f.endswith(".html") or (d == ROOT and f in HOME):
                continue
            path = os.path.join(d, f)
            rel = os.path.relpath(path, ROOT)
            r = process(path, rel, ver)
            if r is None:
                left.append(rel)
            else:
                done += 1
                changed += bool(r)
    print("chrome: %d pages carry the shared header and footer, %d rewritten" % (done, changed))
    if left:
        print("left alone (no site header): " + ", ".join(left))


if __name__ == "__main__":
    main()
