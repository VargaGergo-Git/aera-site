"""Sleep score guides (EN/HU/DE): what is a good sleep score on Apple Watch."""
from article_kit import keys, shot, pull

SS_KEYS = {
    "en": [("81+", "where Apple's High band starts on its 0–100 scale", "Apple Watch User Guide"),
           ("50 pts", "of Apple's 100 come from sleep duration alone", "Apple Support"),
           ("7+ h", "a night, regularly: the adult recommendation", "Watson et al. 2015")],
    "hu": [("81+", "pontnál kezdődik az Apple 0–100-as skáláján a „Maximum” sáv", "Apple Watch felhasználói útmutató"),
           ("50 pont", "az Apple 100 pontjából egyedül az alvás időtartamáért jár", "Apple támogatás"),
           ("7+ óra", "alvás éjszakánként, rendszeresen: ennyit ajánlanak a felnőtteknek", "Watson és mtsai, 2015")],
    "de": [("81+", "ab hier beginnt auf Apples Skala von 0 bis 100 die Stufe „Hoch“", "Apple Watch Benutzerhandbuch"),
           ("50 Pkt.", "von Apples 100 kommen allein aus der Schlafdauer", "Apple Support"),
           ("7+ Std.", "pro Nacht, regelmäßig: die Empfehlung für Erwachsene", "Watson et al. 2015")],
}

SS_PULL = {
    "en": "Half of Apple's score is simply how long you slept.",
    "hu": "Az Apple pontszámának a fele egyszerűen azon múlik, mennyit aludtál.",
    "de": "Die Hälfte von Apples Wert ist schlicht, wie lange du geschlafen hast.",
}

SS_SHOT = {
    "en": ("Aera's sleep score for one night: Excellent, right on the sleep need, 94 of 100 and 7h 25m asleep",
           "Aera's own sleep score",
           "Aera scores the night from 0 to 100 and gives it a word, Excellent from 85 up, beside the time asleep and how it sits against the sleep need learned from your own nights. Tap the score to see where the points went."),
    "hu": ("Az Aera alváspontszáma egy éjszakáról: Kiváló, pont annyi, amennyi kell, 100-ból 94 pont, 7 óra 25 perc alvás",
           "Az Aera saját alváspontszáma",
           "Az Aera 0 és 100 között pontozza az éjszakát, és egy szóval is értékeli: 85 ponttól Kiváló. Mellette látod, mennyit aludtál, és ez hogyan viszonyul az alvásigényedhez, amelyet az Aera a saját éjszakáidból tanult meg. Koppints a pontszámra, és megmutatja, hová mentek a pontok."),
    "de": ("Aeras Schlafscore für eine Nacht: Ausgezeichnet, genau beim Schlafbedarf, 94 von 100 und 7 Std. 25 Min. Schlaf",
           "Aeras eigener Schlafscore",
           "Aera bewertet die Nacht von 0 bis 100 und gibt ihr ein Wort, ab 85 Ausgezeichnet, daneben die Schlafzeit und wie sie zu deinem Schlafbedarf steht, den Aera aus deinen eigenen Nächten lernt. Tipp auf den Wert, und du siehst, wohin die Punkte gegangen sind."),
}

# ---- figure: one low night vs a run of low nights, against the person's own usual ----
FIG_T = {
    "en": dict(title="A 65 after a wedding says little. Five nights in the 60s say a lot.",
               band="your usual", apple="Apple's High band starts at 81", one="a wedding",
               five="five nights in the 60s", nights="nights",
               cap="<b>Illustration with example nights.</b> Dots are single nights' scores. The shaded band is this person's own usual, in the high 80s; the dashed line is where Apple's High band begins. The one low night after a wedding barely matters. Five nights in a row below the usual are the thing to act on."),
    "hu": dict(title="Egy lagzi utáni 65 pont keveset mond. Öt éjszaka 60 körül annál többet.",
               band="a szokásos sávod", apple="81-től: az Apple „Maximum” sávja", one="egy lagzi",
               five="öt éjszaka 60 körül", nights="éjszaka",
               cap="<b>Szemléltetés példa-éjszakákkal.</b> Minden pont egy éjszaka pontszáma. A halvány sáv ennek az embernek a szokásos tartománya, 85 fölött. A szaggatott vonalnál kezdődik az Apple „Maximum” sávja. A lagzi utáni egy gyenge éjszaka alig számít. Az viszont már tennivalót jelez, ha öt éjszakán át a szokásos alatt maradsz."),
    "de": dict(title="Eine 65 nach einer Hochzeit sagt wenig. Fünf Nächte um die 60 sagen viel.",
               band="dein Übliches", apple="Ab 81 beginnt Apples Stufe „Hoch“", one="eine Hochzeit",
               five="fünf Nächte um die 60", nights="Nächte",
               cap="<b>Illustration mit Beispielnächten.</b> Punkte sind die Werte einzelner Nächte. Das Band ist das eigene Übliche dieser Person, bei hohen 80ern; an der gestrichelten Linie beginnt Apples Stufe „Hoch“. Die eine schwache Nacht nach einer Hochzeit zählt kaum. Fünf Nächte in Folge unter dem Üblichen sind das, worum du dich kümmern solltest."),
}

# Example scores: usual in the high 80s, one low night (index 6), then five nights in the 60s.
NIGHTS = [88, 86, 89, 85, 90, 87, 65, 88, 90, 86, 87, 85, 89, 87, 66, 63, 67, 62, 65, 86, 88]


def sleep_score_fig(lang):
    t = FIG_T[lang]
    W, H, L, R, TOP, B = 360, 232, 26, 6, 26, 36
    lo_v, hi_v = 55, 93
    n = len(NIGHTS)
    x = lambda i: L + 6 + (W - L - R - 12) * i / (n - 1)
    y = lambda v: TOP + (H - TOP - B) * (hi_v - v) / (hi_v - lo_v)
    b_lo, b_hi = 84.5, 91
    o = [f'<figure class="fig"><p class="fig-h">{t["title"]}</p><svg viewBox="0 0 {W} {H}" role="img" aria-label="{t["title"]}">']
    for v in (60, 70, 90):
        o.append(f'<line class="grid" x1="{L}" x2="{W - R}" y1="{y(v):.1f}" y2="{y(v):.1f}"/><text class="t" x="{L - 8}" y="{y(v) + 4:.1f}" text-anchor="end">{v}</text>')
    o.append(f'<rect class="band" x="{L}" y="{y(b_hi):.1f}" width="{W - L - R}" height="{y(b_lo) - y(b_hi):.1f}" rx="6"/>')
    o.append(f'<text class="t" x="{W - R}" y="{y(b_hi) - 7:.1f}" text-anchor="end">{t["band"]}</text>')
    # Apple's High band cut-off
    ya = y(81)
    o.append(f'<path class="ann" stroke-dasharray="3 4" d="M{L} {ya:.1f} L{W - R} {ya:.1f}"/><text class="t" x="{L - 8}" y="{ya + 4:.1f}" text-anchor="end">81</text>')
    o.append(f'<text class="t ann-t" x="{x(7) + 2:.1f}" y="{ya + 15:.1f}">{t["apple"]}</text>')
    for i, v in enumerate(NIGHTS):
        cls = "dot lo" if v < 80 else "dot"
        o.append(f'<circle class="{cls}" cx="{x(i):.1f}" cy="{y(v):.1f}" r="3.4"/>')
    # one low night
    xi, yi = x(6), y(NIGHTS[6])
    o.append(f'<path class="ann" d="M{xi:.1f} {yi + 8:.1f} L{xi:.1f} {H - B + 4:.1f}"/><text class="t ann-t" x="{xi:.1f}" y="{H - B + 18:.1f}" text-anchor="middle">{t["one"]}</text>')
    # five nights in a row
    xw0, xw1 = x(14), x(18)
    yw = y(min(NIGHTS[14:19])) + 12
    o.append(f'<path class="ann" d="M{xw0:.1f} {yw:.1f} L{xw1:.1f} {yw:.1f}"/><text class="t ann-t" x="{xw1 + 4:.1f}" y="{yw + 17:.1f}" text-anchor="end">{t["five"]}</text>')
    o.append(f'<text class="t" x="{W - R}" y="{H - 2}" text-anchor="end">{n} {t["nights"]} →</text>')
    o.append(f'</svg><figcaption>{t["cap"]}</figcaption></figure>')
    return "".join(o)


ARTICLES = {}
for lang, fn in [
    ("en", "what-is-a-good-sleep-score.html"),
    ("hu", "jo-alvas-pontszam.html"),
    ("de", "guter-schlafscore.html"),
]:
    ARTICLES[fn] = (lang, [
        ("lead", "keys", keys(SS_KEYS[lang])),
        ("h2:1", "pull", pull(SS_PULL[lang])),
        ("h2:2", "fig", sleep_score_fig(lang)),
        ("aera", "shot", shot("sleep-score", *SS_SHOT[lang], w=640, h=264)),
    ])
