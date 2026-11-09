#!/usr/bin/env python3
"""Build hu.html and de.html from index.html (English is the source).

    python3 tools/build_pages.py

Every English line on the page has its Hungarian and German line here. Each one must
be found in index.html, so a changed English line stops the build instead of leaving
English on a Hungarian or German page. Screens and store pictures come from s/hu and
s/de; the film is shared (it has no words).
"""
import json, os, re
import sys

HEAD = {
    "hu": ("Aera: nézd vissza a futásod, értsd meg a tested",),
    "de": ("Aera: erlebe deinen Lauf noch einmal, versteh deinen Körper",),
}

# (English as it stands in index.html, Hungarian, German)
T = [
    # nav
    ('<a href="#replay">Replay</a>', '<a href="#replay">Visszajátszás</a>', '<a href="#replay">3D-Wiedergabe</a>'),
    ('<a href="#body" class="opt">Your body</a>', '<a href="#body" class="opt">A tested</a>', '<a href="#body" class="opt">Dein Körper</a>'),
    ('<a href="#inside" class="opt">Inside the app</a>', '<a href="#inside" class="opt">Az app</a>', '<a href="#inside" class="opt">Die App</a>'),
    ('<a href="#new">What&#8217;s new</a>', '<a href="#new">Újdonságok</a>', '<a href="#new">Neuigkeiten</a>'),
    ('<div class="langs" aria-label="Language"><a href="./" aria-current="page" hreflang="en">EN</a><a href="hu.html" hreflang="hu">HU</a><a href="de.html" hreflang="de">DE</a></div>',
     '<div class="langs" aria-label="Nyelv"><a href="./" hreflang="en">EN</a><a href="hu.html" aria-current="page" hreflang="hu">HU</a><a href="de.html" hreflang="de">DE</a></div>',
     '<div class="langs" aria-label="Sprache"><a href="./" hreflang="en">EN</a><a href="hu.html" hreflang="hu">HU</a><a href="de.html" aria-current="page" hreflang="de">DE</a></div>'),
    ('id6762456252">Download</a>', 'id6762456252">Letöltés</a>', 'id6762456252">Laden</a>'),

    # opening
    ('aria-label="A morning run over Liberty Bridge in Budapest, replayed in 3D"',
     'aria-label="Egy reggeli futás a budapesti Szabadság hídon, 3D-ben visszajátszva"',
     'aria-label="Ein Morgenlauf über die Freiheitsbrücke in Budapest, in 3D abgespielt"'),
    ('alt="A run replayed in 3D over Liberty Bridge, Budapest: fastest kilometre 4:38"',
     'alt="Futás 3D-ben visszajátszva a budapesti Szabadság hídon: leggyorsabb km 4:38"',
     'alt="Ein Lauf in 3D über der Freiheitsbrücke in Budapest: schnellster km 4:38"'),
    ('alt="The run\'s page: 11.57 km at 5:06 per kilometre, next to your usual"',
     'alt="A futás oldala: 11,57 km, 5:06-os tempó, a szokásosodhoz mérve"',
     'alt="Die Seite des Laufs: 11,57 km, Tempo 5:06, an deinem Normal gemessen"'),
    ('alt="Apple Watch: the next turn, 92 metres to go"',
     'alt="Apple Watch: a következő kanyar, még 92 méter"',
     'alt="Apple Watch: die nächste Abbiegung, noch 92 Meter"'),
    ('<p class="kicker">Aera for iPhone and Apple Watch</p>', '<p class="kicker">Aera iPhone-ra és Apple Watchra</p>', '<p class="kicker">Aera für iPhone und Apple Watch</p>'),
    ('<h1><span>Replay your run.</span> <span>Understand your body.</span></h1>',
     '<h1><span>Nézd vissza a futásod.</span> <span>Értsd meg a tested.</span></h1>',
     '<h1><span>Erlebe deinen Lauf noch einmal.</span> <span>Versteh deinen Körper.</span></h1>'),
    ('<span><small>Download on the</small>App Store</span>', '<span><small>Letölthető az</small>App Store-ból</span>', '<span><small>Laden im</small>App Store</span>'),
    ('<p>Free to start. No account.</p>', '<p>Ingyen elkezdheted. Fiók nélkül.</p>', '<p>Kostenlos starten. Kein Konto.</p>'),


    # the three steps
    ('alt="The replay paused on Liberty Bridge: fastest kilometre 4:38, 7.07 km, 36:23, heart rate 148"',
     'alt="A visszajátszás megállítva a Szabadság hídon: leggyorsabb km 4:38, 7,07 km, 36:24, pulzus 148"',
     'alt="Die 3D-Wiedergabe angehalten auf der Freiheitsbrücke: schnellster km 4:38, 7,09 km, 36:28, Herzfrequenz 148"'),
    ('<h2>4:38 over Liberty&nbsp;Bridge.</h2>', '<h2>4:38 a Szabadság&nbsp;hídon.</h2>', '<h2>4:38 über die Freiheits&shy;brücke.</h2>'),
    ('<p>Aera plays any run from the past week back over the real ground, with distance, time, pace and heart rate as you went, and marks <b>your fastest kilometre where it happened</b>.',
     '<p>Az Aera az elmúlt hét bármelyik futását visszajátssza a valódi terepen, a menet közbeni távval, idővel, tempóval és pulzussal, és <b>ott jelöli a leggyorsabb kilométered, ahol lefutottad</b>.',
     '<p>Aera spielt jeden Lauf der letzten Woche über dem echten Gelände ab, mit Distanz, Zeit, Tempo und Herzfrequenz wie unterwegs, und markiert <b>deinen schnellsten Kilometer genau dort, wo er war</b>.'),
    ('alt="The run\'s page: 11.57 km, 59 minutes, 5:06 per kilometre against a usual 5:23, heart rate 149 against 154"',
     'alt="A futás oldala: 11,57 km, 59 perc, 5:06-os tempó a szokásos 5:23 mellett, pulzus 149 a szokásos 154 mellett"',
     'alt="Die Seite des Laufs: 11,57 km, 59 Minuten, Tempo 5:06 bei üblich 5:23, Herzfrequenz 149 bei üblich 154"'),
    ('<h2>11.57&#8239;km at&nbsp;5:06.</h2>', '<h2>11,57&#8239;km, <span class="nw">5:06-os&nbsp;tempó.</span></h2>', '<h2>11,57&#8239;km, Tempo&nbsp;5:06.</h2>'),
    ('<p>Then the whole run, <b>each figure next to your own usual</b>.<sup><a href="#n1">1</a></sup> Your usual pace is 5:23. Your heart averaged 149 against a usual&nbsp;154.</p>',
     '<p>Aztán az egész futás, <b>minden érték a saját szokásosod mellett</b>.<sup><a href="#n1">1</a></sup> A szokásos tempód 5:23. Az átlagpulzusod 149 volt, a szokásos&nbsp;154.</p>',
     '<p>Dann der ganze Lauf, <b>jeder Wert neben deinem eigenen Normal</b>.<sup><a href="#n1">1</a></sup> Dein übliches Tempo ist 5:23. Dein Puls lag im Schnitt bei 149, üblich sind&nbsp;154.</p>'),
    ('alt="How steady: 196 metres over 149 heartbeats is 1.32 metres per beat"',
     'alt="Mennyire egyenletes: 196 méter 149 szívverésre, vagyis 1,32 méter szívverésenként"',
     'alt="Wie gleichmäßig: 196 Meter auf 149 Herzschläge sind 1,32 Meter pro Schlag"'),
    ('<h2>1.32&#8239;m per heartbeat.</h2>', '<h2>1,32&#8239;m szívverésenként.</h2>', '<h2>1,32&#8239;m pro Herzschlag.</h2>'),
    ('<p>And <b>the working behind every number</b>. 196 metres over 149 beats, how steady you ran, how hard it felt. Tap any figure to see how it was&nbsp;made.</p>',
     '<p>És <b>minden szám mögött ott a számítás</b>. 196 méter 149 szívverésre, mennyire egyenletesen futottál, mennyire volt nehéz. Koppints bármelyik értékre, és megmutatja, honnan&nbsp;jön.</p>',
     '<p>Und <b>der Rechenweg hinter jeder Zahl</b>. 196 Meter auf 149 Schläge, wie gleichmäßig du gelaufen bist, wie hart es sich anfühlte. Tippe auf einen Wert und sieh, wie er&nbsp;entsteht.</p>'),

    # works with
    ('<div class="eh"><span>Works with</span></div>', '<div class="eh"><span>Ezekkel működik</span></div>', '<div class="eh"><span>Funktioniert mit</span></div>'),
    ('<p>Works with</p>', '<p>Ezekkel működik</p>', '<p>Funktioniert mit</p>'),

    # body
    ('<h2 class="huge">Understand<br>your body.</h2>', '<h2 class="huge">Értsd meg<br>a tested.</h2>', '<h2 class="huge">Versteh<br>deinen Körper.</h2>'),
    ('<p class="intro">A resting heart rate that is normal for one person can be unusual for another.<sup><a href="#n2">2</a></sup> So Aera <em>reads your nights, your heart and your blood pressure against your own weeks</em>, and shows its reasons.</p>',
     '<p class="intro">Ami az egyik embernek normális nyugalmi pulzus, az a másiknak szokatlan lehet.<sup><a href="#n2">2</a></sup> Ezért az Aera <em>az éjszakáidat, a szívedet és a vérnyomásodat a saját heteidhez méri</em>, és megmutatja, miből számol.</p>',
     '<p class="intro">Ein Ruhepuls, der für den einen normal ist, kann für den anderen ungewöhnlich sein.<sup><a href="#n2">2</a></sup> Deshalb <em>misst Aera deine Nächte, dein Herz und deinen Blutdruck an deinen eigenen Wochen</em> und zeigt seine Gründe.</p>'),
    ('<p class="num">35.0<small>years</small></p>', '<p class="num">35,0<small>év</small></p>', '<p class="num">35,0<small>Jahre</small></p>'),
    ('<p class="cap"><b>Body age.</b> 3.4 years younger than the calendar, from VO&#8322; max, resting heart, HRV, sleep and steps, each part shown.',
     '<p class="cap"><b>Testkor.</b> 3,4 évvel fiatalabb a naptárnál, a VO&#8322;max, a nyugalmi pulzus, a HRV, az alvás és a lépések alapján, minden részével együtt.',
     '<p class="cap"><b>Körperalter.</b> 3,4 Jahre jünger als der Kalender, aus VO&#8322;max, Ruhepuls, HRV, Schlaf und Schritten, jeder Teil sichtbar.'),
    ('alt="Body age 35.0, 3.4 years younger than the calendar"', 'alt="Testkor 35,0, 3,4 évvel fiatalabb a naptárnál"', 'alt="Körperalter 35,0, 3,4 Jahre jünger als der Kalender"'),
    ('<p class="num">80<small>Great</small></p>', '<p class="num">80<small>Nagyszerű</small></p>', '<p class="num">80<small>Sehr gut</small></p>'),
    ('<p class="cap"><b>Last night.</b> 6&nbsp;h 53&nbsp;m asleep, 37 minutes under a need learned from your own nights.</p>',
     '<p class="cap"><b>A múlt éjszaka.</b> 6&nbsp;ó 53&nbsp;p alvás, 37 perccel a saját éjszakáidból tanult igényed alatt.</p>',
     '<p class="cap"><b>Letzte Nacht.</b> 6&nbsp;h 53&nbsp;m Schlaf, 37 Minuten unter einem Bedarf, der aus deinen eigenen Nächten gelernt ist.</p>'),
    ('alt="Sleep score 80, Great: 6 h 53 m asleep, 37 minutes under your need"', 'alt="Alváspontszám 80, Nagyszerű: 6 ó 53 p alvás, 37 perccel az igényed alatt"', 'alt="Schlafwert 80, Sehr gut: 6 h 53 m geschlafen, 37 Minuten unter deinem Bedarf"'),
    ('<p class="cap"><b>Blood pressure.</b> Mornings beside evenings, tagged and ready as a PDF for your doctor.</p>',
     '<p class="cap"><b>Vérnyomás.</b> A reggelek az esték mellett, címkékkel, PDF-ben az orvosodnak.</p>',
     '<p class="cap"><b>Blutdruck.</b> Morgens neben abends, mit Markierungen und als PDF für deinen Arzt.</p>'),
    ('alt="Blood pressure 124/77 with mornings and evenings"', 'alt="Vérnyomás 124/77, reggelekkel és estékkel"', 'alt="Blutdruck 124/77 mit Morgen- und Abendwerten"'),

    # the store pictures
    ('<h2>A look inside.</h2>', '<h2>Egy pillantás az appba.</h2>', '<h2>Ein Blick in die App.</h2>'),
    ('See Aera on the App Store &#8250;', 'Nézd meg az App Store-ban &#8250;', 'Aera im App Store ansehen &#8250;'),
    ('aria-label="Aera\'s App Store pictures"', 'aria-label="Az Aera képei az App Store-ban"', 'aria-label="Aeras Bilder im App Store"'),
    ('alt="Replay your run in 3D. With Apple Watch or iPhone."', 'alt="Nézd vissza a futásod 3D-ben. Apple Watch-csal vagy iPhone-nal."', 'alt="Dein Lauf, noch einmal in 3D. Mit Apple Watch oder iPhone."'),
    ('alt="Body age, not your birthday."', 'alt="Testkor, nem a naptár szerint."', 'alt="Körperalter, nicht dein Geburtstag."'),
    ('alt="Every run, next to your usual."', 'alt="Minden futás, a szokásosodhoz mérve."', 'alt="Jeder Lauf, an deinem Normal gemessen."'),
    ('alt="Know a route before you run it."', 'alt="Ismerd meg az utat, mielőtt futsz."', 'alt="Kenn jede Strecke vor dem Lauf."'),
    ('alt="Last night, against your need."', 'alt="Az éjszakád, az igényedhez mérve."', 'alt="Letzte Nacht, gemessen an deinem Bedarf."'),
    ('alt="Every number shows its work."', 'alt="Minden szám megmutatja, honnan jön."', 'alt="Jede Zahl zeigt ihren Rechenweg."'),
    ('alt="Your watch. Your iPhone. No account."', 'alt="Az órád. Az iPhone-od. Fiók nélkül."', 'alt="Deine Uhr. Dein iPhone. Kein Konto."'),
    ('alt="Your cuff\'s readings, ready for your doctor."', 'alt="A mérőd adatai, az orvosodnak."', 'alt="Deine Messwerte, bereit für deinen Arzt."'),
    ('alt="Every turn, on your wrist."', 'alt="Minden kanyar a csuklódon."', 'alt="Jede Abbiegung, am Handgelenk."'),
    ('alt="Share the replay as a video."', 'alt="Oszd meg a futásod videóként."', 'alt="Teile den Lauf als Video."'),
    ('data-pause="Pause" data-play="Play" data-again="Play again"', 'data-pause="Szünet" data-play="Lejátszás" data-again="Lejátszás újra"', 'data-pause="Pause" data-play="Abspielen" data-again="Noch einmal abspielen"'),
    ('aria-label="Pause"', 'aria-label="Szünet"', 'aria-label="Pause"'),
    ('role="group" aria-label="Pictures"', 'role="group" aria-label="Képek"', 'role="group" aria-label="Bilder"'),
    ('aria-label="Previous"', 'aria-label="Előző"', 'aria-label="Zurück"'),
    ('aria-label="Next"', 'aria-label="Következő"', 'aria-label="Weiter"'),

    # out the door
    ('<h2>Out the door.</h2>', '<h2>Ki a szabadba.</h2>', '<h2>Raus vor die Tür.</h2>'),
    ('<p class="intro">Ask for a loop from where you stand, by distance or by minutes, and <em>follow every turn on your wrist</em>. With Apple Watch, any other watch, or no watch at all.</p>',
     '<p class="intro">Kérj egy kört onnan, ahol állsz, táv vagy percek szerint, és <em>kövess minden kanyart a csuklódon</em>. Apple Watch-csal, bármilyen más órával, vagy óra nélkül is.</p>',
     '<p class="intro">Lass dir eine Runde ab deinem Standort planen, nach Distanz oder Minuten, und <em>folge jeder Abbiegung am Handgelenk</em>. Mit Apple Watch, jeder anderen Uhr oder ganz ohne.</p>'),
    ('alt="A 9.8 km loop past 30 sights, ready to start"', 'alt="Egy 9,8 km-es kör 30 látnivaló mellett, indulásra készen"', 'alt="Eine 9,8-km-Runde an 30 Sehenswürdigkeiten vorbei, startbereit"'),
    ('<figcaption><b>Loops from your front door.</b> Up to three to choose from, for a walk, run, ride or hike.</figcaption>',
     '<figcaption><b>Körök a házad elől.</b> Legfeljebb három közül választhatsz, sétához, futáshoz, bringázáshoz vagy túrához.</figcaption>',
     '<figcaption><b>Runden ab deiner Haustür.</b> Bis zu drei zur Auswahl, zum Gehen, Laufen, Radfahren oder Wandern.</figcaption>'),
    ('alt="Apple Watch: fork, keep left, 92 metres to go"', 'alt="Apple Watch: elágazás, tarts balra, még 92 méter"', 'alt="Apple Watch: Gabelung, links halten, noch 92 Meter"'),
    ('<figcaption><b>Every turn, on your wrist.</b> Apple Watch shows the next turn before you reach it, and records six sports.</figcaption>',
     '<figcaption><b>Minden kanyar a csuklódon.</b> Az Apple Watch előre mutatja a következő kanyart, és hat sportot rögzít.</figcaption>',
     '<figcaption><b>Jede Abbiegung am Handgelenk.</b> Die Apple Watch zeigt die nächste Abbiegung, bevor du dort bist, und zeichnet sechs Sportarten auf.</figcaption>'),
    ('alt="Devices: Apple Watch, Garmin, COROS, Oura and a linked Polar"', 'alt="Eszközök: Apple Watch, Garmin, COROS, Oura és egy összekapcsolt Polar"', 'alt="Geräte: Apple Watch, Garmin, COROS, Oura und eine verbundene Polar"'),
    ('<figcaption><b>Any watch, or none.</b> Garmin, COROS and Oura through Apple Health. Polar links directly for its nights and workouts.',
     '<figcaption><b>Bármilyen óra, vagy egy sem.</b> A Garmin, a COROS és az Oura az Apple Healthen keresztül. A Polart közvetlenül is összekapcsolhatod az éjszakái és az edzései miatt.',
     '<figcaption><b>Jede Uhr, oder keine.</b> Garmin, COROS und Oura über Apple Health. Polar verbindest du direkt für Nächte und Trainings.'),

    # privacy
    ('<h2>Your health stays on your iPhone.</h2>', '<h2>Az egészséged az iPhone-odon marad.</h2>', '<h2>Deine Gesundheit bleibt auf deinem iPhone.</h2>'),
    ('<div><h3>No account</h3><p>Open the app and start. There is nothing to sign up for.</p></div>',
     '<div><h3>Nincs fiók</h3><p>Nyisd meg az appot, és kezdd el. Nem kell regisztrálni.</p></div>',
     '<div><h3>Kein Konto</h3><p>App öffnen und loslegen. Es gibt nichts, wofür du dich anmelden musst.</p></div>'),
    ('<div><h3>No health server</h3><p>Aera reads Apple Health on your phone and does every calculation there.</p></div>',
     '<div><h3>Nincs egészségügyi szerver</h3><p>Az Aera a telefonodon olvassa az Apple Healtht, és minden számítást ott végez.</p></div>',
     '<div><h3>Kein Gesundheitsserver</h3><p>Aera liest Apple Health auf deinem iPhone und rechnet alles dort.</p></div>'),
    ('<div><h3>Never your health data</h3><p>Usage counts and crash reports never carry health data. You can turn each off in Settings.</p></div>',
     '<div><h3>Egészségadat soha</h3><p>A használati statisztika és a hibajelentések soha nem visznek egészségadatot. Mindkettőt kikapcsolhatod a Beállításokban.</p></div>',
     '<div><h3>Nie deine Gesundheitsdaten</h3><p>Nutzungsstatistiken und Absturzberichte enthalten nie Gesundheitsdaten. Beides schaltest du in den Einstellungen aus.</p></div>'),

    # what's new
    ('<h4>Home and your reads</h4>', '<h4>Otthon és a mutatóid</h4>', '<h4>Heute und Auswertungen</h4>'),
    ('<h4>Sleep</h4>', '<h4>Alvás</h4>', '<h4>Schlaf</h4>'),
    ('<h4>Workouts and Fitness</h4>', '<h4>Edzések és Fitnesz</h4>', '<h4>Trainings und Fitness</h4>'),
    ('<h4>The Map</h4>', '<h4>A Térkép</h4>', '<h4>Die Karte</h4>'),
    ('<h4>Your watch</h4>', '<h4>Az órád</h4>', '<h4>Deine Uhr</h4>'),
    ('<h4>Widgets, Siri and alerts</h4>', '<h4>Widgetek, Siri és értesítések</h4>', '<h4>Widgets, Siri und Hinweise</h4>'),
    ('<h4>Sharing and your data</h4>', '<h4>Megosztás és adataid</h4>', '<h4>Teilen und deine Daten</h4>'),
    ('<h4>Everywhere</h4>', '<h4>Általános</h4>', '<h4>Überall</h4>'),
    ('></i>Energy leads the Timeline<', '></i>Az Energia vezeti az Idővonalat<', '></i>Energie steht oben in der Zeitachse<'),
    ('></i>Rings show today&#8217;s scores<', '></i>A gyűrűk a mai pontszámokat mutatják<', '></i>Ringe zeigen die Werte von heute<'),
    ('></i>Blood pressure on Home<', '></i>Vérnyomás a Főoldalon<', '></i>Blutdruck auf Home<'),
    ('></i>The clock change<', '></i>Az óraátállítás<', '></i>Die Zeitumstellung<'),
    ('></i>A nap after waking is a nap<', '></i>Az ébredés utáni szunyókálás szunyókálás<', '></i>Ein Nickerchen nach dem Aufwachen ist ein Nickerchen<'),
    ('></i>A sleep score that holds<', '></i>Egy alváspontszám, ami nem változik<', '></i>Ein Schlafwert, der bleibt<'),
    ('></i>Say how hard it felt<', '></i>Mondd meg, mennyire volt nehéz<', '></i>Sag, wie anstrengend es war<'),
    ('></i>Pacing and heart drift against your usual<', '></i>Tempó és pulzussodródás a tipikushoz képest<', '></i>Tempoverlauf und Herzdrift im Vergleich zu deinem üblichen Wert<'),
    ('></i>Turn and tilt the map<', '></i>Forgasd és döntsd meg a térképet<', '></i>Karte drehen und neigen<'),
    ('></i>Loops people would run<', '></i>Körök, amiket tényleg lefutnál<', '></i>Runden, die man wirklich läuft<'),
    ('></i>A Compass page<', '></i>Iránytű oldal<', '></i>Eine Kompassseite<'),
    ('></i>A map with no route<', '></i>Térkép útvonal nélkül<', '></i>Eine Karte ohne Route<'),
    ('></i>Your own track on a free run<', '></i>A saját nyomvonalad szabad futásnál<', '></i>Deine eigene Spur bei einem freien Lauf<'),
    ('></i>Siri runs your workout<', '></i>Siri vezeti az edzésedet<', '></i>Siri steuert dein Training<'),
    ('></i>Sync on the Lock Screen<', '></i>Szinkronizálás a zárolási képernyőn<', '></i>Synchronisierung auf dem Sperrbildschirm<'),
    ('></i>A morning note on your night<', '></i>Reggeli értesítés az éjszakádról<', '></i>Ein Morgenhinweis zu deiner Nacht<'),
    ('></i>A screenshot opens a share card<', '></i>A képernyőkép megosztási kártyát nyit<', '></i>Ein Bildschirmfoto öffnet eine Teilen-Karte<'),
    ('></i>Share last night<', '></i>Múlt éjszaka megosztása<', '></i>Letzte Nacht teilen<'),
    ('></i>Cards in your language<', '></i>Kártyák a saját nyelveden<', '></i>Karten in deiner Sprache<'),
    ('></i>A third look, Colour<', '></i>Egy harmadik megjelenés: Szín<', '></i>Ein dritter Look: Farbe<'),
    ('></i>A bigger Field Guide<', '></i>Bővebb Field Guide<', '></i>Ein größerer Field Guide<'),
    ('></i>Opens ready to use<', '></i>Azonnal használható<', '></i>Sofort startklar<'),
    ('<span class="wn">What&#8217;s new</span>', '<span class="wn">Újdonságok</span>', '<span class="wn">Was ist neu</span>'),
    ('<h3>And plenty more</h3><p>Every change in this update, the fixes too, is in Settings under What&#8217;s new.</p>', '<h3>És még sok minden</h3><p>A frissítés minden változását, a javításokat is, a Beállítások › Újdonságok alatt találod.</p>', '<h3>Und vieles mehr</h3><p>Jede Änderung in diesem Update, auch die Fehlerbehebungen, findest du in den Einstellungen unter Was ist neu.</p>'),
    ('></i>Recovery weighs your heart asleep more<', '></i>A Regenerálódás jobban figyel az alvás közbeni szívedre<', '></i>Erholung gewichtet dein Herz im Schlaf stärker<'),
    ('></i>Drag a chart to read it<', '></i>Húzd végig az ujjad egy görbén, és leolvashatod<', '></i>Zieh über eine Kurve, um sie abzulesen<'),
    ('></i>Flyover starts on your map<', '></i>A Flyover a térképeden indul<', '></i>Flyover beginnt auf deiner Karte<'),
    ('></i>Sights stand as posts<', '></i>A látnivalók oszlopként állnak<', '></i>Sehenswürdigkeiten als Wegmarken<'),
    ('></i>A sharper heat map<', '></i>Élesebb hőtérkép<', '></i>Eine schärfere Heatmap<'),
    ('></i>Steps and battery on the move<', '></i>Lépések és akkumulátor útközben<', '></i>Schritte und Akku unterwegs<'),
    ('></i>Plan a run and Last night in Control Center<', '></i>Futás tervezése és Múlt éjszaka a Vezérlőközpontban<', '></i>Lauf planen und Letzte Nacht im Kontrollzentrum<'),
    ('></i>Personal bests and your week<', '></i>Egyéni csúcsok és a heted<', '></i>Bestleistungen und deine Woche<'),
    ('></i>Every hike, its whole pace line<', '></i>Minden túra a teljes tempóvonalával<', '></i>Jede Wanderung mit ihrer ganzen Tempolinie<'),
    ('<span><small>Distance</small><b>11.57<i>km</i></b></span><span><small>Time</small><b>59<i>min</i></b></span><span><small>Pace</small><b>5:06<i>/km</i></b></span><span><small>Heart rate</small><b>149<i>bpm</i></b></span>', '<span><small>Táv</small><b>11,57<i>km</i></b></span><span><small>Idő</small><b>59<i>perc</i></b></span><span><small>Tempó</small><b>5:06<i>/km</i></b></span><span><small>Pulzus</small><b>149<i>bpm</i></b></span>', '<span><small>Distanz</small><b>11,57<i>km</i></b></span><span><small>Zeit</small><b>59<i>min</i></b></span><span><small>Tempo</small><b>5:06<i>/km</i></b></span><span><small>Herzfrequenz</small><b>149<i>bpm</i></b></span>'),
    ('<h2>New in Aera 3.4</h2>', '<h2>Újdonságok az Aera 3.4-ben</h2>', '<h2>Neu in Aera 3.4</h2>'),
    ('Read the release notes &#8250;', 'A teljes lista &#8250;', 'Alle Neuerungen &#8250;'),
    ('<div><h3>The replay, rebuilt</h3><p>Four live figures, camera views and map styles, and with Premium a vertical video to share.</p></div>',
     '<div><h3>A 3D-s nézet, újraépítve</h3><p>Négy élő érték, kameranézetek és térképstílusok, Prémiummal pedig álló videó a megosztáshoz.</p></div>',
     '<div><h3>Die 3D-Ansicht, neu gebaut</h3><p>Vier Live-Werte, Kameraperspektiven und Kartenstile, dazu mit Premium ein Video im Hochformat zum Teilen.</p></div>'),
    ('<div><h3>How hard it felt</h3><p>Rate any workout 1 to 10. Best efforts say where a run sits, like 2nd fastest of&nbsp;41.</p></div>',
     '<div><h3>Mennyire volt nehéz</h3><p>Értékelj bármelyik edzést 1-től 10-ig. A legjobb részidők megmondják, hol áll egy futás, például 41-ből a második&nbsp;leggyorsabb.</p></div>',
     '<div><h3>Wie anstrengend es war</h3><p>Bewerte jedes Training von 1 bis 10. Bestleistungen sagen, wo ein Lauf steht, etwa zweitschnellster von&nbsp;41.</p></div>'),
    ('<div><h3>Trends</h3><p>Cardio fitness, resting heart and endurance, each saying whether a change is real.</p></div>',
     '<div><h3>Trendek</h3><p>Kardió-fittség, nyugalmi pulzus és állóképesség, és mindegyik megmondja, valódi-e a változás.</p></div>',
     '<div><h3>Verläufe</h3><p>Kardiofitness, Ruhepuls und Ausdauer, jeweils mit der Angabe, ob eine Veränderung echt ist.</p></div>'),
    ('<div><h3>Any watch, or none</h3><p>Full pages for Garmin, Polar and COROS. Garmin, FIT, GPX and TCX files import with their routes.</p></div>',
     '<div><h3>Bármilyen óra, vagy egy sem</h3><p>Teljes oldalak a Garminnak, a Polarnak és a COROS-nak. A Garmin-, FIT-, GPX- és TCX-fájlok az útvonalukkal együtt importálhatók.</p></div>',
     '<div><h3>Jede Uhr, oder keine</h3><p>Volle Seiten für Garmin, Polar und COROS. Garmin-, FIT-, GPX- und TCX-Dateien kommen mit ihrer Route.</p></div>'),
    ('<div><h3>How&#8217;s today?</h3><p>Tell Aera how the day feels, and mark time off when you are ill or away.</p></div>',
     '<div><h3>Milyen a napod?</h3><p>Mondd el az Aerának, milyen a napod, és jelölj pihenőt, ha beteg vagy, vagy elutaztál.</p></div>',
     '<div><h3>Wie war heute?</h3><p>Sag Aera, wie sich der Tag anfühlt, und trag eine Auszeit ein, wenn du krank oder unterwegs bist.</p></div>'),
    ('<div><h3>A bigger Field Guide</h3><p>16 articles rebuilt and 10 new, each with its sources.</p></div>',
     '<div><h3>Bővebb Field Guide</h3><p>16 cikk újraírva és 10 új, mindegyik a forrásaival.</p></div>',
     '<div><h3>Ein größerer Field Guide</h3><p>16 Artikel neu geschrieben und 10 neue, jeweils mit Quellen.</p></div>'),

    # closing
    ('<img src="s/icon.png" alt="The Aera icon"', '<img src="s/icon.png" alt="Az Aera ikonja"', '<img src="s/icon.png" alt="Das Aera-Symbol"'),
    ('<h2>Replay your run.<br>Understand your body.</h2>', '<h2>Nézd vissza a futásod.<br>Értsd meg a tested.</h2>', '<h2>Erlebe deinen Lauf noch einmal.<br>Versteh deinen Körper.</h2>'),
    ('<p>Free to start. No account. Works with the watch you already wear.</p>',
     '<p>Ingyen elkezdheted. Fiók nélkül. Azzal az órával működik, amit már most is hordasz.</p>',
     '<p>Kostenlos starten. Kein Konto. Funktioniert mit der Uhr, die du schon trägst.</p>'),

    # footnotes (the two studies keep their published titles)
    ('<li id="n3">The replay is free for runs, walks, rides and hikes from the last 7 days. Older workouts replay with Premium.</li>',
     '<li id="n3">A 3D-s visszajátszás az elmúlt 7 nap futásaira, sétáira, bringázásaira és túráira ingyenes. A régebbi edzések a Premiummal nézhetők vissza.</li>',
     '<li id="n3">Die 3D-Wiedergabe ist für Läufe, Spaziergänge, Radtouren und Wanderungen der letzten 7 Tage kostenlos. Ältere Trainings mit Premium.</li>'),
    ('<li id="n4">Body age is an estimate for everyday wellbeing, not a medical measurement. It needs a watch that records VO&#8322; max and heart rate.</li>',
     '<li id="n4">A testkor a mindennapi jólléthez készült becslés, nem orvosi mérés. Olyan óra kell hozzá, amely méri a VO&#8322;max-ot és a pulzust.</li>',
     '<li id="n4">Das Körperalter ist eine Schätzung für das tägliche Wohlbefinden, keine medizinische Messung. Es braucht eine Uhr, die VO&#8322;max und Herzfrequenz misst.</li>'),
    ('<li id="n5">Garmin, Polar and COROS workouts reach Aera through Apple Health without their route. Import the workout file to replay them (<a href="/guides/replay-a-garmin-run-in-3d.html">how</a>).</li>',
     '<li id="n5">A Garmin, Polar és COROS edzések útvonal nélkül érkeznek az Apple Healthen keresztül. A visszajátszáshoz importáld az edzésfájlt (<a href="/guides/garmin-futas-3d-visszajatszasa.html">így megy</a>).</li>',
     '<li id="n5">Garmin-, Polar- und COROS-Trainings kommen über Apple Health ohne Route an. Importiere die Trainingsdatei, um sie abzuspielen (<a href="/guides/garmin-lauf-in-3d-abspielen.html">so geht es</a>).</li>'),

    # footer
    ('The health app that shows its work. Made in Hungary.', 'Az egészségapp, amely megmutatja, honnan jönnek a számai. Magyarországon készült.', 'Die Gesundheits-App, die ihren Rechenweg zeigt. Gemacht in Ungarn.'),
    ('<li><a href="#body">Your body</a></li>', '<li><a href="#body">A tested</a></li>', '<li><a href="#body">Dein Körper</a></li>'),
    ('<li><a href="#top">Route planner</a></li>', '<li><a href="#top">Útvonaltervező</a></li>', '<li><a href="#top">Routenplaner</a></li>'),
    ('<h4>Read</h4><ul><li><a href="#top">Field Guide</a></li><li><a href="#top">Guides</a></li><li><a href="#top">Press</a></li></ul>',
     '<h4>Olvasnivaló</h4><ul><li><a href="#top">Field Guide</a></li><li><a href="#top">Útmutatók</a></li><li><a href="#top">Sajtó</a></li></ul>',
     '<h4>Lesen</h4><ul><li><a href="#top">Field Guide</a></li><li><a href="#top">Ratgeber</a></li><li><a href="#top">Presse</a></li></ul>'),
    ('<h4>Help</h4><ul><li><a href="#top">Support</a></li><li><a href="#top">Privacy</a></li><li><a href="#top">Terms</a></li><li><a href="hu.html" hreflang="hu">Magyar</a> &#183; <a href="de.html" hreflang="de">Deutsch</a></li></ul>',
     '<h4>Segítség</h4><ul><li><a href="#top">Támogatás</a></li><li><a href="#top">Adatvédelem</a></li><li><a href="#top">Felhasználási feltételek</a></li><li><a href="./" hreflang="en">English</a> &#183; <a href="de.html" hreflang="de">Deutsch</a></li></ul>',
     '<h4>Hilfe</h4><ul><li><a href="#top">Support</a></li><li><a href="#top">Datenschutz</a></li><li><a href="#top">Nutzungsbedingungen</a></li><li><a href="./" hreflang="en">English</a> &#183; <a href="hu.html" hreflang="hu">Magyar</a></li></ul>'),
    ('aria-label="Appearance"', 'aria-label="Megjelenés"', 'aria-label="Darstellung"'),
    ('data-look="light" aria-pressed="false">Light</button><button type="button" data-look="dark" aria-pressed="false">Dark</button>',
     'data-look="light" aria-pressed="false">Világos</button><button type="button" data-look="dark" aria-pressed="false">Sötét</button>',
     'data-look="light" aria-pressed="false">Hell</button><button type="button" data-look="dark" aria-pressed="false">Dunkel</button>'),
    ('aria-label="How Aera works out 1.32 metres per heartbeat: in one minute of this run you covered 196 metres and your heart beat 149 times. 196 metres over 149 beats is 1.32 metres."',
     'aria-label="Így számolja ki az Aera az 1,32 métert szívverésenként: a futás egy perce alatt 196 métert tettél meg, a szíved 149-et vert. 196 méter osztva 149 szívveréssel 1,32 méter."',
     'aria-label="So rechnet Aera 1,32 Meter pro Herzschlag aus: In einer Minute dieses Laufs hast du 196 Meter geschafft, dein Herz schlug 149-mal. 196 Meter durch 149 Schläge sind 1,32 Meter."'),
    ('<span>One minute of this run</span>', '<span>Egy perc ebből a futásból</span>', '<span>Eine Minute dieses Laufs</span>'),
    ('<span>Distance</span>', '<span>Táv</span>', '<span>Strecke</span>'),
    ('<span>Heartbeats</span>', '<span>Szívverés</span>', '<span>Herzschläge</span>'),
    ('>Distance per heartbeat</div>', '>Táv szívverésenként</div>', '>Strecke pro Herzschlag</div>'),
    ('<span class="res">1.32<small>', '<span class="res">1,32<small>', '<span class="res">1,32<small>'),
    ('aria-label="Play again"', 'aria-label="Lejátszás újra"', 'aria-label="Noch einmal abspielen"'),
    ('<p class="sub">Your runs in 3D, over the real streets. Your numbers, next to your own&nbsp;usual.</p>',
     '<p class="sub">A futásaid 3D-ben, a valódi utcák fölött. A számaid a saját szokásosodhoz&nbsp;mérve.</p>',
     '<p class="sub">Deine Läufe in 3D über den echten Straßen. Deine Werte, gemessen an deinem&nbsp;Normal.</p>'),
    ('<h2 class="huge">Replay<br>your run.</h2>', '<h2 class="huge">Nézd vissza<br>a futásod.</h2>', '<h2 class="huge">Erlebe deinen<br>Lauf noch einmal.</h2>'),
    ('<p class="intro">One Saturday morning run across Budapest, 11.57&nbsp;km. <em>Here is what Aera made of it.</em></p>',
     '<p class="intro">Egy szombat reggeli futás Budapesten, 11,57&nbsp;km. <em>Ezt hozta ki belőle az Aera.</em></p>',
     '<p class="intro">Ein Samstagmorgenlauf durch Budapest, 11,57&nbsp;km. <em>Das hat Aera daraus gemacht.</em></p>'),
    ('<b data-v>8</b><span>Perceived effort</span></div>', '<b data-v>8</b><span>Érzett terhelés</span></div>', '<b data-v>8</b><span>Gefühlte Anstrengung</span></div>'),
    ('<div class="ends"><span>Easy</span><span>All Out</span></div>', '<div class="ends"><span>Könnyű</span><span>Maximális</span></div>', '<div class="ends"><span>Locker</span><span>Maximal</span></div>'),
    ('<span class="sw"><span class="on">Cardio fitness</span><span>Resting heart</span></span><b class="sw"><span class="on">48.9</span>',
     '<span class="sw"><span class="on">Kardiofittség</span><span>Nyugalmi pulzus</span></span><b class="sw"><span class="on">48,9</span>',
     '<span class="sw"><span class="on">Ausdauerfitness</span><span>Ruhepuls</span></span><b class="sw"><span class="on">48,9</span>'),
    ('<span>COROS</span><span>No watch</span></div>', '<span>COROS</span><span>Óra nélkül</span></div>', '<span>COROS</span><span>Ohne Uhr</span></div>'),
    ('<div class="chips pick"><span>Run down</span><span>Tired</span><span class="on">Ready</span><span>Primed</span><span class="off">Sick</span><span class="off">Injured</span><span class="off">Away</span></div>',
     '<div class="chips pick"><span>Kimerült</span><span>Fáradt</span><span class="on">Rendben</span><span>Topformában</span><span class="off">Beteg</span><span class="off">Sérült</span><span class="off">Úton</span></div>',
     '<div class="chips pick"><span>Ausgelaugt</span><span>Müde</span><span class="on">Bereit</span><span>Startklar</span><span class="off">Krank</span><span class="off">Verletzt</span><span class="off">Unterwegs</span></div>'),
    ('<div class="roll"><span class="on">Your usual</span><span>Biological age</span><span>Sleep need and reserve</span><span>Heart rate zones</span><span>Body clock</span></div>',
     '<div class="roll"><span class="on">Szokásos</span><span>Biológiai kor</span><span>Alvásigény és tartalék</span><span>Pulzuszónák</span><span>Biológiai óra</span></div>',
     '<div class="roll"><span class="on">Üblich</span><span>Das biologische Alter</span><span>Bedarf und Reserve</span><span>Herzfrequenzbereiche</span><span>Innere Uhr</span></div>'),
]

# The HU/DE route picture draws its loop a little higher and narrower, so the
# runner on it follows its own path (traced by eye from each picture).
_lp = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'loop_paths.json')))
T.append((_lp['en'], _lp['hu'], _lp['de']))

# Pictures with words in them come from the language's own folder.
PICS = ['replay', 'replay-low', 'run', 'formula', 'age', 'sleep', 'bp', 'loops', 'watch', 'devices']


def build(lang, src):
    col = 1 if lang == 'hu' else 2
    out = src
    for row in T:
        en, tr = row[0], row[col]
        n = out.count(en)
        if n == 0:
            sys.exit(f'{lang}: English line not found (changed?): {en[:90]}')
        out = out.replace(en, tr)
    for p in PICS:
        out = out.replace(f'src="s/{p}.webp"', f'src="s/{lang}/{p}.webp"')
    out = out.replace('src="s/store/', f'src="s/store/{lang}/')
    out = out.replace('<title>Aera Home Page</title>', f'<title>{HEAD[lang][0]}</title>')
    # A page of its own, so it carries its own document start.
    out = (f'<!doctype html>\n<html lang="{lang}">\n<head>\n<meta charset="utf-8">\n' + out.replace('<header class="nav"', '</head>\n<body>\n<header class="nav"', 1)
           + '\n</body>\n</html>\n')
    # Nothing English may be left in the visible text.
    text = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', out, flags=re.S)
    text = re.sub(r'<[^>]+>', ' ', text)
    for word in ['Replay your', 'Understand', 'Download on', 'Free to start', 'Your body', 'What’s new', 'Works with',
                 'usual', 'heartbeat', 'Heartbeats', 'One minute', 'Distance', 'Last night', 'Blood pressure', 'Body age', 'Out the door', 'No account', 'Route planner']:
        if word in text:
            sys.exit(f'{lang}: English left on the page: {word}')
    return out


def main():
    src = open('index.html', encoding='utf-8').read()
    for lang, name in (('hu', 'hu.html'), ('de', 'de.html')):
        open(name, 'w', encoding='utf-8').write(build(lang, src))
        print('wrote', name)


if __name__ == '__main__':
    main()
