"""Apple Watch resting heart rate guides (EN/HU/DE)."""
from article_kit import keys, shot, pull

LO_V, HI_V = 35, 115
# Example person's week (illustrative), moving about 3 bpm from day to day as in Quer 2020;
# drawn as the span of the week's readings.
WEEK = [57, 60, 58, 55, 59, 61, 58]

T = {
    "en": dict(title="Wide between people, narrow within one",
               rows=[("Textbook adult range", "60–100"), ("Spodick et al. (1992)", "50–90"),
                     ("Personal averages, 92,457 adults", "40–109, mean 65"), ("One person, one week", "~3 bpm a day")],
               axis="bpm",
               cap="<b>Illustration.</b> The top three bars are the ranges the sources give; the dot marks the wearable study's mean of 65 (Quer and colleagues, 2020). The bottom row is an example person's week, moving about 3 bpm from day to day, as that study found on average."),
    "hu": dict(title="Széles az emberek között, szűk egy emberen belül",
               rows=[("Tankönyvi felnőtt tartomány", "60–100"), ("Spodick és mtsai (1992)", "50–90"),
                     ("Személyes átlagok, 92 457 felnőtt", "40–109, átlag 65"), ("Egy ember, egy hét", "naponta kb. 3")],
               axis="/perc",
               cap="<b>Szemléltetés.</b> A felső három sáv a forrásokban megadott tartomány. A pont az okosórás vizsgálat 65-ös átlaga (Quer és munkatársai, 2020). Az alsó sor egy példaszemély hete: napról napra kb. 3 ütéssel mozdul, ahogy a vizsgálatban átlagosan."),
    "de": dict(title="Breit zwischen Menschen, schmal bei einem",
               rows=[("Lehrbuchbereich Erwachsene", "60–100"), ("Spodick und Kollegen (1992)", "50–90"),
                     ("Persönliche Mittel, 92.457 Erw.", "40–109, Mittel 65"), ("Ein Mensch, eine Woche", "~3 pro Tag")],
               axis="bpm",
               cap="<b>Illustration.</b> Die oberen drei Balken sind die Bereiche aus den Quellen; der Punkt markiert den Mittelwert 65 der Wearable-Studie (Quer und Kollegen, 2020). Die untere Zeile ist die Woche einer Beispielperson, die von Tag zu Tag um etwa 3 Schläge schwankt, wie die Studie im Schnitt fand."),
}


def rhr_spread(lang):
    t = T[lang]
    ranges = [(60, 100, "f-gold"), (50, 90, "f-gold"), (40, 109, "f-sage")]
    W, L, R, ROW, TOP = 360, 14, 14, 56, 6
    n = len(t["rows"])
    H = TOP + ROW * n + 30
    x = lambda v: L + (W - L - R) * (v - LO_V) / (HI_V - LO_V)
    o = [f'<figure class="fig"><p class="fig-h">{t["title"]}</p><svg viewBox="0 0 {W} {H}" role="img" aria-label="{t["title"]}">']
    axis_y = TOP + ROW * n + 2
    for v in range(40, HI_V + 1, 20):
        o.append(f'<line class="grid" x1="{x(v):.1f}" x2="{x(v):.1f}" y1="{TOP + 22}" y2="{axis_y}"/>'
                 f'<text class="t" x="{x(v):.1f}" y="{axis_y + 16}" text-anchor="middle">{v}</text>')
    o.append(f'<text class="t" x="{W - R}" y="{axis_y + 16}" text-anchor="end">{t["axis"]}</text>')
    for k, (label, val) in enumerate(t["rows"]):
        y0 = TOP + ROW * k
        o.append(f'<text class="tb" x="{L}" y="{y0 + 14}">{label}</text>'
                 f'<text class="t" x="{W - R}" y="{y0 + 14}" text-anchor="end">{val}</text>')
        o.append(f'<rect class="f-mute" x="{L}" y="{y0 + 26}" width="{W - L - R}" height="12" rx="6"/>')
        if k < len(ranges):
            lo, hi, fill = ranges[k]
            o.append(f'<rect class="bar h {fill}" style="--d:{k * 140}ms" x="{x(lo):.1f}" y="{y0 + 26}" width="{x(hi) - x(lo):.1f}" height="12" rx="6"/>')
            if k == 2:
                o.append(f'<circle class="dot" cx="{x(65):.1f}" cy="{y0 + 32}" r="4"/>')
        else:
            lo, hi = min(WEEK), max(WEEK)
            o.append(f'<rect class="bar h f-green" style="--d:{k * 140}ms" x="{x(lo):.1f}" y="{y0 + 26}" width="{x(hi) - x(lo):.1f}" height="12" rx="6"/>')
    o.append(f'</svg><figcaption>{t["cap"]}</figcaption></figure>')
    return "".join(o)


KEYS = {
    "en": [("60–100", "beats per minute: the textbook adult range", "American Heart Association"),
           ("40–109", "bpm: personal averages across 92,457 wearable users", "Quer et al. 2020"),
           ("~3 bpm", "average day-to-day change in one person's resting rate", "Quer et al. 2020")],
    "hu": [("60–100", "/perc: a tankönyvi tartomány felnőtteknél", "American Heart Association"),
           ("40–109", "/perc: személyes átlagok 92 457 okosóra-viselőnél", "Quer és mtsai, 2020"),
           ("~3", "ütés/perc: ennyit mozdul átlagosan egy ember nyugalmi pulzusa egyik napról a másikra", "Quer és mtsai, 2020")],
    "de": [("60–100", "Schläge pro Minute: der Lehrbuchbereich für Erwachsene", "American Heart Association"),
           ("40–109", "Schläge pro Minute: persönliche Mittel bei 92.457 Wearable-Nutzern", "Quer et al. 2020"),
           ("~3", "Schläge: mittlere Schwankung des Ruhepulses eines Menschen von Tag zu Tag", "Quer et al. 2020")],
}
PULL = {
    "en": "A low resting heart rate is not a score to chase.",
    "hu": "Az alacsony nyugalmi pulzus nem rekord, amit hajszolni kell.",
    "de": "Ein niedriger Ruhepuls ist kein Rekord, den man jagen sollte.",
}
SHOT = {
    "en": ("Aera's Resting HR tile: 53 bpm, marked Typical, with a dot inside the person's usual band",
           "Resting heart rate in Aera",
           "The tile holds the resting heart rate from Apple Health against your own last two weeks and says Typical, Above your usual or Notably high (or the same downward). With fewer than seven days of readings it says Building baseline."),
    "hu": ("Az Aera Nyugalmi pulzus csempéje: 53/perc, Tipikus jelzés, a pont a saját megszokott sávon belül",
           "Nyugalmi pulzus az Aerában",
           "A csempe az Apple Health nyugalmi pulzusát az elmúlt két heted értékeihez méri, és ennyit ír: Tipikus, A szokásos fölött vagy Feltűnően magas (lefelé ugyanígy). Ha hét napnál kevesebb mérésed van, ezt látod: Alapérték készül."),
    "de": ("Die Kachel Ruheherzfrequenz in Aera: 53 bpm, Typisch, mit einem Punkt im eigenen üblichen Band",
           "Ruhepuls in Aera",
           "Die Kachel misst die Ruheherzfrequenz aus Apple Health an deinen eigenen letzten zwei Wochen und zeigt Typisch, Höher als üblich oder Auffällig hoch (und dasselbe nach unten). Mit weniger als sieben Tagen Messungen steht dort Lernphase."),
}

ARTICLES = {}
for lang, fn in [("en", "apple-watch-resting-heart-rate.html"),
                 ("hu", "nyugalmi-pulzus-apple-watch.html"),
                 ("de", "ruhepuls-apple-watch.html")]:
    ARTICLES[fn] = (lang, [
        ("lead", "keys", keys(KEYS[lang])),
        ("h2:2", "pull", pull(PULL[lang])),
        ("h2:3", "fig", rhr_spread(lang)),
        ("aera", "shot", shot("resting-hr", *SHOT[lang], w=364, h=320)),
    ])
