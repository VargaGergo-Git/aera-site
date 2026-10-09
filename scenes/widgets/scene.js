(function () {
  try {
    var sec = document.getElementById('widgets');
    if (!sec) return;
    var root = document.documentElement;
    var stage = sec.querySelector('.wg-stage');
    var head = sec.querySelector('.wg-head');
    var caps = sec.querySelector('.wg-caps');
    var world = sec.querySelector('.wg-world');
    var dev = sec.querySelector('.wg-dev'), lift = sec.querySelector('.wg-lift'), dim = sec.querySelector('.wg-dim');
    var home = sec.querySelector('.wg-home'), lock = sec.querySelector('.wg-lock');
    var lockText = [].slice.call(sec.querySelectorAll('.wg-clock, .wg-date'));
    var rect = sec.querySelector('.wg-rect'), circ = sec.querySelector('.wg-circ');
    var ws = ['.wg-w1', '.wg-w2', '.wg-w3', '.wg-w4'].map(function (q) { return sec.querySelector('.wg-home ' + q); });
    var cars = [].slice.call(sec.querySelectorAll('.wg-home .wg-car')).map(function (el) {
      var v = el.closest('.wg-v'); return { el: el, o: parseFloat(v && v.style.getPropertyValue('--o')) || .5 };
    });
    var step = 0, measured = false, last = -1;
    var M = { pt: 1, zs: .6, ly: 0 };
    // The film writes final transform and opacity straight onto each moving element,
    // so a frame restyles a handful of nodes, never the whole phone underneath.
    var touched = [];
    function put(el, prop, v) {
      var c = el.__wg || (el.__wg = {});
      if (c[prop] === v) return;
      if (!(prop in c)) touched.push([el, prop]);
      c[prop] = v; el.style.setProperty(prop, v);
    }
    function n(v) { return v.toFixed(4); }
    function c01(v) { return v < 0 ? 0 : v > 1 ? 1 : v; }
    function seg(p, a, b) { return c01((p - a) / (b - a)); }
    function ease(t) { return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; }
    function out(t) { return 1 - Math.pow(1 - t, 3); }
    var cache = {};
    function set(k, v) { v = typeof v === 'number' ? v.toFixed(4) : v; if (cache[k] === v) return; cache[k] = v; sec.style.setProperty(k, v); }
    var KEYS = ['--in', '--w1', '--w2', '--w3', '--w4', '--zoom', '--dots', '--lock', '--a1', '--a2', '--world-top', '--world-h', '--dev-px', '--zoom-s', '--lift-y', '--dev-dy', '--fade-y', '--hout', '--head-top', '--caps-top'];

    function measure() {
      var vw = window.innerWidth, vh = window.innerHeight, phone = vw < 900, wide = vw >= 1100;
      var top, h, ww;
      if (wide) {
        var hh = head.offsetHeight, ch = caps.offsetHeight;
        var ht = Math.max(84, (vh - hh - ch - 28) / 2);
        set('--head-top', ht + 'px');
        set('--caps-top', (ht + hh + 28) + 'px');
        top = 76; h = vh - top - 30;
        ww = world.offsetWidth || vw * .6;
      } else {
        top = head.offsetTop + head.offsetHeight + (phone ? 16 : 24);
        h = Math.max(240, vh - caps.offsetHeight - Math.max(22, vh * .032) - (phone ? 14 : 22) - top);
        ww = vw;
      }
      set('--world-top', top + 'px');
      set('--world-h', h + 'px');
      // The phone fills the height it is given (screen + bezel = 2.238 x its width).
      // On a phone it is allowed to run on under the words and fade out, like a crop.
      var dw = Math.min(h * .95 / 2.238, ww * .8, 420), dy = 0, fade = 0;
      if (phone) {
        dw = Math.min(vw * .74, 340);
        var dh = dw * 2.238;
        if (dh > h) {
          dy = (dh - h) / 2;
          var room = vh - caps.offsetHeight - 30 - top;
          var cut = Math.max(0, Math.min(dh, room + 10));
          fade = top + cut;
        }
      }
      set('--dev-px', Math.max(150, dw) + 'px');
      set('--dev-dy', dy + 'px');
      sec.classList.toggle('wg-faded', fade > 0);
      if (fade > 0) set('--fade-y', Math.round(fade) + 'px');
      // Close-up: This morning grows to most of the room's width.
      var zs = Math.min(Math.min(ww * .86, wide ? 560 : 500) / (dw * 349 / 393), 2.2) - 1;
      set('--zoom-s', Math.max(.12, zs));
      M.zs = Math.max(.12, zs); M.pt = Math.max(150, dw) / 393;
      // Move This morning's centre (10.9% of the screen height above its middle) to the room's middle.
      set('--lift-y', (dw * 852 / 393 * .109 - dy) + 'px');
      M.ly = dw * 852 / 393 * .109 - dy;
      measured = true;
    }
    function clear() {
      KEYS.forEach(function (k) { sec.style.removeProperty(k); });
      cache = {}; sec.classList.remove('wg-faded');
      touched.forEach(function (t) { t[0].style.removeProperty(t[1]); delete t[0].__wg; });
      touched = [];
      sec.removeAttribute('data-step'); sec.classList.remove('wg-lifted');
      step = 0; measured = false; last = -1;
    }
    function update() {

      if (!root.classList.contains('motion')) { if (step) clear(); return; }
      if (!measured) measure();
      var p = film;
      if (Math.abs(p - last) < .0004 && step) return;
      last = p;
      var vin = out(seg(p, 0, .12));
      var z = ease(seg(p, .38, .5)) * (1 - ease(seg(p, .58, .68)));
      sec.classList.toggle('wg-lifted', z > .001);
      put(dev, 'opacity', n(Math.min(1, vin * 2.5)));
      put(dev, 'transform', 'translate3d(0, calc(' + n(1 - vin) + ' * 40svh), 0) rotateX(' + n((1 - vin) * 16) + 'deg) scale(' + n(1 - z * .05) + ')');
      [[.1, .19], [.15, .24], [.2, .29], [.25, .34]].forEach(function (r, i) {
        var k = out(seg(p, r[0], r[1]));
        // While This morning is lifted out, its copy in the phone stays hidden.
        put(ws[i], 'opacity', n(i === 2 && z > .001 ? 0 : k));
        put(ws[i], 'transform', 'translate3d(0, ' + n((1 - k) * -18 * M.pt) + 'px, 0) scale(' + n(1 + (1 - k) * .5) + ')');
      });
      put(lift, 'transform', 'translate3d(0, ' + n(z * M.ly) + 'px, 0) scale(' + n(1 + z * M.zs) + ')');
      put(lift, '--zoom', n(z));
      put(dim, 'opacity', n(z * .5));
      // The dots start at the middle of the band and settle on the night's reading.
      var dots = p < .38 ? 1 : out(seg(p, .44, .56));
      cars.forEach(function (c) { put(c.el, 'transform', 'translate3d(' + n((.5 - c.o) * (1 - dots) * 100) + '%, 0, 0)'); });
      var hout = ease(seg(p, .63, .7)), lk = ease(seg(p, .66, .75)), a1 = out(seg(p, .74, .82)), a2 = out(seg(p, .78, .86));
      put(home, 'opacity', n(1 - hout));
      put(home, 'transform', 'scale(' + n(1 - hout * .08) + ')');
      put(lock, 'opacity', n(lk));
      lockText.forEach(function (el) { put(el, 'transform', 'translate3d(0, ' + n((1 - lk) * -40 * M.pt) + 'px, 0)'); });
      put(rect, 'opacity', n(a1));
      put(rect, 'transform', 'translate3d(0, ' + n((1 - a1) * 14 * M.pt) + 'px, 0) scale(' + n(.9 + a1 * .1) + ')');
      put(circ, 'opacity', n(a2));
      put(circ, 'transform', 'translate3d(0, ' + n((1 - a2) * 14 * M.pt) + 'px, 0) scale(' + n(.9 + a2 * .1) + ')');
      var s = p < .37 ? 1 : p < .63 ? 2 : 3;
      if (s !== step) { step = s; sec.setAttribute('data-step', String(s)); }
    }
    // A film: it plays once when the stage is half in view and holds its last frame.
    var D = 7200, film = 0, t0 = 0, raf = 0;
    var again = sec.querySelector('.wg-again');
    function tick(now) {
      raf = 0;
      if (!root.classList.contains('motion')) { film = 0; t0 = 0; update(); return; }
      film = c01((now - t0) / D);
      update();
      if (film < 1) raf = requestAnimationFrame(tick);
      else sec.classList.add('wg-done');
    }
    function play() {
      if (raf) cancelAnimationFrame(raf);
      sec.classList.remove('wg-done');
      film = 0; last = -1; t0 = performance.now();
      raf = requestAnimationFrame(tick);
    }
    if (again) again.addEventListener('click', play);
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es) {
        if (!t0 && es[0].intersectionRatio >= .5 && root.classList.contains('motion')) play();
        // Scrolled away mid-film: settle on the last frame and stop the clock.
        else if (raf && !es[0].isIntersecting) { cancelAnimationFrame(raf); raf = 0; film = 1; update(); sec.classList.add('wg-done'); }
      }, { threshold: [0, .5] }).observe(stage);
    } else { film = 1; }
    window.addEventListener('resize', function () { measured = false; last = -1; if (!raf) update(); }, { passive: true });
    new MutationObserver(function () { measured = false; last = -1; if (!root.classList.contains('motion')) { t0 = 0; film = 0; } update(); }).observe(root, { attributes: true, attributeFilter: ['class'] });
    update();
  } catch (e) {
    try { var s = document.getElementById('widgets'); if (s) { s.classList.add('wg-off'); s.removeAttribute('data-step'); } } catch (_) {}
  }
})();
