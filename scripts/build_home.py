#!/usr/bin/env python3
"""Builds the homepage in three languages: index.html (en), hu.html, de.html.

    python3 scripts/build_home.py

Copy lives in COPY below, the look in home.css, motion in home.js. Every claim
here must match the live app (store copy in the app repo's Marketing/store/).
Loops are not promised until the 3.2.1 fix is live.
"""
import html
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import landscape  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Once a custom domain is live, the CNAME file names it and every absolute URL
# (canonical, hreflang, og) follows. Until then, the GitHub Pages address.
_cname = os.path.join(ROOT, "CNAME")
BASE = ("https://%s/" % open(_cname).read().strip()) if os.path.exists(_cname) else "https://vargagergo-git.github.io/aera-site/"

APPLE = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12.152 6.896c-.948 0-2.415-1.078-3.96-1.04-2.04.027-3.91 1.183-4.961 3.014'
         '-2.117 3.675-.546 9.103 1.519 12.09 1.013 1.454 2.208 3.09 3.792 3.039 1.52-.065 2.09-.987 3.935-.987 1.831 0 2.35.987 3.96.948'
         ' 1.637-.026 2.676-1.48 3.676-2.948 1.156-1.688 1.636-3.325 1.662-3.415-.039-.013-3.182-1.221-3.22-4.857-.026-3.04 2.48-4.494'
         ' 2.597-4.559-1.429-2.09-3.623-2.324-4.39-2.376-2-.156-3.675 1.09-4.61 1.09zM15.53 3.83c.843-1.012 1.4-2.427 1.245-3.83'
         '-1.207.052-2.662.805-3.532 1.818-.78.896-1.454 2.338-1.273 3.714 1.338.104 2.715-.688 3.559-1.701"/></svg>')

LOCK = ('<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="4.5" y="10.5" width="15" height="10" rx="3"/>'
        '<path d="M8 10.5V7.5a4 4 0 0 1 8 0v3"/></svg>')

COPY = {
    "en": {
        "file": "index.html", "lang": "en", "store": "https://apps.apple.com/app/id6762456252",
        "title": "Aera: turn last night into today's run. Sleep and running for iPhone and Apple Watch",
        "desc": "Aera reads how you slept, what your heart did overnight and how the week went, against your own usual, then tells you how hard to go today. Every number shows how it was worked out. No account.",
        "og_title": "Aera: turn last night into today's run",
        "nav": [("notes/index.html", "Notes"), ("tools/how-far.html", "How far will I run?"), ("support.html", "Support")],
        "get": "Get Aera",
        "skip": "Skip to content",
        "eyebrow": "Aera for iPhone and Apple Watch",
        "h1": "Turn last night into today&#8217;s run.",
        "lede": "Aera reads how you slept, what your heart did overnight and how your week has gone, against your own usual. Then it tells you how hard to go today, and every number shows how it was worked out.",
        "cta": "Download on the App Store",
        "cta2": "See a morning",
        "facts": ["Free to download", "No account", "Health numbers stay on your iPhone"],
        "hero_alt": "Aera's Home screen: Good to go, recovery above your usual after a normal night, and today's session",
        "story_kicker": "A morning with Aera",
        "story_h2": "From last night to out the door.",
        "story_sub": "Every morning starts from the night you actually had. Here is what Aera reads, and what it does with it.",
        "steps": [
            ("sleep", "Last night", "var(--indigo)", "The night as it happened",
             "Hours asleep, the stages, how unbroken it was and your sleeping heart rate, measured against the sleep need Aera learned from your own nights. Watch sleep stages are an estimate, so they count for less, and Aera says so.",
             None, "The Sleep screen: Excellent, right on your need, 7 hours 25 minutes asleep"),
            ("recovery", "Overnight", "var(--pink)", "What your heart did while you slept",
             "Heart rate variability, resting heart rate, breathing and wrist temperature, each against your own last four weeks. Sleep is not an input, so recovery never turns into a second sleep score.",
             None, "The Recovery screen: Ready, recovery is in your usual range"),
            ("home", "This morning", "var(--green)", "One plain word for the day",
             "Your recovery, sleep, stress and recent training decide the call, with the reasons beside it. Free every morning, once Aera has a few weeks of your nights and workouts. Until then it says it is still learning.",
             ["Rest day", "Go easy", "Good to go", "Go for it"], "The Home screen: Good to go"),
            ("session", "Today's run", "var(--gold)", "How long, and how hard",
             "Aera writes today's session from the week you actually had: an easy 35 minutes, say, and nothing at all on a rest day.",
             "Premium", "Today's session: good to go, freshness is the one holding back"),
            ("planner", "Out the door", "var(--orange)", "Draw the route from your door",
             "Tap the map and the line keeps to real paths, with the distance counting as you draw. Follow it turn by turn on your iPhone or Apple Watch, spoken if you want it, even with no signal.",
             None, "The route planner over a satellite map"),
        ],
        "usual_kicker": "Against your usual",
        "usual_h2": "Your body doesn&#8217;t run on averages.",
        "usual_sub": "So Aera doesn't score you against one. Every read sits on your own usual range, learned from weeks of your nights and sessions, and it moves as you change. Today's dot lands where you are.",
        "rails": [
            ("Heart rate variability", "var(--pink)", "84", "ms", "Typical", "28%", "34%", "58%"),
            ("Resting heart rate", "var(--pink)", "53", "bpm", "Typical", "30%", "30%", "44%"),
            ("Asleep", "var(--indigo)", "7h 25m", "", "Right on your need", "36%", "26%", "61%"),
        ],
        "rail_ends": ("Lower", "Your usual", "Higher"),
        "rails_note": "Example readings from the app's own screens.",
        "guide_kicker": "The Field Guide",
        "guide_h2": "Every number shows its work.",
        "guide_sub": "Tap a number and it opens a short article: how it was worked out, the research behind it with sources you can open, and where it stops being reliable.",
        "quote": "Apple Watch sleep stages are an estimate. Aera gives them less weight, and tells you so.",
        "quote_src": "From the article on your sleep score",
        "guide_link": "Read the notes on this site",
        "guide_alts": ("The Field Guide article on your sleep score", "The Field Guide article on what recovery measures"),
        "after_kicker": "After the run",
        "after_h2": "Fly back over the run you just did.",
        "after_sub": "Flyover turns a run into a short film over the real ground. It pauses at your fastest split and the top of the climb. Free for runs from the last seven days.",
        "after_list": [
            "One picture of the whole session: pace with every split, heart rate in your own zones, every hill.",
            "What the run cost you, against your usual.",
            "Every personal best, at every distance, free.",
        ],
        "after_alts": ("A Flyover replay of a run over satellite ground with pace and heart rate", "A morning run read back: distance, time and pace against your usual"),
        "map_kicker": "Your map",
        "map_h2": "Plan it. Then just run.",
        "map_sub": "Draw a route that keeps to real paths, or open a GPX file. On the way, every turn comes before you reach it, on your phone, your wrist or read aloud, with a word when you leave the route and when you are back on it.",
        "map_alts": ("The route planner: tap the map to start, following paths and trails", "Turn by turn: 55 metres, then right"),
        "also_kicker": "Also in the app",
        "also_h2": "Small things, done properly.",
        "tiles": [
            ("Apple Watch", "var(--green)", "Record a run on your watch alone, with auto-pause, and feel each turn of a route."),
            ("Widgets", "var(--indigo)", "In every size, on the Home Screen and the Lock Screen."),
            ("Recap films", "var(--gold)", "Your week, month and year as short films, free."),
            ("Share cards", "var(--orange)", "Satellite, terrain and splits looks. Rewrite any word, pick any colour."),
            ("Your data, out", "var(--pink)", "Raw data as JSON or GPX, free. Reports and every other format with Premium."),
            ("Your language", "var(--sage)", "English, Magyar, Deutsch, Espa&#241;ol, Fran&#231;ais and more."),
        ],
        "priv_h2": "Health numbers stay on your iPhone.",
        "priv_sub": "Aera reads Apple Health on the phone and works out every score there. No account, no sign in, and no language model anywhere in the app. Product analytics stay off until you turn them on and never include health values. Crash reports help fix bugs.",
        "priv_link": "Read the privacy policy",
        "plans_h2": "Free to use. Premium when you want more.",
        "free_h": "Free", "free_note": "Every day, for everyone.",
        "free": ["Recovery, stress, strain and your sleep score", "Hard, easy or rest, every morning",
                 "The route planner and turn by turn", "Every workout read, every personal best",
                 "Flyover for the last seven days", "Twelve months of history, raw data as JSON or GPX"],
        "prem_h": "Premium", "prem_note": "Monthly, yearly, or once and yours for good. Yearly starts with a 7-day free trial.",
        "prem": ["Today's session: how long and how hard", "Your sleep reserve", "Your places",
                 "Flyover for older runs", "Every route you draw, kept (the first is free)",
                 "History past twelve months", "Reports and every export format"],
        "maker_kicker": "Who makes it",
        "maker_h2": "Made by one person.",
        "maker_sub": "Aera is built by Gerg&#337; Varga, on his own, with no company behind it. The app says so in its settings. A message from the app or from this site reaches him directly.",
        "maker_link": "Write to him",
        "close_h2": "Tomorrow morning, see what last night says.",
        "foot_tag": "Sleep, recovery and running, read against you.",
        "foot_app": "App", "foot_legal": "Legal", "foot_more": "More",
        "foot_links_app": [("store", "Download"), ("support.html", "Support"), ("flyover.html", "Flyover")],
        "foot_links_legal": [("privacy.html", "Privacy Policy"), ("terms.html", "Terms of Use"), ("terms.html#eula", "EULA")],
        "foot_links_more": [("notes/index.html", "Notes"), ("tools/how-far.html", "How far will I run?")],
        "foot_base": ("&#169; 2026 Aera", "Not a medical device."),
    },
    "hu": {
        "file": "hu.html", "lang": "hu", "store": "https://apps.apple.com/hu/app/id6762456252",
        "title": "Aera magyarul: az éjszakádból lesz a mai futásod. Alvás és futás iPhone-on és Apple Watch-on",
        "desc": "Az Aera megnézi, hogyan aludtál, mit csinált éjjel a szíved és hogyan telt a heted, a saját szokásodhoz mérve. Aztán megmondja, milyen keményen menj ma. Teljesen magyarul, fiók nélkül.",
        "og_title": "Aera magyarul: az éjszakádból lesz a mai futásod",
        "nav": [("tools/milyen-messze.html", "Kalkulátor"), ("notes/index.html", "Jegyzetek"), ("support.html", "Támogatás")],
        "get": "Letöltés",
        "skip": "Ugrás a tartalomra",
        "eyebrow": "Aera iPhone-ra és Apple Watch-ra",
        "h1": "Az éjszakádból lesz a mai futásod.",
        "lede": "Az Aera megnézi, hogyan aludtál, mit csinált éjjel a szíved és hogyan telt a heted, mindezt a saját szokásodhoz mérve. Aztán megmondja, milyen keményen menj ma, és minden szám elárulja, hogyan jött ki.",
        "cta": "Letöltés az App Store-ból",
        "cta2": "Egy reggel az Aerával",
        "facts": ["Ingyenes", "Nincs fiók", "Teljesen magyarul"],
        "hero_alt": "Az Aera kezdőképernyője: Mehet, a regenerálódás a szokásosnál jobb, és a mai edzés",
        "story_kicker": "Egy reggel az Aerával",
        "story_h2": "A tegnap éjszakától az ajtón túlig.",
        "story_sub": "Minden reggel abból indul, ahogy valóban aludtál. Ezt nézi meg az Aera, és ezt kezdi vele.",
        "steps": [
            ("sleep", "Tegnap éjjel", "var(--indigo)", "Az éjszakád, ahogy tényleg volt",
             "Az alvással töltött órák, az alvásszakaszok, hogy mennyire volt megszakítás nélküli, és az alvás közbeni pulzusod, ahhoz az alvásigényhez mérve, amit az Aera a saját éjszakáidból tanult meg. Az óra csak becsli az alvásszakaszokat, ezért kevesebbet számítanak, és az Aera ezt meg is mondja.",
             None, "Az Alvás képernyő: kiváló, pont az igényed szerint, 7 óra 25 perc alvás"),
            ("recovery", "Éjszaka", "var(--pink)", "Mit csinált a szíved, amíg aludtál",
             "Pulzusvariabilitás, nyugalmi pulzus, légzés és csuklóhőmérséklet, mindegyik a saját elmúlt négy hetedhez mérve. Az alvás nem bemenet, így a regenerálódás sosem lesz egy második alváspontszám.",
             None, "A Regenerálódás képernyő: a szokásos tartományban"),
            ("home", "Ma reggel", "var(--green)", "Egy egyszerű szó a napra",
             "A regenerálódásod, az alvásod, a stresszed és az elmúlt napok edzései döntenek, az okokkal együtt. Minden reggel ingyen, amint az Aera ismer pár hétnyi éjszakát és edzést. Addig kiírja, hogy még tanul.",
             ["Pihenőnap", "Csak lazán", "Mehet", "Hajrá"], "A kezdőképernyő: Mehet"),
            ("session", "A mai futás", "var(--gold)", "Mennyi ideig és milyen keményen",
             "Az Aera megírja a mai edzést abból a hétből, ami valóban volt: mondjuk 35 perc lazán, pihenőnapon pedig semmit.",
             "Premium", "A mai edzés: mehet, csak a frissesség fog vissza"),
            ("planner", "Ki az ajtón", "var(--orange)", "Rajzold meg az útvonalat a kapudtól",
             "Koppints a térképre, és a vonal a valódi ösvényeket követi, rajzolás közben látod a távot. Kövesd kanyarról kanyarra az iPhone-on vagy az Apple Watch-on, ha kéred, hangosan is, térerő nélkül is.",
             None, "Az útvonaltervező műholdas térképen"),
        ],
        "usual_kicker": "A saját szokásodhoz mérve",
        "usual_h2": "A tested nem átlag.",
        "usual_sub": "Ezért az Aera sem egy átlaghoz mér. Minden érték a saját szokásos tartományodon ül, amit hetek éjszakáiból és edzéseiből tanul meg, és veled együtt változik. A mai pötty oda esik, ahol most tartasz.",
        "rails": [
            ("Pulzusvariabilitás", "var(--pink)", "84", "ms", "Tipikus", "28%", "34%", "58%"),
            ("Nyugalmi pulzus", "var(--pink)", "53", "bpm", "Tipikus", "30%", "30%", "44%"),
            ("Alvás", "var(--indigo)", "7 ó 25 p", "", "Pont az igényed szerint", "36%", "26%", "61%"),
        ],
        "rail_ends": ("Alacsonyabb", "Szokásos", "Magasabb"),
        "rails_note": "Példaértékek az app saját képernyőiről.",
        "guide_kicker": "A Field Guide",
        "guide_h2": "Minden szám elmondja, honnan tudja.",
        "guide_sub": "Koppints egy számra, és megnyílik mögötte egy rövid cikk: hogyan jött ki, milyen kutatás áll mögötte, megnyitható forrásokkal, és hol szűnik meg megbízhatónak lenni.",
        "quote": "Az Apple Watch csak becsli az alvásszakaszokat. Az Aera ezért kisebb súlyt ad nekik, és ezt meg is mondja.",
        "quote_src": "Az alváspontszámról szóló cikkből",
        "guide_link": "Jegyzetek az oldalon (angolul)",
        "guide_alts": ("A Field Guide cikke az alváspontszámról", "A Field Guide cikke arról, mit mér a regenerálódás"),
        "after_kicker": "Futás után",
        "after_h2": "Repüld be újra a futásodat.",
        "after_sub": "A Flyover rövid filmet készít a futásodból a valódi terep fölött. Megáll a leggyorsabb részidőnél és az emelkedő tetején. Az elmúlt hét nap futásaihoz ingyenes.",
        "after_list": [
            "Az egész edzés egy képen: tempó minden részidővel, pulzus a saját zónáidban, minden emelkedő.",
            "Mennyibe került neked a futás, a szokásodhoz mérve.",
            "Minden egyéni rekord, minden távon, ingyen.",
        ],
        "after_alts": ("Egy futás Flyover visszajátszása műholdas terep fölött, tempóval és pulzussal", "Egy reggeli futás kiértékelése: táv, idő és tempó a szokásodhoz mérve"),
        "map_kicker": "A térképed",
        "map_h2": "Tervezd meg. Aztán csak fuss.",
        "map_sub": "Rajzolj útvonalat, ami a valódi ösvényeket követi, vagy nyiss meg egy GPX-fájlt. Útközben minden kanyar előbb szól, mint odaérsz, a telefonon, a csuklódon vagy hangosan, és szól, ha letérsz az útvonalról, és ha visszatérsz rá.",
        "map_alts": ("Az útvonaltervező: koppints a térképre az induláshoz", "Kanyarról kanyarra: 55 méter, aztán jobbra"),
        "also_kicker": "Még az appban",
        "also_h2": "Apró dolgok, rendesen megcsinálva.",
        "tiles": [
            ("Apple Watch", "var(--green)", "Futás rögzítése csak az órával, automatikus szünettel, és minden kanyart érzel a csuklódon."),
            ("Widgetek", "var(--indigo)", "Minden méretben, a kezdőképernyőn és a zárolási képernyőn."),
            ("Összegző filmek", "var(--gold)", "A heted, a hónapod és az éved rövid filmként, ingyen."),
            ("Megosztható kártyák", "var(--orange)", "Műholdas, domborzati és részidős kinézet. Bármelyik szót átírhatod, bármilyen színt választhatsz."),
            ("Az adataid", "var(--pink)", "Nyers adatok JSON vagy GPX formátumban, ingyen. Jelentések és minden más formátum a Premiummal."),
            ("Magyarul", "var(--sage)", "Az egész app magyarul, és még kilenc nyelven."),
        ],
        "priv_h2": "Az egészségadataid az iPhone-odon maradnak.",
        "priv_sub": "Az Aera a telefonon olvassa az Apple Health adatait, és minden pontszám ott készül. Nincs fiók, nincs belépés, és az appban sehol nincs nyelvi modell. A termékanalitika ki van kapcsolva, amíg be nem kapcsolod, és sosem tartalmaz egészségadatot. Az összeomlási jelentések a hibák javítását segítik.",
        "priv_link": "Az adatvédelmi szabályzat (angolul)",
        "plans_h2": "Ingyen használható. Premium, ha többet szeretnél.",
        "free_h": "Ingyenes", "free_note": "Minden nap, mindenkinek.",
        "free": ["Regenerálódás, stressz, terhelés és az alváspontszámod", "Kemény, könnyű vagy pihenő, minden reggel",
                 "Útvonaltervező és kanyarról kanyarra navigáció", "Minden edzés kiértékelése, minden egyéni rekord",
                 "Flyover az elmúlt hét napra", "Tizenkét hónapnyi előzmény, nyers adatok JSON vagy GPX formátumban"],
        "prem_h": "Premium", "prem_note": "Havonta, évente, vagy egyszeri vásárlással örökre a tiéd. Az éves előfizetés 7 nap ingyenes próbával indul.",
        "prem": ["A mai edzés: mennyi ideig és milyen keményen", "Az alvástartalékod", "A helyeid",
                 "Flyover a régebbi futásokhoz", "Minden útvonal megmarad, amit rajzolsz (az első ingyenes)",
                 "Tizenkét hónapnál régebbi előzmények", "Jelentések és minden exportformátum"],
        "maker_kicker": "Ki csinálja",
        "maker_h2": "Egyetlen ember készíti.",
        "maker_sub": "Az Aerát Varga Gergő készíti, egyedül, cég nélkül. Az app a beállításokban is ezt írja. Ha az appból vagy erről az oldalról írsz, az üzenet egyenesen hozzá jut.",
        "maker_link": "Írj neki",
        "close_h2": "Holnap reggel nézd meg, mit mond a tegnap éjszaka.",
        "foot_tag": "Alvás, regenerálódás és futás, hozzád mérve.",
        "foot_app": "App", "foot_legal": "Jogi információk", "foot_more": "Még",
        "foot_links_app": [("store", "Letöltés"), ("support.html", "Támogatás"), ("flyover.html", "Flyover")],
        "foot_links_legal": [("privacy.html", "Adatvédelem"), ("terms.html", "Felhasználási feltételek"), ("terms.html#eula", "EULA")],
        "foot_links_more": [("tools/milyen-messze.html", "Milyen messzire futok?"), ("notes/index.html", "Jegyzetek")],
        "foot_base": ("&#169; 2026 Aera", "Nem orvostechnikai eszköz."),
    },
    "de": {
        "file": "de.html", "lang": "de", "store": "https://apps.apple.com/de/app/id6762456252",
        "title": "Aera auf Deutsch: aus letzter Nacht wird dein Lauf von heute. Schlaf und Laufen für iPhone und Apple Watch",
        "desc": "Aera liest, wie du geschlafen hast, was dein Herz in der Nacht gemacht hat und wie deine Woche lief, gemessen an deinem eigenen Üblichen. Dann sagt es dir, wie hart du heute laufen kannst. Kein Konto.",
        "og_title": "Aera: aus letzter Nacht wird dein Lauf von heute",
        "nav": [("tools/wie-weit.html", "Rechner"), ("notes/index.html", "Notizen"), ("support.html", "Support")],
        "get": "Laden",
        "skip": "Zum Inhalt",
        "eyebrow": "Aera für iPhone und Apple Watch",
        "h1": "Aus letzter Nacht wird dein Lauf von heute.",
        "lede": "Aera liest, wie du geschlafen hast, was dein Herz in der Nacht gemacht hat und wie deine Woche lief, gemessen an deinem eigenen Üblichen. Dann sagt es dir, wie hart du heute laufen kannst, und jede Zahl zeigt, wie sie entstanden ist.",
        "cta": "Im App Store laden",
        "cta2": "Ein Morgen mit Aera",
        "facts": ["Kostenlos", "Kein Konto", "Gesundheitswerte bleiben auf deinem iPhone"],
        "hero_alt": "Der Home-Bildschirm von Aera: Bereit, Erholung über deinem Üblichen, und die heutige Einheit",
        "story_kicker": "Ein Morgen mit Aera",
        "story_h2": "Von letzter Nacht bis vor die Haustür.",
        "story_sub": "Jeder Morgen beginnt mit der Nacht, die du wirklich hattest. Das liest Aera, und das macht es daraus.",
        "steps": [
            ("sleep", "Letzte Nacht", "var(--indigo)", "Deine Nacht, wie sie war",
             "Die Stunden Schlaf, die Schlafphasen, wie ungestört die Nacht war und dein Puls im Schlaf, gemessen an dem Schlafbedarf, den Aera aus deinen eigenen Nächten gelernt hat. Die Uhr schätzt die Schlafphasen nur, deshalb zählen sie weniger, und Aera sagt das auch.",
             None, "Der Schlaf-Bildschirm: ausgezeichnet, genau dein Bedarf, 7 Stunden 25 Minuten Schlaf"),
            ("recovery", "In der Nacht", "var(--pink)", "Was dein Herz im Schlaf gemacht hat",
             "Herzfrequenzvariabilität, Ruhepuls, Atmung und Handgelenktemperatur, jeweils gemessen an deinen eigenen letzten vier Wochen. Schlaf fließt nicht ein, damit die Erholung nie zu einem zweiten Schlafwert wird.",
             None, "Der Erholungs-Bildschirm: in deinem üblichen Bereich"),
            ("home", "Heute Morgen", "var(--green)", "Ein klares Wort für den Tag",
             "Deine Erholung, dein Schlaf, dein Stress und dein Training der letzten Tage entscheiden, mit den Gründen daneben. Jeden Morgen kostenlos, sobald Aera ein paar Wochen deiner Nächte und Einheiten kennt. Bis dahin sagt es, dass es noch lernt.",
             ["Ruhetag", "Ruhig angehen", "Bereit", "Leg los"], "Der Home-Bildschirm: Bereit"),
            ("session", "Dein Lauf heute", "var(--gold)", "Wie lange und wie hart",
             "Aera schreibt dir die heutige Einheit aus der Woche, die du wirklich hattest: zum Beispiel 35 Minuten locker, und an einem Ruhetag gar nichts.",
             "Premium", "Die heutige Einheit: bereit, nur die Frische bremst noch"),
            ("planner", "Vor die Tür", "var(--orange)", "Zeichne die Route ab deiner Haustür",
             "Tipp auf die Karte, und die Linie folgt echten Wegen, die Distanz zählt beim Zeichnen mit. Folge ihr mit Abbiegehinweisen auf dem iPhone oder der Apple Watch, auf Wunsch gesprochen, auch ohne Empfang.",
             None, "Der Routenplaner über einer Satellitenkarte"),
        ],
        "usual_kicker": "Gemessen an dir",
        "usual_h2": "Dein Körper läuft nicht nach Durchschnitt.",
        "usual_sub": "Deshalb misst Aera dich auch nicht an einem. Jeder Wert liegt auf deinem eigenen üblichen Bereich, gelernt aus Wochen deiner Nächte und Einheiten, und er verschiebt sich, wenn du dich veränderst. Der Punkt von heute landet dort, wo du gerade stehst.",
        "rails": [
            ("Herzfrequenzvariabilität", "var(--pink)", "84", "ms", "Typisch", "28%", "34%", "58%"),
            ("Ruhepuls", "var(--pink)", "53", "bpm", "Typisch", "30%", "30%", "44%"),
            ("Schlaf", "var(--indigo)", "7 h 25 min", "", "Genau dein Bedarf", "36%", "26%", "61%"),
        ],
        "rail_ends": ("Niedriger", "Üblich", "Höher"),
        "rails_note": "Beispielwerte aus den Bildschirmen der App.",
        "guide_kicker": "Der Field Guide",
        "guide_h2": "Jede Zahl zeigt, wie sie entsteht.",
        "guide_sub": "Tipp auf eine Zahl, und dahinter öffnet sich ein kurzer Artikel: wie sie berechnet wird, welche Forschung dahinter steht, mit Quellen zum Öffnen, und wo sie nicht mehr verlässlich ist.",
        "quote": "Die Apple Watch schätzt die Schlafphasen nur. Aera gibt ihnen deshalb weniger Gewicht und sagt dir das auch.",
        "quote_src": "Aus dem Artikel über deinen Schlafwert",
        "guide_link": "Notizen auf dieser Seite (auf Englisch)",
        "guide_alts": ("Der Field-Guide-Artikel über deinen Schlafwert", "Der Field-Guide-Artikel darüber, was Erholung misst"),
        "after_kicker": "Nach dem Lauf",
        "after_h2": "Flieg noch einmal über deinen Lauf.",
        "after_sub": "Flyover macht aus deinem Lauf einen kurzen Film über dem echten Gelände. Er hält am schnellsten Split und oben am Anstieg. Für Läufe der letzten sieben Tage kostenlos.",
        "after_list": [
            "Die ganze Einheit in einem Bild: Tempo mit jedem Split, Puls in deinen eigenen Zonen, jeder Anstieg.",
            "Was dich der Lauf gekostet hat, gemessen an deinem Üblichen.",
            "Alle Bestleistungen, auf jeder Distanz, kostenlos.",
        ],
        "after_alts": ("Ein Flyover eines Laufs über Satellitengelände mit Tempo und Puls", "Ein Morgenlauf ausgewertet: Distanz, Zeit und Tempo gegen dein Übliches"),
        "map_kicker": "Deine Karte",
        "map_h2": "Plan es. Dann lauf einfach.",
        "map_sub": "Zeichne eine Route, die echten Wegen folgt, oder öffne eine GPX-Datei. Unterwegs kommt jede Abbiegung, bevor du da bist, auf dem Handy, am Handgelenk oder gesprochen, mit einem Hinweis, wenn du die Route verlässt und wenn du wieder auf ihr bist.",
        "map_alts": ("Der Routenplaner: tipp auf die Karte, um zu starten", "Abbiegehinweis: 55 Meter, dann rechts"),
        "also_kicker": "Außerdem in der App",
        "also_h2": "Kleine Dinge, richtig gemacht.",
        "tiles": [
            ("Apple Watch", "var(--green)", "Lauf nur mit der Uhr aufzeichnen, mit Auto-Pause, und jede Abbiegung am Handgelenk spüren."),
            ("Widgets", "var(--indigo)", "In jeder Größe, auf dem Home-Bildschirm und dem Sperrbildschirm."),
            ("Rückblicke", "var(--gold)", "Deine Woche, dein Monat und dein Jahr als kurzer Film, kostenlos."),
            ("Karten zum Teilen", "var(--orange)", "Satellit, Gelände und Splits. Jedes Wort änderbar, jede Farbe wählbar."),
            ("Deine Daten", "var(--pink)", "Rohdaten als JSON oder GPX, kostenlos. Berichte und alle anderen Formate mit Premium."),
            ("Auf Deutsch", "var(--sage)", "Die ganze App auf Deutsch, und in neun weiteren Sprachen."),
        ],
        "priv_h2": "Gesundheitswerte bleiben auf deinem iPhone.",
        "priv_sub": "Aera liest Apple Health auf dem Handy und berechnet jeden Wert dort. Kein Konto, kein Login, und in der App steckt nirgends ein Sprachmodell. Die Produktanalyse bleibt aus, bis du sie einschaltest, und enthält nie Gesundheitswerte. Absturzberichte helfen, Fehler zu beheben.",
        "priv_link": "Datenschutzerklärung (auf Englisch)",
        "plans_h2": "Kostenlos nutzbar. Premium, wenn du mehr willst.",
        "free_h": "Kostenlos", "free_note": "Jeden Tag, für alle.",
        "free": ["Erholung, Stress, Belastung und dein Schlafwert", "Hart, locker oder Ruhe, jeden Morgen",
                 "Der Routenplaner und die Abbiegehinweise", "Die Auswertung jedes Trainings, alle Bestleistungen",
                 "Flyover für die letzten sieben Tage", "Zwölf Monate Verlauf, Rohdaten als JSON oder GPX"],
        "prem_h": "Premium", "prem_note": "Monatlich, jährlich oder einmal kaufen und für immer behalten. Jährlich startet mit 7 Tagen gratis.",
        "prem": ["Die heutige Einheit: wie lange und wie hart", "Deine Schlafreserve", "Deine Orte",
                 "Flyover für ältere Läufe", "Jede Route, die du zeichnest, bleibt gespeichert (die erste ist kostenlos)",
                 "Verlauf über zwölf Monate hinaus", "Berichte und jedes Exportformat"],
        "maker_kicker": "Wer sie macht",
        "maker_h2": "Von einem einzigen Menschen gemacht.",
        "maker_sub": "Aera wird von Gerg&#337; Varga gebaut, allein, ohne Firma dahinter. Die App sagt das auch in ihren Einstellungen. Eine Nachricht aus der App oder von dieser Seite erreicht ihn direkt.",
        "maker_link": "Schreib ihm",
        "close_h2": "Morgen früh siehst du, was die letzte Nacht sagt.",
        "foot_tag": "Schlaf, Erholung und Laufen, gemessen an dir.",
        "foot_app": "App", "foot_legal": "Rechtliches", "foot_more": "Mehr",
        "foot_links_app": [("store", "Laden"), ("support.html", "Support"), ("flyover.html", "Flyover")],
        "foot_links_legal": [("privacy.html", "Datenschutz"), ("terms.html", "Nutzungsbedingungen"), ("terms.html#eula", "EULA")],
        "foot_links_more": [("tools/wie-weit.html", "Wie weit laufe ich?"), ("notes/index.html", "Notizen")],
        "foot_base": ("&#169; 2026 Aera", "Kein Medizinprodukt."),
    },
}

LANG_NAMES = [("en", "index.html", "English"), ("hu", "hu.html", "Magyar"), ("de", "de.html", "Deutsch")]

# Captures of the app on 9 Oct 2026 (main 0ebe9a8). Name -> has light and dark?
THEMED = {"home", "sleep", "recovery", "session", "planner", "article-sleep"}


def picture(name, alt, sizes, eager=False):
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    if name in THEMED:
        d, l = "img/%s-dark" % name, "img/%s-light" % name
        return ('<picture><source media="(prefers-color-scheme: dark)" srcset="%s-400.webp 400w, %s-800.webp 800w" sizes="%s">'
                '<img src="%s-400.webp" srcset="%s-400.webp 400w, %s-800.webp 800w" sizes="%s" width="1206" height="2622" %s alt="%s"></picture>'
                % (d, d, sizes, l, l, l, sizes, load, html.escape(alt)))
    f = "img/%s" % name
    return ('<img src="%s-400.webp" srcset="%s-400.webp 400w, %s-800.webp 800w" sizes="%s" width="1206" height="2622" %s alt="%s">'
            % (f, f, f, sizes, load, html.escape(alt)))


def phone(name, alt, sizes, eager=False, cls=""):
    return '<div class="phone %s"><div class="screen-wrap">%s</div></div>' % (cls, picture(name, alt, sizes, eager))


def build(code):
    c = COPY[code]
    L = landscape.hero_layers()
    store = c["store"]

    def href(h):
        return store if h == "store" else h

    alternates = "".join('<link rel="alternate" hreflang="%s" href="%s%s">' % (lc, BASE, "" if f == "index.html" else f)
                         for lc, f, _ in LANG_NAMES)
    alternates += '<link rel="alternate" hreflang="x-default" href="%s">' % BASE
    canonical = BASE + ("" if c["file"] == "index.html" else c["file"])
    nav = "".join('<a class="opt" href="%s">%s</a>' % (h, t) for h, t in c["nav"])
    facts = "".join("<li>%s</li>" % f for f in c["facts"])

    steps_html, stage = [], []
    for i, (shot, kicker, col, h3, body, extra, alt) in enumerate(c["steps"]):
        words = ""
        pill = ""
        if isinstance(extra, list):
            words = '<ul class="words">%s</ul>' % "".join("<li>%s</li>" % w for w in extra)
        elif extra:
            pill = '<span class="pill">%s</span>' % extra
        steps_html.append(
            '<article class="step%s" style="--c:%s"><p class="step-num"><b>%02d</b> %s</p><h3>%s%s</h3><p>%s</p>%s'
            '<div class="step-shot reveal">%s</div></article>'
            % (" on" if i == 0 else "", col, i + 1, kicker, h3, pill, body, words,
               phone(shot, alt, "(max-width: 899px) 260px, 1px")))
        stage.append('<div class="scr%s">%s</div>' % (" on" if i == 0 else "", picture(shot, alt, "(min-width: 900px) 310px, 1px")))

    rails = "".join(
        '<div class="rail" style="--c:%s;--i:%d"><div class="rail-top"><div><p class="rail-name"><i></i>%s</p>'
        '<p class="rail-word">%s</p></div><p class="rail-val">%s<small>%s</small></p></div>'
        '<div class="track"><span class="band" style="--l:%s;--w:%s"></span><span class="dot" style="--v:%s"></span></div>'
        '<div class="rail-ends"><span>%s</span><span>%s</span><span>%s</span></div></div>'
        % (col, i, name, word, val, unit, l, w, v, *c["rail_ends"])
        for i, (name, col, val, unit, word, l, w, v) in enumerate(c["rails"]))

    tiles = "".join('<div class="tile reveal" style="--c:%s;--d:%dms"><h3><i></i>%s</h3><p>%s</p></div>' % (col, (i % 3) * 80, t, p)
                    for i, (t, col, p) in enumerate(c["tiles"]))
    free = "".join("<li>%s</li>" % x for x in c["free"])
    prem = "".join("<li>%s</li>" % x for x in c["prem"])

    topo = landscape.contours()
    route = ('<path class="route" pathLength="1" d="M760 960 C 780 820, 690 730, 820 640 S 970 560, 1000 430 S 1120 250, 1260 300 S 1420 430, 1500 300 S 1580 160, 1650 140"/>')

    def foot_col(title, links):
        return "<div><h4>%s</h4>%s</div>" % (title, "".join('<a href="%s">%s</a>' % (href(h), t) for h, t in links))

    langs = "".join('<a href="%s" lang="%s" hreflang="%s"%s>%s</a>' % (f, lc, lc, ' aria-current="page"' if lc == code else "", n)
                    for lc, f, n in LANG_NAMES)

    legacy = ""
    if code == "en":
        legacy = """<script>
// The old single-page site lived at /#privacy, /#support, /#terms and /#eula.
// Those URLs are registered with the App Store, so keep them working.
(function () {
  var legacy = { '#privacy': 'privacy.html', '#support': 'support.html', '#terms': 'terms.html', '#eula': 'terms.html#eula' };
  var target = legacy[location.hash];
  if (target) location.replace(target);
})();
</script>"""

    ld = ('{"@context":"https://schema.org","@type":"SoftwareApplication","name":"Aera","applicationCategory":"HealthApplication",'
          '"operatingSystem":"iOS, watchOS","inLanguage":"%s","url":"%s","downloadUrl":"%s","description":"%s",'
          '"author":{"@type":"Person","name":"Gerg\\u0151 Varga"},"offers":{"@type":"Offer","price":"0","priceCurrency":"USD"}}'
          % (code, canonical, store, c["desc"].replace('"', '\\"')))

    return f"""<!DOCTYPE html>
<html lang="{c['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="apple-itunes-app" content="app-id=6762456252">
<title>{c['title']}</title>
<meta name="description" content="{c['desc']}">
<meta name="theme-color" content="#f6f4ef" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#000000" media="(prefers-color-scheme: dark)">
<meta property="og:title" content="{c['og_title']}">
<meta property="og:description" content="{c['desc']}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{BASE}assets/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="{canonical}">
{alternates}
<link rel="icon" href="assets/icon.png">
<link rel="apple-touch-icon" href="assets/icon.png">
<link rel="stylesheet" href="home.css">
<script type="application/ld+json">{ld}</script>
{legacy}
</head>
<body>
<a class="skip" href="#story">{c['skip']}</a>

<header class="bar">
  <div class="wide">
    <a class="brand" href="{c['file']}"><img src="assets/icon.png" alt="" width="30" height="30">Aera</a>
    <nav>{nav}<a class="get" href="{store}">{c['get']}</a></nav>
  </div>
</header>

<main>
<section class="hero" aria-labelledby="h1">
  <div class="sky sky-a"></div><div class="sky sky-b"></div>
  {L['stars']}
  <div class="moon"></div><div class="sun"></div>
  {L['far']}{L['mid']}{L['wood']}
  <div class="wide hero-inner">
    <div class="hero-copy">
      <p class="eyebrow rise" style="--d:.1s">{c['eyebrow']}</p>
      <h1 id="h1" class="rise" style="--d:.2s">{c['h1']}</h1>
      <p class="lede rise" style="--d:.32s">{c['lede']}</p>
      <div class="cta rise" style="--d:.44s">
        <a class="btn btn-store" href="{store}">{APPLE}{c['cta']}</a>
        <a class="btn btn-quiet" href="#story">{c['cta2']}</a>
      </div>
      <ul class="facts rise" style="--d:.54s">{facts}</ul>
    </div>
    <div class="hero-phone">{phone('home', c['hero_alt'], '(max-width: 899px) 64vw, 330px', eager=True)}</div>
  </div>
  {L['near']}
</section>

<section id="story">
  <div class="wide">
    <div class="story-head center reveal">
      <p class="kicker">{c['story_kicker']}</p>
      <h2 class="h2">{c['story_h2']}</h2>
      <p class="sub">{c['story_sub']}</p>
    </div>
    <div class="story">
      <div class="steps">{''.join(steps_html)}</div>
      <div class="stage" aria-hidden="true"><div class="phone"><div class="screen-wrap">{''.join(stage)}</div></div></div>
    </div>
  </div>
</section>

<section class="usual">
  <div class="wide usual-grid">
    <div class="reveal">
      <p class="kicker">{c['usual_kicker']}</p>
      <h2 class="h2">{c['usual_h2']}</h2>
      <p class="sub">{c['usual_sub']}</p>
    </div>
    <div>
      <div class="rails">{rails}</div>
      <p class="footnote">{c['rails_note']}</p>
    </div>
  </div>
</section>

<section>
  <div class="wide guide-grid">
    <div class="reveal">
      <p class="kicker">{c['guide_kicker']}</p>
      <h2 class="h2">{c['guide_h2']}</h2>
      <p class="sub">{c['guide_sub']}</p>
      <div class="quote"><p>&#8220;{c['quote']}&#8221;</p><span>{c['quote_src']}</span></div>
      <a class="link" href="notes/index.html">{c['guide_link']} &#8594;</a>
    </div>
    <div class="fan">
      {phone('article-sleep', c['guide_alts'][0], '(max-width: 899px) 46vw, 270px')}
      {phone('article-recovery-dark', c['guide_alts'][1], '(max-width: 899px) 46vw, 270px')}
    </div>
  </div>
</section>

<section class="after">
  <svg class="topo" viewBox="0 0 1600 900" preserveAspectRatio="xMidYMid slice" aria-hidden="true">{''.join(topo)}{route}</svg>
  <div class="wide after-grid">
    <div class="reveal">
      <p class="kicker">{c['after_kicker']}</p>
      <h2 class="h2">{c['after_h2']}</h2>
      <p class="sub">{c['after_sub']}</p>
      <ul class="list">{''.join('<li>%s</li>' % x for x in c['after_list'])}</ul>
    </div>
    <div class="duo reveal" style="--d:.15s">
      {phone('workout-flyover-dark', c['after_alts'][0], '(max-width: 899px) 46vw, 280px')}
      {phone('workout-detail', c['after_alts'][1], '(max-width: 899px) 46vw, 280px')}
    </div>
  </div>
</section>

<section>
  <div class="wide map-grid">
    <div class="reveal">
      <p class="kicker">{c['map_kicker']}</p>
      <h2 class="h2">{c['map_h2']}</h2>
      <p class="sub">{c['map_sub']}</p>
    </div>
    <div class="duo reveal" style="--d:.15s">
      {phone('planner', c['map_alts'][0], '(max-width: 899px) 46vw, 280px')}
      {phone('routenav', c['map_alts'][1], '(max-width: 899px) 46vw, 280px')}
    </div>
  </div>
</section>

<section class="also">
  <div class="wide">
    <div class="center reveal">
      <p class="kicker">{c['also_kicker']}</p>
      <h2 class="h2">{c['also_h2']}</h2>
    </div>
    <div class="tiles">{tiles}</div>
  </div>
</section>

<section class="privacy">
  <div class="wide center reveal">
    <div class="lock">{LOCK}</div>
    <h2 class="h2">{c['priv_h2']}</h2>
    <p class="sub">{c['priv_sub']}</p>
    <a class="link" href="privacy.html">{c['priv_link']} &#8594;</a>
  </div>
</section>

<section>
  <div class="wide">
    <h2 class="h2 center reveal">{c['plans_h2']}</h2>
    <div class="plans">
      <div class="plan free reveal"><h3>{c['free_h']}</h3><p class="note">{c['free_note']}</p><ul>{free}</ul></div>
      <div class="plan premium reveal" style="--d:.1s"><h3>{c['prem_h']}</h3><p class="note">{c['prem_note']}</p><ul>{prem}</ul></div>
    </div>
  </div>
</section>

<section class="maker-sec">
  <div class="wide maker center reveal">
    <p class="kicker">{c['maker_kicker']}</p>
    <h2 class="h2">{c['maker_h2']}</h2>
    <p class="sub">{c['maker_sub']}</p>
    <a class="link" href="support.html">{c['maker_link']} &#8594;</a>
  </div>
</section>

<section class="closing">
  <div class="wide reveal">
    <h2 class="h2">{c['close_h2']}</h2>
    <div class="cta"><a class="btn btn-store" href="{store}">{APPLE}{c['cta']}</a></div>
  </div>
  <div class="dusk" aria-hidden="true">{landscape.dusk_layers()}</div>
</section>
</main>

<footer>
  <div class="wide">
    <div class="foot">
      <div class="foot-brand"><a class="brand" href="{c['file']}"><img src="assets/icon.png" alt="" width="30" height="30">Aera</a><p>{c['foot_tag']}</p></div>
      {foot_col(c['foot_app'], c['foot_links_app'])}
      {foot_col(c['foot_legal'], c['foot_links_legal'])}
      <div><h4>{c['foot_more']}</h4>{''.join('<a href="%s">%s</a>' % (h, t) for h, t in c['foot_links_more'])}{langs}</div>
    </div>
    <div class="foot-base"><span>{c['foot_base'][0]}</span><span>{c['foot_base'][1]}</span></div>
  </div>
</footer>

<script src="home.js" defer></script>
</body>
</html>
"""


if __name__ == "__main__":
    for code in COPY:
        out = build(code)
        if "—" in out:
            raise SystemExit("em dash in %s" % code)
        with open(os.path.join(ROOT, COPY[code]["file"]), "w", encoding="utf-8") as f:
            f.write(out)
        print(COPY[code]["file"], len(out) // 1024, "KB")
