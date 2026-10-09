"""The painted valley behind the homepage hero, generated once into static SVG.

Deterministic: the same seeds always draw the same valley. Four layers, far to
near, each its own <svg> so the page can move them as separate GPU layers.
Colours come from CSS classes (r1..r4, tk, fir, bale), so light and dark mode
repaint the same shapes.
"""
import math
import random

W = 1600


def _ridge(seed, h, base, waves, step=10):
    rnd = random.Random(seed)
    ph = [rnd.random() * math.tau for _ in waves]
    pts = []
    for x in range(0, W + step, step):
        y = base
        for (amp, freq), p in zip(waves, ph):
            y -= amp * math.sin(x / W * math.tau * freq + p)
        pts.append((x, y))
    return pts


def _fill(pts, h, cls):
    d = "M0 %d L" % h + " L".join("%d %.1f" % (x, y) for x, y in pts) + " L%d %d Z" % (W, h)
    return '<path class="%s" d="%s"/>' % (cls, d)


def _y_at(pts, x):
    step = pts[1][0] - pts[0][0]
    i = min(int(x // step), len(pts) - 2)
    (x0, y0), (x1, y1) = pts[i], pts[i + 1]
    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)


def _fir(x, y, h):
    w = h * 0.3
    right = [(0.42, 0.66), (0.2, 0.64), (0.7, 0.36), (0.34, 0.34), (1.0, 0.06), (0.12, 0.06), (0.12, -0.02)]
    pts = [(x, y - h)]
    pts += [(x + w * a, y - h * b) for a, b in right]
    pts += [(x - w * a, y - h * b) for a, b in reversed(right)]
    return "M" + " L".join("%.1f %.1f" % p for p in pts) + "Z"


def layer_far():
    h = 700
    pts = _ridge(11, h, 430, [(70, 1.3), (38, 3.1), (16, 7.3), (6, 15)])
    mist = _ridge(12, h, 520, [(26, 2.1), (12, 5.2), (5, 11)])
    return h, _fill(pts, h, "r1") + _fill(mist, h, "r1b")


def layer_mid():
    h = 560
    pts = _ridge(23, h, 330, [(40, 1.1), (22, 2.6), (8, 6.4), (3, 13)])
    return h, _fill(pts, h, "r2")


def layer_wood():
    h = 460
    rnd = random.Random(37)
    pts = _ridge(31, h, 270, [(34, 0.9), (16, 2.3), (6, 5.1)])
    trees = []
    x = 0.0
    while x < W:
        dense = 0.5 + 0.5 * math.sin(x / W * math.tau * 2.2 + 1.3)
        if rnd.random() < 0.25 + 0.7 * dense:
            th = 16 + rnd.random() * 26 * (0.6 + dense)
            trees.append(_fir(x, _y_at(pts, x) + 4, th))
        x += 7 + rnd.random() * 12
    return h, _fill(pts, h, "r3") + '<path class="r3" d="%s"/>' % " ".join(trees)


def _bezier(p0, p1, p2, p3, t):
    u = 1 - t
    return tuple(u ** 3 * a + 3 * u * u * t * b + 3 * u * t * t * c + t ** 3 * d
                 for a, b, c, d in zip(p0, p1, p2, p3))


def layer_near(runner=True):
    """The meadow in front of the phone: a cart track over the crest, hay bales,
    two big firs at the edges, and the runner's path (#track) for the script."""
    h = 400
    rnd = random.Random(53)
    pts = _ridge(47, h, 190, [(30, 0.8), (14, 1.9), (4, 4.6)])
    out = [_fill(pts, h, "r4")]

    # Track: the centre line rises from the bottom edge to a point on the crest.
    crest_x = 1010
    crest = (crest_x, _y_at(pts, crest_x) + 3)
    p0, p1, p2 = (690, h + 20), (700, h - 120), (1060, crest[1] + 90)
    left, right, centre = [], [], []
    n = 40
    for i in range(n + 1):
        t = i / n
        x, y = _bezier(p0, p1, p2, crest, t)
        half = 70 * (1 - t) ** 1.6 + 1.2
        left.append((x - half, y))
        right.append((x + half, y))
        centre.append((x, y))
    poly = left + list(reversed(right))
    out.append('<path class="tk" d="M%s Z"/>' % " L".join("%.1f %.1f" % p for p in poly))
    # A grass strip down the middle of the two ruts.
    strip = []
    for i in range(n + 1):
        t = i / n
        x, y = _bezier(p0, p1, p2, crest, t)
        half = 18 * (1 - t) ** 1.6 + 0.2
        strip.append((x - half, y, x + half))
    sp = [(a, y) for a, y, _ in strip] + [(b, y) for _, y, b in reversed(strip)]
    out.append('<path class="r4" d="M%s Z"/>' % " L".join("%.1f %.1f" % p for p in sp))
    if runner:
        out.append('<path id="track" fill="none" stroke="none" d="M%s"/>' %
                   " L".join("%.1f %.1f" % p for p in centre))

    # Hay bales on the left slope.
    bales = []
    for bx in (360, 430, 520, 1250, 1330):
        by = _y_at(pts, bx) + 34 + rnd.random() * 22
        r = 13 + rnd.random() * 5
        bales.append('<ellipse cx="%d" cy="%.1f" rx="%.1f" ry="%.1f"/>' % (bx, by, r * 1.25, r))
    out.append('<g class="bale">%s</g>' % "".join(bales))

    # Big firs at the edges, like the app's foreground.
    firs = []
    for fx, fh in ((40, 260), (95, 190), (150, 140), (1470, 210), (1530, 280), (1590, 170)):
        firs.append(_fir(fx, h + 4, fh))
    out.append('<path class="fir" d="%s"/>' % " ".join(firs))

    # The runner: two stride poses, the script swaps them as the page scrolls.
    pose_a = ('<g class="pose pose-a"><circle cx="1.5" cy="-27" r="3.6"/>'
              '<path d="M-1 -12 L1.6 -22 M1.6 -21 L5.5 -16.5 L8 -19.5 M1.6 -21 L-3 -17 L-5.5 -13.5 '
              'M-1 -12 L4.5 -7 L3.5 0 M-1 -12 L-4.5 -6.5 L-9.5 -4.5"/></g>')
    pose_b = ('<g class="pose pose-b"><circle cx="1.5" cy="-27" r="3.6"/>'
              '<path d="M-1 -12 L1.6 -22 M1.6 -21 L-2.5 -16.5 L-5 -14.5 M1.6 -21 L5 -17 L7.5 -20 '
              'M-1 -12 L-3.5 -6.5 L-1.5 0 M-1 -12 L3.5 -7.5 L1 -2.5"/></g>')
    if not runner:
        return h, "".join(out)
    out.append('<g id="runner" class="runner" transform="translate(%.1f %.1f) scale(1.6)">%s%s</g>'
               % (centre[6][0], centre[6][1], pose_a, pose_b))
    return h, "".join(out)


def stars():
    rnd = random.Random(71)
    dots = []
    for _ in range(140):
        x, y = rnd.random() * W, (rnd.random() ** 1.6) * 520
        r = 0.6 + rnd.random() ** 3 * 1.6
        dots.append('<circle cx="%.0f" cy="%.0f" r="%.1f" opacity="%.2f"/>' % (x, y, r, 0.35 + rnd.random() * 0.6))
    return 900, "".join(dots)


def svg(cls, h, body, extra=""):
    return ('<svg class="layer %s" viewBox="0 0 %d %d" preserveAspectRatio="xMidYMax slice" '
            'aria-hidden="true" focusable="false"%s>%s</svg>' % (cls, W, h, extra, body))


def dusk_layers():
    return svg("l1", *layer_far()) + svg("l3", *layer_wood()) + svg("l4", *layer_near(runner=False))


def hero_layers():
    return {
        "stars": svg("stars", *stars()),
        "far": svg("l1", *layer_far()),
        "mid": svg("l2", *layer_mid()),
        "wood": svg("l3", *layer_wood()),
        "near": svg("l4", *layer_near()),
    }


def contours(seed=5, w=1600, h=900, rings=14):
    """Topographic rings for the Flyover band, drawn on with stroke-dashoffset."""
    rnd = random.Random(seed)
    out = []
    for cx, cy, n in ((1180, 330, rings), (330, 690, rings - 4)):
        ph = [rnd.random() * math.tau for _ in range(3)]
        for k in range(1, n + 1):
            r = k * 34
            pts = []
            for i in range(73):
                a = i / 72 * math.tau
                rr = r * (1 + 0.18 * math.sin(3 * a + ph[0]) + 0.09 * math.sin(5 * a + ph[1] + k * 0.15)
                          + 0.05 * math.sin(9 * a + ph[2]))
                pts.append((cx + rr * math.cos(a), cy + rr * 0.72 * math.sin(a)))
            d = "M" + " L".join("%.0f %.0f" % p for p in pts) + "Z"
            out.append('<path pathLength="1" style="--k:%d" d="%s"/>' % (k, d))
    return out
