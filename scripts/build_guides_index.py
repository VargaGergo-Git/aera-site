#!/usr/bin/env python3
"""Write guides/index.html from the guide pages themselves and keep sitemap.xml in step.

Reads each guides/*.html for its lang, <h1>, meta description and canonical, groups
them by language, and writes one light hub page (styles.css only, no JS). Then adds
any guide URL missing from sitemap.xml. Re-run after adding or renaming a guide.
"""
import html, pathlib, re, datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
GUIDES = ROOT / "guides"
BASE = "https://aerahealth.app"
BEACON = """<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{"token": "4fc0403d67364f1ab92526387bdd0b81"}'></script>"""
LANGS = [("en", "English"), ("hu", "Magyar"), ("de", "Deutsch")]


def read(p):
    s = p.read_text(encoding="utf-8")
    lang = re.search(r'<html lang="([a-z-]+)"', s).group(1)
    h1 = html.unescape(re.sub(r"<[^>]+>", "", re.search(r"<h1>(.*?)</h1>", s, re.S).group(1))).strip()
    desc = html.unescape(re.search(r'<meta name="description" content="([^"]*)"', s).group(1))
    canon = re.search(r'<link rel="canonical" href="([^"]+)"', s).group(1)
    mod = re.search(r'"dateModified": "([0-9-]+)"', s)
    return dict(file=p.name, lang=lang, h1=h1, desc=desc, canon=canon, mod=mod.group(1) if mod else None)


def main():
    pages = [read(p) for p in sorted(GUIDES.glob("*.html")) if p.name != "index.html"]
    sections, items_ld = [], []
    for code, label in LANGS:
        group = [g for g in pages if g["lang"] == code]
        if not group:
            continue
        lis = "\n".join(
            f'    <li><a href="{g["file"]}" hreflang="{code}" lang="{code}">{html.escape(g["h1"])}</a>'
            f'<br><span class="meta" lang="{code}">{html.escape(g["desc"])}</span></li>'
            for g in group
        )
        sections.append(f'  <h2 id="{code}" lang="{code}">{label}</h2>\n  <ul class="note-list">\n{lis}\n  </ul>')
        items_ld += [g["canon"] for g in group]
    ld = ",".join(
        f'{{"@type":"ListItem","position":{i + 1},"url":"{u}"}}' for i, u in enumerate(items_ld)
    )
    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="apple-itunes-app" content="app-id=6762456252">
<title>Running, sleep and Apple Watch guides | Aera</title>
<meta name="description" content="Plain answers to the questions runners and Apple Watch owners search for: sleep, HRV, routes and replays, with the research and the limits left in.">
<meta property="og:title" content="Aera guides">
<meta property="og:description" content="Plain answers on sleep, HRV, running routes and Apple Watch, with the research and the limits left in.">
<meta property="og:type" content="website">
<meta property="og:image" content="{BASE}/assets/icon.png">
<link rel="canonical" href="{BASE}/guides/">
<link rel="icon" href="../assets/icon.png">
<link rel="stylesheet" href="../styles.css">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"CollectionPage","name":"Aera guides","url":"{BASE}/guides/","publisher":{{"@type":"Organization","name":"Aera","url":"{BASE}/"}},"mainEntity":{{"@type":"ItemList","itemListElement":[{ld}]}}}}
</script>
{BEACON}
</head>
<body>
<div class="topbar"><div class="wrap">
  <a class="mark" href="../index.html">Aera</a>
  <nav class="topnav"><a href="index.html" aria-current="page">Guides</a><a href="../notes/index.html">Notes</a><a href="../support.html">Support</a></nav>
</div></div>
<div class="wrap page-head">
  <p class="eyebrow">Aera</p>
  <h1>Guides</h1>
</div>
<div class="wrap legal">
  <p>Plain answers to questions runners and Apple Watch owners ask, each with the research behind it and the point where a watch stops being reliable. For shorter pieces on single numbers, see the <a href="../notes/index.html">field notes</a>. For a quick distance sum, try <a href="../tools/how-far.html">how far will I run?</a></p>
{chr(10).join(sections)}
  <p><a class="btn btn-primary" href="https://apps.apple.com/app/id6762456252">Get Aera on the App Store</a></p>
</div>
<footer class="footer-base"><div class="wrap">
  <p class="meta">Aera is made by Gergő Varga. <a href="../index.html">About the app</a> · <a href="../support.html">Contact</a></p>
</div></footer>
</body>
</html>
"""
    (GUIDES / "index.html").write_text(page, encoding="utf-8")

    sm = ROOT / "sitemap.xml"
    s = sm.read_text(encoding="utf-8")
    today = datetime.date.today().isoformat()
    want = [f"{BASE}/guides/"] + [g["canon"] for g in pages]
    added = []
    for u in want:
        if f"<loc>{u}</loc>" not in s:
            s = s.replace("</urlset>", f"<url><loc>{u}</loc><lastmod>{today}</lastmod></url></urlset>")
            added.append(u)
    sm.write_text(s, encoding="utf-8")
    print(f"guides/index.html: {len(pages)} guides; sitemap added {len(added)}")
    for u in added:
        print("  +", u)


if __name__ == "__main__":
    main()
