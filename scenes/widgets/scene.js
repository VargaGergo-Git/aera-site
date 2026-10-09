(function () {
  try {
    var sec = document.getElementById('widgets');
    if (!sec) return;
    var root = document.documentElement;
    var stage = sec.querySelector('.wg-stage');
    var head = sec.querySelector('.wg-head');
    var caps = sec.querySelector('.wg-caps');
    var world = sec.querySelector('.wg-world');
    var step = 0, measured = false, last = -1;
    function c01(v) { return v < 0 ? 0 : v > 1 ? 1 : v; }
    function seg(p, a, b) { return c01((p - a) / (b - a)); }
    function ease(t) { return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; }
    function out(t) { return 1 - Math.pow(1 - t, 3); }
    // Only changed values are written: an unchanged write still restyles the whole scene.
    var vals = {};
    function set(k, v) { var s = typeof v === 'number' ? v.toFixed(3) : v; if (vals[k] !== s) { vals[k] = s; sec.style.setProperty(k, s); } }
    var KEYS = ['--in', '--w1', '--w2', '--w3', '--w4', '--zoom', '--dots', '--lock', '--a1', '--a2', '--world-top', '--world-h', '--dev-px', '--zoom-s', '--lift-y', '--dev-dy', '--dev-mask', '--hout', '--head-top', '--caps-top'];

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
      var dw = Math.min(h * .95 / 2.238, ww * .8, 420), dy = 0, mask = 'none';
      if (phone) {
        dw = Math.min(vw * .74, 340);
        var dh = dw * 2.238;
        if (dh > h) {
          dy = (dh - h) / 2;
          var room = vh - caps.offsetHeight - 30 - top;
          var cut = Math.max(0, Math.min(dh, room + 10));
          mask = 'linear-gradient(to bottom, #000 ' + Math.round(cut - 120) + 'px, transparent ' + Math.round(cut) + 'px)';
        }
      }
      set('--dev-px', Math.max(150, dw) + 'px');
      set('--dev-dy', dy + 'px');
      set('--dev-mask', mask);
      // Close-up: This morning grows to most of the room's width.
      var zs = Math.min(Math.min(ww * .86, wide ? 560 : 500) / (dw * 349 / 393), 2.2) - 1;
      set('--zoom-s', Math.max(.12, zs));
      // Move This morning's centre (10.9% of the screen height above its middle) to the room's middle.
      set('--lift-y', (dw * 852 / 393 * .109 - dy) + 'px');
      measured = true;
    }
    function clear() {
      KEYS.forEach(function (k) { sec.style.removeProperty(k); });
      sec.removeAttribute('data-step'); sec.classList.remove('wg-lifted');
      step = 0; measured = false; last = -1; vals = {};
    }
    function update() {

      if (!root.classList.contains('motion')) { if (step) clear(); return; }
      if (!measured) measure();
      var p = film;
      if (Math.abs(p - last) < .0004 && step) return;
      last = p;
      set('--in', out(seg(p, 0, .12)));
      set('--w1', out(seg(p, .1, .19)));
      set('--w2', out(seg(p, .15, .24)));
      set('--w3', out(seg(p, .2, .29)));
      set('--w4', out(seg(p, .25, .34)));
      var z = ease(seg(p, .38, .5)) * (1 - ease(seg(p, .58, .68)));
      set('--zoom', z);
      if ((z > .001) !== sec.classList.contains('wg-lifted')) sec.classList.toggle('wg-lifted', z > .001);
      // The dots start at the middle of the band and settle on the night's reading.
      set('--dots', p < .38 ? 1 : out(seg(p, .44, .56)));
      set('--hout', ease(seg(p, .63, .7)));
      set('--lock', ease(seg(p, .66, .75)));
      set('--a1', out(seg(p, .74, .82)));
      set('--a2', out(seg(p, .78, .86)));
      var s = p < .37 ? 1 : p < .63 ? 2 : 3;
      if (s !== step) { step = s; sec.setAttribute('data-step', String(s)); }
    }
    // A film: it plays once when the stage is half in view and holds its last frame.
    var D = 7200, film = 0, t0 = 0, raf = 0;
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

    var again = sec.querySelector('.wg-again');
    function tick(now) {
      raf = 0;
      if (!root.classList.contains('motion')) { film = 0; t0 = 0; update(); return; }
      film = guard(now) ? 1 : c01((now - t0) / D);
      update();
      if (film < 1) raf = requestAnimationFrame(tick);
      else sec.classList.add('wg-done');
    }
    function play() {
      if (raf) cancelAnimationFrame(raf);
      sec.classList.remove('wg-done');
      film = 0; last = -1; t0 = performance.now(); gd = []; gLast = 0;
      raf = requestAnimationFrame(tick);
    }
    // A tap on Play again plays the whole film, whatever the frame guard saw.
    if (again) again.addEventListener('click', function () { play(); gd.length = 99; });
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es) {
        if (!t0 && es[0].intersectionRatio >= .5 && root.classList.contains('motion')) play();
      }, { threshold: [0, .5] }).observe(stage);
      // Scrolled away mid-film: jump to the last frame instead of animating off screen.
      new IntersectionObserver(function (es) {
        if (!es[0].isIntersecting && raf) { cancelAnimationFrame(raf); raf = 0; film = 1; update(); sec.classList.add('wg-done'); }
      }).observe(stage);
    } else { film = 1; }
    window.addEventListener('resize', function () { measured = false; last = -1; if (!raf) update(); }, { passive: true });
    new MutationObserver(function () { measured = false; last = -1; if (!root.classList.contains('motion')) { t0 = 0; film = 0; } update(); }).observe(root, { attributes: true, attributeFilter: ['class'] });
    update();
  } catch (e) {
    try { var s = document.getElementById('widgets'); if (s) { s.classList.add('wg-off'); s.removeAttribute('data-step'); } } catch (_) {}
  }
})();
