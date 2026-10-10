# Generates scenes/inside/section.html from example data: python3 scenes/inside/make_section.py scenes/inside/section.html
import random, statistics, math, sys
random.seed(7)
OUT = sys.argv[1]

def f(x): return ("%.1f" % x).rstrip("0").rstrip(".")

W, H = 520, 320
def plane(cls, body, extra=""):
    return ('<div class="ix-layer %s"><svg viewBox="0 0 %d %d" focusable="false" aria-hidden="true">'
            '<rect class="ix-glass" x="1" y="1" width="%d" height="%d" rx="26"/>%s%s'
            '</svg></div>' % (cls, W, H, W-2, H-2, body, extra))

# Three chart columns on the input and usual planes.
COLS = [(28, "sleep"), (178, "heart"), (328, "load")]
CW, TOP, BOT = 132, 70, 250

# --- Sleep: 13 nights, the last 3 bright; need line.
need = 470
nights = [random.randint(395, 500) for _ in range(10)] + [455, 440, 468]
def sy(m): return BOT - (m - 250) / 300 * (BOT - TOP)
sleep_bars = ""
for i, m in enumerate(nights):
    x = 28 + i * (CW / 13) + 1.5
    y = sy(m)
    cls = "on" if i >= 10 else "off"
    sleep_bars += '<rect class="b %s" x="%s" y="%s" width="%s" height="%s" rx="3"/>' % (cls, f(x), f(y), f(CW/13 - 5), f(BOT - y))

# --- Heart: 28 nights faint, 7 mornings bright, ln HRV around a centre.
base = [random.gauss(0, 1) for _ in range(28)]
mu, sd = statistics.mean(base), statistics.pstdev(base)
recent = [random.gauss(0.25, 0.5) for _ in range(7)]
def hy(z): return 160 - z * 34
heart = ""
for i, z in enumerate(base):
    heart += '<circle class="d off" cx="%s" cy="%s" r="2.6"/>' % (f(178 + 2 + i * 3.3), f(hy(z)))
for i, z in enumerate(recent):
    heart += '<circle class="d on" cx="%s" cy="%s" r="3.6"/>' % (f(178 + 98 + i * 5.2), f(hy(z)))
rmean = statistics.mean(recent)
heart += '<path class="mean" d="M%s %sH%s"/>' % (f(274), f(hy(rmean)), f(310))

# --- Training: 35 days of load, the last 7 bright.
loads = [max(0, random.gauss(42, 22)) if random.random() > .3 else 0 for _ in range(35)]
def ly(v): return BOT - v / 110 * (BOT - TOP)
load = ""
for i, v in enumerate(loads):
    x = 328 + i * (CW / 35)
    cls = "on" if i >= 28 else "off"
    if v > 0:
        load += '<rect class="b %s" x="%s" y="%s" width="%s" height="%s" rx="1.4"/>' % (cls, f(x), f(ly(v)), f(CW/35 - 1.2), f(BOT - ly(v)))
chronic = statistics.mean(loads[:28])

inputs = ('<g class="ix-c sleep">%s</g><g class="ix-c heart">%s</g><g class="ix-c load">%s</g>' % (sleep_bars, heart, load))
inputs += '<path class="ix-axis" d="M28 %dH160M178 %dH310M328 %dH460"/>' % (BOT + 8, BOT + 8, BOT + 8)

# --- Usual plane: bands at the same places.
band_lo, band_hi = hy(mu + .5 * sd), hy(mu - .5 * sd)
usual = ('<g class="ix-band sleep"><path class="need" d="M28 %sH160"/><rect x="28" y="%s" width="132" height="14" rx="7"/></g>' % (f(sy(need)), f(sy(need) - 7)))
usual += ('<g class="ix-band heart"><rect x="178" y="%s" width="132" height="%s" rx="10"/><path class="need" d="M178 %sH310"/></g>' % (f(band_lo), f(band_hi - band_lo), f(hy(mu))))
usual += ('<g class="ix-band load"><rect x="328" y="%s" width="132" height="%s" rx="8"/><path class="need" d="M328 %sH460"/></g>' % (f(ly(chronic * 1.2)), f(ly(chronic) - ly(chronic * 1.2) + 8), f(ly(chronic))))

# --- Checks plane: four rings with marks.
icons = [
    '<path d="M-8 7V-3M-2.5 7V-9M3 7V-1M8.5 7V-6"/>',                         # big session (bars)
    '<path d="M-9 0H9M-9-5V5M-6-7V7M9-5V5M6-7V7"/>',                          # strength (dumbbell)
    '<path d="M-9 6L-3 1L1 4L9-6M4-6H9V-1"/>',                                # ramp
    '<path d="M0 8C-7 3-10-1-10-4.5C-10-7.5-7.6-9.5-5-9.5C-2.8-9.5-1-8.2 0-6.4C1-8.2 2.8-9.5 5-9.5C7.6-9.5 10-7.5 10-4.5C10-1 7 3 0 8Z"/>',  # heart
]
checks = ""
for i, ic in enumerate(icons):
    cx = 86 + i * 116
    checks += ('<g class="ix-gate" style="--i:%d" transform="translate(%d 150)"><circle class="ring" r="40"/><circle class="arc" r="40" pathLength="1"/>'
               '<g class="ic">%s</g><g class="tick" transform="translate(28 -28)"><circle r="12"/><path d="M-5 0.5L-1.4 4L5.2-3.6"/></g></g>' % (i, cx, ic))
checks += '<path class="ix-rail" d="M126 150H160M242 150H276M358 150H392"/>'

# --- Length plane: 14 easy runs on a minutes axis; 60th percentile marker; 1.3x median cap.
runs = [32, 35, 38, 40, 40, 42, 44, 45, 46, 48, 50, 55, 62, 70]
s = sorted(runs)
rank = .6 * (len(s) - 1); lo = int(rank); p60 = s[lo] + (s[lo + 1] - s[lo]) * (rank - lo)
med = statistics.median(s); cap = med * 1.3
target = min(p60, cap); shown = 5 * round(target / 5)
assert shown == 45, shown
def mx(m): return 40 + (m - 20) / 60 * 400
length = '<path class="ix-axis" d="M40 262H440"/>'
for m in (20, 40, 60, 80):
    length += '<path class="ix-tk" d="M%s 256V268"/>' % f(mx(m))
seen = {}
for i, m in enumerate(runs):
    k = seen.get(m, 0); seen[m] = k + 1
    length += '<circle class="d" style="--i:%d" cx="%s" cy="%s" r="8"/>' % (i, f(mx(m)), f(242 - k * 19))
length += '<path class="cap" d="M%s 170V278"/>' % f(mx(cap))
length += '<g class="mark"><path d="M%s 160V286"/><circle cx="%s" cy="160" r="7"/></g>' % (f(mx(shown)), f(mx(shown)))

# --- Card plane.
card = ('<g class="ix-card"><text class="k" x="40" y="66">{{c_today}}</text>'
        '<text class="t" x="40" y="118">{{c_name}}</text>'
        '<text class="m" x="40" y="180">45<tspan class="u" dx="8">{{c_min}}</tspan></text>'
        '<g class="chips" transform="translate(40 224)">'
        '<g><circle cx="7" cy="-5" r="6" class="c1"/><text x="20" y="0">{{c_r1}}</text></g>'
        '<g transform="translate(0 30)"><circle cx="7" cy="-5" r="6" class="c2"/><text x="20" y="0">{{c_r2}}</text></g>'
        '<g transform="translate(0 60)"><circle cx="7" cy="-5" r="6" class="c3"/><text x="20" y="0">{{c_r3}}</text></g>'
        '</g></g>')

layers = (plane("l1", inputs) + plane("l2", usual) + plane("l3", checks) + plane("l4", length) + plane("l5", card))

labels = ""
for i, k in enumerate(["5", "4", "3", "2", "1"]):
    labels += ('<li class="ix-lab k%s" style="--i:%d"><b>{{h%s}}</b><span>{{p%s}}</span></li>' % (k, i, k, k))

html = '''<section class="scene scene-inside" id="inside" aria-labelledby="inside-h">
  <div class="ix-bg" aria-hidden="true"></div>
  <div class="wide ix-wrap">
    <header class="ix-head reveal">
      <h2 class="ix-h2" id="inside-h"><span>{{t1}}</span> <span class="ix-t2">{{t2}}</span></h2>
      <p class="ix-sub">{{sub}}</p>
    </header>
    <div class="ix-body">
      <div class="ix-stage" role="img" aria-label="{{alt}}">
        <div class="ix-float"><div class="ix-stack">
          %s
        </div></div>
        <div class="ix-floor" aria-hidden="true"></div>
      </div>
      <ol class="ix-labs">%s</ol>
    </div>
    <p class="ix-note">{{note}}</p>
  </div>
</section>
''' % (layers, labels)
open(OUT, "w").write(html)
print(len(html), "bytes; p60", p60, "median", med, "cap", cap)
