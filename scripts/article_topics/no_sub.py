"""Apple Watch without a subscription / WHOOP alternative guides (EN/DE)."""
from article_kit import keys, shot, pull

NOSUB_KEYS = {
    "en": [("0.53", "Cohen's kappa for Apple Watch sleep stages against a sleep lab, best of six wrist devices", "Schyvens et al. 2025"),
           ("24 h", "battery rating for Series 11, including six hours of sleep tracking", "Apple"),
           ("10 of 100", "points Aera's sleep score gives to sleep stages", "Aera")],
    "de": [("0,53", "Cohens Kappa der Apple Watch bei den Schlafphasen gegenüber dem Schlaflabor, bester von sechs Geräten", "Schyvens et al. 2025"),
           ("24 h", "Akkulaufzeit laut Apple für die Series 11, darin sechs Stunden Schlaftracking", "Apple"),
           ("10 von 100", "Punkten gibt der Schlafwert von Aera den Schlafphasen", "Aera")],
}
NOSUB_PULL = {
    "en": "A wrist tells sleep from wake well, and the stages much less well.",
    "de": "Schlaf und Wachsein trennt das Handgelenk gut, die einzelnen Phasen deutlich schlechter.",
}
NOSUB_SHOT = {
    "en": ("Aera's sleep screen: a score of 94 of 100, 7 h 25 min asleep, and the last seven nights drawn against a band marked Your need",
           "Sleep in Aera",
           "Last night's score and time asleep, then the week as one line against your own sleep need, so a short night reads against what you usually need."),
    "de": ("Der Schlafbildschirm von Aera: Wert 94 von 100, 7 h 25 min Schlaf und die letzten sieben Nächte vor einem Band mit der Aufschrift Your need",
           "Schlaf in Aera",
           "Wert und Schlafdauer der letzten Nacht, darunter die Woche als Linie gegen deinen eigenen Schlafbedarf. So liest du eine kurze Nacht an dem, was du sonst brauchst."),
}

FIG_T = {
    "en": {"title": "What each setup asks of you",
           "cols": ("Apple Watch you own", "Dedicated strap"),
           "rows": [("Cost", ("No extra fee", "for the built-in features"), ("Yearly membership", "sensor included")),
                    ("Battery, maker's rating", ("Up to 24 h", "Series 11, with 6 h of sleep"), ("About 14 days", "5.0 and MG sensors")),
                    ("Charging", ("A daily top-up", "e.g. shower or breakfast"), ("Battery pack", "charges while you wear it")),
                    ("Screen", ("Yes", "with notifications"), ("None", "by design"))],
           "app": ("Optional: an app on top of Apple Health",
                   "Sleep, heart signals and workouts on one screen.",
                   "Aera: a free tier, plus optional Premium as a",
                   "subscription or a one-time Lifetime purchase."),
           "cap": "<b>Drawn from the facts on this page.</b> Battery figures are the makers' own ratings: Apple for Series 11, WHOOP for its 5.0 and MG sensors. Current prices are on whoop.com and in the App Store."},
    "de": {"title": "Was du jeweils brauchst",
           "cols": ("Deine Apple Watch", "Eigenes Armband"),
           "rows": [("Kosten", ("Keine Zusatzgebühr", "für eingebaute Funktionen"), ("Jahresmitgliedschaft", "Sensor inklusive")),
                    ("Akku, laut Hersteller", ("Bis zu 24 h", "Series 11, mit 6 h Schlaf"), ("Etwa 14 Tage", "Sensoren 5.0 und MG")),
                    ("Laden", ("Täglich nachladen", "z. B. beim Duschen"), ("Akkupack", "lädt beim Tragen")),
                    ("Display", ("Ja", "mit Mitteilungen"), ("Keins", "bewusst so gebaut"))],
           "app": ("Optional: eine App auf Apple Health",
                   "Schlaf, Herzwerte und Training auf einem Bildschirm.",
                   "Aera: kostenlos nutzbar, dazu optional Premium",
                   "als Abo oder einmaliger Lifetime-Kauf."),
           "cap": "<b>Aus den Angaben auf dieser Seite.</b> Die Akkuwerte sind Herstellerangaben: Apple für die Series 11, WHOOP für die Sensoren 5.0 und MG. Aktuelle Preise stehen auf whoop.com und im App Store."},
}


def setup_compare(lang):
    """Neutral side-by-side of what each setup needs, every value taken from the page text."""
    t = FIG_T[lang]
    W, GAP, PAD = 360, 8, 12
    CW = (W - GAP) / 2
    xs = (0, CW + GAP)
    ROW0, ROWH = 40, 56
    nrows = len(t["rows"])
    col_h = ROW0 + nrows * ROWH - 4
    app_y = col_h + 12
    H = app_y + 82
    o = [f'<figure class="fig"><p class="fig-h">{t["title"]}</p><svg viewBox="0 0 {W} {H}" role="img" aria-label="{t["title"]}">']
    for x0, head in zip(xs, t["cols"]):
        o.append(f'<rect class="f-bg" x="{x0:.0f}" y="0" width="{CW:.0f}" height="{col_h}" rx="14"/>')
        o.append(f'<text class="tb" x="{x0 + PAD:.0f}" y="25">{head}</text>')
    for r, (label, a, b) in enumerate(t["rows"]):
        y0 = ROW0 + r * ROWH
        if r:
            for x0 in xs:
                o.append(f'<line class="grid" x1="{x0 + PAD:.0f}" x2="{x0 + CW - PAD:.0f}" y1="{y0 - 6}" y2="{y0 - 6}"/>')
        for x0, (big, small) in zip(xs, (a, b)):
            o.append(f'<text class="t" x="{x0 + PAD:.0f}" y="{y0 + 10}">{label}</text>')
            o.append(f'<text class="tb" x="{x0 + PAD:.0f}" y="{y0 + 28}">{big}</text>')
            o.append(f'<text class="t ann-t" x="{x0 + PAD:.0f}" y="{y0 + 43}">{small}</text>')
    head, line, aera1, aera2 = t["app"]
    o.append(f'<rect class="f-bg" x="0" y="{app_y}" width="{W}" height="76" rx="14"/>')
    o.append(f'<text class="tb" x="{PAD}" y="{app_y + 22}">{head}</text>')
    o.append(f'<text class="t ann-t" x="{PAD}" y="{app_y + 39}">{line}</text>')
    o.append(f'<text class="t" x="{PAD}" y="{app_y + 55}">{aera1}</text>')
    o.append(f'<text class="t" x="{PAD}" y="{app_y + 69}">{aera2}</text>')
    o.append(f'</svg><figcaption>{t["cap"]}</figcaption></figure>')
    return "".join(o)


ARTICLES = {}
for lang, fn in [("en", "apple-watch-sleep-and-training-without-a-subscription.html"),
                 ("de", "whoop-alternative-apple-watch.html")]:
    ARTICLES[fn] = (lang, [
        ("lead", "keys", keys(NOSUB_KEYS[lang])),
        ("h2:2", "pull", pull(NOSUB_PULL[lang])),
        ("h2:1", "fig", setup_compare(lang)),
        ("aera", "shot", shot("no-sub", *NOSUB_SHOT[lang], w=740, h=462)),
    ])
