#!/usr/bin/env python3
"""The one Aera look: the tokens, header, footer and closing band every page shares.

The home page (build_home3.py) takes these directly. Every other page gets them
from add_chrome.py, and styles.css and article.css carry CSS between
/* chrome */ markers that add_chrome.py refreshes from here. Change the look
here, then run the build chain (see scripts/home3/README.md).

The style, in short:
- A warm white page, white panels, black type. One aura (peach to lavender,
  the same one as the Instagram poster) behind the opening and the closing.
- A panel says one thing: a small label, one big real figure, one sentence,
  then the real screen. Orange only where a route is drawn.
- Buttons are black pills. Links are black with a rule under them.
"""

STORE = "https://apps.apple.com/app/id6762456252"

APPLE = ('<svg viewBox="0 0 17 20" aria-hidden="true"><path fill="currentColor" d="M14.2 10.6c0-2.6 2.1-3.8 2.2-3.9-1.2-1.8-3.1-2-3.7-2'
         '-1.6-.2-3.1.9-3.9.9-.8 0-2-.9-3.4-.9-1.7 0-3.3 1-4.2 2.6-1.8 3.1-.5 7.8 1.3 10.3.9 1.2 1.9 2.6 3.2 2.6 1.3-.1 1.8-.8 3.3-.8 1.6 0 '
         '2 .8 3.4.8 1.4 0 2.3-1.3 3.1-2.5 1-1.4 1.4-2.8 1.4-2.9 0 0-2.7-1-2.7-4.2zM11.7 3c.7-.9 1.2-2 1-3.2-1 0-2.3.7-3 1.6-.7.8-1.3 2-1.1 '
         '3.1 1.1.1 2.3-.6 3.1-1.5z"/></svg>')

# Words. Each language is written for its own readers, not swapped line by line.
T = {
    "en": {
        "home": "/", "nav_label": "Site", "lang_label": "Language",
        "nav": [("Replay", "/#replay"), ("Your body", "/#body"), ("Guides", "/guides/"), ("What’s new", "/whats-new.html")],
        "get": "Download", "badge": ("Download on the", "App Store"),
        "line": "The health app that shows its work. Made in Hungary.",
        "cols": [
            ("Aera", [("Replay", "/#replay"), ("Your body", "/#body"), ("What’s new", "/whats-new.html"), ("Route planner", "/plan/")]),
            ("Read", [("Field Guide", "/notes/"), ("Guides", "/guides/"), ("Press", "/press/")]),
            ("Help", [("Support", "/support.html"), ("Feature requests", "/requests.html"), ("Privacy", "/privacy.html"), ("Terms", "/terms.html")]),
        ],
        "look": ("Appearance", "Auto", "Light", "Dark"),
        "close_h": ("Replay your run.", "Understand your body."),
        "close_p": "Free to start. No account. Works with the watch you already wear.",
        "qr": "Or scan with your iPhone", "qr_alt": "QR code that opens Aera on the App Store", "icon_alt": "The Aera icon",
    },
    "hu": {
        "home": "/hu.html", "nav_label": "Oldal", "lang_label": "Nyelv",
        "nav": [("Visszajátszás", "/hu.html#replay"), ("A tested", "/hu.html#body"), ("Útmutatók", "/guides/#hu"), ("Újdonságok", "/ujdonsagok.html")],
        "get": "Letöltés", "badge": ("Letölthető az", "App Store-ból"),
        "line": "Egészségapp, amelyik megmutatja, hogyan számol. Magyarországon készül.",
        "cols": [
            ("Aera", [("Visszajátszás", "/hu.html#replay"), ("A tested", "/hu.html#body"), ("Újdonságok", "/ujdonsagok.html"), ("Útvonaltervező", "/plan/")]),
            ("Olvasnivaló", [("Field Guide", "/notes/"), ("Útmutatók", "/guides/#hu"), ("Sajtó", "/press/")]),
            ("Segítség", [("Ügyfélszolgálat", "/support.html"), ("Ötletek", "/otletek.html"), ("Adatvédelem", "/adatvedelem.html"), ("Felhasználási feltételek", "/felhasznalasi-feltetelek.html")]),
        ],
        "look": ("Megjelenés", "Auto", "Világos", "Sötét"),
        "close_h": ("Nézd vissza a futásod.", "Értsd meg a tested."),
        "close_p": "Ingyen kipróbálhatod, regisztráció nélkül. Azzal az órával is megy, amit most hordasz.",
        "qr": "Vagy olvasd be az iPhone-oddal", "qr_alt": "QR-kód, amely megnyitja az Aerát az App Store-ban", "icon_alt": "Az Aera ikonja",
    },
    "de": {
        "home": "/de.html", "nav_label": "Seite", "lang_label": "Sprache",
        "nav": [("3D-Wiedergabe", "/de.html#replay"), ("Dein Körper", "/de.html#body"), ("Ratgeber", "/guides/#de"), ("Neuigkeiten", "/neuigkeiten.html")],
        "get": "Laden", "badge": ("Laden im", "App Store"),
        "line": "Die Gesundheits-App, die zeigt, wie sie rechnet. Entwickelt in Ungarn.",
        "cols": [
            ("Aera", [("3D-Wiedergabe", "/de.html#replay"), ("Dein Körper", "/de.html#body"), ("Neuigkeiten", "/neuigkeiten.html"), ("Routenplaner", "/plan/")]),
            ("Lesen", [("Field Guide", "/notes/"), ("Ratgeber", "/guides/#de"), ("Presse", "/press/")]),
            ("Hilfe", [("Support", "/support.html"), ("Wünsche", "/wuensche.html"), ("Datenschutz", "/privacy.html"), ("Nutzungsbedingungen", "/terms.html")]),
        ],
        "look": ("Darstellung", "Auto", "Hell", "Dunkel"),
        "close_h": ("Erlebe deinen Lauf noch einmal.", "Versteh deinen Körper."),
        "close_p": "Kostenlos loslegen, ganz ohne Konto. Läuft mit der Uhr, die du schon trägst.",
        "qr": "Oder mit dem iPhone scannen", "qr_alt": "QR-Code, der Aera im App Store öffnet", "icon_alt": "Das Aera-Symbol",
    },
}
LANGS = (("en", "EN", "English", "/"), ("hu", "HU", "Magyar", "/hu.html"), ("de", "DE", "Deutsch", "/de.html"))

TOKENS = """
:root{
  color-scheme:light;
  --paper:#f5f5f3; --panel:#ffffff; --ink:#131313; --ink-2:#6b6b68; --ink-3:#8c8c88; --rule:#e4e3de;
  --btn:#131313; --btn-ink:#ffffff; --route:#f0672b;
  --t-peach:#fbe2cf; --t-lav:#e7e1f8; --t-sky:#dbe8f8; --t-sage:#dcebdf; --t-rose:#f9dfe4; --aura:.9;
  --head-bg:rgba(245,245,243,.8); --head-rule:rgba(0,0,0,.08); --foot:#111211; --foot-rule:transparent; --lift:0 1px 2px rgba(20,20,18,.04),0 18px 44px -22px rgba(20,20,18,.22);
  --font:-apple-system,BlinkMacSystemFont,"SF Pro Text","Inter Tight","Inter","Helvetica Neue",Arial,sans-serif;
  --display:-apple-system,BlinkMacSystemFont,"SF Pro Display","Inter Tight","Inter","Helvetica Neue",Arial,sans-serif;
  --head-h:52px; --r:30px;
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    color-scheme:dark;
    --paper:#000000; --panel:#141514; --ink:#f3f3f1; --ink-2:#a2a29f; --ink-3:#7c7c79; --rule:#282927;
    --btn:#f3f3f1; --btn-ink:#131313;
    --t-peach:#33200f; --t-lav:#221c38; --t-sky:#132437; --t-sage:#14271b; --t-rose:#351820; --aura:.34;
    --head-bg:rgba(0,0,0,.72); --head-rule:rgba(255,255,255,.1); --foot:#000000; --foot-rule:#282927; --lift:0 0 0 1px rgba(255,255,255,.06);
  }
}
:root[data-theme="dark"]{
  color-scheme:dark;
  --paper:#000000; --panel:#141514; --ink:#f3f3f1; --ink-2:#a2a29f; --ink-3:#7c7c79; --rule:#282927;
  --btn:#f3f3f1; --btn-ink:#131313;
  --t-peach:#33200f; --t-lav:#221c38; --t-sky:#132437; --t-sage:#14271b; --t-rose:#351820; --aura:.34;
  --head-bg:rgba(0,0,0,.72); --head-rule:rgba(255,255,255,.1); --foot:#000000; --foot-rule:#282927; --lift:0 0 0 1px rgba(255,255,255,.06);
}
"""

CSS = TOKENS + """
/* header */
.site-head{position:sticky;top:0;z-index:40;background:var(--head-bg);-webkit-backdrop-filter:saturate(1.8) blur(20px);backdrop-filter:saturate(1.8) blur(20px);box-shadow:inset 0 -1px 0 var(--head-rule);font-family:var(--font);letter-spacing:-.01em;line-height:1.2;padding-top:env(safe-area-inset-top,0px)}
.site-head .sh-w{display:flex;align-items:center;gap:26px;height:var(--head-h);max-width:1120px;margin:0 auto;padding-left:max(22px,env(safe-area-inset-left,0px));padding-right:max(22px,env(safe-area-inset-right,0px))}
.sh-brand{display:inline-flex;align-items:center;gap:9px;min-height:44px;font-family:var(--font);font-weight:600;font-size:17px;letter-spacing:-.02em;color:var(--ink);text-decoration:none}
.sh-brand img{width:26px;height:26px;border-radius:6.5px;display:block;box-shadow:0 0 0 .5px rgba(0,0,0,.16)}
.site-head nav{display:flex;gap:26px;margin-left:auto;font-size:13.5px}
.site-head nav a{display:inline-flex;align-items:center;min-height:44px;color:var(--ink-2);text-decoration:none;transition:color .2s}
.site-head nav a:hover,.site-head nav a[aria-current]{color:var(--ink)}
.sh-langs{display:flex;gap:1px;font-size:12.5px;font-weight:500}
.sh-langs a{position:relative;padding:5px 7px;border-radius:7px;color:var(--ink-2);text-decoration:none}
.sh-langs a::after{content:"";position:absolute;inset:-9px -1px}
.sh-langs a:hover{color:var(--ink)}
.sh-langs a[aria-current]{color:var(--ink);box-shadow:inset 0 0 0 1px var(--head-rule)}
.sh-get{position:relative;flex:none;display:inline-flex;align-items:center;height:30px;padding:0 14px;border-radius:999px;background:var(--btn);color:var(--btn-ink);font-size:13px;font-weight:600;text-decoration:none;white-space:nowrap;transition:transform .35s cubic-bezier(.22,1,.36,1),opacity .2s}
.sh-get::after{content:"";position:absolute;inset:-7px 0}
.sh-get:hover{color:var(--btn-ink);opacity:.86}
.sh-get:active{transform:scale(.96)}
@media (max-width:820px){.site-head nav{display:none}.sh-langs{margin-left:auto}.site-head .sh-w{gap:12px}}

/* App Store badge */
.store{display:inline-flex;align-items:center;gap:9px;height:52px;background:#000;color:#fff;text-decoration:none;border-radius:12px;padding:0 19px 0 16px;line-height:1.1;font-family:var(--font);box-shadow:inset 0 0 0 1px rgba(255,255,255,var(--store-edge,0));transition:transform .35s cubic-bezier(.22,1,.36,1)}
.store:hover{color:#fff}
.store:active{transform:scale(.97)}
.store svg{width:20px;height:24px;flex:none;margin-top:-2px}
.store span{display:flex;flex-direction:column;font-size:19px;font-weight:600;letter-spacing:-.01em;white-space:nowrap}
.store small{font-size:10.5px;font-weight:500;letter-spacing:0;margin-bottom:1px}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .store{--store-edge:.32}}
:root[data-theme="dark"] .store{--store-edge:.32}

/* the closing band: the slogan, the badge, and a code to scan on a computer */
.site-get{position:relative;overflow:hidden;isolation:isolate;text-align:center;font-family:var(--font);color:var(--ink);background:var(--paper);padding:clamp(84px,10vw,136px) 22px clamp(84px,10vw,128px)}
.site-get::before{content:"";position:absolute;z-index:-1;left:50%;top:50%;width:max(1100px,120%);height:560px;transform:translate(-50%,-46%);background:url(/h/aura.webp) center/100% 100% no-repeat;opacity:var(--aura)}
.site-get .sg-icon{width:84px;height:84px;border-radius:19px;display:block;margin:0 auto 28px;box-shadow:0 0 0 .5px rgba(0,0,0,.14),0 18px 34px -14px rgba(20,20,18,.35)}
.site-get h2{margin:0;font-family:var(--display);font-size:clamp(30px,8.2vw,80px);font-weight:700;letter-spacing:-.042em;line-height:1.02;color:var(--ink)}
.site-get h2 span{display:block}
.sg-cta{display:flex;align-items:center;justify-content:center;gap:26px;margin-top:clamp(30px,3.4vw,42px)}
.sg-qr{display:none;align-items:center;gap:12px;text-align:left;font-size:13.5px;line-height:1.3;color:var(--ink-2);max-width:11.5em}
.sg-qr img{width:76px;height:76px;flex:none;border-radius:10px;background:#fff;box-shadow:0 0 0 1px var(--rule)}
@media (min-width:900px) and (hover:hover){.sg-qr{display:flex}}
.site-get p{margin:18px auto 0;max-width:30em;font-size:15px;line-height:1.45;color:var(--ink-2)}

/* footer */
.site-foot{background:var(--foot);box-shadow:inset 0 1px 0 var(--foot-rule);color:rgba(255,255,255,.62);font-family:var(--font);font-size:13.5px;line-height:1.45;letter-spacing:-.005em;padding:56px 0 calc(48px + env(safe-area-inset-bottom,0px));text-align:left}
.site-foot .sf-w{display:grid;grid-template-columns:minmax(0,1.5fr) repeat(3,minmax(0,1fr));gap:30px;max-width:1120px;margin:0 auto;padding-left:max(22px,env(safe-area-inset-left,0px));padding-right:max(22px,env(safe-area-inset-right,0px))}
.site-foot .sh-brand{color:#fff;margin-bottom:6px}
.site-foot p{margin:0;max-width:23em;color:inherit}
.site-foot h4{margin:12px 0 12px;font:600 13px/1.3 var(--font);letter-spacing:0;color:#fff;text-transform:none}
.site-foot ul{list-style:none;margin:0;padding:0;display:grid;gap:9px}
.site-foot li{margin:0}
.site-foot a{color:inherit;text-decoration:none}
.site-foot a:hover{color:#fff}
.sf-base{grid-column:1/-1;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:14px;margin-top:22px;padding-top:22px;box-shadow:inset 0 1px 0 rgba(255,255,255,.1)}
.sf-langs{display:flex;gap:16px;margin-right:auto;margin-left:22px}
.sf-langs a[aria-current]{color:#fff}
.sf-look{display:inline-flex;padding:2px;border-radius:9px;background:rgba(255,255,255,.1)}
.sf-look button{border:0;background:transparent;color:rgba(255,255,255,.72);font:500 12.5px/1.2 var(--font);padding:6px 12px;border-radius:7px;cursor:pointer}
.sf-look button[aria-pressed="true"]{background:rgba(255,255,255,.18);color:#fff}
@media (max-width:820px){.site-foot .sf-w{grid-template-columns:repeat(2,minmax(0,1fr))}.site-foot .sf-about{grid-column:1/-1}.sf-langs{margin-left:0;flex-basis:100%;order:3}}
@media (prefers-reduced-motion:reduce){.sh-get,.store{transition:none}}
"""

# Runs before paint in <head>: the chosen look, so a dark reader never sees a white flash.
LOOK_HEAD_JS = ("<script>try{var l=localStorage.getItem('aera-look');if(l==='light'||l==='dark')"
                "document.documentElement.dataset.theme=l}catch(e){}</script>")

# The footer's look switch, and remembering a language picked in the header or footer.
JS = """<script>(function(){var d=document,r=d.documentElement,b=[].slice.call(d.querySelectorAll('[data-look]'));
function set(v){if(v==='light'||v==='dark')r.dataset.theme=v;else delete r.dataset.theme;b.forEach(function(x){x.setAttribute('aria-pressed',String(x.dataset.look===(v==='light'||v==='dark'?v:'auto')))})}
var s=null;try{s=localStorage.getItem('aera-look')}catch(e){}set(s);
b.forEach(function(x){x.addEventListener('click',function(){set(x.dataset.look);try{localStorage.setItem('aera-look',x.dataset.look)}catch(e){}})});
d.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('[data-lsw]');if(a){try{localStorage.setItem('aera-lang',a.getAttribute('data-lsw'))}catch(x){}}});
})();</script>"""


def badge(lang, href, extra=""):
    small, big = T[lang]["badge"]
    return '<a class="store" href="%s"%s>%s<span><small>%s</small>%s</span></a>' % (href, extra, APPLE, small, big)


def lang_links(lang, alts, short=True):
    """alts: {code: href}. Missing ones go to that language's home."""
    out = []
    for code, abbr, name, home in LANGS:
        out.append('<a href="%s" lang="%s" hreflang="%s" data-lsw="%s"%s>%s</a>' % (
            alts.get(code) or home, code, code, code, ' aria-current="page"' if code == lang else "", abbr if short else name))
    return "".join(out)


def header(lang, alts, store_href, current=None, has_alt=True):
    t = T[lang]
    nav = "".join('<a href="%s"%s>%s</a>' % (h, ' aria-current="page"' if current and h.split("#")[0] == current else "", n)
                  for n, h in t["nav"])
    return ('<header class="site-head" id="nav"><div class="sh-w">'
            '<a class="sh-brand" href="%s"><img src="/assets/icon.png" alt="" width="26" height="26">Aera</a>'
            '<nav aria-label="%s">%s</nav>'
            '<div class="sh-langs lsw" data-alt="%d" role="group" aria-label="%s">%s</div>'
            '<a class="sh-get" href="%s">%s</a>'
            '</div></header>' % (t["home"], t["nav_label"], nav, 1 if has_alt else 0, t["lang_label"],
                                 lang_links(lang, alts), store_href, t["get"]))


def closing(lang, store_href):
    t = T[lang]
    return ('<section class="site-get"><img class="sg-icon" src="/assets/icon.png" alt="%s" width="84" height="84" loading="lazy">'
            '<h2><span>%s</span> <span>%s</span></h2>'
            '<div class="sg-cta">%s<span class="sg-qr"><img src="/assets/qr-%s.svg" alt="%s" width="76" height="76" loading="lazy">%s</span></div>'
            '<p>%s</p></section>' % (t["icon_alt"], t["close_h"][0], t["close_h"][1], badge(lang, store_href),
                                     lang, t["qr_alt"], t["qr"], t["close_p"]))


def footer(lang, alts):
    t = T[lang]
    cols = "".join('<div><h4>%s</h4><ul>%s</ul></div>' % (
        title, "".join('<li><a href="%s">%s</a></li>' % (h, n) for n, h in links)) for title, links in t["cols"])
    look = t["look"]
    seg = "".join('<button type="button" data-look="%s" aria-pressed="%s">%s</button>' % (k, "true" if k == "auto" else "false", n)
                  for k, n in zip(("auto", "light", "dark"), look[1:]))
    return ('<footer class="site-foot"><div class="sf-w">'
            '<div class="sf-about"><a class="sh-brand" href="%s"><img src="/assets/icon.png" alt="" width="26" height="26" loading="lazy">Aera</a><p>%s</p></div>'
            '%s'
            '<div class="sf-base"><p>&#169; 2026 Aera</p><div class="sf-langs">%s</div>'
            '<div class="sf-look" role="group" aria-label="%s">%s</div></div>'
            '</div></footer>' % (t["home"], t["line"], cols, lang_links(lang, alts, short=False), look[0], seg))
