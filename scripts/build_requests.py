"""Build the feature request board in EN, HU and DE from support.html's head and footer.

Run add_lang.py afterwards (it adds the language switch). The board talks to the
aera-requests Cloudflare Worker (worker/requests-worker.js); one shared board for all languages.
"""
import pathlib, re, json
root = pathlib.Path(__file__).resolve().parent.parent
MARK = re.compile(r"<!--lsw-->.*?<!--/lsw-->\n?", re.S)
PAGES = {"en": "requests.html", "hu": "otletek.html", "de": "wuensche.html"}
T = {
 "en": dict(title="Feature requests", desc="Ask for a feature in Aera, add details to other requests and +1 the ones you want. No account needed.",
   intro="Write what you would like Aera to do and send it. No account, no sign up. Every request is read by the person who builds Aera.",
   ph="What should Aera do next?", send="Send request", det="Anything else? Optional", mail="Email to hear when it ships. Optional",
   list="Requests", trending="Trending", top="Top", new="New", shipped="Shipped", search="Search", sort="Sort",
   bug='For a bug, write to <a href="support.html">Support</a> so we can reply to you.', loading="Loading requests",
   review="Under review", planned="Planned", progress="In progress", done="Done",
   one="detail", many="details", add="Add a detail", empty="No requests yet. Be the first.", nomatch="Nothing matches yet. Add it above.",
   noship="Nothing shipped from requests yet.", similar="Already asked? Add your vote instead.", vote="Vote", voted="Voted",
   thanksVote="Your vote is in. Thank you.", thanksSent="Sent. It is on the board with your vote.", thanksAdd="Added. Thank you.",
   fail="That did not go through. Try again in a minute.", votes="votes", home="index.html", nav=("Notes","Privacy","Support","Terms"), footHome="Home"),
 "hu": dict(title="Ötletek és kérések", desc="Kérj új funkciót az Aerában, egészítsd ki mások kéréseit, és szavazz arra, amit szeretnél. Fiók nélkül.",
   intro="Írd le, mit tudjon még az Aera, és küldd el. Nem kell fiók, nem kell regisztrálni. Minden kérést az olvas el, aki az Aerát készíti.",
   ph="Mit tudjon még az Aera?", send="Kérés küldése", det="Van még valami? Nem kötelező", mail="E-mail, ha szólnánk, amikor elkészül. Nem kötelező",
   list="Kérések", trending="Felkapott", top="Legtöbb", new="Új", shipped="Elkészült", search="Keresés", sort="Sorrend",
   bug='Hibát a <a href="support.html">Támogatásnak</a> írj, hogy válaszolni tudjunk.', loading="Kérések betöltése",
   review="Átnézzük", planned="Tervben", progress="Készül", done="Elkészült",
   one="kiegészítés", many="kiegészítés", add="Kiegészítem", empty="Még nincs kérés. Legyél te az első.", nomatch="Még nincs ilyen. Írd be fent.",
   noship="Kérésből még nem készült el semmi.", similar="Már kérte valaki? Szavazz inkább arra.", vote="Szavazok", voted="Szavaztál",
   thanksVote="Megkaptuk a szavazatod. Köszönjük.", thanksSent="Elküldve. Kint van a listán a szavazatoddal.", thanksAdd="Hozzáadva. Köszönjük.",
   fail="Ez most nem ment át. Próbáld újra egy perc múlva.", votes="szavazat", home="hu.html", nav=("Jegyzetek","Adatvédelem","Támogatás","Feltételek"), footHome="Kezdőlap"),
 "de": dict(title="Funktionswünsche", desc="Wünsch dir eine Funktion in Aera, ergänze andere Wünsche und gib +1 für die, die du willst. Ohne Konto.",
   intro="Schreib, was Aera können soll, und schick es ab. Kein Konto, keine Anmeldung. Jeden Wunsch liest die Person, die Aera baut.",
   ph="Was soll Aera als Nächstes können?", send="Wunsch senden", det="Noch etwas? Optional", mail="E-Mail, wenn du hören willst, wann es kommt. Optional",
   list="Wünsche", trending="Beliebt", top="Top", new="Neu", shipped="Umgesetzt", search="Suchen", sort="Sortierung",
   bug='Einen Fehler schreib bitte an den <a href="support.html">Support</a>, damit wir antworten können.', loading="Wünsche werden geladen",
   review="Wird geprüft", planned="Geplant", progress="In Arbeit", done="Umgesetzt",
   one="Ergänzung", many="Ergänzungen", add="Ergänzen", empty="Noch keine Wünsche. Fang du an.", nomatch="Noch nichts dazu. Trag es oben ein.",
   noship="Aus Wünschen ist noch nichts umgesetzt.", similar="Schon gewünscht? Stimm lieber dafür.", vote="Dafür", voted="Gestimmt",
   thanksVote="Deine Stimme ist da. Danke.", thanksSent="Gesendet. Er steht mit deiner Stimme auf der Liste.", thanksAdd="Hinzugefügt. Danke.",
   fail="Das hat nicht geklappt. Versuch es in einer Minute noch einmal.", votes="Stimmen", home="de.html", nav=("Notizen","Datenschutz","Support","AGB"), footHome="Startseite"),
}
src = MARK.sub("", (root / "support.html").read_text())
head0 = src[: src.index('<div class="wrap page-head">')]
foot0 = src[src.index("<footer>"):]
body0 = (root / "scripts/requests_body.html").read_text()
alts = "".join(f'<link rel="alternate" hreflang="{l}" href="https://aerahealth.app/{p}">\n' for l, p in PAGES.items())
for lang, page in PAGES.items():
    t = T[lang]
    h = head0.replace('<html lang="en">', f'<html lang="{lang}">')
    h = h.replace("<title>Support · Aera</title>", f"<title>{t['title']} · Aera</title>")
    h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{t["desc"]}">', h)
    h = h.replace('href="https://aerahealth.app/support.html">', f'href="https://aerahealth.app/{page}">\n' + alts.rstrip("\n") + ">"[:0])
    h = h.replace(' aria-current="page">Support', '>Support').replace('href="index.html">Aera', f'href="{t["home"]}">Aera')
    for en, x in zip(("Notes", "Privacy", "Support", "Terms"), t["nav"]):
        h = h.replace(f'.html">{en}</a>', f'.html">{x}</a>')
    f = foot0.replace('href="index.html">Home', f'href="{t["home"]}">{t["footHome"]}')
    for en, x in zip(("Privacy", "Terms"), (t["nav"][1], t["nav"][3])):
        f = f.replace(f'.html">{en}</a>', f'.html">{x}</a>')
    b = body0
    for k in re.findall(r"\{\{(\w+)\}\}", body0):
        b = b.replace("{{%s}}" % k, t[k])
    b = b.replace("/*FR_T*/", "var T=" + json.dumps({k: v for k, v in t.items() if isinstance(v, str)}, ensure_ascii=False) + ";")
    (root / page).write_text(h + b + f)
