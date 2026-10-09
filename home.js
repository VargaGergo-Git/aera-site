/* Aera homepage motion. Everything on the page is readable without this file:
   it only adds the entrance, the sunrise on scroll, the runner, the word-by-word
   headlines, the story phone, the drawn route, the sunset and the reveals.
   One scroll loop drives all of it with transform and opacity. If anything
   throws, motion is dropped and the page stays fully visible. */
(function () {
  var root = document.documentElement;
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  var hero = document.querySelector('.hero');
  var bar = document.querySelector('.bar');
  var run = document.querySelector('.hero-run');
  var dusk = document.querySelector('.dusk');
  var track = document.getElementById('track');
  var runner = document.getElementById('runner');
  var pending = [], io = null;

  function clamp(v) { return v < 0 ? 0 : v > 1 ? 1 : v; }

  function abandon() {
    root.classList.remove('motion');
    pending.forEach(function (el) { el.classList.add('in'); });
    pending = [];
    if (io) io.disconnect();
    if (hero) { hero.style.removeProperty('--p'); hero.style.removeProperty('--sw'); }
  }

  // Headlines: wrap each word so it can rise from behind its own line.
  function splitWords(el) {
    var i = 0;
    [].slice.call(el.childNodes).forEach(function (node) {
      if (node.nodeType !== 3 || !node.textContent.trim()) return;
      var frag = document.createDocumentFragment();
      node.textContent.split(/(\s+)/).forEach(function (part) {
        if (!part) return;
        if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(part)); return; }
        var w = document.createElement('span');
        w.className = 'w';
        var inner = document.createElement('span');
        inner.textContent = part;
        inner.style.setProperty('--i', i++);
        w.appendChild(inner);
        frag.appendChild(w);
      });
      el.replaceChild(frag, node);
    });
  }

  // Geometry is read once and on resize, never inside a frame: frames only use
  // scrollY, so scrolling never forces a style or layout pass.
  var G = null;
  function measure() {
    var sy = window.scrollY, vh = window.innerHeight;
    function box(el) { if (!el) return null; var r = el.getBoundingClientRect(); return { top: r.top + sy, h: r.height }; }
    G = { vh: vh, run: box(run), hero: box(hero), dusk: box(dusk) };
    // Phones: how far the phone climbs so it ends just under the bar.
    var ph = hero && hero.querySelector('.hero-ph');
    if (ph) {
      var top = 0, el = ph;
      while (el && el !== hero) { top += el.offsetTop; el = el.offsetParent; }
      if (el === hero) hero.style.setProperty('--rise', Math.min(0, 140 - top).toFixed(0) + 'px');
    }
  }

  // The runner's path, sampled once: a frame looks points up instead of asking the SVG.
  var LUT = [];
  (function () {
    try {
      var L = track ? track.getTotalLength() : 0;
      for (var i = 0; L && i <= 240; i++) { var q = track.getPointAtLength(L * i / 240); LUT.push(q.x, q.y); }
    } catch (e) { LUT = []; }
  })();
  var lastPose = -1;
  function placeRunner(p) {
    if (!runner || !LUT.length) return;
    var t = 0.12 + p * 0.82, f = t * 240, i = Math.min(239, Math.floor(f)), k = f - i;
    var x = LUT[2 * i] + (LUT[2 * i + 2] - LUT[2 * i]) * k, y = LUT[2 * i + 1] + (LUT[2 * i + 3] - LUT[2 * i + 1]) * k;
    var scale = 1.9 * (1 - t * 0.78);
    runner.setAttribute('transform', 'translate(' + x.toFixed(1) + ' ' + y.toFixed(1) + ') scale(' + scale.toFixed(3) + ')');
    var pose = Math.floor(t * 60) % 2;
    if (pose !== lastPose) { runner.classList.toggle('b', pose === 1); lastPose = pose; }
  }

  // Sunrise: the entrance lifts the sky from first light a little way, then
  // scrolling through the hero carries it the rest of the way to morning.
  var dawn = 0, dawnTarget = 0.24, dawnStart = 0;
  function runProgress(sy) {
    if (G.run && G.run.h > G.vh * 1.2) return clamp((sy - G.run.top) / (G.run.h - G.vh));
    return clamp(sy / (G.vh * 0.6));   // phones without a pin: the first half screen
  }

  // scrollY is read in the scroll event, before any frame callback has touched a
  // style, so reading it never forces a layout that another script dirtied.
  var SY = window.scrollY;
  var frames = 0, last = {};
  function put(el, k, v) { var s = v.toFixed(4); if (last[k] !== s) { last[k] = s; el.style.setProperty(k, s); } }
  function frame() {
    try {
      frames++;
      var sy = SY;
      if (bar) { var sc = sy > 24; if (last.bar !== sc) { last.bar = sc; bar.classList.toggle('scrolled', sc); } }
      if (!root.classList.contains('motion')) return;
      if (!G) measure();
      if (hero && G.hero && sy < G.hero.top + Math.max(G.hero.h, G.run ? G.run.h : 0)) {
        var t = runProgress(sy), p = dawn + (1 - dawn) * t;
        put(hero, '--p', p);
        put(hero, '--sw', clamp((t - 0.22) / 0.32));
        put(hero, '--hr', t);
        var day = t > 0.5;
        if (last.day !== day) { last.day = day; hero.classList.toggle('day', day); }
        placeRunner(p);
      }
      // Closing: the sun sets as you reach the bottom of the page.
      if (dusk && G.dusk) {
        var top = G.dusk.top - sy;
        put(dusk, '--dp', top > G.vh ? 0 : clamp((G.vh - top) / (G.dusk.h + G.vh * 0.35)));
      }
    } catch (e) { abandon(); }
  }

  var ticking = false;
  function request() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () { ticking = false; frame(); });
  }
  function remeasure() { G = null; SY = window.scrollY; request(); }

  function tweenDawn(now) {
    if (!dawnStart) dawnStart = now;
    var k = Math.min((now - dawnStart) / 2200, 1);
    dawn = dawnTarget * (1 - Math.pow(1 - k, 3));
    frame();
    if (k < 1) requestAnimationFrame(tweenDawn);
  }

  // Pointer depth in the hero on desktop: eased toward the cursor.
  var mx = 0, my = 0, tx = 0, ty = 0, easing = false;
  function easePointer() {
    mx += (tx - mx) * 0.08;
    my += (ty - my) * 0.08;
    hero.style.setProperty('--mx', mx.toFixed(3));
    hero.style.setProperty('--my', my.toFixed(3));
    if (Math.abs(tx - mx) > 0.002 || Math.abs(ty - my) > 0.002) requestAnimationFrame(easePointer);
    else easing = false;
  }

  try {
    if (!reduced) {
      root.classList.add('motion');
      [].slice.call(document.querySelectorAll('.split')).forEach(splitWords);
      // Reveals fire once as each block comes 12% above the bottom edge.
      pending = [].slice.call(document.querySelectorAll('.reveal, .fan'));
      if ('IntersectionObserver' in window) {
        io = new IntersectionObserver(function (es) {
          es.forEach(function (e) {
            if (!e.isIntersecting && e.boundingClientRect.top > 0) return;
            e.target.classList.add('in'); io.unobserve(e.target);
            pending = pending.filter(function (x) { return x !== e.target; });
          });
        }, { rootMargin: '0px 0px -12% 0px' });
        pending.forEach(function (el) { io.observe(el); });
      } else { abandon(); }
      if (hero) { hero.style.setProperty('--p', '0'); hero.style.setProperty('--sw', '0'); }
      placeRunner(0);
      requestAnimationFrame(function () {
        requestAnimationFrame(function () {
          if (hero) hero.classList.add('in');
          requestAnimationFrame(tweenDawn);
        });
      });
      if (finePointer && hero) {
        hero.addEventListener('pointermove', function (e) {
          tx = (e.clientX / window.innerWidth) * 2 - 1;
          ty = (e.clientY / window.innerHeight) * 2 - 1;
          if (!easing) { easing = true; requestAnimationFrame(easePointer); }
        }, { passive: true });
      }
    } else {
      placeRunner(0.62);
    }
  } catch (e) { abandon(); }

  window.addEventListener('scroll', function () { SY = window.scrollY; request(); }, { passive: true });
  window.addEventListener('resize', remeasure, { passive: true });
  window.addEventListener('load', remeasure);
  window.addEventListener('pageshow', function () { SY = window.scrollY; remeasure(); });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(remeasure);
  // Page height changes (images, fonts, an opened answer) move what is below.
  if ('ResizeObserver' in window) new ResizeObserver(remeasure).observe(document.body);
  request();

  // If frames never arrive at all, nothing stays hidden.
  setTimeout(function () {
    if (frames > 2) return;
    pending.forEach(function (el) { el.classList.add('in'); });
    pending = [];
    if (hero) hero.classList.add('in');
  }, 9000);
})();

/* The Coach: one-shot hello (a hop that lands with glad eyes) and nod (a dip and
   a squint), as in the app. On the web its eyes also follow the pointer and it
   blinks now and then. Reduced motion keeps it still. */
(function () {
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var coaches = [].slice.call(document.querySelectorAll('.coach'));
  if (!coaches.length) return;
  function play(el, kind) {
    if (reduced || !el) return;
    el.classList.remove('hello', 'nod', 'is-glad', 'is-squint');
    void el.getBoundingClientRect();
    el.classList.add(kind);
    if (kind === 'hello') {
      setTimeout(function () { el.classList.add('is-glad'); }, 300);
      setTimeout(function () { el.classList.remove('is-glad'); }, 1500);
    } else {
      el.classList.add('is-squint');
      setTimeout(function () { el.classList.remove('is-squint'); }, 480);
    }
    setTimeout(function () { el.classList.remove(kind); }, 950);
  }
  window.AeraCoach = { play: play };
  if (reduced) return;

  var fine = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  if (fine) {
    var px = 0, py = 0, queued = false;
    window.addEventListener('pointermove', function (e) {
      px = e.clientX; py = e.clientY;
      if (queued) return;
      queued = true;
      requestAnimationFrame(function () {
        queued = false;
        coaches.forEach(function (c) {
          var r = c.getBoundingClientRect();
          if (r.bottom < 0 || r.top > innerHeight) return;
          var dx = px - (r.left + r.width / 2), dy = py - (r.top + r.height * 0.66);
          var d = Math.sqrt(dx * dx + dy * dy) || 1, k = Math.min(1, d / 260);
          var g = c.querySelector('.eyes');
          if (g) g.setAttribute('transform', 'translate(' + (dx / d * 3.2 * k).toFixed(2) + ' ' + (dy / d * 2.6 * k).toFixed(2) + ')');
        });
      });
    }, { passive: true });
  }
  var onScreen = new Set();
  if ('IntersectionObserver' in window) {
    var vis = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) onScreen.add(e.target); else onScreen.delete(e.target); }); });
    coaches.forEach(function (c) { vis.observe(c); });
  }
  (function blink() {
    setTimeout(function () {
      coaches.forEach(function (c) {
        if (!onScreen.has(c) || c.classList.contains('is-glad')) return;
        c.classList.add('blink');
        setTimeout(function () { c.classList.remove('blink'); }, 140);
      });
      blink();
    }, 2600 + Math.random() * 3200);
  })();

  // The closing coach says hello when you reach it, and again when tapped.
  var cc = document.querySelector('.closing-coach');
  if (cc) {
    var coach = cc.querySelector('.coach'), said = false;
    var poke = function () { play(coach, 'hello'); };
    cc.addEventListener('click', poke);
    cc.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); poke(); } });
    if ('IntersectionObserver' in window) {
      var seen = new IntersectionObserver(function (es) {
        if (!es[0].isIntersecting || said) return;
        said = true; seen.disconnect(); setTimeout(poke, 250);
      }, { rootMargin: '0px 0px -20% 0px' });
      seen.observe(cc);
    }
  }

  // Phones lean toward the pointer, a little.
  if (fine) {
    [].slice.call(document.querySelectorAll('.duo .phone')).forEach(function (ph) {
      ph.addEventListener('pointermove', function (e) {
        var r = ph.getBoundingClientRect();
        var x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
        ph.style.setProperty('--ry', (x * 10).toFixed(2) + 'deg');
        ph.style.setProperty('--rx', (-y * 8).toFixed(2) + 'deg');
      });
      ph.addEventListener('pointerleave', function () { ph.style.setProperty('--ry', '0deg'); ph.style.setProperty('--rx', '0deg'); });
    });
  }
})();

/* Lazy images start loading a screen and a half before they arrive, so pinned
   scenes never show an empty phone while the scroll carries them in. */
(function () {
  if (!('IntersectionObserver' in window)) return;
  var imgs = [].slice.call(document.querySelectorAll('img[loading="lazy"]'));
  if (!imgs.length) return;
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.loading = 'eager'; io.unobserve(e.target); } });
  }, { rootMargin: '150% 0px' });
  imgs.forEach(function (im) { io.observe(im); });
})();

/* Chapter bar: lights the part of the day the reader is in (last night, this
   morning, out the door, after the run) and shows only inside that stretch. */
(function () {
  var bar = document.querySelector('.bar'), nav = document.querySelector('.chapters');
  if (!bar || !nav) return;
  var links = [].slice.call(nav.querySelectorAll('a'));
  var secs = links.map(function (a) { return document.getElementById(a.getAttribute('data-ch')); });
  if (secs.some(function (s) { return !s; })) { nav.parentNode.removeChild(nav); return; }
  var end = document.querySelector('.also'), now = nav.querySelector('.ch-now'), VH = window.innerHeight;
  var cur = -2, shown = null, ticking = false, tops = null, endTop = Infinity, SY = window.scrollY;
  // Section tops are read on load and resize only; scrolling compares them with scrollY.
  function measure() {
    var sy = SY = window.scrollY; VH = window.innerHeight;
    tops = secs.map(function (s) { return s.getBoundingClientRect().top + sy; });
    endTop = end ? end.getBoundingClientRect().top + sy : Infinity;
  }
  function update() {
    ticking = false;
    if (!tops) measure();
    var line = SY + VH * 0.45, idx = -1, i;
    for (i = 0; i < tops.length; i++) if (tops[i] <= line) idx = i;
    var show = idx >= 0 && endTop > line;
    if (show !== shown) { shown = show; bar.classList.toggle('ch-on', show); }
    if (idx === cur) return;
    cur = idx;
    links.forEach(function (a, j) {
      a.classList.toggle('on', j === idx); a.classList.toggle('done', j < idx);
      if (j === idx) a.setAttribute('aria-current', 'step'); else a.removeAttribute('aria-current');
    });
    if (now && idx >= 0) now.textContent = links[idx].textContent;
  }
  function request() { if (!ticking) { ticking = true; requestAnimationFrame(update); } }
  function remeasure() { tops = null; request(); }
  window.addEventListener('scroll', function () { SY = window.scrollY; request(); }, { passive: true });
  window.addEventListener('resize', remeasure, { passive: true });
  window.addEventListener('load', remeasure);
  if ('ResizeObserver' in window) new ResizeObserver(remeasure).observe(document.body);
  request();
})();
