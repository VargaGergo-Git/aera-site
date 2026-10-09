/* Aera homepage motion. Everything on the page is readable without this file:
   it only adds the entrance, the sunrise on scroll, the runner, the story
   phone and the reveals. If anything throws, motion is dropped and the page
   stays fully visible. */
(function () {
  var root = document.documentElement;
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hero = document.querySelector('.hero');
  var bar = document.querySelector('.bar');
  var pending = [];
  var steps = [].slice.call(document.querySelectorAll('.step'));
  var screens = [].slice.call(document.querySelectorAll('.stage .scr'));
  var wide = window.matchMedia('(min-width: 900px)');

  var track = document.getElementById('track');
  var runner = document.getElementById('runner');
  var trackLen = 0;
  try { if (track) trackLen = track.getTotalLength(); } catch (e) { trackLen = 0; }

  function abandon() {
    root.classList.remove('motion');
    pending.forEach(function (el) { el.classList.add('in'); });
    pending = [];
    if (hero) hero.style.removeProperty('--p');
  }

  // Sunrise: the entrance lifts the sky from first light a little way, then
  // scrolling through the hero carries it the rest of the way to morning.
  var dawn = 0;
  var dawnTarget = 0.24;
  var dawnStart = 0;

  function heroProgress() {
    var h = hero.offsetHeight || 1;
    var s = Math.min(Math.max(window.scrollY / (h * 0.85), 0), 1);
    return dawn + (1 - dawn) * s;
  }

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

  function revealVisible() {
    if (!pending.length) return;
    var limit = window.innerHeight * 0.88;
    pending = pending.filter(function (el) {
      if (el.getBoundingClientRect().top > limit) return true;
      el.classList.add('in');
      return false;
    });
  }

  var active = -1;
  function story() {
    if (!steps.length) return;
    var mid = window.innerHeight / 2, best = 0, bestD = Infinity;
    steps.forEach(function (s, i) {
      var r = s.getBoundingClientRect();
      var d = Math.abs(r.top + r.height / 2 - mid);
      if (d < bestD) { bestD = d; best = i; }
    });
    if (best === active) return;
    active = best;
    steps.forEach(function (s, i) { s.classList.toggle('on', i === best); });
    screens.forEach(function (s, i) { s.classList.toggle('on', i === best); });
  }

  var frames = 0;
  function frame() {
    try {
      frames++;
      bar.classList.toggle('scrolled', window.scrollY > 24);
      if (root.classList.contains('motion')) {
        if (hero && hero.getBoundingClientRect().bottom > 0) {
          var p = heroProgress();
          hero.style.setProperty('--p', p.toFixed(4));
          placeRunner(p);
        }
        revealVisible();
        if (wide.matches) story();
      }
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

  try {
    if (!reduced) {
      root.classList.add('motion');
      pending = [].slice.call(document.querySelectorAll('.reveal, .rails, .fan, .after'));
      if (hero) hero.style.setProperty('--p', '0');
      placeRunner(0);
      requestAnimationFrame(function () {
        requestAnimationFrame(function () {
          if (hero) hero.classList.add('in');
          requestAnimationFrame(tweenDawn);
        });
      });
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
