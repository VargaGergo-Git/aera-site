(function () {
  try {
    var sec = document.getElementById('planner');
    if (!sec) return;
    var root = document.documentElement;
    var stage = sec.querySelector('.pl-stage');
    var head = sec.querySelector('.pl-head');
    var caps = sec.querySelector('.pl-caps');
    var route = sec.querySelector('#planner-route');
    var glow = sec.querySelector('.pl-glow');
    var casing = sec.querySelector('.pl-case');
    var dot = sec.querySelector('#planner-head');
    var finger = sec.querySelector('#planner-finger');
    var taps = [].slice.call(sec.querySelectorAll('.pl-tap'));
    var num = sec.querySelector('.pl-num');
    var wdist = sec.querySelector('.pl-wd-num');
    var km = parseFloat(num && num.getAttribute('data-km')) || 6.4;
    var comma = num && num.textContent.indexOf(',') > -1;
    var len = route.getTotalLength();
    // The line's points, sampled once: the film never asks the SVG for geometry mid-frame.
    var PTS = [], NP = 400;
    for (var j = 0; j <= NP; j++) { var q = route.getPointAtLength(len * j / NP); PTS.push([q.x, q.y]); }
    function pointAt(t) {
      var x = t * NP, i0 = Math.min(NP - 1, Math.floor(x)), f0 = x - i0, a0 = PTS[i0], b0 = PTS[i0 + 1];
      return { x: a0[0] + (b0[0] - a0[0]) * f0, y: a0[1] + (b0[1] - a0[1]) * f0 };
    }
    function attr(el, k, v) { var c = el.__pa || (el.__pa = {}); if (c[k] === v) return; c[k] = v; el.setAttribute(k, v); }
    // Where along the line (0..1) each tap lands: start, bridge, park edge, summit.
    var TAP_AT = [0, 0, 0, 0];
    var TAPS_XY = [[505, 588], [262, 398], [190, 256], [452, 104]];
    (function () {
      var best = [1e9, 1e9, 1e9, 1e9];
      for (var i = 0; i <= NP; i++) {
        var pt = PTS[i];
        for (var k = 0; k < 4; k++) {
          var d = Math.hypot(pt[0] - TAPS_XY[k][0], pt[1] - TAPS_XY[k][1]);
          if (d < best[k]) { best[k] = d; TAP_AT[k] = i / NP; }
        }
      }
    })();
    var plane = sec.querySelector('.pl-plane'), wrap = sec.querySelector('.pl-map-wrap'), halo = sec.querySelector('.pl-halo');
    var hud = sec.querySelector('.pl-hud'), watch = sec.querySelector('.pl-watch'), phoneEl = sec.querySelector('.pl-phone');
    var pins = [].slice.call(sec.querySelectorAll('.pl-pin')).map(function (el) {
      return { el: el, inn: el.querySelector('.pl-pin-in'), stem: el.querySelector('.pl-stem'), foot: el.querySelector('.pl-foot') };
    });
    var step = 0, measured = false, last = -1;
    // Knobs the stylesheet sets per layout, read once per measure.
    var K = { rz: -8, ts: .14, as: .5, pd: 14, ay: 40 };
    // The film writes final transform and opacity straight onto each moving element,
    // so a frame restyles a handful of nodes, never the whole map underneath.
    var touched = [];
    function put(el, prop, v) {
      var c = el.__pl || (el.__pl = {});
      if (c[prop] === v) return;
      if (!(prop in c)) touched.push([el, prop]);
      c[prop] = v; el.style.setProperty(prop, v);
    }
    function n(v) { return v.toFixed(4); }
    var BOUNCE = (getComputedStyle(root).getPropertyValue('--bounce') || '').trim() || 'cubic-bezier(.34, 1.56, .64, 1)';

    function c01(v) { return v < 0 ? 0 : v > 1 ? 1 : v; }
    function seg(p, a, b) { return c01((p - a) / (b - a)); }
    function ease(t) { return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; }
    function out(t) { return 1 - Math.pow(1 - t, 3); }
    function back(t) { var c = 1.6; return t <= 0 ? 0 : t >= 1 ? 1 : 1 + (c + 1) * Math.pow(t - 1, 3) + c * Math.pow(t - 1, 2); }
    var cache = {};
    function set(k, v) { v = typeof v === 'number' ? v.toFixed(4) : v; if (cache[k] === v) return; cache[k] = v; sec.style.setProperty(k, v); }

    function measure() {
      var vw = window.innerWidth, vh = window.innerHeight, phone = vw < 900, wide = vw >= 1100;
      var top, h, ww;
      if (wide) {
        // Words on the left: the headline block and the caption sit centred as a pair.
        var hh = head.offsetHeight, ch = caps.offsetHeight;
        var ht = Math.max(84, (vh - hh - ch - 28) / 2);
        set('--head-top', ht + 'px');
        set('--caps-top', (ht + hh + 28) + 'px');
        top = 78; h = vh - top - 34;
        ww = sec.querySelector('.pl-world').offsetWidth || (vw * .6);
      } else {
        var hb = head.offsetTop + head.offsetHeight;
        top = hb + (phone ? 14 : 22);
        var bottom = vh - caps.offsetHeight - Math.max(22, vh * .032) - (phone ? 12 : 20);
        h = Math.max(220, bottom - top);
        ww = vw;
      }
      set('--world-top', top + 'px');
      set('--world-h', h + 'px');
      // Map: as big as the room allows; tilted, it reads wider than it is.
      var mw = Math.min(ww - (phone ? 24 : 60), wide ? 720 : 620, h * .9 * 600 / 640);
      set('--map-px', Math.max(220, mw) + 'px');
      // Watch: tall enough to read the turn from across the room.
      var wpx = Math.min(phone ? vw * .58 : 300, h / (1.19 * 1.42));
      set('--watch-px', Math.max(130, wpx) + 'px');
      set('--away-y', (h * .06) + 'px');
      var cs = getComputedStyle(sec);
      function knob(k, d) { var v = parseFloat(cs.getPropertyValue(k)); return isNaN(v) ? d : v; }
      K = { rz: knob('--rz', -8), ts: knob('--tilt-s', .14), as: knob('--away-s', .5), pd: knob('--pan-d', 14), ay: h * .06 };
      measured = true;
    }
    function clear() {
      ['--in', '--draw', '--tilt', '--pan', '--map-o', '--pin-o', '--p1', '--p2', '--p3', '--hud', '--away', '--wrist', '--ph', '--world-top', '--world-h', '--map-px', '--watch-px', '--away-y', '--head-top', '--caps-top'].forEach(function (k) { sec.style.removeProperty(k); });
      sec.removeAttribute('data-step');
      touched.forEach(function (t) { t[0].style.removeProperty(t[1]); delete t[0].__pl; });
      touched = [];
      step = 0; measured = false; last = -1; cache = {};
    }
    function fmt(v) { var s = v.toFixed(1); return comma ? s.replace('.', ',') : s; }

    function update() {

      if (!root.classList.contains('motion')) { if (step) clear(); return; }
      if (!measured) measure();
      var p = film;
      if (Math.abs(p - last) < .0004 && step) return;
      last = p;

      // Beat 1: draw (0 to .36)
      var vin = out(seg(p, 0, .1)), vhud = out(seg(p, .06, .12));
      var d = seg(p, .1, .34);
      var drawn = ease(d);
      // The finger hops tap to tap; the line follows to the next tap.
      var hop = drawn * 3, k = Math.min(2, Math.floor(hop)), f = hop - k;
      var at = TAP_AT[k] + (TAP_AT[k + 1] - TAP_AT[k]) * c01(f * 1.25);
      if (d >= 1) at = 1;
      var off = len * (1 - at);
      var offS = off.toFixed(1), dash = len + ' ' + len;
      [route, casing, glow].forEach(function (el) { put(el, 'stroke-dasharray', dash); put(el, 'stroke-dashoffset', offS); });
      var pt = pointAt(at);
      attr(dot, 'cx', pt.x.toFixed(1)); attr(dot, 'cy', pt.y.toFixed(1));
      put(dot, 'opacity', d > 0 && d < 1 ? '1' : '0');
      // Finger sits on the tap it is about to make.
      var fi = d <= 0 ? 0 : Math.min(3, f > .8 ? k + 1 : k);
      if (d >= 1) fi = 3;
      attr(finger, 'transform', 'translate(' + TAPS_XY[fi][0] + ' ' + TAPS_XY[fi][1] + ')');
      put(finger, 'opacity', (p > .08 && p < .36) ? '.95' : '0');
      for (var i = 0; i < 4; i++) {
        var tapAt = i === 0 ? 0 : i / 3;
        var on = d > 0 && drawn >= tapAt - .001;
        var since = c01((drawn - tapAt) * 6);
        var rip = taps[i].querySelector('.pl-rip'), wp = taps[i].querySelector('.pl-wp');
        put(wp, 'opacity', on ? '1' : '0');
        put(rip, 'opacity', on ? ((1 - since) * .9).toFixed(3) : '0');
        attr(rip, 'r', (6 + since * 22).toFixed(1));
      }
      // Like the app: the figure updates when a leg lands, it does not tick.
      var legs = d <= 0 ? 0 : d >= 1 ? 3 : Math.min(3, Math.floor(drawn * 3 + .2));
      var shown = km * (legs ? TAP_AT[legs] : 0);
      if (num && num.getAttribute('data-v') !== String(legs)) { num.setAttribute('data-v', String(legs)); num.textContent = fmt(shown); if (legs && num.parentNode.animate) num.parentNode.animate([{ transform: 'scale(1)' }, { transform: 'scale(1.14)', offset: .4 }, { transform: 'scale(1)' }], { duration: 450, easing: BOUNCE }); }

      // Beat 2: tilt into 3D, sights stand up (.36 to .66)
      var back2 = 1 - ease(seg(p, .66, .76));
      var tilt = ease(seg(p, .36, .48)) * back2, pan = ease(seg(p, .42, .66)) * back2;
      var pk = [back(seg(p, .44, .5)), back(seg(p, .5, .56)), back(seg(p, .56, .62))];
      var pinOut = 1 - seg(p, .66, .72);

      // Beat 3: map settles back, the Watch rises (.68 to 1)
      var aw = ease(seg(p, .66, .8));
      var ph = out(seg(p, .7, .84)), wr = out(seg(p, .74, .88));

      put(plane, 'transform', 'translate3d(0, calc(' + n(1 - vin) + ' * 16svh - ' + n(aw * K.ay) + 'px), 0) rotateX(' + n((1 - vin) * 24 + tilt * 52) + 'deg) rotateZ(' + n(tilt * K.rz) + 'deg) scale(' + n(.9 + vin * .1 + tilt * K.ts - aw * K.as) + ') translate3d(0, ' + n(pan * K.pd) + '%, 0)');
      put(wrap, 'opacity', n(1 - aw * .9));
      if (halo) put(halo, 'opacity', n(.4 + tilt * .6));
      put(glow, 'opacity', n(.12 + tilt * .25));
      put(hud, 'opacity', n(vhud * (1 - tilt) * (1 - aw)));
      put(hud, 'transform', 'translateX(-50%) translateY(' + n((1 - vhud) * 16) + 'px)');
      var pinT = 'rotateZ(' + n(-tilt * K.rz) + 'deg) rotateX(' + n(-tilt * 52) + 'deg)', pinO = n(1 - seg(p, .66, .7));
      pins.forEach(function (q, i) {
        var k = pk[i] * pinOut;
        put(q.el, 'opacity', pinO); put(q.el, 'transform', pinT);
        put(q.inn, 'opacity', n(k)); put(q.inn, 'transform', 'translateX(var(--pin-x, -22px)) translateY(' + n((1 - k) * 26) + 'px) scale(' + n(.4 + k * .6) + ')');
        put(q.stem, 'opacity', n(k * .55)); put(q.stem, 'transform', 'scaleY(' + n(k) + ')');
        put(q.foot, 'opacity', n(k)); put(q.foot, 'transform', 'scale(' + n(k) + ')');
      });
      put(phoneEl, 'opacity', n(Math.min(1, ph * 3)));
      put(phoneEl, 'transform', 'translate3d(' + n((1 - ph) * -30) + 'px, calc(' + n(1 - ph) + ' * 70svh), 0) rotate(' + n((1 - ph) * -6) + 'deg)');
      put(watch, 'opacity', n(Math.min(1, wr * 3)));
      put(watch, 'transform', 'translate3d(0, calc(' + n(1 - wr) + ' * 70svh), 0) scale(' + n(.86 + wr * .14) + ')');
      var turn = seg(p, .86, .97);
      sec.classList.toggle('pl-turned', turn >= 1);
      if (wdist) {
        var m = turn >= 1 ? 300 : Math.max(10, Math.round((1 - turn) * 12) * 10);
        wdist.textContent = String(m);
      }

      var s = p < .37 ? 1 : p < .67 ? 2 : 3;
      if (s !== step) { step = s; sec.setAttribute('data-step', String(s)); }
    }
    // A film: it plays once when the stage is half in view and holds its last frame.
    var D = 9500, film = 0, t0 = 0, raf = 0;
    // Frame guard: if this device cannot draw the film smoothly (median frame over
    // 24 ms across its first frames), show the finished frame instead of a stutter.
    var gd = [], gLast = 0, gOff = false;
    function guard(now) {
      if (gOff || gd.length > 14) return false;
      if (gLast) gd.push(now - gLast);
      gLast = now;
      if (gd.length < 12) return false;
      var m = gd.slice(2).sort(function (a, b) { return a - b; })[5];
      if (m > 24) { gOff = true; return true; }
      gd.length = 99; return false;
    }
    var again = sec.querySelector('.pl-again');
    function tick(now) {
      raf = 0;
      if (!root.classList.contains('motion')) { film = 0; t0 = 0; update(); return; }
      film = guard(now) ? 1 : c01((now - t0) / D);
      update();
      if (film < 1) raf = requestAnimationFrame(tick);
      else sec.classList.add('pl-done');
    }
    function play() {
      if (raf) cancelAnimationFrame(raf);
      sec.classList.remove('pl-done');
      film = 0; last = -1; t0 = performance.now(); gd = []; gLast = 0;
      raf = requestAnimationFrame(tick);
    }
    // A tap on Play again plays the whole film, whatever the frame guard saw.
    if (again) again.addEventListener('click', function () { play(); gd.length = 99; });
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es) {
        if (!t0 && es[0].intersectionRatio >= .5 && root.classList.contains('motion')) play();
        // Scrolled away mid-film: settle on the last frame and stop the clock.
        else if (raf && !es[0].isIntersecting) { cancelAnimationFrame(raf); raf = 0; film = 1; update(); sec.classList.add('pl-done'); }
      }, { threshold: [0, .5] }).observe(stage);
    } else { film = 1; }
    window.addEventListener('resize', function () { measured = false; last = -1; if (!raf) update(); }, { passive: true });
    new MutationObserver(function () { measured = false; last = -1; if (!root.classList.contains('motion')) { t0 = 0; film = 0; } update(); }).observe(root, { attributes: true, attributeFilter: ['class'] });
    update();
  } catch (e) {
    try { var s = document.getElementById('planner'); if (s) { s.classList.add('pl-off'); s.removeAttribute('data-step'); } } catch (_) {}
  }
})();
