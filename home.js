/* Aera homepage motion. Everything on the page is readable without this file:
   it only adds the entrance, the sunrise on scroll, the runner, the word-by-word
   headlines, the story phone, the drawn route, the sunset and the reveals.
   One scroll loop drives all of it with transform and opacity. If anything
   throws, motion is dropped and the page stays fully visible. */
(function () {
  var root = document.documentElement;
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  var wide = window.matchMedia('(min-width: 900px)');
  var hero = document.querySelector('.hero');
  var bar = document.querySelector('.bar');
  var steps = [].slice.call(document.querySelectorAll('.step'));
  var screens = [].slice.call(document.querySelectorAll('.stage .scr'));
  var dots = [].slice.call(document.querySelectorAll('.stage .dots i'));
  var stage = document.querySelector('.stage');
  var pars = [].slice.call(document.querySelectorAll('[data-par]'));
  var after = document.querySelector('.after');
  var route = document.getElementById('route');
  var rhead = document.getElementById('rhead');
  var dusk = document.querySelector('.dusk');
  var track = document.getElementById('track');
  var runner = document.getElementById('runner');
  var pending = [];

  function len(path) { try { return path ? path.getTotalLength() : 0; } catch (e) { return 0; } }
  var trackLen = len(track);
  var routeLen = len(route);

  function clamp(v) { return v < 0 ? 0 : v > 1 ? 1 : v; }

  function abandon() {
    root.classList.remove('motion');
    pending.forEach(function (el) { el.classList.add('in'); });
    pending = [];
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

  // Sunrise: the entrance lifts the sky from first light a little way, then
  // scrolling through the hero carries it the rest of the way to morning.
  var dawn = 0, dawnTarget = 0.24, dawnStart = 0;
  var run = document.querySelector('.hero-run');
  // How far through the night-to-morning the visitor has scrolled: through the
  // pinned run on wide screens, through the first part of the hero on phones.
  function runProgress(vh) {
    if (run && run.offsetHeight > vh * 1.2) {
      var r = run.getBoundingClientRect();
      return clamp(-r.top / (r.height - vh));
    }
    // Phones: the first half screen of scrolling turns the night into morning.
    return clamp(window.scrollY / (vh * 0.6));
  }
  function heroProgress(t) {
    return dawn + (1 - dawn) * t;
  }

  // Phones: how far the phone climbs so it ends just under the bar.
  var riseSet = false;
  function measureRise() {
    riseSet = true;
    var ph = hero && hero.querySelector('.hero-ph');
    if (!ph) return;
    var top = 0, el = ph;
    while (el && el !== hero) { top += el.offsetTop; el = el.offsetParent; }
    if (el !== hero) top = ph.getBoundingClientRect().top - hero.getBoundingClientRect().top;
    hero.style.setProperty('--rise', Math.min(0, 140 - top).toFixed(0) + 'px');
  }
  window.addEventListener('resize', function () { riseSet = false; }, { passive: true });

  var lastPose = -1;
  function placeRunner(p) {
    if (!runner || !trackLen) return;
    var t = 0.12 + p * 0.82;
    var pt = track.getPointAtLength(trackLen * t);
    var scale = 1.9 * (1 - t * 0.78);
    runner.setAttribute('transform', 'translate(' + pt.x.toFixed(1) + ' ' + pt.y.toFixed(1) + ') scale(' + scale.toFixed(3) + ')');
    var pose = Math.floor(t * 60) % 2;
    if (pose !== lastPose) { runner.classList.toggle('b', pose === 1); lastPose = pose; }
  }

  function revealVisible(vh) {
    if (!pending.length) return;
    var limit = vh * 0.88;
    pending = pending.filter(function (el) {
      if (el.getBoundingClientRect().top > limit) return true;
      el.classList.add('in');
      return false;
    });
  }

  var active = -1, swapTimer = 0;
  function story(vh) {
    if (!steps.length) return;
    var mid = vh / 2, best = 0, bestD = Infinity;
    steps.forEach(function (s, i) {
      var r = s.getBoundingClientRect();
      var d = Math.abs(r.top + r.height / 2 - mid);
      if (d < bestD) { bestD = d; best = i; }
    });
    if (best === active) return;
    var first = active === -1;
    active = best;
    steps.forEach(function (s, i) { s.classList.toggle('on', i === best); });
    screens.forEach(function (s, i) { s.classList.toggle('on', i === best); });
    dots.forEach(function (s, i) { s.classList.toggle('on', i === best); });
    if (!first && stage) {
      stage.classList.add('swap');
      clearTimeout(swapTimer);
      swapTimer = setTimeout(function () { stage.classList.remove('swap'); }, 450);
    }
  }

  // Paired phones drift at their own speed relative to the middle of the screen.
  function parallax(vh) {
    pars.forEach(function (el) {
      var r = el.getBoundingClientRect();
      if (r.bottom < -100 || r.top > vh + 100) return;
      var y = (r.top + r.height / 2 - vh / 2) * Number(el.getAttribute('data-par'));
      el.style.setProperty('--py', y.toFixed(1) + 'px');
    });
  }

  // Flyover band: the route draws with scroll, a marker rides its head.
  function flyover(vh) {
    if (!after) return;
    var r = after.getBoundingClientRect();
    if (r.bottom < 0 || r.top > vh) return;
    var p = clamp((vh - r.top) / (r.height + vh * 0.2));
    after.style.setProperty('--rp', p.toFixed(4));
    if (rhead && routeLen) {
      var pt = route.getPointAtLength(routeLen * p);
      rhead.setAttribute('cx', pt.x.toFixed(1));
      rhead.setAttribute('cy', pt.y.toFixed(1));
    }
  }

  // Closing: the sun sets as you reach the bottom of the page.
  function sunset(vh) {
    if (!dusk) return;
    var r = dusk.getBoundingClientRect();
    if (r.top > vh) { dusk.style.setProperty('--dp', '0'); return; }
    var p = clamp((vh - r.top) / (r.height + vh * 0.35));
    dusk.style.setProperty('--dp', p.toFixed(4));
  }

  var frames = 0;
  function frame() {
    try {
      frames++;
      bar.classList.toggle('scrolled', window.scrollY > 24);
      if (!root.classList.contains('motion')) return;
      var vh = window.innerHeight;
      if (hero && hero.getBoundingClientRect().bottom > 0) {
        var t = runProgress(vh);
        var p = heroProgress(t);
        hero.style.setProperty('--p', p.toFixed(4));
        hero.style.setProperty('--sw', clamp((t - 0.22) / 0.32).toFixed(4));
        hero.style.setProperty('--hr', t.toFixed(4));
        if (!riseSet) measureRise();
        hero.classList.toggle('day', t > 0.5);
        placeRunner(p);
      }
      revealVisible(vh);
      if (wide.matches) story(vh);
      parallax(vh);
      flyover(vh);
      sunset(vh);
    } catch (e) { abandon(); }
  }

  var ticking = false;
  function request() {
    if (ticking) return;
    ticking = true;
    var run = function () { if (ticking) { ticking = false; frame(); } };
    requestAnimationFrame(run);
    setTimeout(run, 200);   // frames may never come in a background tab
  }

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
      pending = [].slice.call(document.querySelectorAll('.reveal, .fan, .after'));
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

  window.addEventListener('scroll', request, { passive: true });
  window.addEventListener('resize', request, { passive: true });
  window.addEventListener('load', request);
  window.addEventListener('pageshow', request);
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
  (function blink() {
    setTimeout(function () {
      coaches.forEach(function (c) {
        var r = c.getBoundingClientRect();
        if (r.bottom < 0 || r.top > innerHeight || c.classList.contains('is-glad')) return;
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
    var check = function () {
      if (said) return;
      var r = cc.getBoundingClientRect();
      if (r.top < innerHeight * 0.8 && r.bottom > 0) { said = true; setTimeout(poke, 250); window.removeEventListener('scroll', check); }
    };
    window.addEventListener('scroll', check, { passive: true });
    check();
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
