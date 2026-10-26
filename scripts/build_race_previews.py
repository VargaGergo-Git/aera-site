#!/usr/bin/env python3
"""Free race route preview pages: race/<slug>/index.html, embeddable in an iframe.

    python3 scripts/build_race_previews.py

Each race is a GPX file in race/gpx/ plus a row in RACES. The page draws the course
outline and elevation profile from the GPX (inline SVG, no map tiles, no scripts, no
third party requests) and ends in an Aera link on the race's own channel
(/get/race-<slug>/hu/), so Cloudflare Web Analytics and App Store Connect count taps
per race. Add the channel to scripts/outreach_links.json and run
build_outreach_links.py. Courses are the organizer's own published GPX; get the
organizer's yes before a page goes live.
"""
import math
import os
import re
import sys
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RACES = [
    {"slug": "budai-trail-s", "name": "Nyúlcipőbolt Budai Trail S", "organizer": "terepfutas.hu",
     "url": "https://terepfutas.hu/nyulcipobolt-budai-trail/", "gpx": "budai-trail-s.gpx"},
    {"slug": "budai-trail-m", "name": "Nyúlcipőbolt Budai Trail M", "organizer": "terepfutas.hu",
     "url": "https://terepfutas.hu/nyulcipobolt-budai-trail/", "gpx": "budai-trail-m.gpx"},
    {"slug": "budai-trail-l", "name": "Nyúlcipőbolt Budai Trail L", "organizer": "terepfutas.hu",
     "url": "https://terepfutas.hu/nyulcipobolt-budai-trail/", "gpx": "budai-trail-l.gpx"},
    {"slug": "budai-trail-xl", "name": "Nyúlcipőbolt Budai Trail XL", "organizer": "terepfutas.hu",
     "url": "https://terepfutas.hu/nyulcipobolt-budai-trail/", "gpx": "budai-trail-xl.gpx"},
]


def read_gpx(path):
    root = ET.parse(path).getroot()
    for el in root.iter():
        el.tag = el.tag.rsplit("}", 1)[-1]
    pts = []
    for p in root.iter("trkpt"):
        e = p.find("ele")
        pts.append((float(p.get("lat")), float(p.get("lon")), float(e.text) if e is not None else 0.0))
    return pts


def hav(a, b):
    r = 6371000.0
    p1, p2 = math.radians(a[0]), math.radians(b[0])
    dp, dl = p2 - p1, math.radians(b[1] - a[1])
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(h))


def stats(pts):
    cum, gain = [0.0], 0.0
    for i in range(1, len(pts)):
        cum.append(cum[-1] + hav(pts[i - 1], pts[i]))
    # smooth elevation (5-point mean), count rises over 1 m steps to ignore noise
    el = [sum(p[2] for p in pts[max(0, i - 2):i + 3]) / len(pts[max(0, i - 2):i + 3]) for i in range(len(pts))]
    for i in range(1, len(el)):
        d = el[i] - el[i - 1]
        if d > 0:
            gain += d
    return cum, el, gain


def svg_route(pts, w=320, h=240, pad=14):
    lat0 = sum(p[0] for p in pts) / len(pts)
    k = math.cos(math.radians(lat0))
    xs = [p[1] * k for p in pts]
    ys = [-p[0] for p in pts]
    sx, sy = max(xs) - min(xs), max(ys) - min(ys)
    s = min((w - 2 * pad) / sx, (h - 2 * pad) / sy)
    ox = (w - sx * s) / 2 - min(xs) * s
    oy = (h - sy * s) / 2 - min(ys) * s
    d = " ".join("%s%.1f %.1f" % ("M" if i == 0 else "L", x * s + ox, y * s + oy) for i, (x, y) in enumerate(zip(xs, ys)))
    x0, y0 = xs[0] * s + ox, ys[0] * s + oy
    x1, y1 = xs[-1] * s + ox, ys[-1] * s + oy
    return d, (x0, y0), (x1, y1)


def svg_profile(cum, el, w=320, h=90):
    lo, hi = min(el), max(el)
    span = max(hi - lo, 1.0)
    n = max(1, len(cum) // 160)
    pts = [(cum[i] / cum[-1] * w, h - 6 - (el[i] - lo) / span * (h - 14)) for i in range(0, len(cum), n)]
    line = " ".join("%.1f,%.1f" % p for p in pts)
    return line, lo, hi


CSS = """:root{--bg:#f6f4ef;--fg:#1c1c1e;--mute:#6b6b6f;--line:#d9d4c8;--route:#e8590c}
@media(prefers-color-scheme:dark){:root{--bg:#0b0b0c;--fg:#f2f2f2;--mute:#9a9a9f;--line:#2a2a2d}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.45 -apple-system,system-ui,sans-serif}
main{max-width:480px;margin:0 auto;padding:20px 16px 28px}
h1{font-size:22px;line-height:1.2;margin:0 0 4px}p{margin:0 0 12px}.mute{color:var(--mute);font-size:14px}
.stats{display:flex;gap:20px;margin:12px 0 8px}.stats b{display:block;font-size:20px}.stats span{color:var(--mute);font-size:13px}
svg{display:block;width:100%;height:auto}.route{fill:none;stroke:var(--route);stroke-width:3;stroke-linecap:round;stroke-linejoin:round}
.prof{fill:none;stroke:var(--fg);stroke-width:1.5}.box{border-top:1px solid var(--line);padding-top:12px;margin-top:12px}
.cta{display:block;text-align:center;background:var(--fg);color:var(--bg);text-decoration:none;font-weight:600;padding:14px 16px;border-radius:12px;margin-top:16px}
a{color:inherit}"""


def page(r):
    pts = read_gpx(os.path.join(ROOT, "race", "gpx", r["gpx"]))
    cum, el, gain = stats(pts)
    km = cum[-1] / 1000
    d, a, b = svg_route(pts)
    prof, lo, hi = svg_profile(cum, el)
    get = "/get/race-%s/hu/" % r["slug"]
    return """<!doctype html>
<html lang="hu"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>%(name)s: pálya előnézet</title>
<style>%(css)s</style>
<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{"token": "4fc0403d67364f1ab92526387bdd0b81"}'></script>
</head><body><main>
<h1>%(name)s</h1>
<p class="mute">Pálya előnézet. A pálya a szervező (%(org)s) közzétett GPX-fájlja.</p>
<div class="stats"><div><b>%(km).1f km</b><span>távolság</span></div><div><b>%(gain)d m</b><span>szintemelkedés</span></div><div><b>%(lo)d–%(hi)d m</b><span>magasság</span></div></div>
<svg viewBox="0 0 320 240" role="img" aria-label="A pálya vonala"><path class="route" d="%(d)s"/><circle cx="%(ax).1f" cy="%(ay).1f" r="5" fill="var(--route)"/><circle cx="%(bx).1f" cy="%(by).1f" r="5" fill="none" stroke="var(--route)" stroke-width="2"/></svg>
<div class="box"><svg viewBox="0 0 320 90" role="img" aria-label="Szintprofil"><polyline class="prof" points="%(prof)s"/></svg></div>
<a class="cta" href="%(get)s" target="_top">Nézd meg 3D-ben az Aerában</a>
<p class="mute" style="margin-top:12px">Az Aera 3D-ben visszajátssza a futásodat, ingyen, fiók nélkül. Garminnal, Polarral vagy Corosszal is működik az Apple Egészségen át.</p>
<p class="mute"><a href="%(url)s" target="_top">Nevezés és részletek: %(org)s</a></p>
</main></body></html>
""" % {"name": r["name"], "org": r["organizer"], "url": r["url"], "css": CSS, "km": km, "gain": round(gain),
       "lo": round(lo), "hi": round(hi), "d": d, "ax": a[0], "ay": a[1], "bx": b[0], "by": b[1], "prof": prof, "get": get}


def main():
    for r in RACES:
        assert re.fullmatch(r"[a-z0-9-]{1,30}", r["slug"])
        out = os.path.join(ROOT, "race", r["slug"])
        os.makedirs(out, exist_ok=True)
        open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(page(r))
        print("wrote race/%s/" % r["slug"])


if __name__ == "__main__":
    main()
