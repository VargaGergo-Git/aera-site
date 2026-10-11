#!/usr/bin/env python3
"""The home page (index.html, de.html, and hu.html once its words arrive),
built from scripts/keynote_copy.py with the look in keynote.css and the
motion in keynote.js.

    python3 scripts/build_home.py   # calls build() here for each language

One idea per section, a real app render beside it, and nothing drawn over a
device. Motion is a fade-up as a section enters and one replay film that plays
once in view; the page scrolls natively, with no pinned or scroll-driven
scenes."""
import html
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from keynote_copy import K  # noqa: E402

# Widths written for each render in img/k/ (name-<w>.webp).
WIDTHS = {
    "hero-pair": (900, 1800), "scr-run-light": (400, 800), "scr-route": (400, 800), "w-run": (422,),
    "w-turn": (422,),
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
    BASE, APPLE = H["BASE"], H["APPLE"]
    file = H["file"]

    def store(place):
        return "/get/%s/%s/" % (place, code)

    def btn(place, small=False):
        return '<a class="store%s" href="%s">%s<span>%s</span></a>' % (" small" if small else "", store(place), APPLE, k["cta"])

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
         "screenshot": [BASE + "img/k/hero-pair-1800.webp", BASE + "img/k/scr-run-light-800.webp",
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
    chips = "".join("<li>%s</li>" % x for x in k["wear_list"])

    def foot_col(title, links):
        return "<div><h4>%s</h4>%s</div>" % (title, "".join(
            '<a href="%s">%s</a>' % (store("footer") if h == "store" else h, t) for h, t in links))

    langs = "".join('<a href="%s" lang="%s" hreflang="%s"%s>%s</a>' % (f, lc, lc, ' aria-current="page"' if lc == code else "", n)
                    for lc, f, n in H["LANG_NAMES"])
    F = H["foot"]
    run_alts, route_alts = k["run_alts"], k["route_alts"]
    ph = "(max-width: 759px) 44vw, 260px"
    work_link = ('<a class="more-link" href="%s">%s</a>' % k["work_link"]) if "work_link" in k else ""

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
  <div class="hero-shot rise" style="--d:.24s">{img('hero-pair', k['hero_alt'], '(max-width: 759px) 100vw, 820px', eager=True)}</div>
</section>

<section class="sleep">
  <div class="wide intro reveal">
    <h2>{k['sleep_h2']}</h2>
    <p>{k['sleep_p']}</p>
  </div>
</section>

<section class="runs band">
  <div class="wide">
    <div class="copy center reveal">
      <h2>{k['run_h2']}</h2>
      <p>{k['run_p']}</p>
    </div>
    <div class="trio">
      <figure class="phone film reveal">
        <video muted playsinline preload="none" poster="img/k/replay-start-light-540.webp" data-light="media/k/replay-light.mp4" data-dark="media/k/replay-dark.mp4" data-poster-dark="img/k/replay-start-dark-540.webp" aria-label="{run_alts[0]}" width="540" height="1174"></video>
      </figure>
      <figure class="phone reveal" style="--d:.08s">{img('scr-run-light', run_alts[1], ph)}</figure>
      <figure class="watch reveal" style="--d:.16s">{img('w-run', run_alts[2], '(max-width: 759px) 40vw, 200px')}</figure>
    </div>
  </div>
</section>

<section class="route">
  <div class="wide split flip">
    <div class="copy reveal">
      <h2>{k['route_h2']}</h2>
      <p>{k['route_p']}</p>
    </div>
    <div class="pair reveal" style="--d:.1s">
      <figure class="phone">{img('scr-route', route_alts[0], ph)}</figure>
      <figure class="watch">{img('w-turn', route_alts[1], '(max-width: 759px) 40vw, 200px')}</figure>
    </div>
  </div>
</section>

<section class="more">
  <div class="wide">
    <div class="narrow center why reveal">
      <h2>{k['why_h2']}</h2>
      <p>{k['why_p']}</p>
    </div>
    <div class="bento">
      <article class="tile t-priv reveal">
        <h3>{k['priv_h2']}</h3><p>{k['priv_p']}</p><a class="more-link" href="{k['priv_link'][0]}">{k['priv_link'][1]}</a>
      </article>
      <article class="tile t-work reveal" style="--d:.12s">
        <h3>{k['b_work'][0]}</h3><p>{k['b_work'][1]}</p>
        {work_link}
      </article>
      <article class="tile t-wear reveal" style="--d:.18s">
        <h3>{k['wear_h2']}</h3><p>{k['wear_p']}</p>
        <ul class="chips">{chips}</ul>
        <a class="more-link" href="{k['wear_link'][0]}">{k['wear_link'][1]}</a>
      </article>
    </div>
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
  </div>
</section>

<section class="faq-sec">
  <div class="narrow">
    <h2 class="reveal">{k['faq_h2']}</h2>
    <div class="faq reveal">{faq}</div>
  </div>
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
