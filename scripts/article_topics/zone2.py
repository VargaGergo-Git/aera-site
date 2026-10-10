"""Zone 2 running guides (EN/HU/DE)."""
from article_kit import keys, shot, pull

# Example runner from the page: maximum 180, resting 55. The threshold heart rate (165)
# is a made-up example so the third method has a number; the caption says so.
HR_MAX, HR_REST, LTHR = 180, 55, 165
LO_V, HI_V = 100, 150

T = {
    "en": dict(title="One runner, three formulas, three zone 2s",
               rows=["% of maximum (60–70%)", "Heart-rate reserve (60–70%)", "Threshold test (85–89%)"],
               bpm="bpm",
               cap="<b>Illustration with an example runner:</b> maximum 180, resting 55 and a threshold heart rate of 165 from a 30-minute test (made-up values). The same body gets three different zone 2 ranges; the talk test is how you check which one fits."),
    "hu": dict(title="Egy futó, három képlet, három 2-es zóna",
               rows=["Maximális pulzus (60–70%)", "Pulzustartalék (60–70%)", "Küszöbteszt (85–89%)"],
               bpm="/perc",
               cap="<b>Szemléltetés egy példafutóval:</b> 180-as maximális pulzus, 55-ös nyugalmi pulzus és egy 30 perces tesztből kapott 165-ös küszöbpulzus (kitalált értékek). Ugyanaz a futó három különböző 2-es zónát kap. Hogy melyik illik hozzád, azt beszédteszttel ellenőrizheted."),
    "de": dict(title="Ein Läufer, drei Formeln, drei Zonen 2",
               rows=["% vom Maximum (60–70 %)", "Herzfrequenzreserve (60–70 %)", "Schwellentest (85–89 %)"],
               bpm="bpm",
               cap="<b>Illustration mit einem Beispielläufer:</b> Maximum 180, Ruhepuls 55 und eine Schwellen-Herzfrequenz von 165 aus einem 30-Minuten-Test (ausgedachte Werte). Derselbe Körper bekommt drei verschiedene Zone-2-Bereiche; mit dem Sprechtest prüfst du, welcher passt."),
}


def zone2_ranges(lang):
    t = T[lang]
    # The page's own worked numbers: 108–126 (60–70% of 180) and about 130–143 (reserve 125).
    ranges = [(108, 126, "f-gold"),
              (130, 143, "f-green"),
              (0.85 * LTHR, 0.89 * LTHR, "f-indigo")]
    W, L, R, ROW, TOP = 360, 14, 14, 56, 6
    H = TOP + ROW * len(ranges) + 30
    x = lambda v: L + (W - L - R) * (v - LO_V) / (HI_V - LO_V)
    o = [f'<figure class="fig"><p class="fig-h">{t["title"]}</p><svg viewBox="0 0 {W} {H}" role="img" aria-label="{t["title"]}">']
    axis_y = TOP + ROW * len(ranges) + 2
    for v in range(LO_V, HI_V + 1, 10):
        o.append(f'<line class="grid" x1="{x(v):.1f}" x2="{x(v):.1f}" y1="{TOP + 22}" y2="{axis_y}"/>'
                 f'<text class="t" x="{x(v):.1f}" y="{axis_y + 16}" text-anchor="middle">{v}</text>')
    for k, ((lo, hi, fill), label) in enumerate(zip(ranges, t["rows"])):
        y0 = TOP + ROW * k
        o.append(f'<text class="tb" x="{L}" y="{y0 + 14}">{label}</text>'
                 f'<text class="t" x="{W - R}" y="{y0 + 14}" text-anchor="end">{round(lo)}–{round(hi)} {t["bpm"]}</text>')
        o.append(f'<rect class="f-mute" x="{L}" y="{y0 + 26}" width="{W - L - R}" height="12" rx="6"/>')
        o.append(f'<rect class="bar h {fill}" style="--d:{k * 140}ms" x="{x(lo):.1f}" y="{y0 + 26}" width="{x(hi) - x(lo):.1f}" height="12" rx="6"/>')
    o.append(f'</svg><figcaption>{t["cap"]}</figcaption></figure>')
    return "".join(o)


KEYS = {
    "en": [("18,712", "people pooled to replace 220 minus age with 208 minus 0.7 × age", "Tanaka et al. 2001"),
           ("14", "sport scientists and coaches agreed where zone 2 sits: just below the first threshold", "Sitko et al. 2025"),
           ("~75%", "of endurance sessions below the first threshold in well-trained junior skiers", "Seiler & Kjerland 2006")],
    "hu": [("18 712", "ember adataiból született meg a „208 mínusz 0,7 × életkor”, a „220 mínusz életkor” utódja", "Tanaka és mtsai, 2001"),
           ("14", "sporttudós és edző egyezett meg abban, hogy a 2-es zóna közvetlenül az első küszöb alatt van", "Sitko és mtsai, 2025"),
           ("~75%", "a jól edzett junior sífutók állóképességi edzéseiből ennyi zajlott az első küszöb alatt", "Seiler és Kjerland, 2006")],
    "de": [("18.712", "Personen lieferten 208 minus 0,7 × Alter als Ersatz für 220 minus Alter", "Tanaka et al. 2001"),
           ("14", "Sportwissenschaftler und Trainer einigten sich: Zone 2 liegt direkt unter der ersten Schwelle", "Sitko et al. 2025"),
           ("~75 %", "der Ausdauereinheiten unter der ersten Schwelle bei gut trainierten Junioren im Skilanglauf", "Seiler & Kjerland 2006")],
}
PULL = {
    "en": "Run by heart rate and breathing, and let pace be whatever it is.",
    "hu": "Fuss a pulzusod és a légzésed szerint, a tempó pedig legyen, ami lesz.",
    "de": "Lauf nach Puls und Atmung, und lass das Tempo sein, was es ist.",
}
SHOT = {
    "en": ("Aera's run summary: average pace 6:21 per km and average heart rate 133 bpm, each with its usual value underneath",
           "Pace beside heart rate",
           "After a run, Aera puts your average pace and average heart rate over your usual for the same kind of workout from the last 30 days, once there are three to compare. The same heart rate at a quicker pace, week after week, is the aerobic base growing."),
    "hu": ("Az Aera futásösszegzője: 6:21/km átlagtempó és 133/perc átlagpulzus, mindkettő alatt a szokásos érték",
           "Tempó a pulzus mellett",
           "Futás után az Aera az átlagtempódat és az átlagpulzusodat az elmúlt 30 nap hasonló edzéseinek szokásos értékei fölé írja, amint legalább három ilyen edzés van az összevetéshez. Ha ugyanazon a pulzuson hétről hétre gyorsabb vagy, az aerob alapod épül."),
    "de": ("Die Laufübersicht in Aera: Durchschnittstempo 6:21 pro km und Durchschnittspuls 133 bpm, darunter jeweils der übliche Wert",
           "Tempo neben Puls",
           "Nach einem Lauf stellt Aera dein Durchschnittstempo und deinen Durchschnittspuls über dein Übliches aus gleichartigen Trainings der letzten 30 Tage, sobald es drei zum Vergleichen gibt. Gleicher Puls bei schnellerem Tempo, Woche für Woche: So wächst deine aerobe Basis."),
}

ARTICLES = {}
for lang, fn in [("en", "zone-2-heart-rate-running.html"),
                 ("hu", "zona-2-pulzus-futas.html"),
                 ("de", "zone-2-puls-laufen.html")]:
    ARTICLES[fn] = (lang, [
        ("lead", "keys", keys(KEYS[lang])),
        ("h2:0", "fig", zone2_ranges(lang)),
        ("h2:3", "pull", pull(PULL[lang])),
        ("aera", "shot", shot("zone2", *SHOT[lang], w=360, h=365)),
    ])
