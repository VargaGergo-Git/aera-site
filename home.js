/* Aera homepage motion. Everything on the page is readable without this file.
   Like Apple's and Bevel's pages, the page scrolls natively and nothing is tied
   to the scroll position: this only adds the hero's entrance, the dawn on its
   headline and a fade-up as each block arrives, all in CSS (transform and
   opacity). If anything throws, motion is dropped and everything shows. */
(function () {
  var root = document.documentElement;
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hero = document.querySelector('.hero');
  var bar = document.querySelector('.bar');
  var track = document.getElementById('track');
  var runner = document.getElementById('runner');
  var pending = [], io = null;
  var DEV = '.eng-device, .eng-board, .pl-world, .pl-wrist, .wg-world, .fo-film';
  var HEAD = '.eng-head, .wg-head, .fo-head, .guide-head, .pl-words, .rv-lead, .center, .maker';

  function showAll() {
    pending.forEach(function (el) { el.classList.add('in'); });
    pending = [];
    if (io) io.disconnect();
    if (hero) hero.classList.add('in');
  }
  function abandon() { showAll(); root.classList.remove('motion'); }

  // The hero headline: each word is wrapped so the dawn can pass over it word by word.
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
        inner.setAttribute('data-w', part);
        inner.style.setProperty('--i', i++);
        w.appendChild(inner);
        frag.appendChild(w);
      });
      el.replaceChild(frag, node);
    });
  }

  // The runner stands on the path through the meadow, placed once.
  try {
    if (track && runner) {
      var L = track.getTotalLength(), t = 0.12 + 0.62 * 0.82, q = track.getPointAtLength(L * t);
      runner.setAttribute('transform', 'translate(' + q.x.toFixed(1) + ' ' + q.y.toFixed(1) + ') scale(' + (1.9 * (1 - t * 0.78)).toFixed(3) + ')');
    }
  } catch (e) {}

  // The header turns solid once the page has moved. One class, set only when it changes.
  var scrolled = null;
  function onScroll() {
    var s = window.scrollY > 24;
    if (s !== scrolled) { scrolled = s; if (bar) bar.classList.toggle('scrolled', s); }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  try {
    if (reduced || !('IntersectionObserver' in window)) return;
    root.classList.add('motion');
    if (hero) [].slice.call(hero.querySelectorAll('.split')).forEach(splitWords);
    // Each block fades up once, as it comes a little above the bottom edge.
    pending = [].slice.call(document.querySelectorAll('.reveal, .fan, .dusk'));
    // Like Apple's pages: a heading block rises line by line, a device rises from
    // further down and settles to full size, and blocks that arrive together
    // follow one another instead of moving as one slab.
    pending.forEach(function (el) {
      if (!el.classList.contains('reveal')) return;
      if (el.matches(DEV)) { el.classList.add('dev'); return; }
      var kids = [].slice.call(el.children);
      if (kids.length > 1 && kids.length < 7 && (el.matches(HEAD) || el.querySelector(':scope > h2'))) {
        el.classList.add('stag');
        kids.forEach(function (k, i) { k.style.setProperty('--ci', i); });
      }
    });
    io = new IntersectionObserver(function (es) {
      var batch = [];
      es.forEach(function (e) {
        if (!e.isIntersecting && e.boundingClientRect.top > 0) return;
        batch.push(e);
        io.unobserve(e.target);
        pending = pending.filter(function (x) { return x !== e.target; });
      });
      batch.sort(function (a, b) { return (a.boundingClientRect.top - b.boundingClientRect.top) || (a.boundingClientRect.left - b.boundingClientRect.left); });
      batch.forEach(function (e, i) {
        var el = e.target;
        if (i && e.isIntersecting && !el.style.getPropertyValue('--d')) el.style.setProperty('--d', Math.min(i, 5) * 0.09 + 's');
        el.classList.add('in');
      });
    }, { rootMargin: '0px 0px -10% 0px' });
    pending.forEach(function (el) { io.observe(el); });
    requestAnimationFrame(function () {
      requestAnimationFrame(function () {
        if (!hero) return;
        hero.classList.add('in');
        setTimeout(function () { hero.classList.add('dawned'); }, 4500);
      });
    });
    // If frames never arrive (a background tab, a stalled browser), nothing stays hidden.
    setTimeout(function () { if (hero && !hero.classList.contains('in')) showAll(); }, 4000);
  } catch (e) { abandon(); }
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
