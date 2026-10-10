#!/usr/bin/env python3
"""Builds the homepage in three languages: index.html (en), hu.html, de.html.

    python3 scripts/build_home.py

Copy lives in COPY below, the look in home.css, motion in home.js. Every claim
here must match the live app (store copy in the app repo's Marketing/store/).
Loops are not promised until the 3.2.1 fix is live.
"""
import html
import json
import os
import re
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
        "title": "Aera: Sleep &amp; Running Tracker for iPhone and Apple Watch",
        "desc": "Aera reads how you slept, what your heart did overnight and how the week went, against your own usual, then tells you how hard to go today. Every number shows how it was worked out. No account.",
        "og_title": "Aera: turn last night into today's run",
        "nav": [("notes/index.html", "Notes"), ("tools/how-far.html", "How far will I run?"), ("support.html", "Support")],
        "get": "Get Aera",
        "skip": "Skip to content",
        "eyebrow": "Sleep and running tracker for iPhone and Apple Watch",
        "h1": "Turn last night into today&#8217;s run.",
        "lede": "Aera reads your night against your own usual and tells you how hard to go today. Every number shows how it was worked out.",
        "cta": "Download on the App Store",
        "cta2": "See a morning",
        "facts": ["Free to download", "No account", "Health numbers stay on your iPhone"],
        "proof": "5.0 from %d ratings on the Hungarian App Store",
        "chip_night": "7 h 25 m asleep, right on your need", "chip_day": "Recovery above your usual", "sleep_alt": "Aera's Sleep screen: 7 h 25 m asleep, right on your need",
        "hero_alt": "Aera's Sleep screen for last night: excellent, right on your need, 94 of 100 and 7 h 25 min asleep",
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
        "guide_kicker": "The Field Guide",
        "guide_h2": "Every number shows its work.",
        "guide_sub": "Tap a number and it opens a short article: how it was worked out, the research behind it with sources you can open, and where it stops being reliable.",
        "quote": "Apple Watch sleep stages are an estimate. Aera gives them less weight, and tells you so.",
        "quote_src": "From the article on your sleep score",
        "guide_link": "Read the notes on this site",
        "guide_alts": ("The Field Guide article on your sleep score", "The Field Guide article on what recovery measures"),
        "after_kicker": "After the run",
        "after_h2": "Replay the run you just did, in 3D.",
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
        "also_h2": "Also in Aera.",
        "tiles": [
            ("Apple Watch", "var(--green)", "Record a run on your watch alone, with auto-pause, and feel each turn of a route."),
            ("Widgets", "var(--indigo)", "In every size, on the Home Screen and the Lock Screen."),
            ("Recap films", "var(--gold)", "Your week, month and year as short films."),
            ("Share cards", "var(--orange)", "Satellite, terrain and splits looks. Rewrite any word, pick any colour."),
            ("Your data, out", "var(--pink)", "Raw data as JSON or GPX, whenever you want it."),
            ("Your language", "var(--sage)", "English, Magyar, Deutsch, Espa&#241;ol, Fran&#231;ais and more."),
        ],
        "priv_h2": "Health numbers stay on your iPhone.",
        "priv_sub": "Aera reads Apple Health on the phone and works out every score there. No account, no sign in, and no language model anywhere in the app. Product analytics stay off until you turn them on and never include health values. Crash reports help fix bugs.",
        "priv_link": "Read the privacy policy",
        "plans_h2": "What it costs.",
        "free_h": "Free",
        "free": "Sleep, stress and strain against your own usual, and one word for the day every morning. Every workout and personal best, the route planner with turn by turn, Flyover for runs from the last seven days, recap films, and a year of history you can export as JSON or GPX.",
        "prem_h": "Premium",
        "prem": "Today's session, with how long and how hard. Your sleep reserve and your places. Every route you draw after the first, kept. Flyover for older runs, history past a year, reports and every export format.",
        "prem_note": "Premium is monthly, yearly or a one-time purchase. Yearly starts with a 7-day free trial.",
        "faq_kicker": "Questions",
        "faq_h2": "Questions.",
        "faq": [
            ("What does Aera do?", "Aera is an iPhone and Apple Watch app that reads Apple Health and tells you each morning how hard to go: rest day, go easy, good to go or go for it. It reads your sleep, your overnight heart, stress and strain against your own usual, plans routes on a map with turn-by-turn directions, and explains every number in a short article."),
            ("Is Aera free?", "Yes. Recovery, stress, strain and your sleep score, the call for the day, the route planner, turn by turn, every workout read, every personal best and Flyover for the last seven days are free. Premium adds today's session, your sleep reserve, your places, older Flyovers, history past twelve months, reports and every export format."),
            ("Do I need an account, and where does my data go?", "There is no account. Aera reads Apple Health on your iPhone and works out every score there, so health numbers stay on your iPhone. There is no language model in the app. Product analytics stay off until you turn them on and never include health values."),
            ("Do I need an Apple Watch?", "An Apple Watch gives Aera the overnight heart and sleep signals most reads are built on. Without one, Aera works from what your iPhone records, like steps and workouts, and the reads that need a watch wait until there is data."),
            ("How does Aera know what is normal for me?", "It learns your usual range from your own nights and sessions over several weeks, then compares each new day with it. While your history is thin, it says it is still learning instead of guessing."),
            ("Is Aera a medical device?", "No. Aera is for everyday wellbeing and training. Watch measurements such as sleep stages are estimates, and every article says where its number stops being reliable."),
            ("Which languages does Aera speak?", "English, Hungarian, German, Spanish and French in full, and Italian, Japanese, Portuguese and Traditional Chinese in part."),
        ],
        "maker_kicker": "Who makes it",
        "maker_h2": "Made by one person.",
        "maker_sub": "Aera is built by Gerg&#337; Varga, on his own, with no company behind it. The app says so in its settings. A message from the app or from this site reaches him directly.",
        "maker_link": "Write to him",
        "close_h2": "Tomorrow morning, see what last night says.",
        "foot_tag": "Last night and today's run, read against you.",
        "foot_app": "App", "foot_legal": "Legal", "foot_more": "More",
        "foot_links_app": [("store", "Download"), ("support.html", "Support"), ("flyover.html", "Flyover"), ("press/", "Press")],
        "foot_links_legal": [("privacy.html", "Privacy Policy"), ("terms.html", "Terms of Use"), ("terms.html#eula", "EULA")],
        "foot_links_more": [("notes/index.html", "Notes"), ("tools/how-far.html", "How far will I run?"), ("guides/index.html", "Guides")],
        "meta_desc": "Sleep and running tracker for iPhone and Apple Watch. Aera compares last night with your own usual and says how hard to go today. Free, no account.",
        "foot_base": ("&#169; 2026 Aera", "Not a medical device."),
    },
    "hu": {
        "file": "hu.html", "lang": "hu", "store": "https://apps.apple.com/hu/app/id6762456252",
        "title": "Aera: alvás- és futáskövető iPhone-ra és Apple Watch-ra",
        "desc": "Az Aera megnézi, hogyan aludtál, mit csinált éjjel a szíved és hogyan telt a heted, a saját szokásodhoz mérve. Aztán megmondja, milyen keményen menj ma. Teljesen magyarul, fiók nélkül.",
        "og_title": "Aera magyarul: az éjszakádból lesz a mai futásod",
        "nav": [("tools/milyen-messze.html", "Kalkulátor"), ("notes/index.html", "Jegyzetek"), ("support.html", "Támogatás")],
        "get": "Letöltés",
        "skip": "Ugrás a tartalomra",
        "eyebrow": "Alvás- és futáskövető iPhone-ra és Apple Watch-ra",
        "h1": "Az éjszakádból lesz a mai futásod.",
        "lede": "Az Aera a saját szokásodhoz méri az éjszakádat, és megmondja, milyen keményen menj ma. Minden szám elárulja, hogyan jött ki.",
        "cta": "Letöltés az App Store-ból",
        "cta2": "Egy reggel az Aerával",
        "facts": ["Ingyenes", "Nincs fiók", "Teljesen magyarul"],
        "proof": "5,0 a magyar App Store-ban, %d értékelésből",
        "chip_night": "7 ó 25 p alvás, pont az igényed szerint", "chip_day": "A regenerálódás a szokásosnál jobb", "sleep_alt": "Az Aera alvás képernyője: 7 ó 25 p alvás, pont az igényed szerint",
        "hero_alt": "Az Aera alvás képernyője a tegnapi éjszakáról: kiváló, pont annyi, amennyi kell, 94/100 és 7 óra 25 perc alvás",
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
        "guide_kicker": "A Field Guide",
        "guide_h2": "Minden szám elmondja, honnan tudja.",
        "guide_sub": "Koppints egy számra, és megnyílik mögötte egy rövid cikk: hogyan jött ki, milyen kutatás áll mögötte, megnyitható forrásokkal, és hol szűnik meg megbízhatónak lenni.",
        "quote": "Az Apple Watch csak becsli az alvásszakaszokat. Az Aera ezért kisebb súlyt ad nekik, és ezt meg is mondja.",
        "quote_src": "Az alváspontszámról szóló cikkből",
        "guide_link": "Jegyzetek az oldalon (angolul)",
        "guide_alts": ("A Field Guide cikke az alváspontszámról", "A Field Guide cikke arról, mit mér a regenerálódás"),
        "after_kicker": "Futás után",
        "after_h2": "Nézd vissza 3D-ben a futásodat.",
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
        "also_h2": "Ami még benne van.",
        "tiles": [
            ("Apple Watch", "var(--green)", "Futás rögzítése csak az órával, automatikus szünettel, és minden kanyart érzel a csuklódon."),
            ("Widgetek", "var(--indigo)", "Minden méretben, a kezdőképernyőn és a zárolási képernyőn."),
            ("Összegző filmek", "var(--gold)", "A heted, a hónapod és az éved rövid filmként."),
            ("Megosztható kártyák", "var(--orange)", "Műholdas, domborzati és részidős kinézet. Bármelyik szót átírhatod, bármilyen színt választhatsz."),
            ("Az adataid", "var(--pink)", "Nyers adatok JSON vagy GPX formátumban, bármikor."),
            ("Magyarul", "var(--sage)", "Az egész app magyarul, és még kilenc nyelven."),
        ],
        "priv_h2": "Az egészség&shy;adataid az <span class=\"nw\">iPhone-odon</span> maradnak.",
        "priv_sub": "Az Aera a telefonon olvassa az Apple Health adatait, és minden pontszám ott készül. Nincs fiók, nincs belépés, és az appban sehol nincs nyelvi modell. A termékanalitika ki van kapcsolva, amíg be nem kapcsolod, és sosem tartalmaz egészségadatot. Az összeomlási jelentések a hibák javítását segítik.",
        "priv_link": "Az adatvédelmi szabályzat (angolul)",
        "plans_h2": "Mennyibe kerül.",
        "free_h": "Ingyenes",
        "free": "Alvás, stressz és terhelés a saját szokásosodhoz mérve, és minden reggel egy szó a napra. Minden edzés és egyéni rekord, az útvonaltervező kanyarról kanyarra navigációval, Flyover az elmúlt hét nap futásaihoz, összegző filmek, és egy évnyi előzmény, amit JSON vagy GPX formátumban kimenthetsz.",
        "prem_h": "Premium",
        "prem": "A mai edzés: mennyi ideig és milyen keményen. Az alvástartalékod és a helyeid. Az első után minden megrajzolt útvonal megmarad. Flyover a régebbi futásokhoz, egy évnél régebbi előzmények, jelentések és minden exportformátum.",
        "prem_note": "A Premium havi, éves vagy egyszeri vásárlás. Az éves előfizetés 7 nap ingyenes próbával indul.",
        "faq_kicker": "Kérdések",
        "faq_h2": "Kérdések.",
        "faq": [
            ("Mit csinál az Aera?", "Az Aera egy iPhone- és Apple Watch-app, ami az Apple Health adataiból minden reggel megmondja, milyen keményen menj: pihenőnap, csak lazán, mehet vagy hajrá. Az alvásodat, az éjszakai szívritmusodat, a stresszt és a terhelést a saját szokásodhoz méri, útvonalat tervez a térképen kanyarról kanyarra navigációval, és minden számot elmagyaráz egy rövid cikkben."),
            ("Ingyenes az Aera?", "Igen. A regenerálódás, a stressz, a terhelés és az alváspontszám, a napi döntés, az útvonaltervező, a kanyarról kanyarra navigáció, minden edzés kiértékelése, minden egyéni rekord és az elmúlt hét nap Flyovere ingyenes. A Premium hozzáadja a mai edzést, az alvástartalékot, a helyeidet, a régebbi Flyovereket, a tizenkét hónapnál régebbi előzményeket, a jelentéseket és minden exportformátumot."),
            ("Kell fiók? Hová kerülnek az adataim?", "Nincs fiók. Az Aera az iPhone-odon olvassa az Apple Health adatait, és minden pontszám ott készül, így az egészségadataid az iPhone-odon maradnak. Az appban nincs nyelvi modell. A termékanalitika ki van kapcsolva, amíg be nem kapcsolod, és sosem tartalmaz egészségadatot."),
            ("Kell hozzá Apple Watch?", "Az Apple Watch adja azokat az éjszakai szív- és alvásjeleket, amelyekre a legtöbb érték épül. Nélküle az Aera abból dolgozik, amit az iPhone rögzít, például lépésekből és edzésekből, az órát igénylő értékek pedig megvárják az adatot."),
            ("Honnan tudja az Aera, mi a szokásos nálam?", "Több hét alatt megtanulja a saját éjszakáidból és edzéseidből, mi a szokásos tartományod, és minden új napot ahhoz mér. Amíg kevés az adat, kiírja, hogy még tanul, és nem találgat."),
            ("Orvostechnikai eszköz az Aera?", "Nem. Az Aera a mindennapi jólléthez és az edzéshez készült. Az óra méréseit, például az alvásszakaszokat, becslésnek kell tekinteni, és minden cikk megmondja, hol szűnik meg megbízhatónak lenni a szám."),
            ("Milyen nyelveken érhető el?", "Teljesen magyarul, angolul, németül, spanyolul és franciául, részben olaszul, japánul, portugálul és hagyományos kínaiul."),
        ],
        "maker_kicker": "Ki csinálja",
        "maker_h2": "Egyetlen ember készíti.",
        "maker_sub": "Az Aerát Varga Gergő készíti, egyedül, cég nélkül. Az app a beállításokban is ezt írja. Ha az appból vagy erről az oldalról írsz, az üzenet egyenesen hozzá jut.",
        "maker_link": "Írj neki",
        "close_h2": "Holnap reggel nézd meg, mit mond a tegnap éjszaka.",
        "foot_tag": "A tegnapi éjszaka és a mai futás, hozzád mérve.",
        "foot_app": "App", "foot_legal": "Jogi információk", "foot_more": "Még",
        "foot_links_app": [("store", "Letöltés"), ("support.html", "Támogatás"), ("flyover.html", "Flyover"), ("press/", "Sajtó")],
        "foot_links_legal": [("privacy.html", "Adatvédelem"), ("terms.html", "Felhasználási feltételek"), ("terms.html#eula", "EULA")],
        "foot_links_more": [("tools/milyen-messze.html", "Milyen messzire futok?"), ("notes/index.html", "Jegyzetek"), ("guides/index.html#hu", "Útmutatók")],
        "meta_desc": "Alvás- és futáskövető iPhone-ra és Apple Watch-ra, magyarul. A saját szokásodhoz méri az éjszakát, és megmondja, milyen keményen menj ma. Ingyenes.",
        "foot_base": ("&#169; 2026 Aera", "Nem orvostechnikai eszköz."),
    },
    "de": {
        "file": "de.html", "lang": "de", "store": "https://apps.apple.com/de/app/id6762456252",
        "title": "Aera: Schlaf- &amp; Lauftracker für iPhone und Apple Watch",
        "desc": "Aera liest, wie du geschlafen hast, was dein Herz in der Nacht gemacht hat und wie deine Woche lief, gemessen an deinem eigenen Üblichen. Dann sagt es dir, wie hart du heute laufen kannst. Kein Konto.",
        "og_title": "Aera: aus letzter Nacht wird dein Lauf von heute",
        "nav": [("tools/wie-weit.html", "Rechner"), ("notes/index.html", "Notizen"), ("support.html", "Support")],
        "get": "Laden",
        "skip": "Zum Inhalt",
        "eyebrow": "Schlaf- und Lauftracker für iPhone und Apple Watch",
        "h1": "Aus letzter Nacht wird dein Lauf von heute.",
        "lede": "Aera misst deine Nacht an deinem eigenen Üblichen und sagt dir, wie hart du heute laufen kannst. Jede Zahl zeigt, wie sie entstanden ist.",
        "cta": "Im App Store laden",
        "cta2": "Ein Morgen mit Aera",
        "facts": ["Kostenlos", "Kein Konto", "Gesundheitswerte bleiben auf deinem iPhone"],
        "proof": "5,0 aus %d Bewertungen im ungarischen App Store",
        "chip_night": "7 Std. 25 Min. Schlaf, genau dein Bedarf", "chip_day": "Erholung über deinem Üblichen", "sleep_alt": "Der Schlaf-Bildschirm von Aera: 7 Std. 25 Min. Schlaf, genau dein Bedarf",
        "hero_alt": "Der Schlaf-Bildschirm von Aera für letzte Nacht: ausgezeichnet, genau dein Bedarf, 94 von 100 und 7 Std. 25 Min. Schlaf",
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
        "guide_kicker": "Der Field Guide",
        "guide_h2": "Jede Zahl zeigt, wie sie entsteht.",
        "guide_sub": "Tipp auf eine Zahl, und dahinter öffnet sich ein kurzer Artikel: wie sie berechnet wird, welche Forschung dahinter steht, mit Quellen zum Öffnen, und wo sie nicht mehr verlässlich ist.",
        "quote": "Die Apple Watch schätzt die Schlafphasen nur. Aera gibt ihnen deshalb weniger Gewicht und sagt dir das auch.",
        "quote_src": "Aus dem Artikel über deinen Schlafwert",
        "guide_link": "Notizen auf dieser Seite (auf Englisch)",
        "guide_alts": ("Der Field-Guide-Artikel über deinen Schlafwert", "Der Field-Guide-Artikel darüber, was Erholung misst"),
        "after_kicker": "Nach dem Lauf",
        "after_h2": "Spiel deinen Lauf in 3D noch einmal ab.",
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
        "also_h2": "Außerdem in Aera.",
        "tiles": [
            ("Apple Watch", "var(--green)", "Lauf nur mit der Uhr aufzeichnen, mit Auto-Pause, und jede Abbiegung am Handgelenk spüren."),
            ("Widgets", "var(--indigo)", "In jeder Größe, auf dem Home-Bildschirm und dem Sperrbildschirm."),
            ("Rückblicke", "var(--gold)", "Deine Woche, dein Monat und dein Jahr als kurzer Film."),
            ("Karten zum Teilen", "var(--orange)", "Satellit, Gelände und Splits. Jedes Wort änderbar, jede Farbe wählbar."),
            ("Deine Daten", "var(--pink)", "Rohdaten als JSON oder GPX, wann immer du willst."),
            ("Auf Deutsch", "var(--sage)", "Die ganze App auf Deutsch, und in neun weiteren Sprachen."),
        ],
        "priv_h2": "Gesundheits&shy;werte bleiben auf deinem iPhone.",
        "priv_sub": "Aera liest Apple Health auf dem Handy und berechnet jeden Wert dort. Kein Konto, kein Login, und in der App steckt nirgends ein Sprachmodell. Die Produktanalyse bleibt aus, bis du sie einschaltest, und enthält nie Gesundheitswerte. Absturzberichte helfen, Fehler zu beheben.",
        "priv_link": "Datenschutzerklärung (auf Englisch)",
        "plans_h2": "Was es kostet.",
        "free_h": "Kostenlos",
        "free": "Schlaf, Stress und Belastung gemessen an deinem Üblichen, und jeden Morgen ein Wort für den Tag. Jedes Training und jede Bestleistung, der Routenplaner mit Abbiegehinweisen, Flyover für Läufe der letzten sieben Tage, Rückblicke als Film und ein Jahr Verlauf, exportierbar als JSON oder GPX.",
        "prem_h": "Premium",
        "prem": "Die heutige Einheit: wie lange und wie hart. Deine Schlafreserve und deine Orte. Jede weitere Route, die du zeichnest, bleibt gespeichert. Flyover für ältere Läufe, Verlauf über ein Jahr hinaus, Berichte und jedes Exportformat.",
        "prem_note": "Premium gibt es monatlich, jährlich oder als einmaligen Kauf. Jährlich beginnt mit 7 Tagen gratis.",
        "faq_kicker": "Fragen",
        "faq_h2": "Fragen.",
        "faq": [
            ("Was macht Aera?", "Aera ist eine App für iPhone und Apple Watch, die Apple Health liest und dir jeden Morgen sagt, wie hart du heute rangehen kannst: Ruhetag, ruhig angehen, bereit oder leg los. Sie misst Schlaf, dein Herz in der Nacht, Stress und Belastung an deinem eigenen Üblichen, plant Routen auf der Karte mit Abbiegehinweisen und erklärt jede Zahl in einem kurzen Artikel."),
            ("Ist Aera kostenlos?", "Ja. Erholung, Stress, Belastung und dein Schlafwert, die Empfehlung für den Tag, der Routenplaner, die Abbiegehinweise, die Auswertung jedes Trainings, alle Bestleistungen und Flyover für die letzten sieben Tage sind kostenlos. Premium bringt die heutige Einheit, deine Schlafreserve, deine Orte, ältere Flyovers, Verlauf über zwölf Monate hinaus, Berichte und jedes Exportformat."),
            ("Brauche ich ein Konto, und wo landen meine Daten?", "Es gibt kein Konto. Aera liest Apple Health auf deinem iPhone und berechnet jeden Wert dort, deine Gesundheitswerte bleiben also auf deinem iPhone. In der App steckt kein Sprachmodell. Die Produktanalyse bleibt aus, bis du sie einschaltest, und enthält nie Gesundheitswerte."),
            ("Brauche ich eine Apple Watch?", "Die Apple Watch liefert die nächtlichen Herz- und Schlafsignale, auf denen die meisten Werte beruhen. Ohne sie arbeitet Aera mit dem, was dein iPhone aufzeichnet, etwa Schritte und Trainings, und die Werte, die eine Uhr brauchen, warten auf Daten."),
            ("Woher weiß Aera, was für mich normal ist?", "Aera lernt über mehrere Wochen aus deinen eigenen Nächten und Einheiten, was dein üblicher Bereich ist, und vergleicht jeden neuen Tag damit. Solange deine Daten dünn sind, sagt Aera, dass es noch lernt, statt zu raten."),
            ("Ist Aera ein Medizinprodukt?", "Nein. Aera ist für Wohlbefinden und Training im Alltag gemacht. Messungen der Uhr wie die Schlafphasen sind Schätzungen, und jeder Artikel sagt, wo seine Zahl nicht mehr verlässlich ist."),
            ("Welche Sprachen spricht Aera?", "Deutsch, Englisch, Ungarisch, Spanisch und Französisch vollständig, Italienisch, Japanisch, Portugiesisch und traditionelles Chinesisch teilweise."),
        ],
        "maker_kicker": "Wer sie macht",
        "maker_h2": "Von einem einzigen Menschen gemacht.",
        "maker_sub": "Aera wird von Gerg&#337; Varga gebaut, allein, ohne Firma dahinter. Die App sagt das auch in ihren Einstellungen. Eine Nachricht aus der App oder von dieser Seite erreicht ihn direkt.",
        "maker_link": "Schreib ihm",
        "close_h2": "Morgen früh siehst du, was die letzte Nacht sagt.",
        "foot_tag": "Letzte Nacht und der Lauf von heute, gemessen an dir.",
        "foot_app": "App", "foot_legal": "Rechtliches", "foot_more": "Mehr",
        "foot_links_app": [("store", "Laden"), ("support.html", "Support"), ("flyover.html", "Flyover"), ("press/", "Presse")],
        "foot_links_legal": [("privacy.html", "Datenschutz"), ("terms.html", "Nutzungsbedingungen"), ("terms.html#eula", "EULA")],
        "foot_links_more": [("tools/wie-weit.html", "Wie weit laufe ich?"), ("notes/index.html", "Notizen"), ("guides/index.html#de", "Ratgeber")],
        "meta_desc": "Schlaf- und Lauftracker für iPhone und Apple Watch. Aera vergleicht die Nacht mit deinem Üblichen und sagt, wie hart du heute läufst. Kostenlos, ohne Konto.",
        "foot_base": ("&#169; 2026 Aera", "Kein Medizinprodukt."),
    },
}

# Analytics. Both stay off until the real values exist; never invent them.
# CF_BEACON: the site token from Cloudflare > Web Analytics > Add a site (cookieless,
# no banner needed). APPSTORE_PT: the provider token from App Store Connect >
# App Analytics > Campaigns, so Apple counts downloads per page and button (ct=).
CF_BEACON = "4fc0403d67364f1ab92526387bdd0b81"
# Hungarian App Store rating count behind the "5.0" line in the hero. Checked
# 2026-10-09 with itunes.apple.com/lookup?id=6762456252&country=hu (5.0, 7).
# Re-check before each rebuild; set to 0 to drop the line if the average falls.
HU_RATINGS = 7
APPSTORE_PT = ""
OG_LOCALE = {"en": "en_US", "hu": "hu_HU", "de": "de_DE"}

LANG_NAMES = [("en", "index.html", "English"), ("hu", "hu.html", "Magyar"), ("de", "de.html", "Deutsch")]

# Captures of the app on 9 Oct 2026 (main 0ebe9a8). Name -> has light and dark?
FLIES = [(8, 74, 7.5, 0.0), (14, 82, 9.0, 1.2), (22, 70, 8.2, 2.1), (31, 86, 10.0, 0.6), (38, 77, 7.8, 3.0),
         (61, 84, 9.4, 1.7), (69, 72, 8.6, 0.3), (77, 88, 10.4, 2.5), (85, 76, 8.0, 1.0), (92, 83, 9.8, 3.4)]

THEMED = {"home", "sleep", "recovery", "session", "planner", "article-sleep"}



def picture(name, alt, sizes, eager=False):
    load = 'fetchpriority="high"' if eager is True else 'decoding="async"' if eager == "soon" else 'loading="lazy" decoding="async"'
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


# The app's own verdict word for a good morning (Localizable.xcstrings).


# The Coach: the acorn mascot, drawn from the app's own geometry
# (Aera/Components/AeraCoachMark.swift, a 100 x 100 box). Dark ink with the face
# cut out, so the sport-green capsule shows through, exactly as in the app.
COACH_BODY = ("M 24 50.6 C 36 49.2 64 49.2 76 50.6 C 82 51.3 84.8 54.4 85.6 59.4 C 87.4 71.6 81 84.6 68.8 92 C 62.8 95.6 56.4 96.6 52.6 98.6 C 50.9 99.5 49.1 99.5 47.4 98.6 C 43.6 96.6 37.2 95.6 31.2 92 C 19 84.6 12.6 71.6 14.4 59.4 C 15.2 54.4 18 51.3 24 50.6 Z "
              "M 87 40 C 87 44.3 84.6 46.6 80.4 46.6 L 19.6 46.6 C 15.4 46.6 13 44.3 13 40 C 13 25.51 27.17 16.6 46.34 15.6 L 53.66 15.6 C 72.83 16.6 87 25.51 87 40 Z "
              "M 57.4 7.4 C 55.38 9.82 54.47 12.38 54.26 15.6 L 45.68 15.6 C 46.19 10.18 49.1 6.05 54 3.6 C 56.6 2.3 59.2 5.2 57.4 7.4 Z")


def coach_svg(uid, label=""):
    eyes = "".join('<rect class="eye" x="%.2f" y="%.2f" width="11.5" height="17" rx="5.75"/>' % (cx - 5.75, 65.8 - 8.5) for cx in (39.4, 64.2))
    aria = ('role="img" aria-label="%s"' % label) if label else 'aria-hidden="true"'
    return ('<svg class="coach" viewBox="0 0 100 100" %s><defs>'
            '<linearGradient id="%s-ink" x1="0" y1="3" x2="0" y2="99" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#24401F"/><stop offset="1" stop-color="#10200F"/></linearGradient>'
            '<mask id="%s-face" maskUnits="userSpaceOnUse" x="0" y="0" width="100" height="100"><rect width="100" height="100" fill="#fff"/>'
            '<g class="eyes" fill="#000">%s</g>'
            '<path class="glad" d="M 33.4 69.4 Q 38.6 61.6 43.8 69.4 M 56.2 69.4 Q 61.4 61.6 66.6 69.4" fill="none" stroke="#000" stroke-width="4.4" stroke-linecap="round"/>'
            '<path d="M 46.4 82.2 Q 51.8 88.4 57.2 82.2" fill="none" stroke="#000" stroke-width="5.4" stroke-linecap="round"/></mask></defs>'
            '<g class="coach-body"><path d="%s" fill="url(#%s-ink)" mask="url(#%s-face)"/></g></svg>'
            % (aria, uid, uid, eyes, COACH_BODY, uid, uid))


# What early users tell us, as anonymous paraphrases (his ask 2026-10-09: no
# names, no one-by-one quotes). Each line restates one real source and nothing
# more; never invent a review, a reviewer or a rating count.
#   1. Tyler, founding tester, email 2026-10-02 (numbers match how he feels,
#      sleep most of all, Apple Health too generous).
#   2. MicheleMascia, App Store review DE, 5 stars (design, clear data, wellness
#      and training mix).
#   3. Marci0702, App Store review HU, 5 stars (fast, straightforward, intuitive,
#      feature rich).
REVIEWS = {
    "en": [("Matches how I feel", "The numbers line up with how my body actually feels in the morning, sleep most of all. Closer than the sleep scores I was used to.", "Founding tester"),
           ("Clear at a glance", "A design people like, with the data laid out clearly. A good mix of wellness and training.", "App Store review"),
           ("Fast and simple", "Quick, straightforward and easy to find your way around, with a lot inside.", "App Store review")],
    "hu": [("Úgy mutat, ahogy érzem", "A számok azt mutatják, amit reggel a testem tényleg érez, főleg az alvásnál. Pontosabb, mint az alváspontok, amikhez hozzászoktam.", "Alapító tesztelő"),
           ("Első ránézésre érthető", "Szép kialakítás, átlátható adatok. Jó egyensúly a jóllét és az edzés között.", "App Store-értékelés"),
           ("Gyors és egyszerű", "Gyors, egyenes, könnyen kiismerhető, és sok minden van benne.", "App Store-értékelés")],
    "de": [("Passt zu meinem Gefühl", "Die Zahlen passen dazu, wie sich mein Körper morgens wirklich anfühlt, beim Schlaf am meisten. Genauer als die Schlafwerte, die ich kannte.", "Gründungstester"),
           ("Auf einen Blick klar", "Ein Design, das gefällt, und Daten, die klar aufbereitet sind. Eine gute Mischung aus Wohlbefinden und Training.", "App-Store-Bewertung"),
           ("Schnell und einfach", "Schnell, geradlinig und leicht zu verstehen, mit viel drin.", "App-Store-Bewertung")],
}
# The page tells one day. A small bar under the nav lights the chapter you are in.
CHAPTERS = {
    "en": ("Chapters", [("engine", "Last night"), ("guide", "This morning"), ("planner", "Out the door"), ("flyover", "After the run")]),
    "hu": ("Fejezetek", [("engine", "Tegnap éjjel"), ("guide", "Ma reggel"), ("planner", "Ki az ajtón"), ("flyover", "Futás után")]),
    "de": ("Kapitel", [("engine", "Letzte Nacht"), ("guide", "Heute früh"), ("planner", "Raus"), ("flyover", "Nach dem Lauf")]),
}


def chapters_nav(code):
    label, items = CHAPTERS[code]
    links = "".join('<a href="#%s" data-ch="%s"><i></i><span>%s</span></a>' % (i, i, t) for i, t in items)
    return '<nav class="chapters" aria-label="%s">%s<span class="ch-now" aria-hidden="true"></span></nav>' % (label, links)


REVIEW_COPY = {
    "en": {"kicker": "From early users", "h2": "Mornings that feel right.", "note": "What testers and App Store reviewers tell us, in our words."},
    "hu": {"kicker": "Korai felhasználók", "h2": "Reggelek, ahogy tényleg érzed őket.", "note": "Amit a tesztelők és az App Store-értékelések mondanak, a mi szavainkkal."},
    "de": {"kicker": "Erste Stimmen", "h2": "Morgen, die sich richtig anfühlen.", "note": "Was Tester und App-Store-Bewertungen sagen, in unseren Worten."},
}


def reviews_section(code):
    rc = REVIEW_COPY[code]
    (t0, x0, s0), rest = REVIEWS[code][0], REVIEWS[code][1:]
    more = "".join('<figure class="rv reveal" style="--d:%.2fs"><p class="rv-title">%s</p><p class="rv-text">%s</p>'
                   '<figcaption>%s</figcaption></figure>' % (0.1 + i * 0.1, t, x, src)
                   for i, (t, x, src) in enumerate(rest))
    rating = ""
    if HU_RATINGS:
        rating = ('<p class="rv-rating"><span class="rating-stars" aria-hidden="true">&#9733;&#9733;&#9733;&#9733;&#9733;</span>'
                  '<span>%s</span></p>' % (COPY[code]["proof"] % HU_RATINGS))
    return f"""<section class="reviews">
  <div class="wide">
    <figure class="rv-lead reveal">
      <blockquote><p>&#8220;{x0}&#8221;</p></blockquote>
      <figcaption>{s0}</figcaption>
    </figure>
    {rating}
    <div class="rv-grid">{more}</div>
    <p class="footnote center">{rc['note']}</p>
  </div>
</section>"""


# Cinematic scroll scenes live in scenes/<name>/ (see scenes/CONTRACT.md):
# section.html with {{key}} placeholders, strings.json per language, scene.css
# and scene.js. The page links one bundled scenes.css and scenes.js.
SCENES = ["engine", "flyover", "planner", "widgets"]  # add a scene here once it is reviewed


def scene_ready(name):
    return name in SCENES and os.path.exists(os.path.join(ROOT, "scenes", name, "section.html"))


def scene(name, code):
    if not scene_ready(name):
        return ""
    d = os.path.join(ROOT, "scenes", name)
    with open(os.path.join(d, "strings.json"), encoding="utf-8") as f:
        strings = dict(json.load(f)[code])
    strings.setdefault("coach", coach_svg("%s-%s" % (name[:3], code)))
    with open(os.path.join(d, "section.html"), encoding="utf-8") as f:
        return re.sub(r"\{\{(\w+)\}\}", lambda m: strings[m.group(1)], f.read().strip())


def bundle_scenes():
    for ext in ("css", "js"):
        parts = []
        for name in SCENES:
            path = os.path.join(ROOT, "scenes", name, "scene." + ext)
            if scene_ready(name) and os.path.exists(path):
                with open(path, encoding="utf-8") as f:
                    parts.append("/* scenes/%s */\n%s" % (name, f.read().strip()))
        with open(os.path.join(ROOT, "scenes." + ext), "w", encoding="utf-8") as f:
            f.write("/* Generated by scripts/build_home.py from each scenes/NAME/scene.%s. Edit those. */\n" % ext + "\n\n".join(parts) + "\n")


def asset(name):
    """name?v=<content hash>: a deploy changes the URL, so no cache serves a stale file."""
    import hashlib
    with open(os.path.join(ROOT, name), "rb") as f:
        return "%s?v=%s" % (name, hashlib.sha1(f.read()).hexdigest()[:10])


def build(code):
    c = COPY[code]
    L = landscape.hero_layers()

    def store_at(place):
        # Every App Store button goes through /get/<place>/<lang>/ on this site, so
        # each tap is a path Cloudflare's free analytics can count (they drop query
        # strings). write_get_pages() puts a forwarding page at each path; a
        # Cloudflare redirect rule can answer first.
        return "/get/%s/%s/" % (place, code)

    store = store_at("hero")
    store_nav, store_close = store_at("nav"), store_at("closing")

    def href(h):
        return store_at("footer") if h == "store" else h

    alternates = "".join('<link rel="alternate" hreflang="%s" href="%s%s">' % (lc, BASE, "" if f == "index.html" else f)
                         for lc, f, _ in LANG_NAMES)
    alternates += '<link rel="alternate" hreflang="x-default" href="%s">' % BASE
    canonical = BASE + ("" if c["file"] == "index.html" else c["file"])
    nav = "".join('<a class="opt" href="%s">%s</a>' % (h, t) for h, t in c["nav"])
    facts = "".join("<li>%s</li>" % f for f in c["facts"])
    proof = ('<p class="proof rise" style="--d:.62s"><span class="rating-stars" aria-hidden="true">&#9733;&#9733;&#9733;&#9733;&#9733;</span> %s</p>' % (c["proof"] % HU_RATINGS)) if HU_RATINGS else ""

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

    dots = "".join('<i style="--c:%s"%s></i>' % (st[2], ' class="on"' if i == 0 else "") for i, st in enumerate(c["steps"]))

    faq = "".join('<details class="qa reveal"><summary><h3>%s</h3><span class="plus" aria-hidden="true"></span></summary><p>%s</p></details>'
                  % (q, a) for q, a in c["faq"])

    tiles = "".join('<div class="tile reveal" style="--d:%dms"><h3>%s</h3><p>%s</p></div>'
                    % ((i % 3) * 80, t, p)
                    for i, (t, col, p) in enumerate(c["tiles"]))

    topo = landscape.contours()
    route = ('<path class="route-glow" pathLength="1" d="M760 960 C 780 820, 690 730, 820 640 S 970 560, 1000 430 S 1120 250, 1260 300 S 1420 430, 1500 300 S 1580 160, 1650 140"/><path id="route" class="route" pathLength="1" d="M760 960 C 780 820, 690 730, 820 640 S 970 560, 1000 430 S 1120 250, 1260 300 S 1420 430, 1500 300 S 1580 160, 1650 140"/><circle id="rhead" class="rhead" cx="760" cy="960" r="7"/>')

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

    import json as _json
    plain = lambda t: html.unescape(t)
    graph = [
        {"@type": "MobileApplication", "@id": BASE + "#app", "name": "Aera",
         "alternateName": plain(c["title"].split(":")[1].strip()) if ":" in c["title"] else "Aera",
         "applicationCategory": "HealthApplication", "applicationSubCategory": "Sleep and running tracker",
         "operatingSystem": "iOS, watchOS", "inLanguage": ["en", "hu", "de", "es", "fr", "it", "ja", "pt", "zh-Hant"],
         "url": canonical, "downloadUrl": c["store"], "installUrl": c["store"],
         "description": plain(c["desc"]),
         "screenshot": [BASE + "img/sleep-light-800.webp", BASE + "img/session-dark-800.webp", BASE + "img/planner-dark-800.webp"],
         "featureList": [plain(st[3]) for st in c["steps"]] + [plain(c["after_h2"])],
         "author": {"@id": BASE + "#maker"}, "publisher": {"@id": BASE + "#org"}, "isAccessibleForFree": True,
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD", "category": "free"}},
        {"@type": "Person", "@id": BASE + "#maker", "name": "Gerg\u0151 Varga", "url": BASE},
        {"@type": "Organization", "@id": BASE + "#org", "name": "Aera", "url": BASE, "logo": BASE + "assets/icon.png",
         "email": "hello@aerahealth.app", "founder": {"@id": BASE + "#maker"}, "sameAs": [COPY["en"]["store"]]},
        {"@type": "WebSite", "@id": BASE + "#site", "name": "Aera", "url": BASE, "inLanguage": code,
         "publisher": {"@id": BASE + "#org"}},
        {"@type": "FAQPage", "inLanguage": code,
         "mainEntity": [{"@type": "Question", "name": plain(q), "acceptedAnswer": {"@type": "Answer", "text": plain(a)}}
                        for q, a in c["faq"]]},
    ]
    ld = _json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False).replace("</", "<\\/")

    beacon = ""
    if CF_BEACON:
        beacon = ('<script defer src="https://static.cloudflareinsights.com/beacon.min.js" '
                  "data-cf-beacon='{\"token\": \"%s\"}'></script>" % CF_BEACON)

    og_alt = "".join('<meta property="og:locale:alternate" content="%s">' % OG_LOCALE[lc] for lc in OG_LOCALE if lc != code)

    after_old = f"""<section class="after">
  <svg class="topo" viewBox="0 0 1600 900" preserveAspectRatio="xMidYMid slice" aria-hidden="true">{''.join(topo)}{route}</svg>
  <div class="wide after-grid">
    <div class="reveal">
      <p class="kicker">{c['after_kicker']}</p>
      <h2 class="h2 split">{c['after_h2']}</h2>
      <p class="sub">{c['after_sub']}</p>
      <ul class="list">{''.join('<li>%s</li>' % x for x in c['after_list'])}</ul>
    </div>
    <div class="duo reveal" style="--d:.15s">
      {phone('workout-flyover-dark', c['after_alts'][0], '(max-width: 899px) 46vw, 280px', cls='par" data-par="-0.06')}
      {phone('workout-detail', c['after_alts'][1], '(max-width: 899px) 46vw, 280px', cls='par" data-par="0.08')}
    </div>
  </div>
</section>
"""
    map_old = f"""<section>
  <div class="wide map-grid">
    <div class="reveal">
      <p class="kicker">{c['map_kicker']}</p>
      <h2 class="h2 split">{c['map_h2']}</h2>
      <p class="sub">{c['map_sub']}</p>
    </div>
    <div class="duo reveal" style="--d:.15s">
      {phone('planner', c['map_alts'][0], '(max-width: 899px) 46vw, 280px', cls='par" data-par="-0.06')}
      {phone('routenav', c['map_alts'][1], '(max-width: 899px) 46vw, 280px', cls='par" data-par="0.08')}
    </div>
  </div>
</section>
"""
    return f"""<!DOCTYPE html>
<html lang="{c['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="apple-itunes-app" content="app-id=6762456252">
<title>{c['title']}</title>
<meta name="description" content="{c['meta_desc']}">
<meta name="theme-color" content="#f6f4ef" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#000000" media="(prefers-color-scheme: dark)">
<meta property="og:title" content="{c['og_title']}">
<meta property="og:description" content="{c['meta_desc']}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Aera">
<meta property="og:locale" content="{OG_LOCALE[code]}">{og_alt}
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{BASE}assets/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{c['og_title']}">
<meta name="twitter:description" content="{c['meta_desc']}">
<meta name="twitter:image" content="{BASE}assets/og.jpg">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{canonical}">
{alternates}
<link rel="icon" href="assets/icon.png">
<link rel="apple-touch-icon" href="assets/icon.png">
<link rel="stylesheet" href="{asset('home.css')}">
<link rel="stylesheet" href="{asset('scenes.css')}">
<script type="application/ld+json">{ld}</script>
{legacy}
</head>
<body>
<a class="skip" href="#engine">{c['skip']}</a>

<header class="bar">
  <div class="wide">
    <a class="brand" href="{c['file']}"><img src="assets/icon.png" alt="" width="30" height="30">Aera</a>
    <nav>{nav}<a class="get" href="{store_nav}">{c['get']}</a></nav>
  </div>
  {chapters_nav(code)}
</header>

<main>
<section class="hero" aria-labelledby="h1">
  <div class="sky sky-a"></div><div class="sky sky-b"></div>
  {L['stars']}
  <div class="moon"></div><div class="sun"></div>
  <div class="clouds" aria-hidden="true"><i></i><i></i><i></i></div>
  <div class="flies" aria-hidden="true">{''.join('<i style="--x:%d%%;--y:%d%%;--t:%.1fs;--o:%.1fs"></i>' % (x, y, t, o) for x, y, t, o in FLIES)}</div>
  {L['far']}{L['mid']}{L['wood']}
  <div class="wide hero-inner">
    <div class="hero-copy">
      <p class="eyebrow rise" style="--d:.1s">{c['eyebrow']}</p>
      <h1 id="h1" class="rise split" style="--d:.2s">{c['h1']}</h1>
      <p class="lede rise" style="--d:.32s">{c['lede']}</p>
      <div class="cta rise" style="--d:.44s">
        <a class="btn btn-store" href="{store}">{APPLE}{c['cta']}</a>
        <a class="btn btn-quiet" href="#engine">{c['cta2']}</a>
      </div>
      <ul class="facts rise" style="--d:.54s">{facts}</ul>
      {proof}
    </div>
    <div class="hero-phone">
      <div class="phone hero-ph"><div class="screen-wrap">
        <div class="hs hs-home">{picture('sleep', c['hero_alt'], '(max-width: 899px) 64vw, 380px', eager=True)}</div>
      </div></div>
    </div>
  </div>
  {L['near']}
</section>

{scene('engine', code)}

<section id="guide" class="guide-sec">
  <div class="wide guide-grid">
    <div class="reveal">
      <h2 class="h2 split">{c['guide_h2']}</h2>
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



{scene('widgets', code)}

{scene('planner', code) or map_old}

{scene('flyover', code) or after_old}

<section class="privacy">
  <div class="wide center reveal">
    <div class="lock">{LOCK}</div>
    <h2 class="h2 split">{c['priv_h2']}</h2>
    <p class="sub">{c['priv_sub']}</p>
    <a class="link" href="privacy.html">{c['priv_link']} &#8594;</a>
  </div>
</section>

<section class="also">
  <div class="wide">
    <div class="center reveal">
      <h2 class="h2 split">{c['also_h2']}</h2>
    </div>
    <div class="tiles">{tiles}</div>
  </div>
</section>

{reviews_section(code)}

<section>
  <div class="wide">
    <h2 class="h2 split center reveal">{c['plans_h2']}</h2>
    <div class="plans">
      <div class="plan reveal"><h3>{c['free_h']}</h3><p>{c['free']}</p></div>
      <div class="plan reveal" style="--d:.1s"><h3>{c['prem_h']}</h3><p>{c['prem']}</p></div>
    </div>
    <p class="plans-note center reveal">{c['prem_note']}</p>
  </div>
</section>

<section class="faq-sec">
  <div class="wide faq-grid">
    <div class="reveal">
      <h2 class="h2 split">{c['faq_h2']}</h2>
    </div>
    <div class="faq">{faq}</div>
  </div>
</section>

<section class="maker-sec">
  <div class="wide maker center reveal">
    <h2 class="h2 split">{c['maker_h2']}</h2>
    <p class="sub">{c['maker_sub']}</p>
    <a class="link" href="support.html">{c['maker_link']} &#8594;</a>
  </div>
</section>

<section class="closing">
  <div class="wide reveal">
    <img class="closing-icon" src="assets/icon.png" alt="" width="96" height="96" loading="lazy" decoding="async">
    <h2 class="h2 split">{c['close_h2']}</h2>
    <div class="cta"><a class="btn btn-store" href="{store_close}">{APPLE}{c['cta']}</a></div>
  </div>
  <div class="dusk" aria-hidden="true"><div class="dusk-sun"></div>{landscape.dusk_stars()}{landscape.dusk_layers()}</div>
</section>
</main>

<footer>
  <div class="wide">
    <div class="foot">
      <div class="foot-brand"><a class="brand" href="{c['file']}"><img src="assets/icon.png" alt="" width="30" height="30">Aera</a><p>{c['eyebrow']}</p></div>
      {foot_col(c['foot_app'], c['foot_links_app'])}
      {foot_col(c['foot_legal'], c['foot_links_legal'])}
      <div><h4>{c['foot_more']}</h4>{''.join('<a href="%s">%s</a>' % (h, t) for h, t in c['foot_links_more'])}{langs}</div>
    </div>
    <div class="foot-base"><span>{c['foot_base'][0]}</span><span>{c['foot_base'][1]}</span></div>
  </div>
</footer>

<script src="{asset('home.js')}" defer></script>
<script src="{asset('scenes.js')}" defer></script>
{beacon}
</body>
</html>
"""


LOCALES = ("hu", "de")


def localize_media(out, code):
    """On /hu and /de, use the in-app shots in that language where they exist:
    img/NAME.webp -> img/<code>/NAME.webp, media/X/NAME -> media/X/<code>/NAME.
    Same file names per language; anything not yet captured stays English."""
    if code not in LOCALES:
        return out

    def swap(m):
        d, name = m.group(1), m.group(2)
        local = "%s/%s/%s" % (d, code, name)
        return local if os.path.exists(os.path.join(ROOT, local)) else m.group(0)
    return re.sub(r"\b(img|media/[\w-]+)/([\w.-]+\.(?:webp|png|jpg|mp4|webm))", swap, out)


GET_PLACES = ("nav", "hero", "closing", "footer")


def get_page(store, lang, src):
    """One forwarding page: on to that language's App Store page, with
    the campaign tags once APPSTORE_PT is set. Out of search."""
    url = store
    if APPSTORE_PT:
        url += "?pt=%s&ct=site-%s-%s&mt=8" % (APPSTORE_PT, lang, src)
    beacon = ('<script defer src="https://static.cloudflareinsights.com/beacon.min.js" '
              "data-cf-beacon='{\"token\": \"%s\"}'></script>" % CF_BEACON) if CF_BEACON else ""
    return """<!doctype html>
<html lang="%(lang)s"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Aera on the App Store</title>
<meta http-equiv="refresh" content="2; url=%(url)s">
<script>
// Leave a moment after load so the Cloudflare beacon can report the tap first;
// go anyway at 1.5 s if the beacon is blocked or slow.
(function () {
  var go = function () { location.replace(%(js)s); };
  addEventListener('load', function () { setTimeout(go, 400); });
  setTimeout(go, 1500);
})();
</script>
%(beacon)s
<style>body{margin:0;min-height:100vh;display:grid;place-items:center;font:17px/1.4 -apple-system,system-ui,sans-serif;background:#f6f4ef;color:#1c1c1e}@media (prefers-color-scheme:dark){body{background:#0b0b0c;color:#f2f2f2}}a{color:inherit}</style>
</head><body><p><a href="%(url)s">Open Aera on the App Store</a></p></body></html>
""" % {"lang": lang, "url": url.replace("&", "&amp;"), "js": json.dumps(url), "beacon": beacon}


def write_get_pages():
    """get/<place>/<lang>/index.html for every store button, plus get/index.html
    for a bare /get/ (English store)."""
    for c in COPY.values():
        for place in GET_PLACES:
            d = os.path.join(ROOT, "get", place, c["lang"])
            os.makedirs(d, exist_ok=True)
            with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
                f.write(get_page(c["store"], c["lang"], place))
    with open(os.path.join(ROOT, "get", "index.html"), "w", encoding="utf-8") as f:
        f.write(get_page(COPY["en"]["store"], "en", "site"))


if __name__ == "__main__":
    bundle_scenes()
    for code in COPY:
        out = localize_media(build(code), code)
        if "—" in out:
            raise SystemExit("em dash in %s" % code)
        with open(os.path.join(ROOT, COPY[code]["file"]), "w", encoding="utf-8") as f:
            f.write(out)
        print(COPY[code]["file"], len(out) // 1024, "KB")
    write_get_pages()
