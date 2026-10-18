"""Run-after-bad-sleep guides (EN/HU/DE)."""
from article_kit import keys, shot, pull

BS_KEYS = {
    "en": [("8 weeks", "of HRV-guided training: recreational runners did at least as well as on a fixed plan", "Vesterinen et al. 2016"),
           ("1 week", "rolling average: read HRV against your own baseline, not one morning", "Plews et al. 2013"),
           ("10 min", "of easy running, then check in, on any doubtful morning", "This guide")],
    "hu": [("8 hét", "HRV szerint igazított edzés: a hobbifutók legalább olyan jól jártak, mint rögzített tervvel", "Vesterinen és mtsai, 2016"),
           ("1 hét", "mozgóátlaga: a HRV-t a saját alapszintedhez mérd, ne egy reggelhez", "Plews és mtsai, 2013"),
           ("10 perc", "laza futás után figyelj magadra minden bizonytalan reggelen", "Ez az útmutató")],
    "de": [("8 Wochen", "HRV-gesteuertes Training: Freizeitläufer fuhren mindestens so gut wie mit festem Plan", "Vesterinen et al. 2016"),
           ("1 Woche", "gleitender Schnitt: HRV am eigenen Ausgangswert lesen, nicht an einem Morgen", "Plews et al. 2013"),
           ("10 Min.", "locker loslaufen, dann in dich hineinhorchen, an jedem unsicheren Morgen", "Dieser Ratgeber")],
}

BS_PULL = {
    "en": "After a short night, the same pace simply feels harder.",
    "hu": "Rövid éjszaka után ugyanaz a tempó egyszerűen nehezebbnek érződik.",
    "de": "Nach einer kurzen Nacht fühlt sich dasselbe Tempo einfach schwerer an.",
}

BS_SHOT = {
    "en": ("Aera's Sleep chart: the last seven nights drawn against a shaded band marked Your need, from a 6h 40m night to an 8h 27m one",
           "Your nights against your need",
           "Aera's Sleep tab draws your last seven nights against the sleep need it learned from your own nights, so one short night and a run of them look different at a glance."),
    "hu": ("Az Aera alvásgrafikonja: az utolsó hét éjszaka egy „Az igényed” feliratú sávhoz mérve, egy 6 óra 40 perces és egy 8 óra 27 perces éjszakával",
           "Az éjszakáid az igényedhez mérve",
           "Az Aera Alvás lapja az utolsó hét éjszakádat a saját éjszakáidból tanult alvásigényedhez méri, így első ránézésre látszik, hogy egyetlen rövid éjszakáról van szó, vagy már egy sorozatról."),
    "de": ("Aeras Schlafdiagramm: die letzten sieben Nächte vor einem Band mit der Aufschrift Dein Bedarf, von einer Nacht mit 6 Std. 40 Min. bis zu einer mit 8 Std. 27 Min.",
           "Deine Nächte gegen deinen Bedarf",
           "Der Schlaf-Tab von Aera zeigt deine letzten sieben Nächte vor dem Schlafbedarf, den Aera aus deinen eigenen Nächten gelernt hat. So siehst du auf einen Blick, ob es eine kurze Nacht war oder schon eine Reihe."),
}

# ---- figure: the four answers of the guide as a grid of signals ----
FIG_T = {
    "en": dict(title="A bad night is one column, not the whole answer.",
               cols=[["Sleep"], ["Resting HR"], ["HRV"], ["Week"], ["Feel"]],
               rows=["Hard", "Normal", "Easy", "Rest"],
               legend=["as usual", "a little off", "clearly off"],
               cap="<b>Illustration of the guide.</b> Each row is one example morning for that answer, every signal read against your own usual. One bad night, with everything else normal or a little off, points to an easy run. Rest comes when it stacks up with heart signals off for more than one morning and a heavy week. Fever, aches or feeling ill mean rest on their own."),
    "hu": dict(title="A rossz éjszaka csak az egyik oszlop, nem a teljes válasz.",
               cols=[["Alvás"], ["Nyugalmi", "pulzus"], ["HRV"], ["Hét"], ["Közérzet"]],
               rows=["Keményen", "A szokásos", "Csak lazán", "Pihenj"],
               legend=["rendben", "kicsit eltér", "jócskán eltér"],
               cap="<b>Szemléltetés az útmutatóhoz.</b> Minden sor egy-egy példa-reggel az adott válaszhoz, minden jel a saját szokásodhoz mérve. Ha csak az éjszaka volt rossz, és minden más rendben van vagy kicsit eltér, akkor laza futás. Pihenés akkor jön, ha ehhez több reggelen át eltérő szívjelek és egy kemény hét is társul. Láz, izomfájdalom vagy rossz közérzet önmagában is pihenőt jelent."),
    "de": dict(title="Die schlechte Nacht ist nur eine Spalte, nicht die ganze Antwort.",
               cols=[["Schlaf"], ["Ruhepuls"], ["HRV"], ["Woche"], ["Gefühl"]],
               rows=["Hart", "Wie geplant", "Locker", "Pause"],
               legend=["wie üblich", "etwas daneben", "klar daneben"],
               cap="<b>Illustration zur Entscheidungshilfe.</b> Jede Zeile ist ein Beispielmorgen für diese Antwort, jedes Signal an deinem eigenen Üblichen gemessen. Eine schlechte Nacht, sonst alles normal oder nur etwas daneben, spricht für einen lockeren Lauf. Pause heißt es, wenn dazu Herzwerte über mehr als einen Morgen daneben liegen und eine harte Woche kommt. Fieber, Gliederschmerzen oder Krankheitsgefühl bedeuten für sich allein schon Pause."),
}

# 0 = as usual, 1 = a little off, 2 = clearly off. Columns: sleep, resting HR, HRV, week, feel.
GRID = [
    [0, 0, 0, 0, 0],  # hard
    [1, 0, 0, 0, 0],  # normal: night a bit short
    [2, 1, 1, 0, 0],  # easy: one bad night, heart a little off
    [2, 2, 2, 2, 2],  # rest: it all stacks up
]
FILL = ["f-green", "f-gold", "f-pink"]


def bad_sleep_fig(lang):
    t = FIG_T[lang]
    W, H = 360, 226
    cx = [106, 160, 214, 268, 322]
    head_y = 22
    row_y = [62, 98, 134, 170]
    o = [f'<figure class="fig"><p class="fig-h">{t["title"]}</p><svg viewBox="0 0 {W} {H}" role="img" aria-label="{t["title"]}">']
    for c, lines in zip(cx, t["cols"]):
        y0 = head_y - (len(lines) - 1) * 13
        for k, line in enumerate(lines):
            o.append(f'<text class="t" x="{c}" y="{y0 + 13 * k + 14}" text-anchor="middle">{line}</text>')
    for r, (ry, label) in enumerate(zip(row_y, t["rows"])):
        o.append(f'<line class="grid" x1="2" x2="{W - 2}" y1="{ry - 18}" y2="{ry - 18}"/>')
        o.append(f'<text class="tb" x="2" y="{ry + 4.5}">{label}</text>')
        for k, c in enumerate(cx):
            o.append(f'<circle class="dot {FILL[GRID[r][k]]}" style="transition-delay:{(r * 5 + k) * 40}ms" cx="{c}" cy="{ry}" r="8"/>')
    o.append(f'<line class="grid" x1="2" x2="{W - 2}" y1="{row_y[-1] + 18}" y2="{row_y[-1] + 18}"/>')
    ly = H - 8
    for k, (lx, label) in enumerate(zip([8, 124, 240], t["legend"])):
        o.append(f'<circle class="dot {FILL[k]}" cx="{lx}" cy="{ly - 4}" r="5"/><text class="t" x="{lx + 11}" y="{ly}">{label}</text>')
    o.append(f'</svg><figcaption>{t["cap"]}</figcaption></figure>')
    return "".join(o)


ARTICLES = {}
for lang, fn in [
    ("en", "should-i-run-after-bad-sleep.html"),
    ("hu", "fussak-ha-rosszul-aludtam.html"),
    ("de", "laufen-nach-schlechtem-schlaf.html"),
]:
    ARTICLES[fn] = (lang, [
        ("lead", "keys", keys(BS_KEYS[lang])),
        ("h2:0", "pull", pull(BS_PULL[lang])),
        ("h2:2", "fig", bad_sleep_fig(lang)),
        ("aera", "shot", shot("bad-sleep", *BS_SHOT[lang], w=640, h=276)),
    ])
