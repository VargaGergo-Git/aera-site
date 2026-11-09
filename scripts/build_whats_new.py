#!/usr/bin/env python3
"""What's new in Aera, per release, in EN/HU/DE (one page per language, never mixed).

    python3 scripts/build_whats_new.py && python3 scripts/add_chrome.py && python3 scripts/add_campaign.py

Text follows the App Store What's New for each release (Marketing/store/<v>/text in the app
repo). Leave out anything that is off in the build (4.0: races and Events on the map).
The <head> is copied from support.html; the header and footer are the shared ones,
filled in by add_chrome.py.
"""
import html, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
FILES = {"en": "whats-new.html", "hu": "ujdonsagok.html", "de": "neuigkeiten.html"}

UI = {
    "en": {"title": "What's new in Aera", "h1": "What's new",
           "lead": "Every number explained. No guessing.",
           "desc": "Every Aera release and what it brought, newest first."},
    "hu": {"title": "Újdonságok az Aerában", "h1": "Újdonságok",
           "lead": "Minden számhoz jár magyarázat. Semmi találgatás.",
           "desc": "Az Aera minden kiadása, és amit hozott, a legújabb elöl."},
    "de": {"title": "Neu in Aera", "h1": "Neu in Aera",
           "lead": "Jede Zahl erklärt. Kein Rätselraten.",
           "desc": "Jede Aera-Version und was sie gebracht hat, die neueste zuerst."},
}

# (version, date per language, intro, [(heading, text)], [also new])
# Each language is written for its own readers. Feature names are the app's own.
RELEASES = {
"en": [("4.0", "November 2026",
  "The biggest update Aera has had, and most of it is for runners: your run again in 3D, every effort against your own, and the watch you already wear.",
  [("Your run, again, in 3D", "The replay is rebuilt as a film: four live figures, camera views and map styles. Every run of the past week replays free, and with Premium you can share it as a vertical video."),
   ("How hard it felt", "Tap 1 to 10 on any workout, saved to Apple Health with your OK. Best efforts say where a run sits, like 2nd fastest of 41."),
   ("Trends", "Cardio fitness, resting heart rate, effort, endurance and more, each saying what changed and whether the change is real."),
   ("Any watch, or none", "Garmin, Polar, COROS and every watch that writes to Apple Health now get full pages, and each page says plainly what it can read and what would add more. Link Polar directly for its nights and workouts. Import Garmin exports and FIT, GPX or TCX files with their GPS tracks, ready to replay."),
   ("How's today?", "Tell Aera how the day feels, and mark time off when you are ill or away. Your scores and notes take it into account."),
   ("Premium, rebuilt", "Your scores every day, with their last 30 days, stay free, and so do the replays of the past week. Premium keeps your whole history, every replay and the longer reports, and the yearly plan starts with a free week.")],
  ["On your watch: pick the pages for each sport and follow turns.",
   "The Map opens on satellite. Turn and tilt it, and on a segment your best pass races your last.",
   "Your sleep score over weeks and months, and last night as a card to share.",
   "Blood pressure reports as a PDF, a spreadsheet or a QR code.",
   "At most three notes a day: your morning, How's today? and blood pressure.",
   "Siri starts, pauses and ends a workout. Plan a route from Control Center.",
   "A bigger Field Guide: 16 reads rebuilt and 10 new, each with its sources.",
   "A third look, Colour."])],
"hu": [("4.0", "2026. november",
  "Az Aera eddigi legnagyobb frissítése, és a java a futóknak szól: 3D-ben nézheted vissza a futásaidat, minden eredményedet a saját korábbi eredményeidhez mérheted, és azzal az órával is működik, amit most hordasz.",
  [("Megújult a visszajátszás", "A futásod most úgy pereg le, mint egy film: négy élő adat, többféle kameraállás és térképstílus. Az elmúlt hét futásait ingyen nézheted vissza, Premiummal pedig álló videóként meg is oszthatod."),
   ("Mennyire volt nehéz", "Bármelyik edzést értékelheted 1-től 10-ig, és ha engeded, az Apple Healthbe is bekerül. A legjobb részidőknél azt is látod, hol áll egy futás, például 41-ből a második leggyorsabb."),
   ("Trendek", "Kardiofittség, nyugalmi pulzus, erőkifejtés, állóképesség és még több. Mindegyiknél megmondja, mi változott, és hogy valódi-e a változás."),
   ("Bármilyen óra jó, de óra nélkül is megy", "A Garmin, a Polar, a COROS és minden óra, amelyik az Apple Healthbe ír, saját oldalt kapott. Mindegyik oldal világosan megmondja, mit tud kiolvasni, és mitől lenne teljesebb a kép. A Polart közvetlenül is összekapcsolhatod, így az éjszakáid és az edzéseid is megérkeznek. A Garmin-exportokat és a FIT-, GPX- vagy TCX-fájlokat a GPS-nyomvonalukkal együtt importálhatod, és már nézheted is vissza őket."),
   ("Milyen a napod?", "Megmondhatod az Aerának, hogy érzed magad, és jelezheted, ha beteg vagy, vagy elutaztál. A pontszámaid és az értesítéseid ezt is figyelembe veszik."),
   ("Az új Premium", "A napi pontszámaid az elmúlt 30 nappal együtt ingyenesek maradnak, ahogy az elmúlt hét visszajátszásai is. Premiummal megmarad a teljes előzményed, minden visszajátszás és a hosszabb jelentések is, az éves előfizetés pedig egy ingyenes héttel indul.")],
  ["Az órádon: sportáganként te választod ki az oldalakat, és a kanyarokat is mutatja.",
   "A Térkép műholdképpel nyílik. Forgathatod és dönthetsz rajta, egy szakaszon pedig a legjobb futásod versenyez a legutóbbival.",
   "Az alváspontszámod hetekre és hónapokra visszamenőleg, a múlt éjszakád pedig megosztható kártyán.",
   "Vérnyomásjelentés PDF-ben, táblázatban vagy QR-kóddal.",
   "Naponta legfeljebb három értesítés: a reggeled, a Milyen a napod? és a vérnyomás.",
   "A Sirivel elindíthatod, szüneteltetheted és befejezheted az edzést. Útvonalat a Vezérlőközpontból is tervezhetsz.",
   "Bővebb Field Guide: 16 cikk újraírva, 10 új, mindegyik forrásokkal.",
   "Egy harmadik megjelenés: Szín."])],
"de": [("4.0", "November 2026",
  "Das größte Update, das Aera je bekommen hat, und das meiste ist für alle, die laufen: dein Lauf noch einmal in 3D, jede Leistung im Vergleich mit deinen eigenen, und das alles mit der Uhr, die du schon trägst.",
  [("Die 3D-Wiedergabe, neu gebaut", "Dein Lauf läuft jetzt ab wie ein Film: vier Live-Werte, mehrere Kameraperspektiven und Kartenstile. Alle Läufe der letzten Woche spielst du kostenlos ab, und mit Premium teilst du sie als Hochkantvideo."),
   ("Wie anstrengend war es?", "Bewerte jedes Training von 1 bis 10. Wenn du magst, landet der Wert auch in Apple Health. Bei Bestzeiten siehst du, wo ein Lauf steht, zum Beispiel als zweitschnellster von 41."),
   ("Verläufe", "Cardiofitness, Ruhepuls, Aufwand, Ausdauer und mehr. Jeder Verlauf sagt dir, was sich verändert hat und ob die Veränderung echt ist."),
   ("Jede Uhr, oder gar keine", "Garmin, Polar, COROS und jede Uhr, die in Apple Health schreibt, haben jetzt eigene Seiten. Jede sagt klar, was sie auslesen kann und womit das Bild vollständiger würde. Polar verbindest du direkt, dann kommen auch deine Nächte und Trainings an. Garmin-Exporte sowie FIT-, GPX- und TCX-Dateien importierst du mitsamt GPS-Spur und kannst sie gleich abspielen."),
   ("Wie war heute?", "Sag Aera, wie sich dein Tag anfühlt, und trag eine Auszeit ein, wenn du krank oder verreist bist. Deine Werte und Mitteilungen berücksichtigen das."),
   ("Premium, neu gebaut", "Deine täglichen Werte samt der letzten 30 Tage bleiben kostenlos, genauso wie die Wiedergaben der letzten Woche. Mit Premium behältst du deinen ganzen Verlauf, jede Wiedergabe und die längeren Berichte. Das Jahresabo beginnt mit einer kostenlosen Woche.")],
  ["Auf der Uhr: Wähle für jede Sportart deine Seiten und lass dir das Abbiegen anzeigen.",
   "Die Karte öffnet sich als Satellitenbild. Du kannst sie drehen und neigen, und auf einem Segment tritt dein bester Lauf gegen deinen letzten an.",
   "Dein Schlafwert über Wochen und Monate, und die letzte Nacht als Karte zum Teilen.",
   "Blutdruckberichte als PDF, als Tabelle oder per QR-Code.",
   "Höchstens drei Mitteilungen am Tag: dein Morgen, Wie war heute? und Blutdruck.",
   "Siri startet, pausiert und beendet dein Training. Eine Route planst du auch direkt aus dem Kontrollzentrum.",
   "Ein größerer Field Guide: 16 Artikel überarbeitet und 10 neue, alle mit Quellen.",
   "Ein dritter Look: Farbe."])],
}
ALSO = {"en": "Also new", "hu": "Még új", "de": "Außerdem neu"}

CSS = """<style>
.wn{padding-bottom:72px}
.wn .lead{margin:0 0 36px}
.wn article{border-top:1px solid var(--rule);padding-top:28px;margin-top:8px}
.wn .ver{display:flex;gap:12px;align-items:baseline;flex-wrap:wrap;margin:0 0 10px}
.wn .ver h2{margin:0;font-size:clamp(30px,5vw,44px);letter-spacing:-.04em}
.wn .ver span{color:var(--ink-3);font-size:15px}
.wn h3{margin:26px 0 4px}
.wn p,.wn li{font-size:17px;line-height:1.55;color:var(--ink-2)}
.wn article>p:first-of-type{color:var(--ink);font-size:19px;line-height:1.45;font-weight:500;letter-spacing:-.015em}
.wn ul{padding-left:20px}
</style>"""


def page(lang):
    src = (ROOT / "support.html").read_text()
    head = src[:src.index("</head>")]
    u = UI[lang]
    head = head.replace('<html lang="en">', f'<html lang="{lang}">')
    head = re.sub(r"<!--chrome:head-->.*?<!--/chrome:head-->\n?", "", head, flags=re.S)
    head = re.sub(r"<style>.*?</style>\n?", "", head, flags=re.S)
    head = re.sub(r"<title>.*?</title>", f"<title>{html.escape(u['title'])} · Aera</title>", head)
    head = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{html.escape(u["desc"])}">', head)
    head = re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n?', "", head)
    alts = "".join(f'<link rel="alternate" hreflang="{l}" href="https://aerahealth.app/{f}">\n' for l, f in FILES.items())
    head = re.sub(r'<link rel="canonical" href="[^"]*">',
                  f'<link rel="canonical" href="https://aerahealth.app/{FILES[lang]}">\n' + alts.rstrip("\n"), head)
    head += CSS + "\n</head>\n<body>\n<!--chrome:header--><!--/chrome:header-->\n"
    body = [f'<div class="wrap page-head">\n  <h1>{u["h1"]}</h1>\n</div>',
            f'<main class="wrap wn">\n<p class="lede lead">{u["lead"]}</p>']
    for v, date, intro, parts, also in RELEASES[lang]:
        body.append(f'<article id="v{v.replace(".", "-")}">\n<div class="ver"><h2>Aera {v}</h2><span>{date}</span></div>\n<p>{intro}</p>')
        for h, t in parts:
            body.append(f"<h3>{h}</h3>\n<p>{t}</p>")
        body.append(f"<h3>{ALSO[lang]}</h3>\n<ul>" + "".join(f"<li>{a}</li>" for a in also) + "</ul>\n</article>")
    body.append("</main>\n")
    return head + "\n".join(body) + "<!--chrome:footer--><!--/chrome:footer-->\n</body>\n</html>\n"


for lang, f in FILES.items():
    (ROOT / f).write_text(page(lang))
    print(f)
