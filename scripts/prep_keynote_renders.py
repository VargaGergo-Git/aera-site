"""Cut the Press renders in /mnt/project-files into the home page's img/k/,
and into img/k/<lang>/ wherever a -de or -hu capture exists.

    python3 scripts/prep_keynote_renders.py

Share cards sit on a blurred frame of a real replay, so a sticker or an ink
tile has ground under it. The place replays in media/k/ are cut separately
at the end of this script: 9 s at 480 px, no audio, cut where the route runs over
land, since a replay that opens on open water reads as nothing."""
import os, subprocess, sys, tempfile
import numpy as np
from PIL import Image, ImageFilter
P = '/mnt/project-files/'
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'img/k/')
S = tempfile.mkdtemp()
for clip, t in (('braies', 4), ('braies', 20), ('seawall', 12), ('bled', 21)):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(t), '-i', P + 'press-replay-%s.mp4' % clip,
                    '-frames:v', '1', os.path.join(S, 'bg-%s-%d.png' % (clip, t))], check=True)

def save(im, name, widths, lang=None):
    d = OUT + (lang + '/' if lang else '')
    os.makedirs(d, exist_ok=True)
    for w in widths:
        h = round(im.height * w / im.width)
        im.resize((w, h), Image.LANCZOS).save(d + '%s-%d.webp' % (name, w), quality=86, method=6)

def src(base, lang):
    if lang is None: return P + base
    root, ext = os.path.splitext(base)
    f = P + root + '-' + lang + ext
    return f if os.path.exists(f) else None

def key_pb(path):
    p = np.array(Image.open(path).convert('RGB')).astype(float)
    x0, y0, x1, y1 = 100, 495, 1105, 2283
    c = p[y0:y1, x0:x1]
    lum = c @ np.array([.3, .59, .11]); sat = c.max(2) - c.min(2)
    a = np.clip((lum - 58) / 50, 0, 1); a = np.maximum(a, (sat > 22).astype(float))[..., None]
    bg = Image.open(os.path.join(S, 'bg-braies-4.png')).convert('RGB')
    bw = 590; bx = (bg.width - bw) // 2
    bg = bg.crop((bx, 200, bx + bw, 200 + round(bw * (y1 - y0) / (x1 - x0)))).resize((x1 - x0, y1 - y0), Image.LANCZOS).filter(ImageFilter.GaussianBlur(40))
    g = np.linspace(0, 1, y1 - y0)[:, None, None]
    nb = np.array(bg).astype(float) * (.78 - .3 * g)
    return Image.fromarray(np.clip(a * c + (1 - a) * nb, 0, 255).astype(np.uint8))

def week(path):
    w = np.array(Image.open(path).convert('RGB'))
    for y in range(225, 325): w[y, 1060:1180] = w[y, 1000]
    c = w[186:2180]
    pad = np.zeros((round(c.shape[1] * 16 / 9) - c.shape[0], c.shape[1], 3), np.uint8) + c[-1:].astype(np.uint8)
    return Image.fromarray(np.vstack([c, pad]))

def clock(path):
    c = np.array(Image.open(path).convert('RGB'))
    cc = c[485:2234, 110:1095].copy()
    cc[2190 - 485:2245 - 485, 500 - 110:700 - 110] = c[2150, 600]
    return Image.fromarray(cc)

# The -de/-hu share-week/pb/clock captures still carry English text; add a language
# here once its translated captures land, so no page mixes languages.
SHARE_READY = set()

PHONES = {'scr-age-light': 'press-phone-light-longevity.png', 'scr-age-dark': 'press-phone-dark-longevity.png',
          'scr-sleep-light': 'press-phone-light-sleep-stages.png', 'scr-sleep-dark': 'press-phone-dark-sleep-stages.png',
          'scr-loops': 'press-phone-dark-loops-from-here.png', 'scr-loop-route': 'press-phone-dark-loop-route.png'}
for lang in (None, 'de', 'hu'):
    for name, f in PHONES.items():
        s = src(f, lang)
        if s: save(Image.open(s).convert('RGB'), name, (400, 800), lang)
    BG = {'splits': 'bg-seawall-12', 'zones': 'bg-bled-21'}
    for t in BG:
        s = src('press-tile-%s-light-ink.png' % t, lang)
        if not s: continue
        bg = Image.open(os.path.join(S, BG[t] + '.png')).convert('RGB')
        bw = 590; x0 = (bg.width - bw) // 2; bg = bg.crop((x0, 200, x0 + bw, 200 + round(bw * 16 / 9))).resize((1080, 1920), Image.LANCZOS).filter(ImageFilter.GaussianBlur(48))
        g = np.linspace(0, 1, 1920)[:, None, None] ** 1.6
        bga = np.array(bg).astype(float) * (1 - .55 * g) * .72
        card = Image.fromarray(bga.clip(0, 255).astype(np.uint8)).convert('RGBA')
        card.alpha_composite(Image.open(s).convert('RGBA'))
        save(card.convert('RGB'), 'card-' + t, (360, 720), lang)
    for name, f in (('w-page-run', 'press-watch-page-run.png'), ('w-now', 'press-watch-nav-now.png')):
        s = src(f, lang)
        if s: save(Image.open(s).convert('RGB'), name, (422,), lang)
    for name, f, fn in (('card-week', 'share-week.png', week), ('card-pb', 'share-pb.png', key_pb), ('card-clock', 'share-clock.png', clock)):
        s = src(f, lang) if lang is None or lang in SHARE_READY else None
        if s: save(fn(s), name, (360, 720), lang)
print('ok')

# Replay clips for the place player, per language wherever a capture exists.
# (source, start second, poster second): each start sits where the route crosses land.
MEDIA = os.path.join(os.path.dirname(OUT.rstrip('/')), '..', 'media/k/')
CLIPS = {'seawall': ('press-replay-seawall.mp4', 2.5, 3), 'braies': ('press-replay-braies.mp4', 0.3, 4),
         'greenlake': ('press-clip-replay-orbit-dark.mp4', 11, 1)}
for lang in (None, 'de', 'hu'):
    for name, (f, t0, tp) in CLIPS.items():
        s_ = src(f, lang)
        if not s_: continue
        d = os.path.normpath(MEDIA) + '/' + (lang + '/' if lang else '')
        os.makedirs(d, exist_ok=True)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(t0), '-t', '9', '-i', s_, '-an', '-vf', 'scale=480:-2,fps=30',
                        '-c:v', 'libx264', '-crf', '27', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
                        d + 'place-%s.mp4' % name], check=True)
        dp = OUT + (lang + '/' if lang else '')
        os.makedirs(dp, exist_ok=True)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(tp), '-i', d + 'place-%s.mp4' % name, '-frames:v', '1',
                        '-c:v', 'libwebp', '-quality', '82', dp + 'place-%s-480.webp' % name], check=True)
