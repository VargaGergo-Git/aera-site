"""Shared building blocks for article topics (see build_articles.py)."""

def keys(items):
    return '<ul class="keys">' + "".join(f"<li><b>{b}</b>{t}<small>{s}</small></li>" for b, t, s in items) + "</ul>"

def shot(img, alt, head, body, w=740, h=335):
    return (f'<div class="shot"><div class="frame"><picture>'
            f'<source srcset="../assets/article/{img}-dark.webp" media="(prefers-color-scheme: dark)">'
            f'<img src="../assets/article/{img}-light.webp" alt="{alt}" width="{w}" height="{h}" loading="lazy" decoding="async">'
            f'</picture></div><p><b>{head}</b>{body}</p></div>')


def pull(text):
    return f'<blockquote class="pull">{text}</blockquote>'
