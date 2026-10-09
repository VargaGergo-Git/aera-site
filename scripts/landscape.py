"""The painted valley behind the homepage hero, generated once into static SVG.

Deterministic: the same seeds always draw the same valley. Four layers, far to
near, each its own <svg> so the page can move them as separate GPU layers.
Colours come from CSS classes (r1..r4, tk, fir, bale) and page variables
(--haze for the atmosphere ramps, see scripts/hero-art.css), so light and dark
mode repaint the same shapes. Gradient and shape ids take a prefix, so the
hero ("h") and the closing dusk band ("d") can share one page.
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


def _y_at(pts, x):
    step = pts[1][0] - pts[0][0]
    i = min(int(x // step), len(pts) - 2)
    (x0, y0), (x1, y1) = pts[i], pts[i + 1]
    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)


def _f(v):
    """Short number: one decimal, trailing zeros dropped."""
    s = "%.1f" % v
    return s[:-2] if s.endswith(".0") else s


def _poly(pts, prec=_f):
    return "M" + " L".join("%s %s" % (prec(x), prec(y)) for x, y in pts) + "Z"


def _fir(x, y, h, w=None, lean=0.0, tiers=3, rnd=None, prec=_f):
    """A fir in 2 or 3 drooping tiers. Returns (outline, shaded right half).

    lean tips the crown sideways as a share of the height; rnd jitters each
    tier's reach so no two trees in a row match."""
    w = w if w is not None else h * 0.3
    sx = lambda b: x + lean * h * b  # the trunk line drifts with the lean
    right = []
    for i in range(tiers):
        b = 1 - (i + 1) / tiers * 0.94
        reach = (i + 1) / tiers * (0.92 + (rnd.random() * 0.16 if rnd else 0.08))
        right.append((reach, b - 0.012))
        if i < tiers - 1:
            right.append((reach * 0.36, b + 0.03))
    right += [(0.11, 0.06), (0.11, -0.02)]
    tip = (sx(1), y - h)
    side = [(sx(b) + w * a, y - h * b) for a, b in right]
    other = [(sx(b) - w * a * (0.94 if rnd else 1), y - h * b) for a, b in reversed(right)]
    outline = _poly([tip] + side + other, prec)
    shade = _poly([tip] + side + [(sx(-0.02), y + h * 0.02)], prec)
    return outline, shade


def _haze_grad(gid, top, bottom, alpha, var="--haze", fade_in=False):
    """A vertical haze ramp in user space: strongest at the ridge's top edge,
    gone by `bottom`. fade_in flips it (clear at the top, solid lower) for
    valley mist. The colour is a page variable so light and dark repaint it."""
    if fade_in:
        stops = ((0, 0), (0.5, alpha * 0.7), (1, alpha))
    else:
        stops = ((0, alpha), (0.42, alpha * 0.38), (1, 0))
    s = "".join('<stop offset="%s" style="stop-color:var(%s,transparent);stop-opacity:%.2f"/>' % (_f(o), var, a)
                for o, a in stops)
    return ('<linearGradient id="%s" gradientUnits="userSpaceOnUse" x1="0" y1="%d" x2="0" y2="%d">%s</linearGradient>'
            % (gid, top, bottom, s))


def _ridge_with_haze(prefix, key, pts, h, cls, alpha, extra_top=0):
    """Solid ridge in its colour class, then the same shape again through a
    haze ramp, so the top edge melts toward the sky and the body stays rich."""
    ys = [y for _, y in pts]
    pid, gid = prefix + key, prefix + key + "h"
    d = "M0 %d L" % h + " L".join("%d %s" % (x, _f(y)) for x, y in pts) + " L%d %d Z" % (W, h)
    defs = _haze_grad(gid, min(ys) - extra_top, max(ys) + 40, alpha)
    body = '<g class="%s"><path id="%s" d="%s"/></g><use href="#%s" fill="url(#%s)"/>' % (cls, pid, d, pid, gid)
    return defs, body, gid


def _birds(spots):
    """Small gull strokes in the sky, drawn in the hero's ink at low weight."""
    out = []
    for x, y, s in spots:
        out.append("M%s %s q%s %s %s %s q%s %s %s %s" % (
            _f(x - 6 * s), _f(y - 1.5 * s), _f(3 * s), _f(-3 * s), _f(6 * s), _f(1.5 * s),
            _f(3 * s), _f(-4.5 * s), _f(6 * s), _f(-1.5 * s)))
    return ('<path class="birds" fill="none" stroke="currentColor" stroke-opacity=".42" stroke-width="1.6" '
            'stroke-linecap="round" stroke-linejoin="round" d="%s"/>' % " ".join(out))


def layer_far(prefix="h"):
    h = 700
    pts = _ridge(11, h, 430, [(70, 1.3), (38, 3.1), (16, 7.3), (6, 15)])
    mist = _ridge(12, h, 520, [(26, 2.1), (12, 5.2), (5, 11)])
    defs, body, _ = _ridge_with_haze(prefix, "a", pts, h, "r1", 0.5)
    # Valley mist: clear at its top, so it rises softly between the ridges.
    mid = prefix + "m"
    defs += _haze_grad(mid, min(y for _, y in mist), max(y for _, y in mist) + 50, 1, var="--r1b", fade_in=True)
    md = "M0 %d L" % h + " L".join("%d %s" % (x, _f(y)) for x, y in mist) + " L%d %d Z" % (W, h)
    body += '<path class="mist" fill="url(#%s)" d="%s"/>' % (mid, md)
    # Two loose flocks where the sky is clear of the copy and the phone.
    body += _birds([(770, 352, 1.0), (792, 338, 0.8), (812, 357, 0.9), (838, 344, 0.7),
                    (1462, 168, 1.1), (1486, 154, 0.8), (1510, 172, 0.9)])
    return h, "<defs>%s</defs>%s" % (defs, body)


def layer_mid(prefix="h"):
    h = 560
    rnd = random.Random(29)
    pts = _ridge(23, h, 330, [(40, 1.1), (22, 2.6), (8, 6.4), (3, 13)])
    defs, body, _ = _ridge_with_haze(prefix, "b", pts, h, "r2", 0.5)
    # A sprinkle of distant firs along the crest, half lost in the haze.
    trees = []
    x = 20.0
    while x < W:
        if rnd.random() < 0.55:
            th = 7 + rnd.random() * 7
            trees.append(_fir(x, _y_at(pts, x) + 3, th, th * 0.32, tiers=2, prec=lambda v: "%.0f" % v)[0])
        x += 9 + rnd.random() * 40
    body += '<path class="r3" fill-opacity=".55" d="%s"/>' % "".join(trees)
    return h, "<defs>%s</defs>%s" % (defs, body)


def layer_wood(prefix="h"):
    h = 460
    rnd = random.Random(37)
    pts = _ridge(31, h, 270, [(34, 0.9), (16, 2.3), (6, 5.1)])
    trees, shades = [], []
    tops = []
    x = 0.0
    p0 = lambda v: "%.0f" % v
    while x < W:
        dense = 0.5 + 0.5 * math.sin(x / W * math.tau * 2.2 + 1.3)
        if rnd.random() < 0.25 + 0.7 * dense:
            th = 16 + rnd.random() * 28 * (0.6 + dense)
            tw = th * (0.24 + rnd.random() * 0.12)
            lean = (rnd.random() - 0.5) * 0.08
            tiers = 3 if th > 26 else 2
            y = _y_at(pts, x) + 4
            o, s = _fir(x, y, th, tw, lean, tiers, rnd, p0)
            trees.append(o)
            shades.append(s)
            tops.append(y - th)
        x += 7 + rnd.random() * 12
    defs, body, gid = _ridge_with_haze(prefix, "c", pts, h, "r3", 0.42, extra_top=0)
    # The haze ramp starts at the tallest tip, so treetops pale into the distance.
    ys = [y for _, y in pts]
    defs = _haze_grad(gid, min(tops), max(ys) + 40, 0.42)
    tid = prefix + "t"
    body = ('<g class="r3 wd"><path id="%s" d="%s"/></g>' % (tid, "".join(trees)) +
            '<path fill="#000" fill-opacity=".14" d="%s"/>' % "".join(shades) +
            body + '<use href="#%s" fill="url(#%s)"/>' % (tid, gid))
    return h, "<defs>%s</defs>%s" % (defs, body)


def _bezier(p0, p1, p2, p3, t):
    u = 1 - t
    return tuple(u ** 3 * a + 3 * u * u * t * b + 3 * u * t * t * c + t ** 3 * d
                 for a, b, c, d in zip(p0, p1, p2, p3))


def _bale(x, gy, r):
    """A round bale lying on the meadow: soft contact shadow cast away from the
    sun, the rolled body behind, and the lit end face with its spiral."""
    L = r * 0.75
    sh = ('<ellipse class="bale-sh" fill="#3a2c12" fill-opacity=".2" cx="%s" cy="%s" rx="%s" ry="%s"/>'
          % (_f(x - r * 0.9), _f(gy - r * 0.06), _f(r * 2.1), _f(r * 0.34)))
    body = ('<path class="bale-b" d="M%s %sH%sA%s %s 0 0 0 %s %sH%sZ"/>'
            % (_f(x), _f(gy - 2 * r), _f(x - L), _f(r * 0.5), _f(r), _f(x - L), _f(gy), _f(x)))
    face = '<ellipse class="bale-f" cx="%s" cy="%s" rx="%s" ry="%s"/>' % (_f(x), _f(gy - r), _f(r * 0.8), _f(r))
    rings = ('<path class="bale-r" fill="none" stroke="#7a5a1c" stroke-opacity=".32" stroke-width="%s" d="'
             'M%s %sa%s %s 0 1 0 %s 0a%s %s 0 1 0 %s 0M%s %sa%s %s 0 1 0 %s 0a%s %s 0 1 0 %s 0"/>'
             % (_f(max(1.0, r * 0.08)),
                _f(x - r * 0.52), _f(gy - r), _f(r * 0.52), _f(r * 0.66), _f(r * 1.04), _f(r * 0.52), _f(r * 0.66), _f(-r * 1.04),
                _f(x - r * 0.24), _f(gy - r), _f(r * 0.24), _f(r * 0.3), _f(r * 0.48), _f(r * 0.24), _f(r * 0.3), _f(-r * 0.48)))
    return sh + body + face + rings


DEER_STAND = ("M-6 -8C-6 -11 -2 -11.6 3 -11.2C6 -11 7.6 -10.2 7.6 -8.6L7.2 -7L7.4 0H6.4L6 -6.4L5.2 -6.6L4.9 0H4L3.8 -7"
              "L-3.4 -7.2L-3.8 0H-4.7L-4.9 -6.8L-5.5 -7L-5.6 0H-6.5L-6.7 -8.2L-7.6 -11.4L-8.4 -15L-10 -15.3L-10.6 -16.5"
              "L-9.4 -17.4L-9.2 -19.4L-8.5 -17.5L-7.8 -19.6L-7.6 -17.3L-6.6 -16.6L-6.7 -14.2L-5.4 -10.4Z")
DEER_GRAZE = ("M-6 -8C-6 -11 -2 -11.6 3 -11.2C6 -11 7.6 -10.2 7.6 -8.6L7.2 -7L7.4 0H6.4L6 -6.4L5.2 -6.6L4.9 0H4L3.8 -7"
              "L-3.4 -7.2L-3.8 0H-4.7L-4.9 -6.8L-5.5 -7L-5.6 0H-6.5L-6.7 -7.8L-8.6 -4L-10.6 -1.6L-10.2 -0.6L-8.4 -1.4"
              "L-7.6 -3L-5.2 -9.6Z")


def _runner_pose(cls, near_leg, far_leg, near_arm, far_arm, head, hip, sh):
    """One stride pose in profile. The far-side limbs take a softer tone
    (class "far") so the figure reads as a body, not a stick figure."""
    K = 2.4
    pl = lambda pts: "M" + " L".join("%s %s" % (_f(px * K), _f(py * K)) for px, py in pts)
    return ('<g class="pose %s">'
            '<path class="far" stroke-width="4.2" d="%s"/>'
            '<path class="far" stroke-width="3.4" d="%s"/>'
            '<path stroke-width="6.6" d="%s"/>'
            '<circle cx="%s" cy="%s" r="%s"/>'
            '<path stroke-width="4.6" d="%s"/>'
            '<path stroke-width="3.6" d="%s"/></g>'
            % (cls, pl(far_leg), pl(far_arm), pl([hip, sh, (sh[0] + 0.7, sh[1] - 1.8)]),
               _f(head[0] * K), _f(head[1] * K), _f(2.55 * K), pl(near_leg), pl(near_arm)))


def runner_poses():
    hip, sh, head = (0, -14.4), (2.7, -23.4), (4.1, -27.1)
    pose_a = _runner_pose("pose-a",  # flight: long reach forward, push-off leg trailing
                          near_leg=[hip, (5.2, -9.4), (7.6, -2.8), (9.2, -2.9)],
                          far_leg=[hip, (-2.2, -7.6), (-7.8, -4.4), (-8.9, -5.2)],
                          near_arm=[sh, (-1.2, -19.8), (0.4, -16.6)],
                          far_arm=[sh, (5.6, -20.4), (7.6, -23.2)],
                          head=head, hip=hip, sh=sh)
    pose_b = _runner_pose("pose-b",  # passing: weight over the foot, recovery leg folded
                          near_leg=[hip, (1.9, -7.6), (0.3, -0.5), (2.5, -0.3)],
                          far_leg=[hip, (4.6, -10.2), (0.0, -8.4), (-0.6, -7.0)],
                          near_arm=[sh, (5.2, -20.0), (7.4, -22.4)],
                          far_arm=[sh, (-0.8, -19.8), (0.6, -16.8)],
                          head=head, hip=hip, sh=sh)
    return pose_a, pose_b


def layer_near(runner=True, prefix="h"):
    """The meadow in front of the phone: a cart track over the crest, round
    bales with their shadows, two deer, big firs at the edges, and the runner's
    path (#track) for the script."""
    h = 400
    rnd = random.Random(53)
    pts = _ridge(47, h, 190, [(30, 0.8), (14, 1.9), (4, 4.6)])
    defs, ridge, _ = _ridge_with_haze(prefix, "d", pts, h, "r4", 0.34)
    out = [ridge]

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

    # Deer grazing mid-meadow, left of the track, small with distance.
    deer = []
    for dx, dd, s, flip, shape in ((842, 12, 0.95, 1, DEER_GRAZE), (874, 15, 1.05, -1, DEER_STAND)):
        deer.append('<path transform="translate(%s %s) scale(%s %s)" d="%s"/>'
                    % (dx, _f(_y_at(pts, dx) + dd), _f(s * flip), _f(s), shape))
    out.append('<g class="deer" fill="#4d3b2a" fill-opacity=".85">%s</g>' % "".join(deer))

    # Round bales sit on the ground: bigger the nearer (lower) they lie.
    bales = []
    for bx, depth in ((300, 34), (452, 18), (566, 46), (1186, 24), (1312, 50), (1438, 24)):
        gy = _y_at(pts, bx) + depth
        r = 8 + depth * 0.2 + rnd.random() * 2.5
        bales.append((gy, _bale(bx, gy, r)))
    bales.sort()
    out.append('<g class="bale">%s</g>' % "".join(b for _, b in bales))

    # Big firs at the edges, like the app's foreground, each its own shape.
    firs, shades = [], []
    frnd = random.Random(61)
    for fx, fh in ((-6, 230), (40, 268), (96, 186), (148, 132), (1452, 196), (1512, 284), (1566, 222), (1612, 150)):
        o, s = _fir(fx, h + 4, fh, fh * (0.26 + frnd.random() * 0.08), (frnd.random() - 0.5) * 0.05, 3, frnd)
        firs.append(o)
        shades.append(s)
    out.append('<path class="fir" d="%s"/>' % "".join(firs))
    out.append('<path fill="#000" fill-opacity=".2" d="%s"/>' % "".join(shades))

    if not runner:
        return h, "<defs>%s</defs>%s" % (defs, "".join(out))
    # The runner: two stride poses, the script swaps them as the page scrolls.
    pose_a, pose_b = runner_poses()
    shadow = '<ellipse fill="#000" fill-opacity=".16" stroke="none" cx="1" cy="1" rx="15" ry="3"/>'
    out.append('<g id="runner" class="runner" transform="translate(%.1f %.1f) scale(1.6)">%s%s%s</g>'
               % (centre[6][0], centre[6][1], shadow, pose_a, pose_b))
    return h, "<defs>%s</defs>%s" % (defs, "".join(out))


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


def dusk_stars():
    rnd = random.Random(83)
    dots = "".join('<circle cx="%.0f" cy="%.0f" r="%.1f" style="--s:%.2f"/>' % (rnd.random() * W, rnd.random() ** 1.4 * 260,
                   0.7 + rnd.random() ** 3 * 1.4, rnd.random()) for _ in range(46))
    return '<svg class="dusk-stars" viewBox="0 0 %d 400" preserveAspectRatio="xMidYMin slice" aria-hidden="true">%s</svg>' % (W, dots)


def dusk_layers():
    return (svg("l1", *layer_far("d")) + svg("l3", *layer_wood("d"))
            + svg("l4", *layer_near(runner=False, prefix="d")))


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
