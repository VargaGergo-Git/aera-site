#!/usr/bin/env python3
"""What's new in Aera, per release, in EN/HU/DE (one page per language, never mixed).

    python3 scripts/build_whats_new.py && python3 scripts/add_lang.py

Text follows the App Store What's New for each release (Marketing/store/<v>/text in the app
repo). Leave out anything that is off in the build (3.4: races and Events on the map).
Shell (head, nav, footer) is copied from support.html so the look matches.
"""
import html, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
FILES = {"en": "whats-new.html", "hu": "ujdonsagok.html", "de": "neuigkeiten.html"}

UI = {
    "en": {"title": "What's new in Aera", "eyebrow": "Aera", "h1": "What's new",
           "lead": "Replay your run. Understand your body.", "home": "index.html", "home_l": "Home",
           "desc": "Every Aera release and what it brought, newest first."},
    "hu": {"title": "Újdonságok az Aerában", "eyebrow": "Aera", "h1": "Újdonságok",
           "lead": "Nézd vissza a futásod. Értsd meg a tested.", "home": "hu.html", "home_l": "Főoldal",
           "desc": "Az Aera minden kiadása, és amit hozott, a legújabb elöl."},
    "de": {"title": "Neu in Aera", "eyebrow": "Aera", "h1": "Neu in Aera",
           "lead": "Erlebe deinen Lauf noch einmal. Versteh deinen Körper.", "home": "de.html", "home_l": "Startseite",
           "desc": "Jede Aera-Version und was sie gebracht hat, die neueste zuerst."},
}

# (version, date per language, intro, [(heading, text)], [also new])
RELEASES = {
"en": [("3.4", "November 2026",
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
"hu": [("3.4", "2026. november",
  "Az Aera eddigi legnagyobb frissítése, és a java a futóknak szól: a futásod újra, 3D-ben, minden teljesítményed a sajátjaidhoz mérve, és az óra, amit már most is hordasz.",
  [("A futásod újra, 3D-ben", "A 3D-s nézet filmként épült újra: négy élő érték, kameranézetek és térképstílusok. Az elmúlt hét minden futása ingyen visszanézhető, Prémiummal pedig álló videóként is megoszthatod."),
   ("Mennyire volt nehéz", "Bármelyik edzésnél koppints 1 és 10 között, és ha engeded, az Apple Healthbe is bekerül. A legjobb részidők megmondják, hol áll egy futás, például 41-ből a második leggyorsabb."),
   ("Trendek", "Kardió-fittség, nyugalmi pulzus, terhelés, állóképesség és még több. Mindegyik megmondja, mi változott, és hogy valódi-e a változás."),
   ("Bármilyen óra, vagy egy sem", "A Garmin, a Polar, a COROS és minden óra, ami az Apple Healthbe ír, most teljes oldalakat kap, és minden oldal világosan megmondja, mit tud kiolvasni, és mi adna hozzá még többet. A Polart közvetlenül is összekapcsolhatod, hogy az éjszakái és az edzései is bejöjjenek. Importálhatod a Garmin-exportokat és a FIT-, GPX- vagy TCX-fájlokat a GPS-nyomvonallal együtt, így 3D-ben is visszanézheted őket."),
   ("Milyen a napod?", "Mondd el az Aerának, milyen a napod, és jelölj pihenőt, ha beteg vagy, vagy elutaztál. A pontszámaid és az értesítéseid ezt is figyelembe veszik."),
   ("Az új Premium", "A pontszámaid minden nap, az elmúlt 30 nappal együtt, ingyenesek maradnak, és az elmúlt hét 3D-ben is. A Premium megőrzi a teljes előzményedet, minden edzésedet 3D-ben és a hosszabb jelentéseket, és az éves előfizetés egy ingyenes héttel indul.")],
  ["Az órádon: sportáganként választhatsz oldalakat, és követheted a kanyarokat.",
   "A Térkép műholdképpel nyílik. Forgasd és döntsd meg, és egy szakaszon a legjobb menetedet versenyeztetheted a legutóbbival.",
   "Az alváspontszámod hetekre és hónapokra, és a múlt éjszaka megosztható kártyaként.",
   "Vérnyomásjelentés PDF-ben, táblázatban vagy QR-kódként.",
   "Naponta legfeljebb három értesítés: a reggeled, a Milyen a napod? és a vérnyomás.",
   "A Siri elindítja, szünetelteti és befejezi az edzést. Útvonal tervezése a Vezérlőközpontból.",
   "Bővebb Field Guide: 16 érték újraírva és 10 új, mindegyik forrásokkal.",
   "Egy harmadik megjelenés: Szín."])],
"de": [("3.4", "November 2026",
  "Das größte Update, das Aera je hatte, und das meiste davon ist für alle, die laufen: dein Lauf noch einmal in 3D, jede Leistung an deinen eigenen gemessen, und die Uhr, die du schon trägst.",
  [("Dein Lauf, noch einmal, in 3D", "Die 3D-Ansicht ist als Film neu gebaut: vier Live-Werte, Kameraperspektiven und Kartenstile. Jeder Lauf der letzten Woche ist kostenlos, und mit Premium teilst du ihn als Video im Hochformat."),
   ("Wie anstrengend es war", "Tippe bei jedem Training 1 bis 10, mit deinem Okay auch in Apple Health. Bestleistungen sagen, wo ein Lauf steht, etwa zweitschnellster von 41."),
   ("Verläufe", "Kardiofitness, Ruhepuls, Anstrengung, Ausdauer und mehr. Jeder Verlauf sagt, was sich verändert hat und ob die Veränderung echt ist."),
   ("Jede Uhr, oder keine", "Garmin, Polar, COROS und jede Uhr, die in Apple Health schreibt, bekommen jetzt volle Seiten, und jede Seite sagt klar, was sie lesen kann und was mehr bringen würde. Verbinde Polar direkt für seine Nächte und Trainings. Importiere Garmin-Exporte und FIT-, GPX- oder TCX-Dateien mit ihrer GPS-Spur, bereit für die 3D-Ansicht."),
   ("Wie war heute?", "Sag Aera, wie sich der Tag anfühlt, und trag eine Auszeit ein, wenn du krank oder unterwegs bist. Deine Werte und Hinweise berücksichtigen das."),
   ("Premium, neu gebaut", "Deine Werte jeden Tag, mit ihren letzten 30 Tagen, bleiben kostenlos, und die letzte Woche in 3D auch. Premium behält deinen ganzen Verlauf, jede Aktivität in 3D und die längeren Berichte, und das Jahresabo beginnt mit einer kostenlosen Woche.")],
  ["Auf der Uhr: Seiten für jede Sportart wählen und Abbiegungen folgen.",
   "Die Karte öffnet als Satellitenbild. Dreh und neige sie, und auf einem Segment tritt dein bester Lauf gegen deinen letzten an.",
   "Dein Schlafwert über Wochen und Monate, und die letzte Nacht als Karte zum Teilen.",
   "Blutdruckberichte als PDF, Tabelle oder QR-Code.",
   "Höchstens drei Hinweise am Tag: dein Morgen, Wie war heute? und Blutdruck.",
   "Siri startet, pausiert und beendet ein Training. Route planen im Kontrollzentrum.",
   "Ein größerer Field Guide: 16 Werte neu geschrieben und 10 neue, jeweils mit Quellen.",
   "Ein dritter Look: Farbe."])],
}
NAV = {
    "en": [("guides/index.html", "Guides"), ("support.html", "Support")],
    "hu": [("guides/index.html#hu", "Útmutatók"), ("hu.html", "Főoldal")],
    "de": [("guides/index.html#de", "Ratgeber"), ("de.html", "Startseite")],
}
FOOT = {
    "hu": [('href="privacy.html">Privacy', 'href="adatvedelem.html">Adatvédelem'),
           ('href="terms.html">Terms', 'href="felhasznalasi-feltetelek.html">Felhasználási feltételek'),
           ('href="terms.html#eula">EULA', 'href="felhasznalasi-feltetelek.html">EULA')],
    "de": [('href="privacy.html">Privacy', 'href="privacy.html">Datenschutz'),
           ('href="terms.html">Terms', 'href="terms.html">Nutzungsbedingungen')],
}
ALSO = {"en": "Also new", "hu": "Még új", "de": "Außerdem neu"}

CSS = """<style>
.wn{max-width:680px;padding-bottom:48px}
.wn .lead{font-size:20px;line-height:1.35;margin:0 0 32px}
.wn article{border-top:1px solid color-mix(in srgb,currentColor 18%,transparent);padding-top:24px;margin-top:8px}
.wn .ver{display:flex;gap:12px;align-items:baseline;flex-wrap:wrap;margin:0 0 8px}
.wn .ver h2{margin:0}
.wn .ver span{opacity:.65;font-size:15px}
.wn h3{font-size:17px;margin:22px 0 4px}
.wn p,.wn li{font-size:16px;line-height:1.55}
.wn ul{padding-left:20px}
</style>"""

def page(lang):
    src = (ROOT / "support.html").read_text()
    head, rest = src.split('<div class="wrap page-head">', 1)
    foot = rest[rest.index("<footer"):]
    u = UI[lang]
    head = head.replace('<html lang="en">', f'<html lang="{lang}">')
    head = re.sub(r"<title>.*?</title>", f"<title>{html.escape(u['title'])} · Aera</title>", head)
    head = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{html.escape(u["desc"])}">', head)
    head = re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n?', "", head)
    alts = "".join(f'<link rel="alternate" hreflang="{l}" href="https://aerahealth.app/{f}">\n' for l, f in FILES.items())
    head = re.sub(r'<link rel="canonical" href="[^"]*">',
                  f'<link rel="canonical" href="https://aerahealth.app/{FILES[lang]}">\n' + alts.rstrip("\n"), head)
    head = re.sub(r'<nav class="topnav">.*?(<!--lsw-->|</nav>)',
                  lambda m: '<nav class="topnav">\n      ' + "\n      ".join(f'<a href="{h}">{t}</a>' for h, t in NAV[lang]) + "\n    " + m.group(1),
                  head, count=1, flags=re.S)
    head = head.replace("</head>", CSS + "\n</head>", 1)
    body = [f'<div class="wrap page-head">\n  <p class="eyebrow">{u["eyebrow"]}</p>\n  <h1>{u["h1"]}</h1>\n</div>',
            f'<main class="wrap wn">\n<p class="lead">{u["lead"]}</p>']
    for v, date, intro, parts, also in RELEASES[lang]:
        body.append(f'<article id="v{v.replace(".", "-")}">\n<div class="ver"><h2>Aera {v}</h2><span>{date}</span></div>\n<p>{intro}</p>')
        for h, t in parts:
            body.append(f"<h3>{h}</h3>\n<p>{t}</p>")
        body.append(f"<h3>{ALSO[lang]}</h3>\n<ul>" + "".join(f"<li>{a}</li>" for a in also) + "</ul>\n</article>")
    body.append("</main>\n")
    if lang != "en":
        foot = foot.replace('href="index.html">Home', f'href="{u["home"]}">{u["home_l"]}')
        for a, b in FOOT[lang]:
            foot = foot.replace(a, b)
    return head + "\n".join(body) + foot

for lang, f in FILES.items():
    (ROOT / f).write_text(page(lang))
    print(f)
