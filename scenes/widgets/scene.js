/* Widgets scene: scroll through the pin and the Home Screen straightens, the
   widgets fly in from depth one by one, then it dims to the Lock Screen.
   Writes custom properties only; CSS turns them into transforms. */
(function () {
  try {
    var root = document.documentElement;
    var sec = document.querySelector('.scene-widgets');
    if (!sec) return;
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    var pin = sec.querySelector('.wg-pin');
    var beats = [].slice.call(sec.querySelectorAll('.wg-beats li'));
    var watch = sec.querySelector('.wg-watch');
    var nums = [].slice.call(sec.querySelectorAll('.wg-num'));
    if (!pin) return;

    function clamp(v) { return v < 0 ? 0 : v > 1 ? 1 : v; }
    function seg(t, a, b) { return clamp((t - a) / (b - a)); }
    function out3(x) { return 1 - Math.pow(1 - x, 3); }
    function inOut(x) { return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; }
    function back(x) { var c1 = 1.5, c3 = c1 + 1; return x <= 0 ? 0 : x >= 1 ? 1 : 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); }

    var last = {}, lastBeat = -1, lastWatch = null, lastNum = -1;
    function set(k, v) {
      var s = v.toFixed(4);
      if (last[k] === s) return;
      last[k] = s;
      sec.style.setProperty(k, s);
    }

    // Widget windows along the pin: [start, end].
    var W = [[0.06, 0.26], [0.13, 0.33], [0.22, 0.44], [0.31, 0.53]];

    function paint(t) {
      var a = inOut(seg(t, 0, 0.52));
      set('--tilt', 1 - a);
      set('--sh', Math.sin(Math.PI * seg(t, 0.12, 0.6)));
      for (var i = 0; i < 4; i++) {
        var p = seg(t, W[i][0], W[i][1]);
        set('--w' + (i + 1), back(p));
        set('--o' + (i + 1), clamp(p * 2.6));
      }
      var f1 = out3(seg(t, 0.2, 0.36));
      set('--f1', f1);
      set('--f3', out3(seg(t, 0.36, 0.52)));
      set('--f4', out3(seg(t, 0.45, 0.62)));
      set('--lk', inOut(seg(t, 0.62, 0.71)));
      set('--lc', out3(seg(t, 0.67, 0.79)));
      set('--l1', back(seg(t, 0.72, 0.84)));
      set('--l2', back(seg(t, 0.77, 0.89)));

      var n = Math.round(84 * f1);
      if (n !== lastNum) {
        lastNum = n;
        nums.forEach(function (el) { el.textContent = String(n); });
      }
      var b = t < 0.62 ? 0 : t < 0.9 ? 1 : 2;
      if (b !== lastBeat) {
        lastBeat = b;
        beats.forEach(function (li, j) { li.classList.toggle('on', j === b); });
      }
      var w = t > 0.88;
      if (w !== lastWatch && watch) { lastWatch = w; watch.classList.toggle('on', w); }
    }

    var ticking = false;
    function frame() {
      ticking = false;
      try {
        if (!root.classList.contains('motion')) { stop(); return; }
        var vh = window.innerHeight;
        var r = pin.getBoundingClientRect();
        if (r.bottom < -vh * 0.5 || r.top > vh * 1.5) return;
        var span = r.height - vh;
        var t = span > 0 ? clamp(-r.top / span) : 1;
        paint(t);
      } catch (e) { stop(); }
    }
    function request() {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(frame);
    }
    function stop() {
      sec.classList.remove('wg-live');
      ['--tilt', '--sh', '--w1', '--w2', '--w3', '--w4', '--o1', '--o2', '--o3', '--o4', '--f1', '--f3', '--f4', '--lk', '--lc', '--l1', '--l2']
        .forEach(function (k) { sec.style.removeProperty(k); });
      nums.forEach(function (el) { el.textContent = el.getAttribute('data-to'); });
      beats.forEach(function (li, j) { li.classList.toggle('on', j === 0); });
      window.removeEventListener('scroll', request);
      window.removeEventListener('resize', request);
    }

    // home.js adds .motion; wait for it if this file runs first.
    var started = false;
    function boot() {
      if (started || !root.classList.contains('motion')) return;
      started = true;
      paint(0);
      sec.classList.add('wg-live');
      window.addEventListener('scroll', request, { passive: true });
      window.addEventListener('resize', request, { passive: true });
      request();
    }
    boot();
    document.addEventListener('DOMContentLoaded', boot);
    window.addEventListener('load', function () { boot(); if (started) request(); });
  } catch (e) {
    try {
      var s = document.querySelector('.scene-widgets');
      if (s) {
        s.classList.remove('wg-live');
        [].slice.call(s.querySelectorAll('.wg-num')).forEach(function (el) { el.textContent = el.getAttribute('data-to'); });
      }
    } catch (e2) { /* static state stays */ }
  }
})();
