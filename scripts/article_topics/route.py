"""Running-route planning guides (EN/HU/DE)."""
import math
from article_kit import keys, shot, pull

ROUTE_KEYS = {
    "en": [(">1.5×", "the energy per metre of the flat when running up a 10% climb", "Minetti et al. 2002"),
           ("3 shapes", "out-and-back, loop or point-to-point: pick the one that suits the day", "This guide"),
           ("7 days", "of runs that Flyover replays in 3D for free", "Aera")],
    "hu": [(">1,5×", "ennyi energiát kér méterenként egy 10%-os emelkedő a síkhoz képest", "Minetti és mtsai, 2002"),
           ("3 forma", "oda-vissza, kör vagy A-ból B-be: válaszd azt, amelyik illik a naphoz", "Ez az útmutató"),
           ("7 nap", "ennyi napra visszamenőleg játssza vissza a Flyover ingyen, 3D-ben a futásaidat", "Aera")],
    "de": [(">1,5×", "so viel Energie pro Meter bei 10 % Steigung wie in der Ebene", "Minetti et al. 2002"),
           ("3 Formen", "hin und zurück, Runde oder von A nach B: nimm die, die zum Tag passt", "Dieser Ratgeber"),
           ("7 Tage", "so weit zurück spielt Flyover deine Läufe kostenlos in 3D ab", "Aera")],
}
ROUTE_PULL = {
    "en": "The honest time for a route is a range from your own runs, not one number from a map.",
    "hu": "Hogy meddig tart egy útvonal, arra a legőszintébb válasz egy tartomány a saját futásaidból, nem egyetlen szám a térképről.",
    "de": "Die ehrliche Zeit für eine Route ist eine Spanne aus deinen eigenen Läufen, keine einzelne Zahl von einer Karte.",
}
ROUTE_SHOT = {
    "en": ("Aera's route navigation banner: 55 m, Off the route, line is north-west, still recording, with a rail showing 55 m right of the line",
           "Off the route, in Aera",
           "When you leave the planned line, the banner says how far away you are and which way the line lies, and a rail shows which side of it you are on. The run keeps recording."),
    "hu": ("Az Aera navigációs sávja: 55 m, letértél az útvonalról, a vonal északnyugatra van, a rögzítés megy tovább, alatta egy csík: 55 m-rel a vonaltól jobbra",
           "Letértél az útvonalról",
           "Ha letérsz a megtervezett vonalról, a sáv megmondja, milyen messze vagy, és merre van a vonal. Alatta egy csík mutatja, melyik oldalán jársz. A futás rögzítése közben megy tovább."),
    "de": ("Das Navigationsbanner in Aera: 55 m, von der Route abgekommen, die Linie liegt im Nordwesten, Aufzeichnung läuft, darunter eine Leiste: 55 m rechts der Linie",
           "Von der Route ab, in Aera",
           "Verlässt du die geplante Linie, sagt das Banner, wie weit du weg bist und in welcher Richtung die Linie liegt, und eine Leiste zeigt, auf welcher Seite du bist. Der Lauf wird weiter aufgezeichnet."),
}

FIG = {
    "en": dict(title="Climbing costs far more than the flat. Descending gives only some back.",
               flat="flat: 1×", climb="10% climb: over 1.5×", d1="downhill is cheaper,", d2="until it gets steep",
               down="← downhill", up="uphill →", unit="energy per metre",
               cap="<b>Illustration drawn from the curve Minetti and colleagues (2002) fitted to their treadmill measurements.</b> The energy each metre of running costs on each slope, against the flat. A 10% climb costs more than one and a half times as much; a gentle descent costs less, but past a certain steepness the cost rises again because your legs brake on every stride."),
    "hu": dict(title="Felfelé sokkal több energia kell, mint síkon. Lefelé ennek csak egy részét kapod vissza.",
               flat="sík: 1×", climb="10%-os emelkedő: több mint 1,5×", d1="lejtőn olcsóbb,", d2="amíg nem túl meredek",
               down="← lejtő", up="emelkedő →", unit="energia méterenként",
               cap="<b>Szemléltetés Minetti és munkatársai (2002) görbéje alapján, amelyet futópados méréseikre illesztettek.</b> Ennyi energiát kér egy méter futás az egyes meredekségeken, a síkhoz képest. Egy 10%-os emelkedőn több mint másfélszer annyit. Az enyhe lejtő olcsóbb, egy bizonyos meredekség után viszont újra nő a költség, mert a lábad minden lépésnél fékez."),
    "de": dict(title="Bergauf kostet weit mehr als die Ebene. Bergab gibt nur einen Teil zurück.",
               flat="Ebene: 1×", climb="10 % Steigung: über 1,5×", d1="bergab günstiger,", d2="bis es steil wird",
               down="← bergab", up="bergauf →", unit="Energie pro Meter",
               cap="<b>Illustration nach der Kurve, die Minetti und Kollegen (2002) an ihre Laufbandmessungen angepasst haben.</b> Wie viel Energie ein Meter Laufen auf jeder Neigung kostet, im Vergleich zur Ebene. Bei 10 % Steigung mehr als das Anderthalbfache; ein leichtes Gefälle ist günstiger, ab einer gewissen Steilheit steigen die Kosten aber wieder, weil die Beine bei jedem Schritt bremsen."),
}


def _cost(i):
    """Minetti et al. 2002, energy cost of running (J/kg/m) at gradient i (fraction)."""
    return 155.4 * i**5 - 30.4 * i**4 - 43.3 * i**3 + 46.3 * i**2 + 19.5 * i + 3.6


def route_hills(lang):
    t = FIG[lang]
    W, H, L, R, TOP, B = 360, 236, 28, 8, 30, 42
    g0, g1 = -0.30, 0.20
    lo_v, hi_v = 0.3, 2.7
    x = lambda g: L + (W - L - R) * (g - g0) / (g1 - g0)
    y = lambda v: TOP + (H - TOP - B) * (hi_v - v) / (hi_v - lo_v)
    rel = lambda g: _cost(g) / _cost(0)
    o = [f'<figure class="fig"><p class="fig-h">{t["title"]}</p><svg viewBox="0 0 {W} {H}" role="img" aria-label="{t["title"]}">']
    for v in (1, 2):
        o.append(f'<line class="grid" x1="{L}" x2="{W - R}" y1="{y(v):.1f}" y2="{y(v):.1f}"/><text class="t" x="{L - 6}" y="{y(v) + 4:.1f}" text-anchor="end">{v}×</text>')
    o.append(f'<text class="t" x="{L}" y="{TOP - 14}">{t["unit"]}</text>')
    for g in (-0.3, -0.2, -0.1, 0, 0.1, 0.2):
        lab = "0" if g == 0 else ("+" if g > 0 else "−") + f"{abs(round(g * 100))}%"
        anchor = "start" if g == g0 else ("end" if g == g1 else "middle")
        o.append(f'<text class="t" x="{x(g):.1f}" y="{H - B + 16}" text-anchor="{anchor}">{lab}</text>')
    o.append(f'<text class="t" x="{L}" y="{H - 6}">{t["down"]}</text><text class="t" x="{W - R}" y="{H - 6}" text-anchor="end">{t["up"]}</text>')
    pts = [(x(g0 + (g1 - g0) * k / 100), y(rel(g0 + (g1 - g0) * k / 100))) for k in range(101)]
    length = sum(math.dist(pts[k], pts[k + 1]) for k in range(len(pts) - 1))
    o.append(f'<path class="s-green" style="--len:{length:.0f}" d="M' + " L".join("%.1f %.1f" % p for p in pts) + '"/>')
    # flat and 10% climb
    o.append(f'<circle class="dot" cx="{x(0):.1f}" cy="{y(1):.1f}" r="3.6"/>')
    o.append(f'<text class="t ann-t" x="{x(0) + 8:.1f}" y="{y(1) + 15:.1f}">{t["flat"]}</text>')
    o.append(f'<circle class="dot" cx="{x(0.1):.1f}" cy="{y(rel(0.1)):.1f}" r="3.6"/>')
    o.append(f'<text class="tb" x="{x(0.1) - 8:.1f}" y="{y(rel(0.1)) - 6:.1f}" text-anchor="end">{t["climb"]}</text>')
    # cheapest point on the descent
    gm = min((g0 + (g1 - g0) * k / 200 for k in range(201)), key=rel)
    o.append(f'<circle class="dot" cx="{x(gm):.1f}" cy="{y(rel(gm)):.1f}" r="3.2"/>')
    o.append(f'<path class="ann" d="M{x(gm):.1f} {y(rel(gm)) - 7:.1f} L{x(gm):.1f} {y(1.12):.1f}"/>')
    o.append(f'<text class="t ann-t" x="{x(gm):.1f}" y="{y(1.42):.1f}" text-anchor="middle">{t["d1"]}</text>')
    o.append(f'<text class="t ann-t" x="{x(gm):.1f}" y="{y(1.42) + 13:.1f}" text-anchor="middle">{t["d2"]}</text>')
    o.append(f'</svg><figcaption>{t["cap"]}</figcaption></figure>')
    return "".join(o)


ARTICLES = {}
for lang, fn in [
    ("en", "plan-a-running-route.html"),
    ("hu", "futoutvonal-tervezes.html"),
    ("de", "laufroute-planen.html"),
]:
    ARTICLES[fn] = (lang, [
        ("lead", "keys", keys(ROUTE_KEYS[lang])),
        ("h2:2", "fig", route_hills(lang)),
        ("h2:6", "pull", pull(ROUTE_PULL[lang])),
        ("aera", "shot", shot("route", *ROUTE_SHOT[lang], w=740, h=299)),
    ])
