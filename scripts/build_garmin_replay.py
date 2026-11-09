#!/usr/bin/env python3
"""The Garmin replay guides (EN, HU, DE): how to bring a run's route into Aera from a
Garmin, Polar, COROS or Suunto file, so the 3D replay can fly it.

    python3 scripts/build_garmin_replay.py && python3 scripts/add_lang.py && python3 scripts/build_guides_index.py

Each page borrows its frame (top bar, footer, scripts) from the same language's Garmin
guide, so the look stays the guides' own. The words follow the app's own labels in
Settings, Devices, Import workouts (SettingsImportPage.swift, Aera 4.0). The store
button goes through /get/guide-garmin-replay/<lang>/, so taps count per language.
"""
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://aerahealth.app/guides/"
DATE = "2026-11-09"
FILES = {"en": "replay-a-garmin-run-in-3d.html", "hu": "garmin-futas-3d-visszajatszasa.html",
         "de": "garmin-lauf-in-3d-abspielen.html"}
FRAME = {"en": "garmin-data-on-iphone-explained.html", "hu": "garmin-adatok-iphone-on.html",
         "de": "garmin-daten-auf-dem-iphone-erklaert.html"}
LSW = re.compile(r"<!--lsw-->.*?<!--/lsw-->\n?", re.S)

T = {
"en": dict(
    title="Replay a Garmin run in 3D on iPhone: export the file, open it in Aera",
    og="Replay a Garmin run in 3D",
    desc="Garmin Connect sends runs to Apple Health without the route. Export the run's file from Garmin, Polar, COROS or Suunto, open it in Aera, and replay it in 3D.",
    kind="How to · Devices",
    h1="How do I replay my Garmin run in 3D?",
    alt="A run replayed in 3D over the real ground in Aera, with distance, pace and heart rate",
    cap="A 3D replay in Aera.",
    answer="<strong>Export the run as a file and open it in Aera.</strong> Garmin Connect puts your runs into Apple Health without the GPS route, so there is no line to fly over. The run's file has it. Aera keeps that route on your iPhone next to the run, and Flyover replays it in 3D over the real ground. Needs Aera 4.0 or later.",
    toc="On this page",
    s=[
     ("Why the route is missing",
      "<p>Garmin Connect writes your runs to Apple Health with their time, distance and heart rate, but not the route. Only the app that saved a workout can add a route to it later, so no other app can put it back in Apple Health.</p>"
      "<p>When you give Aera the run's file, it reads the route from it and keeps it on this iPhone, next to the run Garmin already saved. The map and the replay use it from then on. The route stays on the phone and is left out of backups. There is no account and no upload.</p>"),
     ("Export a run from Garmin Connect",
      "<ol><li>Open <strong>connect.garmin.com</strong> in a browser and sign in. On iPhone, if the page sends you to the app, tap <strong>aA</strong> and choose <strong>Request Desktop Website</strong>.</li>"
      "<li>Open the run, tap the <strong>gear</strong> at the top right and choose <strong>Export Original</strong>. You get a zip with the run's FIT file. <strong>Export to GPX</strong> or <strong>Export to TCX</strong> works too.</li>"
      "<li>On a computer, AirDrop or mail the file to your iPhone, or save it to iCloud Drive.</li></ol>"
      "<p><strong>Your whole history at once:</strong> in your Garmin account, Data Management, then Export Your Data, tap <strong>Request Data Export</strong>. Garmin mails you a link to one zip, which can take a few days. Aera reads that zip as it is.</p>"),
     ("Polar, COROS and Suunto",
      "<ul><li><strong>Polar Flow:</strong> on flow.polar.com, open the session from your diary, then <strong>Export</strong> at the top right. Choose FIT or GPX.</li>"
      "<li><strong>COROS:</strong> in the COROS app, open the activity, tap the three dots at the top right, then <strong>Export Data</strong>, and choose FIT.</li>"
      "<li><strong>Suunto:</strong> in the Suunto app, open the workout, tap the three dots at the top right and export it as FIT or GPX.</li></ul>"
      "<p>Menu names come from each maker's own help pages and can change with their app versions.</p>"),
     ("Open it in Aera",
      "<p>Either way works:</p><ul>"
      "<li><strong>From Files, Mail or a share button:</strong> share the file to Aera. For one run, Aera asks what it is: tap <strong>Add as a workout</strong>. A zip goes straight to the import.</li>"
      "<li><strong>From Aera:</strong> Settings, then <strong>Devices</strong>, then <strong>Import workouts</strong>, and <strong>Choose export or files</strong>.</li></ul>"
      "<p>Aera shows what it found before it changes anything. If Apple Health already has the run from Garmin, you see <strong>GPS tracks to keep</strong>: tap <strong>Keep GPS tracks in Aera</strong>. If Apple Health doesn't have it, tap <strong>Add workouts to Apple Health</strong>, and Aera saves the run with its route.</p>"),
     ("Watch the replay",
      "<p>Open the run in Aera and tap <strong>Flyover</strong>. The camera flies the route over the real ground, with distance, pace and heart rate running underneath. From the replay you can save a short upright video to Photos.</p>"
      "<p>Runs from the last 7 days replay free. Older runs replay with Premium. The replay is only as exact as the GPS that recorded the route. More in <a href=\"../flyover.html\">the 3D replay</a>.</p>"),
    ],
    note_t="Aera, for iPhone",
    note="Aera reads what your watch puts into Apple Health and holds it against your own normal. Tap a number and the Field Guide shows how it was worked out. Everything stays on your iPhone, with no account. Aera is not a medical device.",
    btn="Get Aera on the App Store",
    faq_t="Quick answers",
    faq=[
     ("Can Aera get the route from Garmin by itself?", "No. Garmin Connect doesn't write the route to Apple Health, and Aera has no Garmin account link, so the route comes from a file you export."),
     ("Which files work?", "FIT, GPX and TCX, zipped or not, and a whole Garmin or Strava export zip."),
     ("Will the run show up twice?", "No. A run counts as already in Apple Health when Health has one at the same time, even under another sport. Aera then only keeps its route."),
     ("Does the file leave my iPhone?", "No. Aera reads it on the phone and keeps the route there, out of backups. There is no account."),
     ("Has this been tested with every watch?", "No. The import reads the FIT, GPX and TCX formats these makers use, but we have not tried every watch and app version. If a file doesn't open, write to us from the support page."),
    ],
    related="Related", rel=[("garmin-data-on-iphone-explained.html", "Garmin data on iPhone, explained"), ("aera-with-garmin-oura-whoop.html", "Aera with Garmin, Oura, WHOOP and other trackers"), ("index.html", "All guides")],
),
"hu": dict(
    title="Garmin-futás 3D visszajátszása iPhone-on: exportáld a fájlt, nyisd meg az Aerában",
    og="Garmin-futás visszajátszása 3D-ben",
    desc="A Garmin Connect útvonal nélkül küldi a futásokat az Apple Health-be. Exportáld a futás fájlját a Garminból, Polarból, COROS-ból vagy Suuntóból, nyisd meg az Aerában, és játszd vissza 3D-ben.",
    kind="A gyakorlatban · Eszközök",
    h1="Hogyan játszhatom vissza 3D-ben a Garminnal futott futásomat?",
    alt="Egy futás 3D visszajátszása a valódi terep fölött az Aerában, távval, tempóval és pulzussal",
    cap="3D visszajátszás az Aerában.",
    answer="<strong>Exportáld a futást fájlként, és nyisd meg az Aerában.</strong> A Garmin Connect a GPS-útvonal nélkül írja a futásaidat az Apple Health-be, így nincs mit végigrepülni. A futás fájljában viszont benne van. Az Aera ezt az útvonalat az iPhone-odon tartja a futás mellett, a Flyover pedig 3D-ben, a valódi terep fölött játssza vissza. Az Aera 4.0 vagy újabb kell hozzá.",
    toc="Ezen az oldalon",
    s=[
     ("Miért hiányzik az útvonal?",
      "<p>A Garmin Connect idővel, távval és pulzussal írja a futásaidat az Apple Health-be, de útvonal nélkül. Egy edzéshez utólag csak az az app adhat útvonalat, amelyik elmentette, ezért más app nem tudja visszatenni az Apple Health-be.</p>"
      "<p>Ha odaadod az Aerának a futás fájlját, kiolvassa belőle az útvonalat, és ezen az iPhone-on tartja, a Garmin által már elmentett futás mellett. Innentől a térkép és a visszajátszás ezt használja. Az útvonal a telefonon marad, a biztonsági mentésbe sem kerül. Nincs fiók, nincs feltöltés.</p>"),
     ("Futás exportálása a Garmin Connectből",
      "<ol><li>Nyisd meg a <strong>connect.garmin.com</strong> oldalt böngészőben, és jelentkezz be. iPhone-on, ha az oldal az appba küld, koppints az <strong>aA</strong> gombra, és kérd az asztali webhelyet.</li>"
      "<li>Nyisd meg a futást, koppints a jobb felső <strong>fogaskerékre</strong>, és válaszd az eredeti fájl exportálását (<strong>Export Original</strong>). Egy zipet kapsz a futás FIT-fájljával. A GPX- és a TCX-export is jó.</li>"
      "<li>Számítógépről AirDroppal vagy e-mailben küldd át a fájlt az iPhone-odra, vagy mentsd az iCloud Drive-ra.</li></ol>"
      "<p><strong>Az egész előzményed egyszerre:</strong> a Garmin-fiókodban az adatkezelésnél (Data Management, Export Your Data) koppints a <strong>Request Data Export</strong> gombra. A Garmin e-mailben küld egy linket egyetlen zipre, ez néhány napig is eltarthat. Az Aera ezt a zipet úgy olvassa, ahogy van.</p>"),
     ("Polar, COROS és Suunto",
      "<ul><li><strong>Polar Flow:</strong> a flow.polar.com oldalon nyisd meg az edzést a naplóból, majd jobb fent az <strong>Export</strong> menüben válaszd a FIT-et vagy a GPX-et.</li>"
      "<li><strong>COROS:</strong> a COROS appban nyisd meg az edzést, koppints a jobb felső három pöttyre, majd az adatok exportálására, és válaszd a FIT-et.</li>"
      "<li><strong>Suunto:</strong> a Suunto appban nyisd meg az edzést, koppints a jobb felső három pöttyre, és exportáld FIT vagy GPX formában.</li></ul>"
      "<p>A menük nevét a gyártók saját súgójából vettük, az appjaik frissítéseivel változhatnak.</p>"),
     ("Megnyitás az Aerában",
      "<p>Két út van:</p><ul>"
      "<li><strong>A Fájlokból, a Mailből vagy egy megosztás gombbal:</strong> oszd meg a fájlt az Aerával. Egy futásnál az Aera megkérdezi, mi ez: koppints a <strong>Hozzáadás edzésként</strong> gombra. A zip egyenesen az importáláshoz megy.</li>"
      "<li><strong>Az Aerából:</strong> Beállítások, majd <strong>Eszközök</strong>, majd <strong>Edzések importálása</strong>, és <strong>Export vagy fájlok kiválasztása</strong>.</li></ul>"
      "<p>Az Aera előbb megmutatja, mit talált, és csak utána változtat bármin. Ha az Apple Health-ben már megvan a futás a Garmintól, a <strong>Megtartandó GPS-útvonalak</strong> sort látod: koppints a <strong>GPS-útvonalak megtartása az Aerában</strong> gombra. Ha az Apple Health-ben nincs meg, koppints az <strong>Edzések hozzáadása az Apple Health-hez</strong> gombra, és az Aera az útvonalával együtt menti a futást.</p>"),
     ("A visszajátszás",
      "<p>Nyisd meg a futást az Aerában, és koppints a <strong>Flyover</strong> gombra. A kamera a valódi terep fölött repüli végig az útvonalat, alul fut a táv, a tempó és a pulzus. A visszajátszásból rövid, álló videót menthetsz a Fotókba.</p>"
      "<p>Az elmúlt 7 nap futásai ingyen játszhatók vissza, a régebbiek a Premiummal. A visszajátszás csak annyira pontos, mint a GPS, amely az útvonalat rögzítette. Bővebben: <a href=\"futas-3d-visszajatszas.html\">futás 3D visszajátszása</a>.</p>"),
    ],
    note_t="Aera, iPhone-ra",
    note="Az Aera azt olvassa, amit az órád az Apple Health-be ír, és a saját megszokott szintedhez méri. Koppints egy számra, és a Field Guide megmutatja, hogyan jött ki. Minden az iPhone-odon marad, fiók nélkül. Az Aera nem orvostechnikai eszköz.",
    btn="Töltsd le az App Store-ból",
    faq_t="Gyors válaszok",
    faq=[
     ("Meg tudja szerezni az Aera magától az útvonalat a Garmintól?", "Nem. A Garmin Connect nem írja az útvonalat az Apple Health-be, és az Aera nem kapcsolódik Garmin-fiókhoz, ezért az útvonal egy általad exportált fájlból jön."),
     ("Milyen fájlok jók?", "FIT, GPX és TCX, tömörítve vagy anélkül, és a teljes Garmin- vagy Strava-export zip is."),
     ("Kétszer fog megjelenni a futás?", "Nem. Egy futás akkor számít már meglévőnek az Apple Health-ben, ha ott ugyanabban az időben van egy edzés, akár más sportágként is. Ilyenkor az Aera csak az útvonalát tartja meg."),
     ("Elhagyja a fájl az iPhone-omat?", "Nem. Az Aera a telefonon olvassa be, és ott tartja az útvonalat, a biztonsági mentésen kívül. Nincs fiók."),
     ("Minden órával kipróbáltátok?", "Nem. Az importálás a gyártók által használt FIT, GPX és TCX formátumot olvassa, de nem próbáltunk ki minden órát és appverziót. Ha egy fájl nem nyílik meg, írj nekünk a támogatási oldalról."),
    ],
    related="Kapcsolódó", rel=[("garmin-adatok-iphone-on.html", "Garmin-adatok az iPhone-on"), ("aera-garmin-oura-whoop-vel.html", "Az Aera Garminnal, Ourával, WHOOP-pal és más eszközökkel"), ("index.html#hu", "Összes útmutató")],
),
"de": dict(
    title="Einen Garmin-Lauf in 3D abspielen auf dem iPhone: Datei exportieren, in Aera öffnen",
    og="Einen Garmin-Lauf in 3D abspielen",
    desc="Garmin Connect schickt Läufe ohne Route an Apple Health. Exportiere die Datei des Laufs aus Garmin, Polar, COROS oder Suunto, öffne sie in Aera und spiel ihn in 3D ab.",
    kind="Praxis · Geräte",
    h1="Wie spiele ich meinen Garmin-Lauf in 3D ab?",
    alt="Ein Lauf in Aera als 3D-Wiedergabe über echtem Gelände mit Distanz, Tempo und Puls",
    cap="Eine 3D-Wiedergabe in Aera.",
    answer="<strong>Exportiere den Lauf als Datei und öffne sie in Aera.</strong> Garmin Connect legt deine Läufe ohne GPS-Route in Apple Health ab, also gibt es keine Linie zum Abfliegen. Die Datei des Laufs hat sie. Aera behält diese Route auf deinem iPhone beim Lauf, und Flyover spielt sie in 3D über echtem Gelände ab. Dafür brauchst du Aera 4.0 oder neuer.",
    toc="Auf dieser Seite",
    s=[
     ("Warum die Route fehlt",
      "<p>Garmin Connect schreibt deine Läufe mit Zeit, Distanz und Puls in Apple Health, aber ohne Route. Eine Route kann später nur die App ergänzen, die das Training gespeichert hat. Keine andere App kann sie also in Apple Health nachtragen.</p>"
      "<p>Gibst du Aera die Datei des Laufs, liest Aera die Route daraus und behält sie auf diesem iPhone, beim Lauf, den Garmin schon gespeichert hat. Karte und Wiedergabe nutzen sie ab dann. Die Route bleibt auf dem Telefon und ist nicht im Backup. Kein Konto, kein Upload.</p>"),
     ("Einen Lauf aus Garmin Connect exportieren",
      "<ol><li>Öffne <strong>connect.garmin.com</strong> im Browser und melde dich an. Schickt dich die Seite auf dem iPhone in die App, tippe auf <strong>aA</strong> und wähle die Desktop-Website.</li>"
      "<li>Öffne den Lauf, tippe oben rechts auf das <strong>Zahnrad</strong> und wähle <strong>Original exportieren</strong> (Export Original). Du bekommst eine ZIP mit der FIT-Datei des Laufs. Der Export als GPX oder TCX geht auch.</li>"
      "<li>Am Computer schick die Datei per AirDrop oder Mail an dein iPhone, oder leg sie in iCloud Drive.</li></ol>"
      "<p><strong>Dein ganzer Verlauf auf einmal:</strong> In deinem Garmin-Konto unter Datenverwaltung (Data Management, Export Your Data) tippst du auf <strong>Request Data Export</strong>. Garmin schickt dir einen Link zu einer ZIP, das kann ein paar Tage dauern. Aera liest diese ZIP so, wie sie ist.</p>"),
     ("Polar, COROS und Suunto",
      "<ul><li><strong>Polar Flow:</strong> Öffne auf flow.polar.com die Einheit aus deinem Tagebuch, dann oben rechts <strong>Exportieren</strong>. Wähle FIT oder GPX.</li>"
      "<li><strong>COROS:</strong> Öffne in der COROS-App die Aktivität, tippe oben rechts auf die drei Punkte, dann auf Daten exportieren, und wähle FIT.</li>"
      "<li><strong>Suunto:</strong> Öffne in der Suunto-App das Training, tippe oben rechts auf die drei Punkte und exportiere es als FIT oder GPX.</li></ul>"
      "<p>Die Menünamen stammen aus den Hilfeseiten der Hersteller und können sich mit ihren App-Versionen ändern.</p>"),
     ("In Aera öffnen",
      "<p>Beides geht:</p><ul>"
      "<li><strong>Aus Dateien, Mail oder über Teilen:</strong> Teile die Datei mit Aera. Bei einem einzelnen Lauf fragt Aera, was er ist: Tippe auf <strong>Als Training hinzufügen</strong>. Eine ZIP geht direkt zum Import.</li>"
      "<li><strong>In Aera:</strong> Einstellungen, dann <strong>Geräte</strong>, dann <strong>Trainings importieren</strong>, und <strong>Export oder Dateien wählen</strong>.</li></ul>"
      "<p>Aera zeigt erst, was es gefunden hat, bevor es etwas ändert. Hat Apple Health den Lauf schon von Garmin, siehst du <strong>GPS-Strecken zum Behalten</strong>: Tippe auf <strong>GPS-Strecken in Aera behalten</strong>. Hat Apple Health ihn nicht, tippe auf <strong>Einheiten zu Apple Health hinzufügen</strong>, und Aera speichert den Lauf mit seiner Route.</p>"),
     ("Die Wiedergabe",
      "<p>Öffne den Lauf in Aera und tippe auf <strong>Flyover</strong>. Die Kamera fliegt die Route über echtem Gelände ab, unten laufen Distanz, Tempo und Puls mit. Aus der Wiedergabe kannst du ein kurzes Video im Hochformat in deinen Fotos sichern.</p>"
      "<p>Läufe der letzten 7 Tage spielst du kostenlos ab, ältere mit Premium. Die Wiedergabe ist nur so genau wie das GPS, das die Route aufgezeichnet hat. Mehr dazu: <a href=\"lauf-in-3d-abspielen.html\">einen Lauf in 3D abspielen</a>.</p>"),
    ],
    note_t="Aera, für iPhone",
    note="Aera liest, was deine Uhr in Apple Health ablegt, und misst es an deinem eigenen Normal. Tippe auf eine Zahl, und der Field Guide zeigt, wie sie entstanden ist. Alles bleibt auf deinem iPhone, ohne Konto. Aera ist kein Medizinprodukt.",
    btn="Aera im App Store laden",
    faq_t="Kurze Antworten",
    faq=[
     ("Holt sich Aera die Route selbst von Garmin?", "Nein. Garmin Connect schreibt die Route nicht in Apple Health, und Aera ist mit keinem Garmin-Konto verbunden. Die Route kommt also aus einer Datei, die du exportierst."),
     ("Welche Dateien gehen?", "FIT, GPX und TCX, gezippt oder nicht, und eine ganze Export-ZIP von Garmin oder Strava."),
     ("Taucht der Lauf dann doppelt auf?", "Nein. Ein Lauf gilt als schon in Apple Health, wenn dort eines zur selben Zeit liegt, auch unter einer anderen Sportart. Aera behält dann nur seine Route."),
     ("Verlässt die Datei mein iPhone?", "Nein. Aera liest sie auf dem Telefon und behält die Route dort, außerhalb des Backups. Es gibt kein Konto."),
     ("Ist das mit jeder Uhr getestet?", "Nein. Der Import liest die Formate FIT, GPX und TCX, die diese Hersteller nutzen, aber wir haben nicht jede Uhr und App-Version ausprobiert. Öffnet sich eine Datei nicht, schreib uns über die Support-Seite."),
    ],
    related="Verwandt", rel=[("garmin-daten-auf-dem-iphone-erklaert.html", "Garmin-Daten auf dem iPhone, erklärt"), ("aera-mit-garmin-oura-whoop.html", "Aera mit Garmin, Oura, WHOOP"), ("index.html#de", "Alle Ratgeber")],
),
}


def strip(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s))


def page(lang):
    t = T[lang]
    frame = open(os.path.join(ROOT, "guides", FRAME[lang]), encoding="utf-8").read()
    frame = LSW.sub("", frame)
    top = re.search(r'<div class="topbar">.*?</div></div>\n', frame, re.S).group(0)
    foot = re.search(r'<footer class="footer-base">.*?</footer>\n', frame, re.S).group(0)
    url = BASE + FILES[lang]
    alts = "".join('<link rel="alternate" hreflang="%s" href="%s">\n' % (l, BASE + f) for l, f in FILES.items())
    alts += '<link rel="alternate" hreflang="x-default" href="%s">\n' % (BASE + FILES["en"])
    article = {"@context": "https://schema.org", "@type": "HowTo", "name": t["h1"], "inLanguage": lang,
               "description": t["desc"], "image": "https://aerahealth.app/assets/guide/hero-replay-light.webp",
               "step": [{"@type": "HowToStep", "name": h, "text": strip(b)} for h, b in t["s"][1:5]]}
    article_ld = {"@context": "https://schema.org", "@type": "Article", "headline": t["og"], "name": t["title"],
                  "inLanguage": lang, "datePublished": DATE, "dateModified": DATE,
                  "image": "https://aerahealth.app/assets/guide/hero-replay-light.webp",
                  "author": {"@type": "Person", "name": "Gergő Varga"},
                  "publisher": {"@type": "Organization", "name": "Aera", "url": "https://aerahealth.app/"},
                  "mainEntityOfPage": url, "description": t["desc"]}
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": lang,
              "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in t["faq"]]}
    switch = " · ".join('<a href="%s" hreflang="%s" lang="%s"%s>%s</a>' % (f, l, l, ' aria-current="page"' if l == lang else "",
                                                                           {"en": "English", "hu": "Magyar", "de": "Deutsch"}[l])
                        for l, f in FILES.items())
    toc = "".join('<li><a href="#s%d">%s</a></li>' % (i + 1, html.escape(h)) for i, (h, _) in enumerate(t["s"]))
    toc += '<li><a href="#s%d">%s</a></li>' % (len(t["s"]) + 1, html.escape(t["faq_t"]))
    secs = "\n\n".join('<h2 id="s%d">%s</h2>\n%s' % (i + 1, html.escape(h), b) for i, (h, b) in enumerate(t["s"]))
    faq = "\n".join("<h3>%s</h3>\n<p>%s</p>" % (html.escape(q), html.escape(a)) for q, a in t["faq"])
    rel = " · ".join('<a href="%s">%s</a>' % (f, html.escape(n)) for f, n in t["rel"])
    n = len(t["s"]) + 1
    return """<!DOCTYPE html>
<html lang="%(lang)s">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="apple-itunes-app" content="app-id=6762456252">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
<meta property="og:title" content="%(og)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:type" content="article">
<meta property="og:image" content="https://aerahealth.app/assets/guide/hero-replay-light.webp">
<link rel="canonical" href="%(url)s">
%(alts)s<link rel="icon" href="../assets/icon.png">
<link rel="stylesheet" href="../article.css">
<script type="application/ld+json">
%(article)s
</script>
<script type="application/ld+json">
%(howto)s
</script>
<script type="application/ld+json">
%(faq_ld)s
</script>
<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{"token": "4fc0403d67364f1ab92526387bdd0b81"}'></script>
</head>
<body>
%(top)s<div class="wrap page-head">
  <p class="g-type">%(kind)s</p>
  <h1>%(h1)s</h1>
  <p class="meta lang-switch">%(switch)s</p>
<figure class="g-hero"><picture><source srcset="../assets/guide/hero-replay-dark.webp" media="(prefers-color-scheme: dark)"><img src="../assets/guide/hero-replay-light.webp" alt="%(alt)s" width="1206" height="1380" decoding="async"></picture><figcaption class="g-cap">%(cap)s</figcaption></figure>
</div>
<div class="wrap legal">
<p class="g-answer">%(answer)s</p>

<ul class="g-toc" aria-label="%(toc_l)s">%(toc)s</ul>
%(secs)s

<div class="note">
<p><strong>%(note_t)s</strong></p>
<p>%(note)s</p>
</div>
<p><a class="btn btn-primary" href="/get/guide-garmin-replay/%(lang)s/">%(btn)s</a></p>

<h2 id="s%(n)d">%(faq_t)s</h2>
%(faq)s
<p>%(related)s: %(rel)s</p>
</div>
%(foot)s<script src="../article.js" defer></script>
</body>
</html>
""" % dict(lang=lang, title=html.escape(t["title"]), desc=html.escape(t["desc"]), og=html.escape(t["og"]), url=url,
           alts=alts, article=json.dumps(article_ld, ensure_ascii=False), howto=json.dumps(article, ensure_ascii=False),
           faq_ld=json.dumps(faq_ld, ensure_ascii=False), top=top, kind=t["kind"], h1=html.escape(t["h1"]),
           switch=switch, alt=html.escape(t["alt"]), cap=t["cap"], answer=t["answer"], toc_l=t["toc"], toc=toc,
           secs=secs, note_t=t["note_t"], note=t["note"], btn=t["btn"], n=n, faq_t=t["faq_t"], faq=faq,
           related=t["related"], rel=rel, foot=foot)


def main():
    for lang, f in FILES.items():
        with open(os.path.join(ROOT, "guides", f), "w", encoding="utf-8") as out:
            out.write(page(lang))
        print("guides/" + f)


if __name__ == "__main__":
    main()
