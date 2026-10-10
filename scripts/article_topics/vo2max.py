"""Apple Watch VO2 max guides (EN/HU/DE)."""
import math
from article_kit import keys, shot, pull

VO2_KEYS = {
    "en": [("13–16%", "average gap between Apple Watch and a lab test to exhaustion, usually reading low", "Caserman 2024; Lambe 2025"),
           ("+4.9–5.5", "ml/kg/min from endurance or interval training across 28 controlled trials", "Milanović et al. 2015"),
           ("1.5 ml/kg/min", "change before Aera calls your cardio fitness Fitter or Easing", "Aera")],
    "hu": [("13–16%", "az átlagos eltérés az Apple Watch és egy kimerülésig tartó laborteszt között, az óra többnyire kevesebbet mutat", "Caserman 2024; Lambe 2025"),
           ("+4,9–5,5", "ml/kg/perc javulás állóképességi vagy intervallumedzéssel, 28 kontrollált vizsgálat összesítésében", "Milanović és mtsai, 2015"),
           ("1,5 ml/kg/perc", "változás kell ahhoz, hogy az Aera kiírja a kardiofittségedre: Fittebb vagy Csökken", "Aera")],
    "de": [("13–16 %", "mittlere Abweichung der Apple Watch von einem Labortest bis zur Erschöpfung, meist zu niedrig", "Caserman 2024; Lambe 2025"),
           ("+4,9–5,5", "ml/kg/min durch Ausdauer- oder Intervalltraining in 28 kontrollierten Studien", "Milanović et al. 2015"),
           ("1,5 ml/kg/min", "Veränderung, bevor Aera deine Ausdauerfitness Fitter oder Sinkt nennt", "Aera")],
}
VO2_PULL = {
    "en": "VO2 max is built over weeks and months, so a steady habit beats any one big week.",
    "hu": "A VO2 max hetek és hónapok alatt épül, ezért a rendszeres mozgás többet ér egyetlen nagy hétnél.",
    "de": "Die VO2max wächst über Wochen und Monate, deshalb zählt Regelmäßigkeit mehr als eine große Woche.",
}
VO2_SHOT = {
    "en": ("Key stats of a run in Aera: average pace, grade-adjusted pace, average heart rate, and VO2 max 48.6 with +1.0 in a month",
           "VO₂ max on a run",
           "On an outdoor run or walk, Aera prints the estimate Apple Health recorded that day and how far it has moved against the reading about a month earlier."),
    "hu": ("Egy futás fő adatai az Aerában: átlagtempó, emelkedőhöz igazított tempó, átlagpulzus és 48,6-os VO2 max, egy hónap alatt +1,0",
           "VO₂ max egy futásnál",
           "Kültéri futás vagy gyaloglás után az Aera kiírja, mekkora becslést mentett aznap az Apple Health, és mennyit változott a nagyjából egy hónappal korábbihoz képest."),
    "de": ("Kennzahlen eines Laufs in Aera: Durchschnittstempo, steigungsbereinigtes Tempo, Durchschnittspuls und VO2max 48,6 mit +1,0 in einem Monat",
           "VO₂max bei einem Lauf",
           "Bei einem Lauf oder Gehen im Freien zeigt Aera die Schätzung, die Apple Health an diesem Tag gespeichert hat, und wie weit sie sich gegenüber dem Wert von etwa einem Monat davor bewegt hat."),
}

FIG = {
    "en": dict(title="The watch reads low, but it rises with you.", lab="lab test", trend="watch trend", unit="ml/kg/min",
               gap1="about 13–16%", gap2="lower", weeks="weeks",
               cap="<b>Illustration with example values.</b> The dashed line is what a lab test to exhaustion would show; dots are single Apple Watch estimates and the green line is their trend. In Caserman and colleagues (2024) and Lambe and colleagues (2025) the watch was about 13 to 16 percent off on average, usually low. It is much better at showing that you are getting fitter than at giving your exact number, and the real gap differs from person to person."),
    "hu": dict(title="Az óra kevesebbet mutat, de veled együtt emelkedik.", lab="laborteszt", trend="az óra trendje", unit="ml/kg/perc",
               gap1="kb. 13–16%-kal", gap2="kevesebb", weeks="hét",
               cap="<b>Szemléltetés példaértékekkel.</b> A szaggatott vonal azt mutatja, amit egy kimerülésig tartó laborteszt adna. A pontok egy-egy Apple Watch-becslést jelölnek, a zöld vonal ezek trendje. Caserman és munkatársai (2024), valamint Lambe és munkatársai (2025) vizsgálatában az óra átlagosan nagyjából 13–16%-kal tért el, többnyire lefelé. Azt, hogy fittebb leszel-e, sokkal jobban mutatja, mint a pontos értékedet, és a valódi eltérés emberenként más."),
    "de": dict(title="Die Uhr liest zu niedrig, aber sie steigt mit dir.", lab="Labortest", trend="Verlauf der Uhr", unit="ml/kg/min",
               gap1="etwa 13–16 %", gap2="niedriger", weeks="Wochen",
               cap="<b>Illustration mit Beispielwerten.</b> Die gestrichelte Linie zeigt, was ein Labortest bis zur Erschöpfung ergäbe; Punkte sind einzelne Schätzungen der Apple Watch, die grüne Linie ihr Verlauf. Bei Caserman und Kollegen (2024) und Lambe und Kollegen (2025) lag die Uhr im Schnitt um etwa 13 bis 16 % daneben, meist zu niedrig. Ob du fitter wirst, zeigt sie viel besser als deinen genauen Wert, und die echte Abweichung ist von Mensch zu Mensch verschieden."),
}

# Example: lab VO2 max rising from 43 to 47.5 over 24 weeks; watch estimates ~14% under it, with noise.
NOISE = [0.9, -0.7, 0.4, -1.1, 0.6, 1.0, -0.5, -0.9, 0.7, 0.2, -1.0, 0.8, -0.3, 0.5, -0.8, -0.6, 0.3]


def vo2_gap(lang):
    t = FIG[lang]
    W, H, L, R, TOP, B = 360, 236, 26, 6, 34, 26
    lo_v, hi_v = 34, 50
    weeks = 24
    x = lambda w: L + (W - L - R) * w / weeks
    y = lambda v: TOP + (H - TOP - B) * (hi_v - v) / (hi_v - lo_v)
    lab = lambda w: 43 + 4.5 * (1 - math.exp(-w / 14)) / (1 - math.exp(-weeks / 14))
    ratio = 0.86
    o = [f'<figure class="fig"><p class="fig-h">{t["title"]}</p><svg viewBox="0 0 {W} {H}" role="img" aria-label="{t["title"]}">']
    for v in (36, 40, 44, 48):
        o.append(f'<line class="grid" x1="{L}" x2="{W - R}" y1="{y(v):.1f}" y2="{y(v):.1f}"/><text class="t" x="{L - 6}" y="{y(v) + 4:.1f}" text-anchor="end">{v}</text>')
    lab_pts = [(x(w / 2), y(lab(w / 2))) for w in range(0, weeks * 2 + 1)]
    o.append('<path class="mid" fill="none" d="M' + " L".join("%.1f %.1f" % p for p in lab_pts) + '"/>')
    n = len(NOISE)
    for k, e in enumerate(NOISE):
        w = 0.6 + (weeks - 1.2) * k / (n - 1)
        o.append(f'<circle class="dot" cx="{x(w):.1f}" cy="{y(lab(w) * ratio + e):.1f}" r="3.2"/>')
    tr = [(x(w / 2), y(lab(w / 2) * ratio)) for w in range(0, weeks * 2 + 1)]
    length = sum(math.dist(tr[k], tr[k + 1]) for k in range(len(tr) - 1))
    o.append(f'<path class="avg" style="--len:{length:.0f}" d="M' + " L".join("%.1f %.1f" % p for p in tr) + '"/>')
    # gap bracket near the right edge
    gx = x(weeks - 1.6)
    y_top, y_bot = y(lab(weeks - 1.6)) + 5, y(lab(weeks - 1.6) * ratio) - 9
    o.append(f'<path class="ann" d="M{gx - 4:.1f} {y_top:.1f} L{gx:.1f} {y_top:.1f} L{gx:.1f} {y_bot:.1f} L{gx - 4:.1f} {y_bot:.1f}"/>')
    ym = (y_top + y_bot) / 2
    o.append(f'<text class="t ann-t" x="{gx - 8:.1f}" y="{ym - 2:.1f}" text-anchor="end">{t["gap1"]}</text>')
    o.append(f'<text class="t ann-t" x="{gx - 8:.1f}" y="{ym + 11:.1f}" text-anchor="end">{t["gap2"]}</text>')
    # legend
    ly = TOP - 18
    o.append(f'<path class="mid" fill="none" d="M{L + 4} {ly} L{L + 22} {ly}"/><text class="t" x="{L + 28}" y="{ly + 4}">{t["lab"]}</text>')
    lx = L + 120
    o.append(f'<path class="avg-key" d="M{lx} {ly} L{lx + 18} {ly}"/><text class="t" x="{lx + 24}" y="{ly + 4}">{t["trend"]}</text>')
    o.append(f'<text class="t" x="{W - R}" y="{ly + 4}" text-anchor="end">{t["unit"]}</text>')
    o.append(f'<text class="t" x="{W - R}" y="{H - 6}" text-anchor="end">{weeks} {t["weeks"]} →</text>')
    o.append(f'</svg><figcaption>{t["cap"]}</figcaption></figure>')
    return "".join(o)


ARTICLES = {}
for lang, fn in [
    ("en", "apple-watch-vo2-max.html"),
    ("hu", "vo2-max-apple-watch-pontossag.html"),
    ("de", "vo2max-apple-watch-genauigkeit.html"),
]:
    ARTICLES[fn] = (lang, [
        ("lead", "keys", keys(VO2_KEYS[lang])),
        ("h2:1", "fig", vo2_gap(lang)),
        ("h2:4", "pull", pull(VO2_PULL[lang])),
        ("aera", "shot", shot("vo2max", *VO2_SHOT[lang], w=740, h=335)),
    ])
