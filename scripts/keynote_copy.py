# -*- coding: utf-8 -*-
"""Words for the home page (index.html, hu.html, de.html), built by
scripts/build_keynote.py. One idea per section; the picture carries the rest.

Rules (Gergő, 2026-10): lead with the motto, never pitch recovery or
readiness, never say AI, never sound Apple-Watch-only, no kickers over every
headline, no icon tiles, no em dashes. Hungarian lines come from the
Hungarian site copy thread, never written here by hand."""

K = {
    "en": {
        "title": "Aera: your watch counts, Aera explains",
        "desc": "Aera tells you what your watch's numbers mean for you, and shows how it knows. Sleep, heart and runs from Apple Health, against your own usual. Free, no account.",
        "og_title": "Your watch counts. Aera explains.",
        "skip": "Skip to content",
        "nav": [("guides/index.html", "Guides"), ("notes/index.html", "Notes"), ("support.html", "Support")],
        "get": "Get Aera",
        "h1": "Your watch counts.<br>Aera explains.",
        "sub": "Aera tells you what your watch&#8217;s numbers mean for you, and shows how it knows.",
        "cta": "Download on the App Store",
        "note": "Free &#183; No account &#183; Works with any watch or ring that writes to Apple Health",
        "hero_alt": "Aera on iPhone and Apple Watch: last night's sleep, 55 minutes over your need, and the day so far on the watch",
        "why_h2": "A number with no reason is just a number.",
        "why_p": "Watches count everything: hours asleep, heartbeats, kilometres. Then they stop at a score and leave you guessing. <b>Aera picks up where the score stops.</b> It holds each number against your own usual, says in plain words what it means, and opens it to show how it was worked out.",
        "bento_h2": "Everything your watch counts, measured against your usual.",
        "work_link": ("guides/what-is-a-good-sleep-score.html", "Read one: the sleep score"),
        "b_sleep": ("Sleep, against your own need.", "Not eight hours for everyone. The need Aera learned from your own nights."),
        "b_run": ("Every run, against your usual.", "Pace, heart rate and time, each beside what is normal for you."),
        "b_replay": ("Replay a run in 3D.", "Your route, flown over the real ground."),
        "b_route": ("Plan a route from your door.", "Tap the map and the line keeps to real paths."),
        "b_watch": ("On your wrist, too.", "Last night and the day so far, a glance away."),
        "b_lock": ("No account.", "Every score is worked out on your iPhone."),
        "b_work": ("Every number shows its work.", "Tap any number for how it was worked out, the research behind it, and where it stops being reliable."),
        "sleep_h2": "Sleep, explained.",
        "sleep_p": "Your watch says how long you slept. Aera says what that means for you: <b>measured against the sleep you need</b>, learned from your own nights. Stages are shown as what they are: an estimate.",
        "sleep_alt": "Aera's Sleep screen on iPhone: Excellent, 55 minutes over your need, 89 of 100, 8 hours 19 minutes asleep",
        "run_h2": "Runs, read back.",
        "run_p": "Every run sits beside your usual: <b>faster or slower than normal for you, harder or easier on your heart.</b> Then fly it again in 3D, over the ground you ran.",
        "run_alts": ("A run replayed in 3D over satellite ground, with distance, pace and heart rate", "A morning run read back: distance, time, pace and energy, each against your usual", "Aera on Apple Watch during a run: time, distance, pace and heart rate in zone 3"),
        "route_h2": "Plan it. Then just run.",
        "route_p": "Draw a route that keeps to real paths, or open a GPX file. <b>Every turn comes before you reach it</b>, on your phone, your wrist or read aloud.",
        "route_alts": ("A route drawn from the door around Green Lake, keeping to real paths", "Turn by turn on Apple Watch: 202 metres, fork, keep right"),
        "wear_h2": "Wear what you like.",
        "wear_p": "Aera reads Apple Health, so it works with an Apple Watch, and with any watch, ring or app that writes your sleep and workouts there.",
        "wear_list": ["Apple Watch", "Garmin", "Oura", "WHOOP", "iPhone"],
        "wear_link": ("guides/aera-with-garmin-oura-whoop.html", "What reaches Apple Health from each"),
        "priv_h2": "Health numbers stay on your iPhone.",
        "priv_p": "No account and no server doing the maths. Aera reads Apple Health on your phone and works out every score there. Analytics stay off until you turn them on, and never include health values.",
        "priv_link": ("privacy.html", "Read the privacy policy"),
        "lock_alt": "",
        "plans_h2": "Free to start.",
        "free_h": "Free",
        "free": ["Sleep, stress and strain, against your usual", "Every run read back, every personal best", "Route planner with turn by turn", "Flyover for the last seven days"],
        "prem_h": "Premium",
        "prem": ["Today&#8217;s session: how long, how hard", "Your sleep reserve and your places", "Unlimited saved routes", "Older Flyovers, full history, every export"],
        "prem_note": "Monthly, yearly or a one-time purchase. Yearly starts with a 7-day free trial.",
        "faq_h2": "Questions.",
        "faq": [
            ("What does Aera do?", "Aera reads what your watch, ring or phone writes to Apple Health and tells you what those numbers mean for you. Sleep, stress, strain and every run are held against your own usual, said in plain words, and each number opens a short article on how it was worked out. It also plans routes with turn-by-turn directions and replays runs in 3D."),
            ("Do I need an Apple Watch?", "No. Aera reads Apple Health, so any watch, ring or app that writes your sleep, heart rate and workouts there will do: Apple Watch, Garmin, Oura, WHOOP and others. With only an iPhone, Aera works from steps and workouts, and the reads that need overnight heart data wait until there is some."),
            ("Is Aera free?", "Yes. Sleep, stress and strain against your usual, every run read back, every personal best, the route planner with turn by turn and Flyover for the last seven days are free. Premium adds today&#8217;s session, your sleep reserve, your places, unlimited saved routes, older Flyovers, full history and every export format."),
            ("Do I need an account, and where does my data go?", "There is no account. Aera reads Apple Health on your iPhone and works out every score there, so health numbers stay on your iPhone. Product analytics stay off until you turn them on and never include health values."),
            ("How does Aera know what is normal for me?", "It learns your usual range from your own nights and sessions over several weeks, then compares each new day with it. While your history is thin, it says it is still learning instead of guessing."),
            ("Is Aera a medical device?", "No. Aera is for everyday wellbeing and training. Watch measurements such as sleep stages are estimates, and every article says where its number stops being reliable."),
            ("Which languages does Aera speak?", "English, Hungarian, German, Spanish and French in full, and Italian, Japanese, Portuguese and Traditional Chinese in part."),
        ],
        "maker_h2": "Made by one person.",
        "maker_p": "Aera is built by Gerg&#337; Varga, on his own, with no company behind it. A message from the app or from this site reaches him directly.",
        "maker_link": ("mailto:hello@aerahealth.app", "Write to him"),
        "close_h2": "Your watch counts.<br>Aera explains.",
        "close_note": "Free on the App Store. No account.",
        "foot_tag": "Your watch counts. Aera explains.",
    },
    "hu": {'title': 'Aera: az órád méri, az Aera elmagyarázza',
     'desc': 'Az Aera elmondja, mit jelentenek neked az órád számai, és megmutatja, honnan tudja. Alvás, szív és '
             'futás az Apple Health-ből, a saját megszokottadhoz mérve. Ingyenes, fiók nélkül.',
     'og_title': 'Az órád méri. Az Aera elmagyarázza.',
     'skip': 'Ugrás a tartalomra',
     'nav': [('guides/index.html', 'Útmutatók'),
             ('notes/index.html', 'Jegyzetek'),
             ('support.html', 'Támogatás')],
     'get': 'Aera letöltése',
     'h1': 'Az órád méri.<br>Az Aera elmagyarázza.',
     'sub': 'Az Aera elmondja, mit jelentenek neked az órád számai, és megmutatja, honnan tudja.',
     'cta': 'Letöltés az App Store-ból',
     'note': 'Ingyenes &#183; Fiók nélkül &#183; Bármilyen órával vagy gyűrűvel, amelyik az Apple Health-be ír',
        'work_link': ('guides/jo-alvas-pontszam.html', 'Nézz meg egyet: az alváspontszám'),
     'hero_alt': 'Az Aera iPhone-on és Apple Watch-on: a tegnap éjszakai alvás 58 perccel az igényed fölött, az '
                 'órán pedig az eddigi nap',
     'why_h2': 'Egy szám magyarázat nélkül csak egy szám.',
     'why_p': 'Az órák mindent megszámolnak: alvóórákat, szívveréseket, kilométereket. Aztán megállnak egy '
              'pontszámnál, és a többit rád bízzák. <b>Az Aera ott folytatja, ahol a pontszám véget ér.</b> '
              'Minden számot a saját megszokottadhoz mér, egyszerű szavakkal elmondja, mit jelent, és ha '
              'megnyitod, megmutatja, hogyan jött ki.',
     'bento_h2': 'Mindaz, amit az órád mér, hozzád mérve.',
     'b_sleep': ('Alvás a saját igényedhez mérve.',
                 'Nem mindenkinek nyolc óra. Az az igény, amit az Aera a saját éjszakáidból tanult meg.'),
     'b_run': ('Minden futás a megszokottadhoz mérve.',
               'Tempó, pulzus és idő, mindegyik amellett, ami nálad megszokott.'),
     'b_replay': ('Nézd vissza a futásod 3D-ben.', 'Az útvonalad, a valódi terep fölött.'),
     'b_route': ('Tervezz útvonalat a kapudtól.', 'Koppints a térképre, és a vonal a valódi utakon marad.'),
     'b_watch': ('A csuklódon is.', 'A tegnap éjszaka és az eddigi nap, egy pillantással.'),
     'b_lock': ('Fiók nélkül.', 'Minden pontszámot az iPhone-od számol ki.'),
     'b_work': ('Minden szám megmutatja, honnan jön.',
                'Koppints bármelyik számra: látod, hogyan jött ki, milyen kutatás áll mögötte, és meddig '
                'bízhatsz benne.'),
     'sleep_h2': 'Az alvásod, érthetően.',
     'sleep_p': 'Az órád megmondja, mennyit aludtál. Az Aera azt mondja meg, mit jelent ez neked: <b>ahhoz '
                'mérve, amennyi alvásra szükséged van</b>, a saját éjszakáidból tanulva. Az alvásfázisokat pedig '
                'annak mutatja, amik: becslésnek.',
     'sleep_alt': 'Az Aera Alvás képernyője iPhone-on: Kiváló, 58 perccel az igényed fölött, 100-ból 88 pont, 8 '
                  'óra 22 perc alvás',
     'run_h2': 'A futásaid, visszaolvasva.',
     'run_p': 'Minden futás a megszokottad mellett áll: <b>gyorsabb vagy lassabb volt-e, mint nálad szokásos, és '
              'jobban vagy kevésbé terhelte-e a szíved.</b> Aztán nézd vissza 3D-ben, a terep fölött, amin '
              'futottál.',
     'run_alts': ('Egy futás 3D-s visszajátszása műholdképes terep fölött, távval, tempóval és pulzussal',
                  'Egy reggeli futás visszaolvasva: táv, idő, tempó és energia, mindegyik a megszokottadhoz '
                  'mérve',
                  'Az Aera Apple Watch-on futás közben: idő, táv, tempó és pulzus a 3-as zónában'),
     'route_h2': 'Tervezd meg. Aztán csak fuss.',
     'route_p': 'Rajzolj olyan útvonalat, ami a valódi utakon marad, vagy nyiss meg egy GPX-fájlt. <b>Minden '
                'kanyart még előtte jelez</b>, a telefonodon, a csuklódon vagy hangosan felolvasva.',
     'route_alts': ('Útvonal a kaputól a Green Lake körül, végig a valódi utakon',
                    'Kanyarról kanyarra Apple Watch-on: 202 méter, elágazás, tarts jobbra'),
     'wear_h2': 'Hordd, amit szeretsz.',
     'wear_p': 'Az Aera az Apple Health-ből olvas, így működik Apple Watch-csal, és bármilyen órával, gyűrűvel '
               'vagy appal, amelyik oda írja az alvásodat és az edzéseidet.',
     'wear_list': ['Apple Watch', 'Garmin', 'Oura', 'WHOOP', 'iPhone'],
     'wear_link': ('guides/aera-garmin-oura-whoop-vel.html', 'Mi jut át az egyes eszközökről az Apple Health-be'),
     'priv_h2': 'Az egészségadataid az iPhone-odon maradnak.',
     'priv_p': 'Nincs fiók, és nincs szerver, ami számolna. Az Aera az iPhone-odon olvassa az Apple Health-et, '
               'és ott számol ki minden pontszámot. Az analitika ki van kapcsolva, amíg be nem kapcsolod, és '
               'egészségadatot soha nem tartalmaz.',
     'priv_link': ('privacy.html', 'Az adatvédelmi tájékoztató'),
     'lock_alt': '',
     'plans_h2': 'Ingyen kezdheted.',
     'free_h': 'Ingyenes',
     'free': ['Alvás, stressz és terhelés a megszokottadhoz mérve',
              'Minden futás visszaolvasva, minden egyéni rekord',
              'Útvonaltervező, kanyarról kanyarra navigációval',
              'Flyover az elmúlt hét napra'],
     'prem_h': 'Premium',
     'prem': ['Mai edzés: mennyi ideig, milyen keményen',
              'Az Alvásbankod és a helyeid',
              'Korlátlan mentett útvonal',
              'Régebbi Flyoverek, teljes előzmények, minden exportformátum'],
     'prem_note': 'Havi vagy éves előfizetés, vagy egyszeri vásárlás. Az éves 7 napos ingyenes próbával indul.',
     'faq_h2': 'Kérdések.',
     'faq': [('Mit csinál az Aera?',
              'Az Aera azt olvassa, amit az órád, a gyűrűd vagy a telefonod az Apple Health-be ír, és elmondja, '
              'mit jelentenek neked ezek a számok. Az alvást, a stresszt, a terhelést és minden futást a saját '
              'megszokottadhoz méri, egyszerű szavakkal mondja el, és minden számból egy rövid cikk nyílik '
              'arról, hogyan jött ki. Útvonalat is tervez kanyarról kanyarra navigációval, és 3D-ben '
              'visszajátssza a futásaidat.'),
             ('Kell hozzá Apple Watch?',
              'Nem. Az Aera az Apple Health-ből olvas, így bármilyen óra, gyűrű vagy app megfelel, amelyik oda '
              'írja az alvásodat, a pulzusodat és az edzéseidet: Apple Watch, Garmin, Oura, WHOOP és mások. Csak '
              'iPhone-nal az Aera a lépésekből és az edzésekből dolgozik, az éjszakai szívadatot igénylő '
              'elemzések pedig megvárják, amíg ilyen adat is lesz.'),
             ('Ingyenes az Aera?',
              'Igen. Ingyenes az alvás, a stressz és a terhelés a megszokottadhoz mérve, minden futás '
              'visszaolvasása, minden egyéni rekord, az útvonaltervező kanyarról kanyarra navigációval és a '
              'Flyover az elmúlt hét napra. A Premium ehhez hozzáadja a Mai edzést, az Alvásbankot, a helyeidet, '
              'a korlátlan mentett útvonalat, a régebbi Flyovereket, a teljes előzményeket és minden '
              'exportformátumot.'),
             ('Kell fiók, és hová kerülnek az adataim?',
              'Nincs fiók. Az Aera az iPhone-odon olvassa az Apple Health-et, és ott számol ki minden '
              'pontszámot, így az egészségadataid az iPhone-odon maradnak. A termékanalitika ki van kapcsolva, '
              'amíg be nem kapcsolod, és egészségadatot soha nem tartalmaz.'),
             ('Honnan tudja az Aera, mi a megszokott nálam?',
              'Néhány hét alatt a saját éjszakáidból és edzéseidből tanulja meg a szokásos tartományodat, és '
              'minden új napot ehhez mér. Amíg kevés az adat, nem találgat, hanem kiírja, hogy még tanul.'),
             ('Orvosi eszköz az Aera?',
              'Nem. Az Aera a mindennapi jólléthez és az edzéshez készült. Az órás mérések, például az '
              'alvásfázisok, becslések, és minden cikk megmondja, meddig lehet a számában bízni.'),
             ('Milyen nyelveken érhető el az Aera?',
              'Teljesen angolul, magyarul, németül, spanyolul és franciául, részben olaszul, japánul, portugálul '
              'és hagyományos kínaiul.')],
     'maker_h2': 'Egyetlen ember készíti.',
     'maker_p': 'Az Aerát Varga Gerg&#337; készíti, egyedül, cég nélkül. Ha az appból vagy erről az oldalról '
                'írsz, az üzeneted egyenesen hozzá jut.',
     'maker_link': ('mailto:hello@aerahealth.app', 'Írj neki'),
     'close_h2': 'Az órád méri.<br>Az Aera elmagyarázza.',
     'close_note': 'Ingyenes az App Store-ban. Fiók nélkül.',
     'foot_tag': 'Az órád méri. Az Aera elmagyarázza.'},
    "de": {
        "title": "Aera: Deine Uhr misst, Aera erkl&#228;rt",
        "desc": "Aera sagt dir, was die Zahlen deiner Uhr f&#252;r dich bedeuten, und zeigt, woher es das wei&#223;. Schlaf, Herz und L&#228;ufe aus Apple Health, verglichen mit deinem eigenen Normal. Kostenlos, ohne Konto.",
        "og_title": "Deine Uhr misst. Aera erkl&#228;rt.",
        "skip": "Zum Inhalt springen",
        "nav": [("guides/index.html", "Ratgeber"), ("notes/index.html", "Notizen"), ("support.html", "Support")],
        "get": "Aera laden",
        "h1": "Deine Uhr misst.<br>Aera erkl&#228;rt.",
        "sub": "Aera sagt dir, was die Zahlen deiner Uhr f&#252;r dich bedeuten, und zeigt, woher es das wei&#223;.",
        "cta": "Laden im App Store",
        "note": "Kostenlos &#183; Kein Konto &#183; Mit jeder Uhr und jedem Ring, die in Apple Health schreiben",
        "hero_alt": "Aera auf iPhone und Apple Watch: die letzte Nacht, 58 Minuten &#252;ber deinem Bedarf, und der bisherige Tag auf der Uhr",
        "why_h2": "Eine Zahl ohne Grund ist nur eine Zahl.",
        "why_p": "Uhren z&#228;hlen alles: Stunden Schlaf, Herzschl&#228;ge, Kilometer. Dann h&#246;ren sie bei einem Wert auf und lassen dich raten. <b>Aera macht da weiter, wo der Wert aufh&#246;rt.</b> Jede Zahl wird mit deinem eigenen Normal verglichen, in klaren Worten erkl&#228;rt und l&#228;sst sich &#246;ffnen, um zu zeigen, wie sie berechnet wurde.",
        "bento_h2": "Alles, was deine Uhr misst, gemessen an deinem Normal.",
        "work_link": ("guides/guter-schlafscore.html", "Ein Beispiel: der Schlafscore"),
        "b_sleep": ("Schlaf, gemessen an deinem Bedarf.", "Nicht acht Stunden f&#252;r alle. Der Bedarf, den Aera aus deinen eigenen N&#228;chten gelernt hat."),
        "b_run": ("Jeder Lauf, verglichen mit deinem Normal.", "Pace, Herzfrequenz und Zeit, jeweils neben dem, was f&#252;r dich normal ist."),
        "b_replay": ("Jeden Lauf in 3D nacherleben.", "Deine Route, &#252;ber das echte Gel&#228;nde geflogen."),
        "b_route": ("Eine Route ab deiner T&#252;r.", "Tippe auf die Karte, und die Linie folgt echten Wegen."),
        "b_watch": ("Auch am Handgelenk.", "Die letzte Nacht und der bisherige Tag, mit einem Blick."),
        "b_lock": ("Kein Konto.", "Jeder Wert wird auf deinem iPhone berechnet."),
        "b_work": ("Jede Zahl zeigt ihren Rechenweg.", "Tippe auf eine Zahl und sieh, wie sie berechnet wurde, welche Forschung dahintersteht und wo sie an ihre Grenzen kommt."),
        "sleep_h2": "Schlaf, erkl&#228;rt.",
        "sleep_p": "Deine Uhr sagt, wie lange du geschlafen hast. Aera sagt, was das f&#252;r dich bedeutet: <b>gemessen an dem Schlaf, den du brauchst</b>, gelernt aus deinen eigenen N&#228;chten. Schlafphasen zeigt Aera als das, was sie sind: eine Sch&#228;tzung.",
        "sleep_alt": "Aeras Schlafbildschirm auf dem iPhone: Ausgezeichnet, 58 Minuten &#252;ber deinem Bedarf, 88 von 100, 8 Stunden 22 Minuten Schlaf",
        "run_h2": "L&#228;ufe, nachgelesen.",
        "run_p": "Jeder Lauf steht neben deinem Normal: <b>schneller oder langsamer als sonst, h&#228;rter oder leichter f&#252;rs Herz.</b> Dann fliegst du ihn noch einmal in 3D, &#252;ber das Gel&#228;nde, auf dem du gelaufen bist.",
        "run_alts": ("Ein Lauf in 3D &#252;ber Satellitengel&#228;nde, mit Distanz, Pace und Herzfrequenz", "Ein Morgenlauf im R&#252;ckblick: Distanz, Zeit, Pace und Energie, jeweils neben deinem Normal", "Aera auf der Apple Watch w&#228;hrend eines Laufs: Zeit, Distanz, Pace und Herzfrequenz in Zone 3"),
        "route_h2": "Planen. Dann einfach laufen.",
        "route_p": "Zeichne eine Route, die echten Wegen folgt, oder &#246;ffne eine GPX-Datei. <b>Jede Abzweigung kommt, bevor du sie erreichst</b>, auf dem iPhone, am Handgelenk oder vorgelesen.",
        "route_alts": ("Eine Route ab der Haust&#252;r um den Green Lake, auf echten Wegen", "Abbiegehinweis auf der Apple Watch: 202 Meter, Gabelung, rechts halten"),
        "wear_h2": "Trag, was du magst.",
        "wear_p": "Aera liest Apple Health. Es funktioniert also mit der Apple Watch und mit jeder Uhr, jedem Ring und jeder App, die Schlaf und Training dorthin schreibt.",
        "wear_list": ["Apple Watch", "Garmin", "Oura", "WHOOP", "iPhone"],
        "wear_link": ("guides/aera-mit-garmin-oura-whoop.html", "Was von welchem Ger&#228;t in Apple Health ankommt"),
        "priv_h2": "Gesundheitsdaten bleiben auf deinem iPhone.",
        "priv_p": "Kein Konto und kein Server, der rechnet. Aera liest Apple Health auf deinem Telefon und berechnet dort jeden Wert. Analysen bleiben aus, bis du sie einschaltest, und enthalten nie Gesundheitswerte.",
        "priv_link": ("privacy.html", "Datenschutzerkl&#228;rung lesen"),
        "lock_alt": "",
        "plans_h2": "Kostenlos starten.",
        "free_h": "Kostenlos",
        "free": ["Schlaf, Stress und Belastung, verglichen mit deinem Normal", "Jeder Lauf im R&#252;ckblick, jede Bestzeit", "Routenplaner mit Abbiegehinweisen", "Flyover f&#252;r die letzten sieben Tage"],
        "prem_h": "Premium",
        "prem": ["Die Einheit f&#252;r heute: wie lange, wie hart", "Deine Schlafreserve und deine Orte", "Unbegrenzt gespeicherte Routen", "&#196;ltere Flyover, ganze Historie, jeder Export"],
        "prem_note": "Monatlich, j&#228;hrlich oder als Einmalkauf. J&#228;hrlich beginnt mit 7 Tagen gratis.",
        "faq_h2": "Fragen.",
        "faq": [
            ("Was macht Aera?", "Aera liest, was deine Uhr, dein Ring oder dein iPhone in Apple Health schreibt, und sagt dir, was diese Zahlen f&#252;r dich bedeuten. Schlaf, Stress, Belastung und jeder Lauf werden mit deinem eigenen Normal verglichen und in klaren Worten erkl&#228;rt, und jede Zahl &#246;ffnet einen kurzen Artikel dar&#252;ber, wie sie berechnet wurde. Dazu plant Aera Routen mit Abbiegehinweisen und zeigt L&#228;ufe in 3D."),
            ("Brauche ich eine Apple Watch?", "Nein. Aera liest Apple Health, also passt jede Uhr, jeder Ring und jede App, die Schlaf, Herzfrequenz und Training dorthin schreibt: Apple Watch, Garmin, Oura, WHOOP und andere. Nur mit dem iPhone arbeitet Aera mit Schritten und Trainings, und was n&#228;chtliche Herzdaten braucht, wartet, bis es welche gibt."),
            ("Ist Aera kostenlos?", "Ja. Schlaf, Stress und Belastung im Vergleich zu deinem Normal, jeder Lauf im R&#252;ckblick, jede Bestzeit, der Routenplaner mit Abbiegehinweisen und Flyover f&#252;r die letzten sieben Tage sind kostenlos. Premium bringt die Einheit f&#252;r heute, deine Schlafreserve, deine Orte, unbegrenzt gespeicherte Routen, &#228;ltere Flyover, die ganze Historie und jedes Exportformat."),
            ("Brauche ich ein Konto, und wohin gehen meine Daten?", "Es gibt kein Konto. Aera liest Apple Health auf deinem iPhone und berechnet dort jeden Wert, also bleiben Gesundheitsdaten auf deinem iPhone. Produktanalysen bleiben aus, bis du sie einschaltest, und enthalten nie Gesundheitswerte."),
            ("Woher wei&#223; Aera, was f&#252;r mich normal ist?", "Es lernt deinen &#252;blichen Bereich &#252;ber einige Wochen aus deinen eigenen N&#228;chten und Einheiten und vergleicht jeden neuen Tag damit. Solange deine Historie d&#252;nn ist, sagt es, dass es noch lernt, statt zu raten."),
            ("Ist Aera ein Medizinprodukt?", "Nein. Aera ist f&#252;r Wohlbefinden und Training im Alltag. Messwerte der Uhr wie Schlafphasen sind Sch&#228;tzungen, und jeder Artikel sagt, wo seine Zahl an Grenzen st&#246;&#223;t."),
            ("Welche Sprachen spricht Aera?", "Englisch, Ungarisch, Deutsch, Spanisch und Franz&#246;sisch vollst&#228;ndig, Italienisch, Japanisch, Portugiesisch und traditionelles Chinesisch teilweise."),
        ],
        "maker_h2": "Von einem Menschen gemacht.",
        "maker_p": "Aera wird von Gerg&#337; Varga gebaut, allein und ohne Firma dahinter. Eine Nachricht aus der App oder von dieser Seite erreicht ihn direkt.",
        "maker_link": ("mailto:hello@aerahealth.app", "Schreib ihm"),
        "close_h2": "Deine Uhr misst.<br>Aera erkl&#228;rt.",
        "close_note": "Kostenlos im App Store. Kein Konto.",
        "foot_tag": "Deine Uhr misst. Aera erkl&#228;rt.",
    },
}

# The Hungarian lines come from the Hungarian site copy thread (keynote_hu.py
# in the project's site-polish reports); never written here by hand.
