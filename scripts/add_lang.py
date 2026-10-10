"""Put the language switch (English, Magyar, Deutsch) on every page.

Header: a small globe button with the page's language code; it opens a menu of
the three languages. Each entry links to the page's own translation when one
exists (its <link rel="alternate" hreflang> tags), otherwise to that
language's home page. Footer: the same three links as a quiet line, plus Privacy (the header
hides its Privacy link on phones to make room for the switch). The home
pages (index, hu, de) already list the languages in their footer, so they get
the header button only.

The choice is remembered in localStorage. On an English page, a browser set
to Hungarian or German that has made no choice gets one quiet bottom card
offering that language (dismissed for good with its close button). Nothing
ever redirects: on a page
with no translation, links back to the English home point to the chosen
language's home instead.

Idempotent: everything sits between <!--lsw--> markers and is rebuilt on each
run. Re-run after build_home.py, build_articles.py or adding a page.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from build_home import ROOT  # noqa: E402

SKIP_DIRS = {".git", "scenes", "shots", "assets", "img", "scripts", "get", "hi", "media"}
HOME = {"index.html", "hu.html", "de.html"}
LANGS = (("en", "English", "/"), ("hu", "Magyar", "/hu.html"), ("de", "Deutsch", "/de.html"))
LABEL = {"en": "Language", "hu": "Nyelv", "de": "Sprache"}
PRIVACY = {"en": "Privacy", "hu": "Adatvédelem", "de": "Datenschutz"}
MARK = re.compile(r"<!--lsw-->.*?<!--/lsw-->\n?", re.S)
ALT = re.compile(r'<link rel="alternate" hreflang="(en|hu|de)" href="https://aerahealth\.app([^"]*)">')

GLOBE = ('<svg viewBox="0 0 16 16" aria-hidden="true" focusable="false"><g fill="none" stroke="currentColor" '
         'stroke-width="1.3"><circle cx="8" cy="8" r="6.5"/><path d="M1.5 8h13M8 1.5c1.9 2 2.8 4.1 2.8 6.5S9.9 12.5 '
         '8 14.5M8 1.5C6.1 3.5 5.2 5.6 5.2 8s.9 4.5 2.8 6.5"/></g></svg>')

CSS = """<!--lsw--><style>
.lsw{position:relative;display:inline-flex;align-items:center}
.topnav:has(.lsw){align-items:center}
.lsw>summary{list-style:none;display:inline-flex;align-items:center;gap:6px;min-height:44px;min-width:44px;justify-content:center;padding:0 10px;margin:0 -6px;border-radius:999px;cursor:pointer;font-family:inherit;font-size:13px;font-weight:600;letter-spacing:.04em;line-height:1;color:inherit;-webkit-tap-highlight-color:transparent;-webkit-user-select:none;user-select:none}
.lsw>summary::-webkit-details-marker{display:none}
@media (hover:hover){.lsw>summary:hover{background:color-mix(in srgb,currentColor 12%,transparent)}}
.lsw>summary:focus-visible{outline:2px solid currentColor;outline-offset:2px}
.lsw svg{width:16px;height:16px;flex:none}
.lsw-menu{position:absolute;top:calc(100% + 8px);right:-6px;z-index:80;display:grid;min-width:172px;padding:6px;border-radius:14px;background:#fff;color:#1d1d1f;box-shadow:0 14px 36px rgba(0,0,0,.18),0 0 0 .5px rgba(0,0,0,.1)}
.lsw[open] .lsw-menu{animation:lsw-in .2s cubic-bezier(.2,.8,.2,1)}
@keyframes lsw-in{from{opacity:0;transform:translateY(-6px) scale(.98)}}
.lsw-menu a{display:flex;align-items:center;justify-content:space-between;gap:16px;min-height:42px;padding:0 12px;border-radius:9px;color:inherit!important;text-decoration:none;font-size:15px;font-weight:500;line-height:1.2;white-space:nowrap}
@media (hover:hover){.lsw-menu a:hover{background:rgba(0,0,0,.055)}}
.lsw-menu a[aria-current]{font-weight:600}
.lsw-menu a[aria-current]::after{content:"";width:12px;height:6px;margin-top:-3px;border:solid currentColor;border-width:0 0 2px 2px;transform:rotate(-45deg)}
@media (prefers-color-scheme:dark){.lsw-menu{background:#2c2c2e;color:#f5f5f7;box-shadow:0 14px 36px rgba(0,0,0,.55),0 0 0 .5px rgba(255,255,255,.12)}@media (hover:hover){.lsw-menu a:hover{background:rgba(255,255,255,.08)}}}
@media (prefers-reduced-motion:reduce){.lsw[open] .lsw-menu{animation:none}}
.bar .lsw{color:var(--hero-ink-2);transition:opacity .35s ease .2s,visibility 0s}
.bar.scrolled .lsw{color:var(--ink-2)}
.bar.ch-on .lsw{opacity:0;visibility:hidden;pointer-events:none;transition:opacity .2s ease,visibility 0s .2s}
.lsw-foot{display:flex;flex-wrap:wrap;align-items:center;gap:6px 18px;padding-block:2px 22px;font-size:14px}
.lsw-foot a{color:inherit;opacity:.72;text-decoration:none}
.lsw-foot a[aria-current]{opacity:1;font-weight:600}
@media (hover:hover){.lsw-foot a:hover{opacity:1}}
.lsw-hint{position:fixed;left:50%;bottom:calc(16px + env(safe-area-inset-bottom,0px));z-index:90;display:flex;align-items:center;gap:4px;max-width:calc(100vw - 24px);padding:5px 5px 5px 18px;border-radius:999px;background:#fff;color:#1d1d1f;box-shadow:0 14px 36px rgba(0,0,0,.2),0 0 0 .5px rgba(0,0,0,.1);font:500 15px/1.2 -apple-system,BlinkMacSystemFont,"Inter",system-ui,sans-serif;white-space:nowrap;transform:translateX(-50%);animation:lsw-up .6s cubic-bezier(.16,1,.3,1) both}
@keyframes lsw-up{from{opacity:0;transform:translate(-50%,18px)}}
.lsw-hint span{overflow:hidden;text-overflow:ellipsis;margin-right:8px}
.lsw-hint a{display:inline-flex;align-items:center;min-height:44px;padding:0 18px;border-radius:999px;background:#1d1d1f;color:#fff;font-weight:600;text-decoration:none}
.lsw-hint button{flex:none;width:44px;height:44px;border:0;border-radius:50%;background:none;color:inherit;font-size:22px;line-height:1;cursor:pointer;opacity:.6}
@media (hover:hover){.lsw-hint button:hover{opacity:1}}
@media (prefers-color-scheme:dark){.lsw-hint{background:#2c2c2e;color:#f5f5f7;box-shadow:0 14px 36px rgba(0,0,0,.55),0 0 0 .5px rgba(255,255,255,.12)}.lsw-hint a{background:#f5f5f7;color:#000}}
@media (prefers-reduced-motion:reduce){.lsw-hint{animation:none}}
@media (max-width:479px){.topnav .lsw>summary{padding:0;margin:0 -10px 0 -6px}.topnav .lsw>summary span{display:none}.topnav:has(.lsw){gap:12px}.topnav:has(.lsw)>a[href*="privacy"]{display:none}}
@media (max-width:359px){.topnav:has(.lsw){gap:9px}}
</style><!--/lsw-->
"""

JS = """<!--lsw--><script>(function(){var d=document,K='aera-lang';
function shut(o){o.removeAttribute('open')}
d.addEventListener('click',function(e){var t=e.target,a=t.closest&&t.closest('[data-lsw]');
if(a){try{localStorage.setItem(K,a.getAttribute('data-lsw'))}catch(x){}}
[].forEach.call(d.querySelectorAll('.lsw[open]'),function(o){if(!o.contains(t))shut(o)})});
d.addEventListener('keydown',function(e){if(e.key!=='Escape')return;[].forEach.call(d.querySelectorAll('.lsw[open]'),function(o){shut(o);o.querySelector('summary').focus()})});
var s=d.querySelector('.lsw');if(!s)return;
var l;try{l=localStorage.getItem(K)}catch(x){}
// An English page, a browser set to Hungarian or German, no choice made yet: one quiet offer, never a redirect.
var H={hu:['Magyarul is olvasható.','Magyar','Bezárás'],de:['Auch auf Deutsch.','Deutsch','Schließen']},HK='aera-lang-hint';
try{var nv=(navigator.languages||[navigator.language||''])[0].slice(0,2).toLowerCase(),seen=localStorage.getItem(HK),
to=s.querySelector('[data-lsw="'+nv+'"]');
if(!l&&!seen&&H[nv]&&d.documentElement.lang==='en'&&to)setTimeout(function(){var b=d.createElement('div');b.className='lsw-hint';b.setAttribute('role','region');b.setAttribute('aria-label',H[nv][1]);b.setAttribute('lang',nv);
b.innerHTML='<span></span><a data-lsw="'+nv+'" hreflang="'+nv+'"></a><button type="button">\u00d7</button>';
b.firstChild.textContent=H[nv][0];b.children[1].textContent=H[nv][1];b.children[1].href=to.getAttribute('href');b.lastChild.setAttribute('aria-label',H[nv][2]);
b.lastChild.onclick=function(){try{localStorage.setItem(HK,'1')}catch(x){}b.remove()};d.body.appendChild(b)},1200)}catch(x){}
if(s.getAttribute('data-alt')!=='0')return;
var home={hu:'/hu.html',de:'/de.html'}[l];if(!home||d.documentElement.lang===l)return;
[].forEach.call(d.querySelectorAll('a[href]'),function(a){if(a.closest('.lsw,.lsw-foot'))return;
var u=new URL(a.href,location.href);if(u.origin===location.origin&&(u.pathname==='/'||u.pathname==='/index.html')&&!u.hash)a.setAttribute('href',home)})})();</script><!--/lsw-->
"""


def targets(s):
    alts = dict(ALT.findall(s))
    out = []
    for code, name, home in LANGS:
        out.append((code, name, alts.get(code) or home))
    return out, bool(alts)


def links(cur, tg, cls=""):
    return "".join('<a href="%s" lang="%s" hreflang="%s" data-lsw="%s"%s>%s</a>' % (
        href, code, code, code, ' aria-current="page"' if code == cur else "", name) for code, name, href in tg)


def button(cur, tg, has_alt):
    return ('<!--lsw--><details class="lsw" data-alt="%d"><summary aria-label="%s: %s">%s<span>%s</span></summary>'
            '<div class="lsw-menu">%s</div></details><!--/lsw-->' % (
                1 if has_alt else 0, LABEL[cur], dict((c, n) for c, n, _ in LANGS)[cur], GLOBE, cur.upper(),
                links(cur, tg)))


def process(path, home):
    s = open(path, encoding="utf-8").read()
    m = re.search(r'<html[^>]*\blang="(en|hu|de)"', s)
    if not m or "</head>" not in s or "</body>" not in s:
        return False
    cur = m.group(1)
    new = MARK.sub("", s)
    tg, has_alt = targets(new)
    btn = button(cur, tg, has_alt)
    if home:
        if '<a class="get"' not in new:
            return False
        new = new.replace('<a class="get"', btn + '<a class="get"', 1)
    else:
        i = new.find('<nav class="topnav">')
        if i < 0:
            return False
        j = new.find("</nav>", i)
        new = new[:j] + btn + new[j:]
        k = new.rfind("</footer>")
        if k > 0:
            new = new[:k] + '<!--lsw--><div class="wrap lsw-foot">%s<a href="/privacy.html">%s</a></div><!--/lsw-->\n' % (
                links(cur, tg), PRIVACY[cur]) + new[k:]
    new = new.replace("</head>", CSS + "</head>", 1)
    b = new.rfind("</body>")
    new = new[:b] + JS + new[b:]
    if new != s:
        open(path, "w", encoding="utf-8").write(new)
        return True
    return False


def main():
    changed = 0
    for d, dirs, files in os.walk(ROOT):
        dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
        for f in files:
            if f.endswith(".html") and process(os.path.join(d, f), d == ROOT and f in HOME):
                changed += 1
    print("language switch: %d pages updated" % changed)


if __name__ == "__main__":
    main()
