/* Flyover scene: scroll flies a camera over the contour model. The route draws
   with the runner on its head, the camera follows it, eases to a stop at the
   fastest split and at the top of the climb, then pulls back up and away while
   the real capture rises in. Only transforms and opacity change per frame.
   Without .motion the CSS defaults are the finished frame; this file then only
   pins the runner and the two callouts to it. On any error it steps aside. */
(function () {
  var sec = document.getElementById('flyover');
  if (!sec) return;
  var root = document.documentElement;
  var stage, pin, cam, world, puck, copy, chips, layers, nums, routeEl;
  var PX = [], PY = [], HD = [], Z, E, PACE, HR, pS, pC, NS = 300;
  var cfg = {}, alive = true, ticking = false, mode = '', copyIn = false, saved = [];

  function clamp(v) { return v < 0 ? 0 : v > 1 ? 1 : v; }
  function ss(a, b, x) { x = clamp((x - a) / (b - a)); return x * x * (3 - 2 * x); }
  function lerp(a, b, k) { return a + (b - a) * k; }
  function bump(a, m, b, x) { return x < m ? ss(a, m, x) : 1 - ss(m, b, x); }
  function sample(arr, p) {
    var f = clamp(p) * (arr.length - 1), i = Math.floor(f), k = f - i;
    return i >= arr.length - 1 ? arr[arr.length - 1] : arr[i] + (arr[i + 1] - arr[i]) * k;
  }
  function list(name) { return (sec.getAttribute('data-' + name) || '0').split(',').map(Number); }
  function num(cs, name, fallback) { var v = parseFloat(cs.getPropertyValue(name)); return isNaN(v) ? fallback : v; }
  function mmss(s) { s = Math.round(s); var m = Math.floor(s / 60), r = s % 60; return m + ':' + (r < 10 ? '0' : '') + r; }
  function put(el, name, v) { el.style.setProperty(name, v); }

  function setup() {
    stage = sec.querySelector('.fo-stage');
    pin = sec.querySelector('.fo-pin');
    cam = sec.querySelector('.fo-cam');
    world = sec.querySelector('.fo-world');
    puck = sec.querySelector('.fo-puck');
    copy = sec.querySelector('.fo-copy');
    routeEl = document.getElementById('flyover-r');
    chips = [].slice.call(sec.querySelectorAll('.fo-chip'));
    layers = [].slice.call(sec.querySelectorAll('.fo-l[data-r]')).map(function (el) {
      var r = el.getAttribute('data-r').split(' ').map(Number);
      return { el: el, lo: r[0], hi: r[1], d: -1 };
    });
    nums = {};
    [].slice.call(sec.querySelectorAll('.fo-hud b[data-k]')).forEach(function (b) {
      nums[b.getAttribute('data-k')] = { el: b, v: b.textContent };
    });
    Z = list('z'); E = list('e'); PACE = list('pace'); HR = list('hr');
    pS = Number(sec.getAttribute('data-ps')) || 0.25;
    pC = Number(sec.getAttribute('data-pc')) || 0.7;

    var len = routeEl.getTotalLength(), ang = [], i, j;
    for (i = 0; i <= NS; i++) {
      var q = routeEl.getPointAtLength(len * i / NS);
      PX.push(q.x); PY.push(q.y);
    }
    for (i = 0; i < NS; i++) ang.push(Math.atan2(PY[i + 1] - PY[i], PX[i + 1] - PX[i]));
    ang.push(ang[NS - 1]);
    for (i = 1; i <= NS; i++) {            // unwrap
      while (ang[i] - ang[i - 1] > Math.PI) ang[i] -= 2 * Math.PI;
      while (ang[i] - ang[i - 1] < -Math.PI) ang[i] += 2 * Math.PI;
    }
    var sig = 26, w = [];                    // wide kernel: switchbacks average out
    for (j = -3 * sig; j <= 3 * sig; j++) w.push(Math.exp(-j * j / (2 * sig * sig)));
    for (i = 0; i <= NS; i++) {
      var s = 0, ws = 0;
      for (j = -3 * sig; j <= 3 * sig; j++) {
        var k = Math.min(NS, Math.max(0, i + j)), wt = w[j + 3 * sig];
        s += ang[k] * wt; ws += wt;
      }
      HD.push(-90 - (s / ws) * 180 / Math.PI);
    }
    [world, puck, stage].concat(chips, layers.map(function (l) { return l.el; })).forEach(function (el) {
      saved.push([el, el.getAttribute('style')]);
    });
  }

  function readConfig() {
    var cs = getComputedStyle(world), cs2 = getComputedStyle(sec), cc = getComputedStyle(cam);
    cfg.W = world.offsetWidth;
    cfg.u = cfg.W / 1000;
    cfg.dz = cfg.W * num(cs2, '--dzk', 0.018);
    cfg.oZm = num(cs2, '--o-zm', 0.86);
    cfg.fZm = num(cs2, '--f-zm', 1.8);
    cfg.fCy = num(cs2, '--f-cy', 0.15);
    cfg.eTilt = num(cs, '--e-tilt', 52);
    cfg.eHd = num(cs, '--e-hd', -18);
    cfg.eZm = num(cs, '--e-zm', 0.86);
    cfg.eFx = num(cs, '--e-fx', 520);
    cfg.eFy = num(cs, '--e-fy', 540);
    cfg.eCx = num(cs, '--e-cx', 0);
    cfg.eCy = num(cs, '--e-cy', 0.1);
    cfg.endChips = num(cs2, '--end-chips', 1);
    cfg.eCyPx = cfg.eCy * cfg.W;
    if (cfg.vw < 900 && copy.offsetHeight) {
      // Phones: fit the finished model into the space the copy leaves free.
      var below = copy.offsetTop + copy.offsetHeight, free = cfg.vh - below;
      var k = Math.min(1.2, Math.max(0.7, free / 454));
      cfg.eZm *= k;
      cfg.eCyPx = below + free * 0.6 - cfg.vh / 2;
      if (free < 400) cfg.endChips = 0;
    }
    cfg.eHdU = cfg.eHd + 360 * Math.round((HD[NS] - cfg.eHd) / 360);
    cfg.d = parseFloat(cc.perspective) || 1500;
    var po = cc.perspectiveOrigin.split(' ');
    cfg.vw = cam.clientWidth;
    cfg.vh = cam.clientHeight;
    cfg.pox = parseFloat(po[0]); if (isNaN(cfg.pox)) cfg.pox = cfg.vw / 2;
    cfg.poy = parseFloat(po[1]); if (isNaN(cfg.poy)) cfg.poy = cfg.vh / 2;
  }

  // Route progress: eases into a full stop at the split and at the summit.
  var K = null;
  function progress(t) {
    if (!K) K = [[0.08, 0], [0.24, pS], [0.31, pS], [0.58, pC], [0.66, pC], [0.79, 1]];
    if (t <= K[0][0]) return 0;
    for (var i = 1; i < K.length; i++) {
      if (t <= K[i][0]) return lerp(K[i - 1][1], K[i][1], ss(K[i - 1][0], K[i][0], t));
    }
    return 1;
  }

  // The camera for a moment t of the flight. pose(1) equals the CSS defaults.
  function pose(t) {
    var p = progress(t), pl = progress(t - 0.014);
    var dive = ss(0.02, 0.2, t), away = ss(0.74, 0.95, t);
    var atTop = bump(0.55, 0.62, 0.7, t), atSplit = bump(0.21, 0.275, 0.34, t);
    var hx = sample(PX, pl), hy = sample(PY, pl), hz = sample(Z, pl);
    var hd = lerp(HD[0] + 46 * (1 - ss(0, 0.2, t)), sample(HD, pl), dive);
    return {
      p: p,
      fx: lerp(lerp(515, hx, dive), cfg.eFx, away),
      fy: lerp(lerp(560, hy, dive), cfg.eFy, away),
      fz: lerp(hz * dive, 0, away),
      hd: lerp(hd, cfg.eHdU, away),
      zm: lerp(lerp(cfg.oZm, cfg.fZm, dive), cfg.eZm, away) * (1 - 0.2 * atTop) * (1 + 0.06 * atSplit),
      tilt: lerp(lerp(48, 62, dive) - 9 * atTop - 12 * ss(0.6, 0.7, t), cfg.eTilt, away),
      cx: cfg.eCx * cfg.W * away,
      cy: lerp((lerp(0.06, cfg.fCy, dive) - 0.1 * atTop) * cfg.vh, cfg.eCyPx, away)
    };
  }

  // Where a point of the model lands on the stage, the same chain the CSS uses.
  function project(c, xw, yw, lv) {
    var x = (xw - 500) * cfg.u + (500 - c.fx) * cfg.u;
    var y = (yw - 500) * cfg.u + (500 - c.fy) * cfg.u;
    var z = lv * cfg.dz - c.fz * cfg.dz;
    x *= c.zm; y *= c.zm; z *= c.zm;
    var a = c.hd * Math.PI / 180, ca = Math.cos(a), sa = Math.sin(a);
    var x1 = x * ca - y * sa, y1 = x * sa + y * ca;
    var b = c.tilt * Math.PI / 180, cb = Math.cos(b), sb = Math.sin(b);
    var y2 = y1 * cb - z * sb, z2 = y1 * sb + z * cb;
    var X = cfg.vw / 2 + x1 + c.cx, Y = cfg.vh / 2 + y2 + c.cy;
    var s = cfg.d / Math.max(cfg.d - z2, 1);
    return [cfg.pox + (X - cfg.pox) * s, cfg.poy + (Y - cfg.poy) * s];
  }

  function pinTo(el, c, xw, yw, lv) {
    var q = project(c, xw, yw, lv);
    put(el, '--sx', q[0].toFixed(1) + 'px');
    put(el, '--sy', q[1].toFixed(1) + 'px');
  }

  function pins(c, p) {
    pinTo(puck, c, sample(PX, p), sample(PY, p), sample(Z, p));
    pinTo(chips[0], c, sample(PX, pS), sample(PY, pS), sample(Z, pS));
    pinTo(chips[1], c, sample(PX, pC), sample(PY, pC), sample(Z, pC));
  }

  function applyWorld(c) {
    put(world, '--tilt', c.tilt.toFixed(2) + 'deg');
    put(world, '--hd', c.hd.toFixed(2) + 'deg');
    put(world, '--zm', c.zm.toFixed(4));
    put(world, '--px', ((500 - c.fx) * cfg.u).toFixed(1) + 'px');
    put(world, '--py', ((500 - c.fy) * cfg.u).toFixed(1) + 'px');
    put(world, '--pz', (-c.fz * cfg.dz).toFixed(1) + 'px');
    put(world, '--cx', c.cx.toFixed(1) + 'px');
    put(world, '--cy', c.cy.toFixed(1) + 'px');
  }

  function render(t) {
    var c = pose(t), p = c.p;
    applyWorld(c);
    pins(c, p);

    layers.forEach(function (l) {
      var d = 1 - Math.min(l.hi, Math.max(l.lo, p));
      if (Math.abs(d - l.d) > 0.0002) { l.d = d; put(l.el, '--d', d.toFixed(4)); }
    });

    var end1 = ss(0.86, 0.93, t) * cfg.endChips, end2 = ss(0.88, 0.95, t);
    put(chips[0], '--a', Math.max(ss(0.19, 0.235, t) * (1 - ss(0.35, 0.4, t)), end1).toFixed(3));
    put(chips[1], '--a', Math.max(ss(0.53, 0.575, t) * (1 - ss(0.69, 0.74, t)), end2).toFixed(3));

    put(puck, '--pa', (1 - ss(0.8, 0.88, t)).toFixed(3));
    put(stage, '--hud', (ss(0.015, 0.07, t) * (1 - ss(0.72, 0.78, t))).toFixed(3));
    put(stage, '--p', p.toFixed(4));
    put(stage, '--ct', Math.max(1 - ss(0.05, 0.13, t), ss(0.76, 0.88, t)).toFixed(3));
    put(stage, '--cp', ss(0.79, 0.91, t).toFixed(3));
    put(stage, '--pr', ss(0.78, 0.97, t).toFixed(4));
    var want = t < 0.09 || t > 0.75;
    if (want !== copyIn) { copyIn = want; copy.classList.toggle('in', want); }

    text('e', String(Math.round(sample(E, p))));
    text('pace', mmss(sample(PACE, p)));
    text('hr', String(Math.round(sample(HR, p))));
  }

  function text(k, v) {
    var n = nums[k];
    if (n && n.v !== v) { n.v = v; n.el.textContent = v; }
  }

  function reset() {
    saved.forEach(function (it) {
      if (it[1] === null) it[0].removeAttribute('style'); else it[0].setAttribute('style', it[1]);
    });
    layers.forEach(function (l) { l.d = -1; });
    copy.classList.add('in');
    copyIn = true;
  }

  function frame() {
    ticking = false;
    if (!alive) return;
    try {
      var moving = root.classList.contains('motion');
      if (!moving) {
        // The finished frame: only the runner and the callouts need placing.
        if (mode !== 'still') {
          reset(); mode = 'still'; readConfig();
          var c = pose(1); applyWorld(c); pins(c, 1);
          if (!cfg.endChips) put(chips[0], 'display', 'none');
        }
        return;
      }
      var r = pin.getBoundingClientRect(), vh = window.innerHeight;
      if (r.bottom < -200 || r.top > vh + 200) return;
      if (mode !== 'fly') { mode = 'fly'; readConfig(); copyIn = false; copy.classList.remove('in'); }
      var span = r.height - vh;
      render(span > 0 ? clamp(-r.top / span) : 1);
    } catch (e) {
      alive = false;
      try { reset(); sec.classList.remove('fo-js'); } catch (e2) { /* the static frame stays */ }
    }
  }
  function request() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(frame);
    setTimeout(function () { if (ticking) frame(); }, 250);
  }

  try {
    setup();
    sec.classList.add('fo-js');
    window.addEventListener('scroll', request, { passive: true });
    window.addEventListener('resize', function () { mode = ''; request(); }, { passive: true });
    window.addEventListener('load', function () { mode = ''; request(); });
    request();
  } catch (e) {
    alive = false;
  }
})();
