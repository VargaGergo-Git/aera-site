#!/usr/bin/env python3
"""Figures for the article pages: small inline SVG diagrams, text in each language.

Each figure is illustrative (example data, labelled so), drawn with CSS classes
from article.css so it follows light and dark mode.
"""
import math, statistics

T = {
    "hrv_band": {
        "en": dict(title="One low night is noise. A low week is a signal.", y="HRV (ms)", band="your usual range", avg="7-night average",
                   one="one low night", week="a week below your usual", nights="nights", cap="<b>Illustration with example nights.</b> Dots are single nights; the shaded band is this person's own usual range from earlier weeks; the green line is a 7-night rolling average, the way Plews and colleagues (2013) suggest reading HRV."),
        "hu": dict(title="Egy rossz éjszaka zaj. Egy rossz hét jelzés.", y="HRV (ms)", band="a saját szokásos tartományod", avg="7 éjszakás átlag",
                   one="egy alacsony éjszaka", week="egy hét a szokásos alatt", nights="éjszaka", cap="<b>Szemléltetés példa-éjszakákkal.</b> A pontok egy-egy éjszakát jelölnek; a sáv az illető korábbi hetekből számolt saját szokásos tartománya; a zöld vonal 7 éjszakás mozgóátlag, ahogy Plews és munkatársai (2013) javasolják olvasni a HRV-t."),
        "de": dict(title="Eine schlechte Nacht ist Rauschen. Eine schlechte Woche ein Signal.", y="HRV (ms)", band="dein üblicher Bereich", avg="7-Nächte-Mittel",
                   one="eine niedrige Nacht", week="eine Woche unter deinem Üblichen", nights="Nächte", cap="<b>Illustration mit Beispielnächten.</b> Punkte sind einzelne Nächte; das Band ist der übliche Bereich dieser Person aus früheren Wochen; die grüne Linie ist ein gleitendes 7-Nächte-Mittel, so wie Plews und Kollegen (2013) HRV zu lesen empfehlen."),
    }
}

# Example nights: steady around 52 ms, one isolated low night, then a week below.
NIGHTS = [53, 49, 56, 51, 47, 55, 52, 50, 54, 35, 52, 57, 49, 53, 51, 55, 50, 52, 48, 42, 40, 43, 39, 41, 44, 40, 47, 50]


def hrv_band(lang):
    t = T["hrv_band"][lang]
    W, H, L, R, TOP, B = 360, 230, 26, 6, 26, 34
    lo_v, hi_v = 30, 62
    n = len(NIGHTS)
    x = lambda i: L + (W - L - R) * i / (n - 1)
    y = lambda v: TOP + (H - TOP - B) * (hi_v - v) / (hi_v - lo_v)
    base = NIGHTS[:14]
    med = statistics.median(base)
    mad = statistics.median([abs(v - med) for v in base]) * 1.4826
    b_lo, b_hi = med - mad, med + mad
    avg = []
    for i in range(6, n):
        avg.append((i, sum(NIGHTS[i - 6:i + 1]) / 7))
    pts = [(x(i), y(v)) for i, v in avg]
    path = "M" + " L".join("%.1f %.1f" % p for p in pts)
    length = sum(math.dist(pts[k], pts[k + 1]) for k in range(len(pts) - 1))
    o = [f'<figure class="fig"><p class="fig-h">{t["title"]}</p><svg viewBox="0 0 {W} {H}" role="img" aria-label="{t["title"]}">']
    for v in (35, 45, 55):
        o.append(f'<line class="grid" x1="{L}" x2="{W - R}" y1="{y(v):.1f}" y2="{y(v):.1f}"/><text class="t" x="{L - 8}" y="{y(v) + 4:.1f}" text-anchor="end">{v}</text>')
    o.append(f'<rect class="band" x="{L}" y="{y(b_hi):.1f}" width="{W - L - R}" height="{y(b_lo) - y(b_hi):.1f}" rx="6"/>')
    o.append(f'<line class="mid" x1="{L}" x2="{W - R}" y1="{y(med):.1f}" y2="{y(med):.1f}"/>')
    o.append(f'<text class="t" x="{W - R}" y="{y(b_hi) - 6:.1f}" text-anchor="end">{t["band"]}</text>')
    for i, v in enumerate(NIGHTS):
        cls = "dot lo" if v < b_lo - 4 else "dot"
        o.append(f'<circle class="{cls}" cx="{x(i):.1f}" cy="{y(v):.1f}" r="3.2"/>')
    o.append(f'<path class="avg" style="--len:{length:.0f}" d="{path}"/>')
    # annotations
    xi, yi = x(9), y(NIGHTS[9])
    o.append(f'<path class="ann" d="M{xi:.1f} {yi + 8:.1f} L{xi:.1f} {H - B + 4:.1f}"/><text class="t ann-t" x="{xi:.1f}" y="{H - B + 18:.1f}" text-anchor="middle">{t["one"]}</text>')
    xw0, xw1 = x(19), x(25)
    yw = y(min(NIGHTS[19:26])) + 14
    o.append(f'<path class="ann" d="M{xw0:.1f} {yw:.1f} L{xw1:.1f} {yw:.1f}"/><text class="t ann-t" x="{(xw0 + xw1) / 2:.1f}" y="{yw + 19:.1f}" text-anchor="middle">{t["week"]}</text>')
    o.append(f'<text class="t" x="{W - R}" y="{H - 4}" text-anchor="end">{n} {t["nights"]} →</text>')
    o.append(f'<path class="avg-key" d="M{L + 6} {TOP - 12} L{L + 22} {TOP - 12}"/><text class="t" x="{L + 28}" y="{TOP - 8}">{t["avg"]}</text>')
    o.append(f'</svg><figcaption>{t["cap"]}</figcaption></figure>')
    return "".join(o)


if __name__ == "__main__":
    print(hrv_band("en")[:300])
