#!/usr/bin/env python3
"""Give guide pages the article layout: article.css + article.js, key-number cards,
an explanatory figure and a real app shot. Idempotent: injected blocks sit between
<!--art:NAME--> markers and are replaced on each run. Edit ARTICLES and re-run.
"""
import pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import importlib

ROOT = pathlib.Path(__file__).resolve().parent.parent


# Each module in scripts/article_topics/ defines ARTICLES = {file: (lang, [(where, name, html)])}.
ARTICLES = {}
sys.path.insert(0, str(pathlib.Path(__file__).parent / "article_topics"))
for mod in sorted((pathlib.Path(__file__).parent / "article_topics").glob("*.py")):
    ARTICLES.update(importlib.import_module(mod.stem).ARTICLES)


def mark(name, html):
    return f"<!--art:{name}-->{html}<!--/art:{name}-->"


def apply(fn, lang, blocks):
    p = ROOT / "guides" / fn
    s = p.read_text(encoding="utf-8")
    s = re.sub(r"<!--art:(\w+)-->.*?<!--/art:\1-->\n?", "", s, flags=re.S)
    s = s.replace('<link rel="stylesheet" href="../styles.css">', '<link rel="stylesheet" href="../article.css">')
    if "article.js" not in s:
        s = s.replace("</body>", '<script src="../article.js" defer></script>\n</body>')
    body_start = s.index('<div class="wrap legal">')
    h2s = [m.start() for m in re.finditer(r"\n<h2>", s) if m.start() > body_start]
    for where, name, html in blocks:
        block = mark(name, html) + "\n"
        if where == "lead":
            i = s.index("</p>", body_start) + len("</p>\n")
        elif where.startswith("h2:"):
            k = int(where[3:])
            h = s.index("\n<h2>", body_start)
            for _ in range(k):
                h = s.index("\n<h2>", h + 1)
            i = s.index("</p>", h) + len("</p>\n")
        elif where == "aera":
            h = s.index('<div class="note">', body_start)
            i = h
        s = s[:i] + block + s[i:]
    p.write_text(s, encoding="utf-8")
    print("built", fn)


if __name__ == "__main__":
    only = sys.argv[1:]
    for fn, (lang, blocks) in ARTICLES.items():
        if only and fn not in only:
            continue
        apply(fn, lang, blocks)
