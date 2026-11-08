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

Pictures live in h/ (h/hu/, h/de/ for the ones with words in them). The
store strip's layers (h/store/{t,d}NN.webp and h/field.webp) come from
scripts/home3/frames_web.js, run in the project's store-picture folder.
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
from build_home import CF_BEACON  # noqa: E402

FILES = {"en": "index.html", "hu": "hu.html", "de": "de.html"}

# Footer links that were placeholders in the mock, in the order they appear.
FOOT = {
    "en": ["plan/", "notes/index.html", "guides/index.html", "press/", "support.html", "privacy.html", "terms.html"],
    "hu": ["plan/", "notes/index.html", "guides/index.html#hu", "press/", "support.html", "adatvedelem.html", "felhasznalasi-feltetelek.html"],
    "de": ["plan/", "notes/index.html", "guides/index.html#de", "press/", "support.html", "privacy.html", "terms.html"],
}
NEWS = {"en": "whats-new.html", "hu": "ujdonsagok.html", "de": "neuigkeiten.html"}

FAQ_CSS = """
/* Questions: the live site's answers, in this page's look. */
.faq-sec{padding:clamp(80px,10vw,128px) 0;background:var(--paper)}
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
    if lang != "en":
        col = 1 if lang == "hu" else 2
        for row in words.T:
            en, tr = row[0], row[col]
            if en not in out:
                sys.exit("%s: English line not found (changed?): %s" % (lang, en[:90]))
            out = out.replace(en, tr)
        for p in words.PICS:
            out = out.replace('src="s/%s.webp"' % p, 'src="s/%s/%s.webp"' % (lang, p))
        out = out.replace('src="s/store/', 'src="s/store/%s/' % lang)

    # Head: the live page's own, then the page's look.
    cut = out.index('<header class="nav"')
    look, body = out[:cut], out[cut:]
    look = re.sub(r"<title>.*?</title>\n?", "", look)
    look = re.sub(r'<meta name="(claude:viewport-fit-sides|viewport)"[^>]*>\n?', "", look)
    look = re.sub(r'<link rel="(preconnect|stylesheet)" href="https://fonts\.[^>]*>\n?', "", look)
    look = look.replace("</style>", FAQ_CSS + "</style>", 1)
    head = open(os.path.join(SRC, "head-%s.html" % lang), encoding="utf-8").read()

    # Store links, each counted on its own.
    places = iter(["nav", "hero", "shelf", "closing"])
    body = re.sub(r'href="https://apps\.apple\.com/app/id6762456252"',
                  lambda m: 'href="/get/%s/%s/"' % (next(places), lang), body)
    if next(places, None) is not None:
        sys.exit("%s: a store link went missing" % lang)

    # Release notes link and footer.
    body = body.replace('<a class="link" href="#new">', '<a class="link" href="%s">' % NEWS[lang], 1)
    f = body.index("<footer")
    foot = body[f:]
    links = iter(FOOT[lang])
    foot = re.sub(r'(<li><a href=")#top(")', lambda m: m.group(1) + next(links) + m.group(2), foot)
    if next(links, None) is not None:
        sys.exit("%s: footer links changed" % lang)
    faq = open(os.path.join(SRC, "faq-%s.html" % lang), encoding="utf-8").read()
    faq = faq.replace('<section class="faq-sec">', '<section class="faq-sec" id="faq">', 1)
    faq = faq.replace('class="wide qa-grid"', 'class="w qa-grid"').replace(' class="reveal"', "").replace("faq reveal", "faq")
    closing = body.index('<section class="closing">')
    body = body[:closing] + faq + body[closing:f] + foot

    # Pictures live in h/.
    body = re.sub(r'(["\'`(])s/', r"\1h/", body)
    look = re.sub(r'(["\'`(])s/', r"\1h/", look)

    beacon = ('<script defer src="https://static.cloudflareinsights.com/beacon.min.js" '
              "data-cf-beacon='{\"token\": \"%s\"}'></script>\n" % CF_BEACON) if CF_BEACON else ""
    html = ('<!DOCTYPE html>\n<html lang="%s">\n<head>\n%s%s</head>\n<body>\n%s\n%s</body>\n</html>\n'
            % (lang, head, look.strip() + "\n", body.strip(), beacon))

    for bad in ("—", 'href="https://apps.apple.com', "fonts.googleapis", 'href="#top">Support'):
        if bad in (html if bad == "—" else body):
            sys.exit("%s: left in the page: %s" % (lang, bad))
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", body, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    if lang != "en":
        for word in ("Replay your", "Understand", "Download on", "Free to start", "Your body", "What’s new",
                     "Works with", "usual", "Heartbeats", "One minute", "Last night", "Blood pressure",
                     "Body age", "Out the door", "No account", "Route planner"):
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
