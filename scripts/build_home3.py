#!/usr/bin/env python3
"""The home page (index.html, hu.html, de.html), take 3 of the 3.4 site.

    python3 scripts/build_home3.py

The page itself is scripts/home3/page-en.html, the approved mock as it was
published (8 Nov 2026, v12). scripts/home3/words.py holds every Hungarian and
German line as an exact swap of the English one, and stops if an English line
it expects is gone. This builder then puts the live site's own parts around it:

- the head of each language (title, description, social cards, canonical,
  hreflang, schema, the /#privacy redirect): scripts/home3/head-<lang>.html
- the questions with their answers, which the FAQ schema in that head repeats:
  scripts/home3/faq-<lang>.html
- tracked store links (/get/<place>/<lang>/), real footer links, and the
  Cloudflare beacon (cookieless).

Pictures live in h/ (h/hu/, h/de/ for the ones with words in them). The opening's
replay is h/film.mp4 with its last frame h/film.webp (the app's own recording of the
Budapest run, its words blurred out so the page can draw them in each language).
The carousel's store pictures are h/store/lNN.webp, h/store/hu/, h/store/de/.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(HERE, "home3")
sys.path.insert(0, SRC)
sys.path.insert(0, HERE)
import words  # noqa: E402
import lines  # noqa: E402
import chrome  # noqa: E402
from build_home import CF_BEACON  # noqa: E402

FILES = {"en": "index.html", "hu": "hu.html", "de": "de.html"}

NEWS = {"en": "whats-new.html", "hu": "ujdonsagok.html", "de": "neuigkeiten.html"}

FAQ_CSS = """
/* Questions: the live site's answers, in this page's look. */
.faq-sec{padding:0 0 clamp(72px,9vw,112px);background:var(--paper)}
.faq-sec .qa-grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,2fr);gap:24px 56px;align-items:start}
.faq-sec h2{font-size:clamp(40px,5.6vw,64px);font-weight:700;letter-spacing:-.035em;line-height:1.04;margin:0}
.faq-sec .faq{border-top:1px solid var(--rule)}
.faq-sec details{border-bottom:1px solid var(--rule)}
.faq-sec summary{list-style:none;display:flex;justify-content:space-between;align-items:center;gap:20px;min-height:44px;padding:20px 0;cursor:pointer;-webkit-tap-highlight-color:transparent}
.faq-sec summary::-webkit-details-marker{display:none}
.faq-sec summary h3{margin:0;font-size:clamp(18px,1.9vw,21px);font-weight:600;letter-spacing:-.012em;line-height:1.3;color:var(--ink)}
.faq-sec summary i{flex:none;position:relative;width:14px;height:14px}
.faq-sec summary i::before,.faq-sec summary i::after{content:"";position:absolute;left:0;top:6px;width:14px;height:2px;border-radius:1px;background:var(--ink-2);transition:transform .3s cubic-bezier(.22,1,.36,1)}
.faq-sec summary i::after{transform:rotate(90deg)}
.faq-sec details[open] summary i::after{transform:rotate(0deg)}
.faq-sec details p{margin:0 0 24px;max-width:44em;font-size:17px;line-height:1.5;color:var(--ink-2)}
@media (hover:hover){.faq-sec summary:hover h3{color:var(--accent)}}
@media (max-width:860px){.faq-sec .qa-grid{grid-template-columns:1fr}}
@media (prefers-reduced-motion:reduce){.faq-sec summary i::before,.faq-sec summary i::after{transition:none}}
"""


def page(lang, src):
    out = src
    for key, val in lines.C[lang].items():
        out = out.replace("{{%s}}" % key, val)
    # The carousel: that language's store pictures, in that store's order.
    folder = "s/store/" if lang == "en" else "s/store/%s/" % lang
    deck = "".join('<figure class="cd"><img src="%sl%02d.webp" alt="%s" width="600" height="1304" loading="lazy" draggable="false"></figure>'
                   % (folder, i + 1, alt.replace('"', "&quot;")) for i, alt in enumerate(lines.STORE[lang]))
    if out.count("<!--deck-->") != 1:
        sys.exit("the carousel's slot is gone from page-en.html")
    out = out.replace("<!--deck-->", deck)
    left = re.search(r"\{\{\w+\}\}", out)
    if left:
        sys.exit("%s: no words for %s" % (lang, left.group(0)))
    if lang != "en":
        col = 1 if lang == "hu" else 2
        for row in words.T:
            en, tr = row[0], row[col]
            if en not in out:
                sys.exit("%s: English line not found (changed?): %s" % (lang, en[:90]))
            out = out.replace(en, tr)
        for p in words.PICS:
            out = out.replace('src="s/%s.webp"' % p, 'src="s/%s/%s.webp"' % (lang, p))

    # Head: the live page's own, then the page's look with the shared tokens and chrome.
    cut = out.index("<!--chrome:header-->")
    look, body = out[:cut], out[cut:]
    look = re.sub(r"<title>.*?</title>\n?", "", look)
    look = re.sub(r'<meta name="(claude:viewport-fit-sides|viewport|color-scheme)"[^>]*>\n?', "", look)
    look = look.replace("/*chrome:css*/", chrome.CSS.strip(), 1)
    look = look.replace("</style>", FAQ_CSS + "</style>", 1)
    head = open(os.path.join(SRC, "head-%s.html" % lang), encoding="utf-8").read()

    # The shared header, badge, closing band and footer; store links counted by place.
    alts = dict((c, h) for c, _, _, h in chrome.LANGS)
    get = lambda place: "/get/%s/%s/" % (place, lang)
    body = body.replace("<!--chrome:header-->", chrome.header(lang, alts, get("nav"), home=True), 1)
    body = body.replace("<!--chrome:badge-->", chrome.badge(lang, get("hero")), 1)
    body = body.replace("<!--chrome:closing-->", "<!--closing-->" + chrome.closing(lang, get("closing")), 1)
    body = body.replace("<!--chrome:footer-->", chrome.footer(lang, alts), 1)
    n = body.count('href="https://apps.apple.com/app/id6762456252"')
    if n != 1:
        sys.exit("%s: expected the one store link of the picture strip, found %d" % (lang, n))
    body = body.replace('href="https://apps.apple.com/app/id6762456252"', 'href="%s"' % get("shelf"))
    if "<!--chrome:" in body:
        sys.exit("%s: a chrome slot was left unfilled" % lang)

    # Release notes link, then the questions above the closing band.
    body = body.replace('<a class="link" href="#new">', '<a class="link" href="%s">' % NEWS[lang], 1)
    faq = open(os.path.join(SRC, "faq-%s.html" % lang), encoding="utf-8").read()
    faq = faq.replace('<section class="faq-sec">', '<section class="faq-sec" id="faq">', 1)
    faq = faq.replace('class="wide qa-grid"', 'class="w qa-grid"').replace(' class="reveal"', "").replace("faq reveal", "faq")
    body = body.replace("<!--closing-->", faq, 1)

    # Pictures live in h/.
    body = re.sub(r'(["\'`(])s/', r"\1h/", body)
    look = re.sub(r'(["\'`(])s/', r"\1h/", look)

    beacon = ('<script defer src="https://static.cloudflareinsights.com/beacon.min.js" '
              "data-cf-beacon='{\"token\": \"%s\"}'></script>\n" % CF_BEACON) if CF_BEACON else ""
    html = ('<!DOCTYPE html>\n<html lang="%s">\n<head>\n%s%s\n%s\n</head>\n<body>\n%s\n%s\n%s</body>\n</html>\n'
            % (lang, head, chrome.LOOK_HEAD_JS, look.strip(), body.strip(), chrome.JS, beacon))

    for bad in ("—", 'href="https://apps.apple.com', "fonts.googleapis", "{{"):
        if bad in (html if bad == "—" else body):
            sys.exit("%s: left in the page: %s" % (lang, bad))
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", body, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    if lang != "en":
        for word in ("Replay your", "Understand", "Download on", "Free to start", "Your body", "What’s new",
                     "Works with", "usual", "Heartbeats", "One minute", "Last night", "Blood pressure",
                     "Body age", "Out the door", "No account", "Route planner", "Fastest", "Private"):
            if word in text:
                sys.exit("%s: English left on the page: %s" % (lang, word))
    return html


def main():
    src = open(os.path.join(SRC, "page-en.html"), encoding="utf-8").read()
    for lang, name in FILES.items():
        out = page(lang, src)
        with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
            f.write(out)
        print(name, len(out) // 1024, "KB")


if __name__ == "__main__":
    main()
