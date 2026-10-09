"""3D run replay guides (HU/DE). The EN page is /flyover.html, outside guides/."""
import math
from article_kit import keys, shot, pull

REPLAY_KEYS = {
    "hu": [("≈45 mp", "alatt repül végig egy hosszabb futás, a megállók külön kapnak egy pillanatot", "Aera"),
           ("7 nap", "edzéseinek visszajátszása ingyenes, a régebbieké a Premium része", "Aera"),
           ("15 / 20 / 30 mp", "hosszú álló, 9:16-os videó lesz belőle a Fotókban", "Aera")],
    "de": [("≈45 s", "dauert der Flug über einen längeren Lauf, jeder Halt bekommt einen eigenen Moment", "Aera"),
           ("7 Tage", "zurück ist das Abspielen kostenlos, ältere Trainings gehören zu Premium", "Aera"),
           ("15 / 20 / 30 s", "lang wird das Video im Hochformat 9:16 in deinen Fotos", "Aera")],
}
REPLAY_PULL = {
    "hu": "A visszajátszás csak annyira pontos, mint a GPS, amely a nyomvonalat rögzítette.",
    "de": "Der Flug ist nur so genau wie das GPS, das den Track aufgezeichnet hat.",
}
REPLAY_SHOT = {
    "hu": ("Az Aera 3D-s visszajátszásának vezérlősávja a műholdkép fölött: táv, tempó, pulzus, idővonal és sebességkapcsoló",
           "Visszajátszás az Aerában",
           "Alul fut a táv, a tempó és a pulzus. Az idővonalon előre- és visszaugorhatsz, a pötty egy megállót jelöl, az 1× gomb dupla sebességre vált."),
    "de": ("Die Leiste des 3D-Flugs in Aera über dem Satellitenbild: Distanz, Tempo, Puls, Zeitleiste und Tempo-Umschalter",
           "Der Flug in Aera",
           "Unten laufen Distanz, Tempo und Puls mit. Auf der Zeitleiste springst du vor oder zurück, ein Punkt markiert einen Halt, und 1× schaltet auf doppelte Geschwindigkeit."),
}

FIG_T = {
    "hu": {"title": "Így lesz a futásból rövid repülés", "key": "A kamera magassága",
           "whole": "Teljes útvonal", "dive": "Lemerül a futó mögé", "lift": "Kanyar előtt emelkedik",
           "s1": "Leggyorsabb km", "s2": "Emelkedő teteje", "t0": "0 mp", "t1": "≈ 45 mp + megállók",
           "cap": "<b>Szemléltetés, nem valódi repülés.</b> A kamera a teljes útvonal fölött indul, lemerül a futó mögé, a kanyarok előtt kicsit felemelkedik, és megáll néhány érdekes ponton, a végén pedig visszaemelkedik a teljes képre. Egy hosszabb futás nagyjából 45 másodperc alatt repül végig, a megállók külön kapnak egy-egy pillanatot."},
    "de": {"title": "Wie aus einem Lauf ein kurzer Flug wird", "key": "Höhe der Kamera",
           "whole": "Ganze Strecke", "dive": "Taucht hinter dir ein", "lift": "Steigt vor Kurven",
           "s1": "Schnellster km", "s2": "Gipfel des Anstiegs", "t0": "0 s", "t1": "≈ 45 s + Halte",
           "cap": "<b>Illustration, kein echter Flug.</b> Die Kamera beginnt über der ganzen Strecke, taucht hinter dir ein, steigt vor Kurven ein Stück an und hält an ein paar Stellen kurz an. Am Ende steigt sie wieder auf den Überblick. Ein längerer Lauf ist in etwa 45 Sekunden durchgeflogen, jeder Halt bekommt einen eigenen Moment."},
}


def _ss(u):
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


def replay_flight(lang):
    """Camera height over film time, following the acts in FlyoverScript (overview, dive, chase, land)."""
    t = FIG_T[lang]
    W, H, L, R = 360, 214, 12, 12
    HI, LO = 56.0, 130.0                 # camera height: overview / chase (y)
    T_END, DIVE0, DIVE1, LAND0 = 57.0, 1.5, 3.9, 53.8
    STOPS, LIFT = (17.0, 41.0), 29.0
    x = lambda s: L + (W - L - R) * s / T_END

    def y(s):
        if s <= DIVE0:
            return HI
        if s <= DIVE1:
            return HI + (LO - HI) * _ss((s - DIVE0) / (DIVE1 - DIVE0))
        if s >= LAND0:
            return LO + (HI - LO) * _ss((s - LAND0) / (T_END - LAND0))
        v = LO - 18 * math.exp(-((s - LIFT) / 2.2) ** 2)          # lift before a turn
        for c in STOPS:
            v += 7 * math.exp(-((s - c) / 1.3) ** 2)            # close in at a stop
        return v

    pts = [(x(i / 10), y(i / 10)) for i in range(int(T_END * 10) + 1)]
    path = "M" + " L".join("%.1f %.1f" % p for p in pts)
    length = sum(math.dist(pts[k], pts[k + 1]) for k in range(len(pts) - 1))
    base = 176
    o = [f'<figure class="fig"><p class="fig-h">{t["title"]}</p><svg viewBox="0 0 {W} {H}" role="img" aria-label="{t["title"]}">']
    o.append(f'<path class="avg-key" d="M{L} 14 L{L + 16} 14"/><text class="t" x="{L + 22}" y="18">{t["key"]}</text>')
    o.append(f'<line class="grid" x1="{L}" x2="{W - R}" y1="{base}" y2="{base}"/>')
    o.append(f'<text class="t" x="{L}" y="{HI - 10}">{t["whole"]}</text>')
    o.append(f'<text class="t" x="{W - R}" y="{HI - 10}" text-anchor="end">{t["whole"]}</text>')
    o.append(f'<path class="s-green" style="--len:{length:.0f}" d="{path}"/>')
    # dive
    xd, yd = x(3.0), y(3.0)
    o.append(f'<path class="ann" d="M{xd + 5:.1f} {yd:.1f} L{xd + 20:.1f} {yd:.1f}"/><text class="t ann-t" x="{xd + 24:.1f}" y="{yd + 4:.1f}">{t["dive"]}</text>')
    # lift
    xl, yl = x(LIFT), y(LIFT)
    o.append(f'<path class="ann" d="M{xl:.1f} {yl - 6:.1f} L{xl:.1f} {yl - 16:.1f}"/><text class="t ann-t" x="{xl:.1f}" y="{yl - 22:.1f}" text-anchor="middle">{t["lift"]}</text>')
    # stops
    for c, key in zip(STOPS, ("s1", "s2")):
        xs, ys = x(c), y(c)
        o.append(f'<circle class="dot" cx="{xs:.1f}" cy="{ys:.1f}" r="4"/>')
        o.append(f'<path class="ann" d="M{xs:.1f} {ys + 8:.1f} L{xs:.1f} {ys + 18:.1f}"/><text class="t ann-t" x="{xs:.1f}" y="{ys + 31:.1f}" text-anchor="middle">{t[key]}</text>')
    o.append(f'<text class="t" x="{L}" y="{base + 18}">{t["t0"]}</text>')
    o.append(f'<text class="t" x="{W - R}" y="{base + 18}" text-anchor="end">{t["t1"]} →</text>')
    o.append(f'</svg><figcaption>{t["cap"]}</figcaption></figure>')
    return "".join(o)


ARTICLES = {}
for lang, fn in [("hu", "futas-3d-visszajatszas.html"), ("de", "lauf-in-3d-abspielen.html")]:
    ARTICLES[fn] = (lang, [
        ("lead", "keys", keys(REPLAY_KEYS[lang])),
        ("h2:4", "pull", pull(REPLAY_PULL[lang])),
        ("h2:2", "fig", replay_flight(lang)),
        ("aera", "shot", shot("replay-hud", *REPLAY_SHOT[lang], w=740, h=287)),
    ])
