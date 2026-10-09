/* Flyover scene: the real Flyover film plays once when half the scene is in
   view and holds on its last frame; "Watch again" replays it. The callouts
   light up as the film reaches each stop (data-stops, fractions of the film).
   A 24x40 canvas samples the film a few times a second so its light spills
   into the stage. The film loads a screen ahead, never with the page.
   Reduced motion or a blocked autoplay: the poster stays and a button plays
   the film on request. On any error the poster frame stays.
   Without a <video> in the section (poster mode) the poster frame shows, both
   callouts light as the phone sets down, and nothing runs per frame.
   Frame guard: if the first 12 frames of the film run at a median over 24 ms,
   the film jumps to its last frame instead of stuttering. */
(function () {
  var sec = document.getElementById('flyover');
  if (!sec) return;
  var root = document.documentElement;
  var video = sec.querySelector('.fo-video');
  var poster = sec.querySelector('.fo-poster');
  var amb = sec.querySelector('.fo-amb');
  var btn = sec.querySelector('.fo-replay');
  var calls = [].slice.call(sec.querySelectorAll('.fo-call'));
  var stops = (sec.getAttribute('data-stops') || '').split(',').map(Number);
  var ctx = null, guard = [], guardT = 0, loaded = false, played = false, inView = false, looping = false, frameNo = 0, broken = false;

  function moving() { return root.classList.contains('motion'); }

  function paint(src) {
    if (!ctx) return;
    try { ctx.drawImage(src, 0, 0, amb.width, amb.height); } catch (e) { /* not ready, or tainted */ }
  }

  function load() {
    if (loaded) return;
    loaded = true;
    [['data-src-mp4', 'video/mp4; codecs="avc1.640028"'], ['data-src-webm', 'video/webm; codecs="vp9"']].forEach(function (s) {
      var url = video.getAttribute(s[0]);
      if (!url || !video.canPlayType(s[1])) return;
      var el = document.createElement('source');
      el.src = url; el.type = s[1];
      video.appendChild(el);
    });
    if (!video.querySelector('source')) { fail(); return; }
    video.preload = 'auto';
    video.load();
  }

  function lightCalls(f) {
    calls.forEach(function (c, i) {
      var on = f >= (stops[i] || 0) - 0.01;
      if (on !== c.classList.contains('on')) c.classList.toggle('on', on);
    });
  }

  function tick(now) {
    if (!looping) return;
    if (guard.length < 12) {
      if (guardT) guard.push(now - guardT);
      guardT = now;
      if (guard.length === 12) {
        var g = guard.slice().sort(function (a, b) { return a - b; });
        if (g[6] > 24) { looping = false; video.pause(); video.currentTime = video.duration || 0; land(); return; }
      }
    }
    var d = video.duration;
    if (d > 0) lightCalls(video.currentTime / d);
    if (frameNo++ % 6 === 0) paint(video);
    requestAnimationFrame(tick);
  }
  function startLoop() { if (!looping) { looping = true; requestAnimationFrame(tick); } }

  function play() {
    load();
    var p = video.play();
    if (p && p.catch) p.catch(function () { if (!video.ended) ask(); });
  }

  function ask() {
    sec.classList.add('fo-ask');
    btn.hidden = false;
  }

  function fail() {
    broken = true;
    looping = false;
    sec.classList.remove('fo-live');
    btn.hidden = true;
    calls.forEach(function (c) { c.classList.add('on'); });
  }

  function land() {
    lightCalls(1);
    paint(video);
    sec.classList.remove('fo-ask');
    btn.hidden = false;
  }

  try {
    ctx = amb.getContext('2d');
    if (poster.complete && poster.naturalWidth) paint(poster);
    else poster.addEventListener('load', function () { paint(poster); });

    if (!video || !btn) {
      var arrive = function () { sec.classList.add('in'); calls.forEach(function (c) { c.classList.add('on'); }); };
      if (!('IntersectionObserver' in window)) { arrive(); return; }
      var io = new IntersectionObserver(function (es) {
        if (es[0].intersectionRatio >= 0.25) { arrive(); io.disconnect(); }
      }, { threshold: [0, 0.25] });
      io.observe(sec.querySelector('.fo-film'));
      return;
    }

    video.addEventListener('playing', function () {
      sec.classList.add('fo-live');
      sec.classList.remove('fo-ask');
      btn.hidden = true;
      startLoop();
    });
    video.addEventListener('pause', function () { looping = false; });
    video.addEventListener('ended', function () { looping = false; land(); });
    video.addEventListener('error', fail, true);

    btn.addEventListener('click', function () {
      if (broken) return;
      guard = []; guardT = 0;
      if (video.ended || video.currentTime > 0.1) {
        video.currentTime = 0;
        if (moving()) calls.forEach(function (c) { c.classList.remove('on'); });
      }
      played = true;
      play();
    });

    if (!('IntersectionObserver' in window)) {
      if (!moving()) ask();
      return;
    }

    // A screen ahead: fetch the film so it is ready when the scene arrives.
    new IntersectionObserver(function (es) {
      if (es[0].isIntersecting) load();
    }, { rootMargin: '100% 0px 100% 0px' }).observe(sec);

    var film = sec.querySelector('.fo-film');
    new IntersectionObserver(function (es) {
      var e = es[0];
      inView = e.intersectionRatio > 0;
      if (e.intersectionRatio >= 0.25) sec.classList.add('in');
      if (!moving()) { if (!played && btn.hidden && !broken) ask(); return; }
      if (broken) return;
      if (e.intersectionRatio >= 0.55 && !played) { played = true; play(); }
      else if (!inView && !video.paused) video.pause();
      else if (e.intersectionRatio >= 0.55 && played && video.paused && !video.ended && video.currentTime > 0) play();
    }, { threshold: [0, 0.25, 0.55] }).observe(film);
  } catch (e) {
    try { fail(); } catch (e2) { /* the poster stays */ }
  }
})();
