#!/usr/bin/env python3
"""The home page (index.html, de.html, and hu.html once its words arrive),
built from scripts/keynote_copy.py with the look in keynote.css and the
motion in keynote.js.

    python3 scripts/build_home.py   # calls build() here for each language

One idea per section, a real app render beside it, and nothing drawn over a
device. Motion: sections fade up as they enter, devices settle in on scroll
where the browser supports view timelines, one 3D replay plays at a time with
places to pick, the route phone's screens take turns, and the share cards fan
in. The page scrolls natively, with no pinned or scroll-hijacking scenes."""
import html
import re
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from keynote_copy import K  # noqa: E402

# Widths written for each render in img/k/ (name-<w>.webp).
WIDTHS = {
    "hero-pair": (900, 1800), "scr-run-light": (400, 800), "scr-route": (400, 800), "w-run": (422,),
    "w-turn": (422,), "scr-age-light": (400, 800), "scr-vitals": (400, 800), "scr-today": (400, 800), "scr-age-dark": (400, 800), "scr-sleep-light": (400, 800), "scr-sleep-dark": (400, 800), "art-sleep-light": (400, 800), "art-sleep-dark": (400, 800), "scr-loops": (400, 800), "scr-loop-route": (400, 800), "w-now": (422,), "place-greenlake": (480,), "place-braies": (480,), "place-seawall": (480,),
    **{"card-" + c: (360, 720) for c in ("week", "pb", "clock", "splits", "zones")},
}


def _size(name):
    """Intrinsic size of the largest file, for width/height (no layout shift)."""
    from PIL import Image
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with Image.open(os.path.join(root, "img/k/%s-%d.webp" % (name, WIDTHS[name][-1]))) as im:
        return im.size


def img(name, alt, sizes, eager=False, cls=""):
    ws = WIDTHS[name]
    w, h = _size(name)
    srcset = ", ".join("img/k/%s-%d.webp %dw" % (name, x, x) for x in ws)
    return ('<img%s src="img/k/%s-%d.webp" srcset="%s" sizes="%s" alt="%s" width="%d" height="%d"%s decoding="async">'
            % (' class="%s"' % cls if cls else "", name, ws[0], srcset, sizes, alt, w, h,
               ' fetchpriority="high"' if eager else ' loading="lazy"'))


def pic(light, dark, alt, sizes, cls=""):
    """A render with its dark-mode capture swapped in by the browser."""
    srcset = ", ".join("img/k/%s-%d.webp %dw" % (dark, x, x) for x in WIDTHS[dark])
    return ('<picture><source media="(prefers-color-scheme: dark)" srcset="%s" sizes="%s">%s</picture>'
            % (srcset, sizes, img(light, alt, sizes, cls=cls)))


def localize(out, code):
    """On /de and /hu, swap in the renders captured in that language where they
    exist: img/k/NAME -> img/k/<code>/NAME, media/k/NAME -> media/k/<code>/NAME."""
    import re
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def swap(m):
        local = "%s/%s/%s" % (m.group(1), code, m.group(2))
        return local if os.path.exists(os.path.join(root, local)) else m.group(0)
    return re.sub(r"\b((?:img|media)/k)/([\w.-]+\.(?:webp|jpg|png|mp4))", swap, out)


def build(code, H):
    """H carries what the page shares with build_home: BASE, APPLE, CF_BEACON,
    OG_LOCALE, LANG_NAMES, asset(), the store URL and footer links."""
    k = K[code]
    missing = [x for x in K["en"] if x not in k]
    if missing:  # a language still waiting on its words for a newer section
        print("build_keynote: %s falls back to English for %s" % (code, ", ".join(missing)), file=sys.stderr)
        k = {**K["en"], **k}
    # A page never mixes languages inside its screens: the "loops from here"
    # frame exists in English only, so /de and /hu skip it.
    here = lambda name: code == "en" or os.path.exists(os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "img/k/%s/%s" % (code, name)))
    ph_ = "(max-width: 759px) 72vw, 300px"
    loops = img('scr-loops', k['route_more_alts'][0], "(max-width: 759px) 44vw, 260px", cls='alt') if here("scr-loops-400.webp") else ""
    sleep_pic = (pic('scr-sleep-light', 'scr-sleep-dark', k['sleep_alt'], ph_) if here("scr-sleep-light-400.webp")
                 else pic('art-sleep-light', 'art-sleep-dark', k['sleep_art_alt'], ph_))
    # Section one of the identity brief: one number inside its band explains "usual".
    # Shown only where its words exist in this language (no mixed pages).
    normal_sec = (f'''<section class="ch ch-first">
  <div class="wide">
    <div class="panel grow p-normal">
      <div class="copy reveal">
        <h2>{k['normal_h2']}</h2>
        <p>{k['normal_p']}</p>
        <p class="fine">{k['normal_cap']}</p>
      </div>
      <div class="stage full"><figure class="phone rise-in">{img('scr-vitals', k['normal_alt'], ph_)}</figure></div>
    </div>
    @@SEC_NORMAL@@
  </div>
</section>
''' if "normal_h2" in K[code] and here("scr-vitals-400.webp") else "")
    BASE, APPLE = H["BASE"], H["APPLE"]
    file = H["file"]

    def store(place):
        return "/get/%s/%s/" % (place, code)

    def btn(place, small=False, light=False):
        return '<a class="store%s%s" href="%s">%s<span>%s</span></a>' % (" small" if small else "", " light" if light else "", store(place), APPLE, k["cta"])

    def sec_cta(place):
        # The same store button once more at the foot of a main section, so the
        # next step is never far; each place is its own /get/ path (GET_PLACES).
        return '<div class="panel-cta sec-cta reveal">%s</div>' % btn(place)

    canonical = BASE + ("" if file == "index.html" else file)
    alternates = "".join('<link rel="alternate" hreflang="%s" href="%s%s">' % (lc, BASE, "" if f == "index.html" else f)
                         for lc, f, _ in H["LANG_NAMES"])
    alternates += '<link rel="alternate" hreflang="x-default" href="%s">' % BASE
    og_alt = "".join('<meta property="og:locale:alternate" content="%s">' % H["OG_LOCALE"][lc]
                     for lc in H["OG_LOCALE"] if lc != code)
    nav = "".join('<a class="opt" href="%s">%s</a>' % (h, t) for h, t in k["nav"])
    plain = html.unescape

    graph = [
        {"@type": "MobileApplication", "@id": BASE + "#app", "name": "Aera", "alternateName": plain(k["og_title"]),
         "applicationCategory": "HealthApplication", "operatingSystem": "iOS, watchOS",
         "inLanguage": ["en", "hu", "de", "es", "fr", "it", "ja", "pt", "zh-Hant"],
         "url": canonical, "downloadUrl": H["store"], "installUrl": H["store"], "description": plain(k["desc"]),
         "screenshot": [BASE + "img/k/hero-pair-1800.webp", BASE + "img/k/art-sleep-light-800.webp", BASE + "img/k/scr-run-light-800.webp",
                        BASE + "img/k/scr-route-800.webp"],
         "author": {"@id": BASE + "#maker"}, "publisher": {"@id": BASE + "#org"}, "isAccessibleForFree": True,
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD", "category": "free"}},
        {"@type": "Person", "@id": BASE + "#maker", "name": "Gergő Varga", "url": BASE},
        {"@type": "Organization", "@id": BASE + "#org", "name": "Aera", "url": BASE, "logo": BASE + "assets/icon.png",
         "email": "hello@aerahealth.app", "founder": {"@id": BASE + "#maker"}, "sameAs": [H["store_en"]]},
        {"@type": "WebSite", "@id": BASE + "#site", "name": "Aera", "url": BASE, "inLanguage": code,
         "publisher": {"@id": BASE + "#org"}},
        {"@type": "FAQPage", "inLanguage": code,
         "mainEntity": [{"@type": "Question", "name": plain(q), "acceptedAnswer": {"@type": "Answer", "text": plain(a)}}
                        for q, a in k["faq"]]},
    ]
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False).replace("</", "<\\/")

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

    beacon = ""
    if H["CF_BEACON"]:
        beacon = ('<script defer src="https://static.cloudflareinsights.com/beacon.min.js" '
                  "data-cf-beacon='{\"token\": \"%s\"}'></script>" % H["CF_BEACON"])

    faq = "".join('<details class="qa"><summary><h3>%s</h3><i aria-hidden="true"></i></summary><p>%s</p></details>' % qa
                  for qa in k["faq"])
    li = lambda xs: "".join("<li>%s</li>" % x for x in xs)
    marks = "".join('<li class="reveal" style="--d:%.2fs">%s</li>' % (i * .06, x) for i, x in enumerate(k["wear_list"]))
    why_b = re.search(r"<b>(.*?)</b>", k["why_p"]).group(1)
    # The lead lights up word by word as it crosses the screen (CSS scroll timeline;
    # without one it simply shows in full).
    _w = [(w, "g") for w in k["why_h2"].split()] + [(w, "") for w in why_b.split()]
    lead = " ".join('<span class="w %s" style="--i:%d">%s</span>' % (c, i, w) for i, (w, c) in enumerate(_w))

    def foot_col(title, links):
        return "<div><h4>%s</h4>%s</div>" % (title, "".join(
            '<a href="%s">%s</a>' % (store("footer") if h == "store" else h, t) for h, t in links))

    langs = "".join('<a href="%s" lang="%s" hreflang="%s"%s>%s</a>' % (f, lc, lc, ' aria-current="page"' if lc == code else "", n)
                    for lc, f, n in H["LANG_NAMES"])
    F = H["foot"]
    run_alts, route_alts = k["run_alts"], k["route_alts"]
    ph = "(max-width: 759px) 44vw, 260px"
    # Land first: Gergő found the Green Lake opening "only water", so the seawall
    # leads and every clip is cut where the route runs over land.
    names = ("greenlake", "bled", "braies", "seawall")
    places_ = [("img/k/place-%s-480.webp" % n, "media/k/place-%s.mp4" % n) + k["places"][names.index(n)]
               for n in ("seawall", "greenlake", "braies")
               if here("place-%s-480.webp" % n)]
    places_p = k["places_p"] if len(places_) > 1 else k["places_p"].rsplit(". ", 1)[0] + "."  # no "pick a place" with one place
    tabs = "".join('<button type="button" role="tab" aria-selected="%s" data-poster="%s" data-src="%s" data-label="%s">%s</button>'
                   % ("true" if i == 0 else "false", p, v, alt, cap) for i, (p, v, cap, alt) in enumerate(places_))
    cards = "".join('<li class="card" style="--i:%d"><figure>%s<figcaption>%s</figcaption></figure></li>'
                    % (i, img("card-" + c, alt, "(max-width: 759px) 62vw, 300px"), cap)
                    for i, (c, cap, alt) in enumerate(k["share_cards"]))
    # The share rail shows on /de and /hu only once every card is captured in that language.
    share_sec = (f'''<section class="share">
  <div class="wide">
    <div class="copy center reveal">
      <h2>{k['share_h2']}</h2>
      <p>{k['share_p']}</p>
    </div>
  </div>
  <div class="rail-wrap reveal" style="--d:.1s">
    <ul class="rail" tabindex="0">{cards}</ul>
    <div class="wide rail-nav"><button class="rail-btn prev" type="button" aria-label="{k['share_prev']}"></button><button class="rail-btn next" type="button" aria-label="{k['share_next']}"></button></div>
  </div>
  <div class="wide">{sec_cta('sec-share')}</div>
</section>'''
                 if all(here("card-%s-360.webp" % c[0]) for c in k["share_cards"]) else "")
    work_link = ('<a class="more-link" href="%s">%s</a>' % k["work_link"]) if "work_link" in k else ""

    # The identity brief (Gergő, 13 Oct): hero, then Your normal, Today, What
    # changed, the long view, and the closer. A language gets it once its words
    # exist; until then it keeps the earlier chapters (no mixed pages).
    new = "today_h2" in K[code] and here("scr-vitals-400.webp") and here("scr-today-400.webp")
    old_story = f'''<section class="statement">
  <div class="wide">
    <p class="lead" style="--n:{len(_w)}">{lead}</p>
  </div>
</section>

<section class="ch">
  <div class="wide">
    <div class="panel grow p-sleep">
      <div class="copy reveal">
        <h2>{k['sleep_h2']}</h2>
        <p>{k['sleep_p']}</p>
      </div>
      <div class="stage"><figure class="phone rise-in">{sleep_pic}</figure></div>
    </div>
    {sec_cta('sec-sleep')}
  </div>
</section>

<section class="ch">
  <div class="wide">
    <div class="dark-pair grow">
    <div class="panel p-dark p-runs">
      <div class="copy reveal">
        <h2>{k['run_h2']}</h2>
        <p>{k['run_p']}</p>
      </div>
      <div class="stage wide-stage"><div class="pair">
        <figure class="phone rise-in">{img('scr-run-light', run_alts[1], ph)}</figure>
        <figure class="watch slide-in">{img('w-run', run_alts[2], '(max-width: 759px) 34vw, 180px')}</figure>
      </div></div>
    </div>
    <div class="panel p-dark p-fly">
      <div class="copy center reveal">
        <h2>{k['places_h2']}</h2>
        <p>{places_p}</p>
      </div>
      <div class="player reveal" style="--d:.1s">
        <div class="phone clip settle"><video muted playsinline preload="none" poster="{places_[0][0]}" data-src="{places_[0][1]}" aria-label="{places_[0][3]}" width="480" height="1044"></video></div>
        {'<div class="tabs" role="tablist">%s</div>' % tabs if len(places_) > 1 else ''}
      </div>
      <div class="panel-cta reveal">{btn('flyover', light=True)}</div>
    </div>
    </div>
  </div>
</section>

{share_sec}

<section class="ch">
  <div class="wide">
    <div class="panel grow p-route flip">
      <div class="copy reveal">
        <h2>{k['route_h2']}</h2>
        <p>{k['route_p']}</p>
      </div>
      <div class="stage wide-stage"><div class="pair">
        <figure class="phone cycle rise-in">{img('scr-route', route_alts[0], ph)}{loops}{img('scr-loop-route', k['route_more_alts'][1], ph, cls='alt')}</figure>
        <figure class="watch slide-in">{img('w-turn', route_alts[1], '(max-width: 759px) 40vw, 200px')}</figure>
      </div></div>
    </div>
    {sec_cta('sec-route')}
  </div>
</section>

<section class="ch">
  <div class="wide">
    <div class="panel grow p-age">
      <div class="copy reveal">
        <h2>{k['age_h2']}</h2>
        <p>{k['age_p']}</p>
        <p class="fine">{k['age_note']}</p>
      </div>
      <div class="stage"><figure class="phone rise-in">{pic('scr-age-light', 'scr-age-dark', k['age_alt'], ph_)}</figure></div>
    </div>
    {sec_cta('sec-age')}
  </div>
</section>'''
    fly_player = f'''<div class="player reveal" style="--d:.1s">
        <div class="phone clip settle"><video muted playsinline preload="none" poster="{places_[0][0]}" data-src="{places_[0][1]}" aria-label="{places_[0][3]}" width="480" height="1044"></video></div>
        {'<div class="tabs" role="tablist">%s</div>' % tabs if len(places_) > 1 else ''}
      </div>'''
    new_story = (f'''<section class="ch">
  <div class="wide">
    <div class="panel grow p-today flip">
      <div class="copy reveal">
        <h2>{k.get('today_h2', '')}</h2>
        <p>{k.get('today_p', '')}</p>
      </div>
      <div class="stage full"><figure class="phone rise-in">{img('scr-today', k.get('today_alt', ''), ph_)}</figure></div>
    </div>
    {sec_cta('sec-today')}
  </div>
</section>

<section class="ch">
  <div class="wide">
    <div class="panel grow p-dark p-fly">
      <div class="copy center reveal">
        <h2>{k.get('changed_h2', '')}</h2>
        <p>{k.get('changed_p', '')}</p>
      </div>
      {fly_player}
      <div class="panel-cta reveal">{btn('flyover', light=True)}</div>
    </div>
  </div>
</section>

<section class="longview">
  <div class="narrow center reveal"><p>{k.get('long_p', '')}</p></div>
</section>

{share_sec}
''' if new else "")
    normal_sec = normal_sec.replace("@@SEC_NORMAL@@", sec_cta("sec-normal"))
    story = (normal_sec + new_story) if new else (normal_sec + old_story)
    work_blk = "" if new else f'''    <div class="work narrow center reveal">
      <h2>{k['b_work'][0]}</h2>
      <p>{k['b_work'][1]}</p>
      {work_link}
    </div>'''
    return localize(f"""<!DOCTYPE html>
<html lang="{code}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="apple-itunes-app" content="app-id=6762456252">
<title>{k['title']}</title>
<meta name="description" content="{k['desc']}">
<meta name="theme-color" content="#f6f4ef" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#000000" media="(prefers-color-scheme: dark)">
<meta property="og:title" content="{k['og_title']}">
<meta property="og:description" content="{k['desc']}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Aera">
<meta property="og:locale" content="{H['OG_LOCALE'][code]}">{og_alt}
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{BASE}assets/og-k.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{k['og_title']}">
<meta name="twitter:description" content="{k['desc']}">
<meta name="twitter:image" content="{BASE}assets/og-k.jpg">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{canonical}">
{alternates}
<link rel="icon" href="assets/icon.png">
<link rel="apple-touch-icon" href="assets/icon.png">
<link rel="preload" as="image" href="img/k/hero-pair-900.webp" imagesrcset="img/k/hero-pair-900.webp 900w, img/k/hero-pair-1800.webp 1800w" imagesizes="(max-width: 759px) 100vw, 820px">
<link rel="stylesheet" href="{H['asset']('keynote.css')}">
<script type="application/ld+json">{ld}</script>
{legacy}
</head>
<body>
<a class="skip" href="#main">{k['skip']}</a>

<header class="bar">
  <div class="wide">
    <a class="brand" href="{file}"><img src="assets/icon.png" alt="" width="28" height="28">Aera</a>
    <nav>{nav}<a class="get" href="{store('nav')}">{k['get']}</a></nav>
  </div>
</header>

<main id="main">
<section class="hero">
  <div class="wide">
    <h1 class="rise">{k['h1']}</h1>
    <p class="lede rise" style="--d:.08s">{k['sub']}</p>
    <div class="cta rise" style="--d:.16s">{btn('hero')}<p class="note">{k['note']}</p></div>
  </div>
  <div class="hero-shot rise" style="--d:.24s"><div class="hero-zoom">{img('hero-pair', k['hero_alt'], '(max-width: 759px) 100vw, 820px', eager=True)}</div></div>
</section>

<section class="works">
  <div class="wide reveal">
    <p class="works-h">{k['wear_h2']}</p>
    <ul class="marks">{marks}</ul>
    <a class="more-link" href="{k['wear_link'][0]}">{k['wear_link'][1]}</a>
  </div>
</section>

{story}

<section class="priv-sec">
  <div class="wide">
    <div class="priv grow">
      <img class="priv-icon pop" src="assets/icon.png" alt="" width="72" height="72" loading="lazy" decoding="async">
      <h2>{k['priv_h2']}</h2>
      <p>{k['priv_p']}</p>
      <a class="more-link" href="{k['priv_link'][0]}">{k['priv_link'][1]}</a>
      <div class="panel-cta">{btn('engine', light=True)}</div>
    </div>
{work_blk}
  </div>
</section>

<section class="plans-sec">
  <div class="wide">
    <h2 class="center reveal">{k['plans_h2']}</h2>
    <div class="plans">
      <div class="plan reveal"><h3>{k['free_h']}</h3><ul>{li(k['free'])}</ul></div>
      <div class="plan prem reveal" style="--d:.08s"><h3>{k['prem_h']}</h3><ul>{li(k['prem'])}</ul></div>
    </div>
    <p class="plans-note center reveal">{k['prem_note']}</p>
    {sec_cta('sec-plans')}
  </div>
</section>

<section class="faq-sec">
  <div class="wide qa-grid">
    <h2 class="reveal">{k['faq_h2']}</h2>
    <div class="faq reveal">{faq}</div>
  </div>
  <div class="wide">{sec_cta('sec-faq')}</div>
</section>

<section class="maker">
  <div class="narrow center reveal">
    <h2>{k['maker_h2']}</h2>
    <p>{k['maker_p']}</p>
    <a class="more-link" href="{k['maker_link'][0]}">{k['maker_link'][1]}</a>
  </div>
</section>

<section class="closing">
  <div class="wide center reveal">
    <img class="icon" src="assets/icon.png" alt="" width="88" height="88" loading="lazy" decoding="async">
    <h2>{k['close_h2']}</h2>
    {'<p class="closer">%s</p>' % k['closer'] if 'closer' in K[code] else ''}
    {btn('closing')}
    <p class="note">{k['close_note']}</p>
  </div>
</section>
</main>

<footer>
  <div class="wide">
    <div class="foot">
      <div class="foot-brand"><a class="brand" href="{file}"><img src="assets/icon.png" alt="" width="28" height="28">Aera</a><p>{k['foot_tag']}</p></div>
      {foot_col(F['app'], F['links_app'])}
      {foot_col(F['legal'], F['links_legal'])}
      <div><h4>{F['more']}</h4>{''.join('<a href="%s">%s</a>' % (h, t) for h, t in F['links_more'])}{langs}</div>
    </div>
    <div class="foot-base"><span>{F['base'][0]}</span><span>{F['base'][1]}</span></div>
  </div>
</footer>

<script src="{H['asset']('keynote.js')}" defer></script>
{beacon}
</body>
</html>
""", code)
