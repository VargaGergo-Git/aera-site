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
    // Where along the line (0..1) each tap lands: start, bridge, park edge, summit.
    var TAP_AT = [0, 0, 0, 0];
    var TAPS_XY = [[505, 588], [262, 398], [190, 256], [452, 104]];
    (function () {
      var n = 240, best = [1e9, 1e9, 1e9, 1e9];
      for (var i = 0; i <= n; i++) {
        var pt = route.getPointAtLength(len * i / n);
        for (var k = 0; k < 4; k++) {
          var d = Math.hypot(pt.x - TAPS_XY[k][0], pt.y - TAPS_XY[k][1]);
          if (d < best[k]) { best[k] = d; TAP_AT[k] = i / n; }
        }
      }
    })();
    var step = 0, measured = false, last = -1;

    function c01(v) { return v < 0 ? 0 : v > 1 ? 1 : v; }
    function seg(p, a, b) { return c01((p - a) / (b - a)); }
    function ease(t) { return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; }
    function out(t) { return 1 - Math.pow(1 - t, 3); }
    function back(t) { var c = 1.6; return t <= 0 ? 0 : t >= 1 ? 1 : 1 + (c + 1) * Math.pow(t - 1, 3) + c * Math.pow(t - 1, 2); }
    function set(k, v) { sec.style.setProperty(k, typeof v === 'number' ? v.toFixed(4) : v); }

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
      measured = true;
    }
    function clear() {
      ['--in', '--draw', '--tilt', '--pan', '--map-o', '--pin-o', '--p1', '--p2', '--p3', '--hud', '--away', '--wrist', '--ph', '--world-top', '--world-h', '--map-px', '--watch-px', '--away-y', '--head-top', '--caps-top'].forEach(function (k) { sec.style.removeProperty(k); });
      sec.removeAttribute('data-step');
      route.style.strokeDasharray = route.style.strokeDashoffset = '';
      glow.style.strokeDasharray = glow.style.strokeDashoffset = '';
      casing.style.strokeDasharray = casing.style.strokeDashoffset = '';
      step = 0; measured = false; last = -1;
    }
    function fmt(v) { var s = v.toFixed(1); return comma ? s.replace('.', ',') : s; }

    function update() {

      if (!root.classList.contains('motion')) { if (step) clear(); return; }
      if (!measured) measure();
      var p = film;
      if (Math.abs(p - last) < .0004 && step) return;
      last = p;

      // Beat 1: draw (0 to .36)
      set('--in', out(seg(p, 0, .1)));
      set('--hud', out(seg(p, .06, .12)));
      var d = seg(p, .1, .34);
      var drawn = ease(d);
      // The finger hops tap to tap; the line follows to the next tap.
      var hop = drawn * 3, k = Math.min(2, Math.floor(hop)), f = hop - k;
      var at = TAP_AT[k] + (TAP_AT[k + 1] - TAP_AT[k]) * c01(f * 1.25);
      if (d >= 1) at = 1;
      var off = len * (1 - at);
      route.style.strokeDasharray = len + ' ' + len; route.style.strokeDashoffset = off;
      casing.style.strokeDasharray = len + ' ' + len; casing.style.strokeDashoffset = off;
      glow.style.strokeDasharray = len + ' ' + len; glow.style.strokeDashoffset = off;
      var pt = route.getPointAtLength(len * at);
      dot.setAttribute('cx', pt.x.toFixed(1)); dot.setAttribute('cy', pt.y.toFixed(1));
      dot.style.opacity = d > 0 && d < 1 ? 1 : 0;
      // Finger sits on the tap it is about to make.
      var fi = d <= 0 ? 0 : Math.min(3, f > .8 ? k + 1 : k);
      if (d >= 1) fi = 3;
      finger.setAttribute('transform', 'translate(' + TAPS_XY[fi][0] + ' ' + TAPS_XY[fi][1] + ')');
      finger.style.opacity = (p > .08 && p < .36) ? .95 : 0;
      for (var i = 0; i < 4; i++) {
        var tapAt = i === 0 ? 0 : i / 3;
        var on = d > 0 && drawn >= tapAt - .001;
        var since = c01((drawn - tapAt) * 6);
        var rip = taps[i].querySelector('.pl-rip'), wp = taps[i].querySelector('.pl-wp');
        wp.style.opacity = on ? 1 : 0;
        rip.style.opacity = on ? (1 - since) * .9 : 0;
        rip.setAttribute('r', (6 + since * 22).toFixed(1));
      }
      // Like the app: the figure updates when a leg lands, it does not tick.
      var legs = d <= 0 ? 0 : d >= 1 ? 3 : Math.min(3, Math.floor(drawn * 3 + .2));
      var shown = km * (legs ? TAP_AT[legs] : 0);
      if (num && num.getAttribute('data-v') !== String(legs)) { num.setAttribute('data-v', String(legs)); num.textContent = fmt(shown); num.parentNode.classList.remove('pl-bump'); void num.offsetWidth; if (legs) num.parentNode.classList.add('pl-bump'); }

      // Beat 2: tilt into 3D, sights stand up (.36 to .66)
      set('--tilt', ease(seg(p, .36, .48)) * (1 - ease(seg(p, .66, .76))));
      set('--pan', ease(seg(p, .42, .66)) * (1 - ease(seg(p, .66, .76))));
      set('--p1', back(seg(p, .44, .5)) * (1 - seg(p, .66, .72)));
      set('--p2', back(seg(p, .5, .56)) * (1 - seg(p, .66, .72)));
      set('--p3', back(seg(p, .56, .62)) * (1 - seg(p, .66, .72)));

      // Beat 3: map settles back, the Watch rises (.68 to 1)
      var aw = ease(seg(p, .66, .8));
      set('--away', aw);
      set('--map-o', 1 - aw * .9);
      set('--pin-o', 1 - seg(p, .66, .7));
      set('--ph', out(seg(p, .7, .84)));
      set('--wrist', out(seg(p, .74, .88)));
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
    var again = sec.querySelector('.pl-again');
    function tick(now) {
      raf = 0;
      if (!root.classList.contains('motion')) { film = 0; t0 = 0; update(); return; }
      film = c01((now - t0) / D);
      update();
      if (film < 1) raf = requestAnimationFrame(tick);
      else sec.classList.add('pl-done');
    }
    function play() {
      if (raf) cancelAnimationFrame(raf);
      sec.classList.remove('pl-done');
      film = 0; last = -1; t0 = performance.now();
      raf = requestAnimationFrame(tick);
    }
    if (again) again.addEventListener('click', play);
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es) {
        if (!t0 && es[0].intersectionRatio >= .5 && root.classList.contains('motion')) play();
      }, { threshold: [0, .5] }).observe(stage);
    } else { film = 1; }
    window.addEventListener('resize', function () { measured = false; last = -1; if (!raf) update(); }, { passive: true });
    new MutationObserver(function () { measured = false; last = -1; if (!root.classList.contains('motion')) { t0 = 0; film = 0; } update(); }).observe(root, { attributes: true, attributeFilter: ['class'] });
    update();
  } catch (e) {
    try { var s = document.getElementById('planner'); if (s) { s.classList.add('pl-off'); s.removeAttribute('data-step'); } } catch (_) {}
  }
})();
