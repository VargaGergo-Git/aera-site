/* The home page's motion (scripts/build_keynote.py): sections fade up once as
   they enter, the header gains a backdrop after the first scroll, one 3D
   replay plays while in view and walks through its places, the route phone's
   screens take turns, and the share cards fan in. The page always scrolls
   natively; nothing pins or hijacks it. */
(function () {
  var d = document, root = d.documentElement;
  var still = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var dark = matchMedia('(prefers-color-scheme: dark)').matches;

  var bar = d.querySelector('.bar');
  var onScroll = function () { bar.classList.toggle('scrolled', scrollY > 8); };
  addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Share rail: arrows page by one card.
  var rail = d.querySelector('.rail');
  if (rail) {
    var prev = d.querySelector('.rail-btn.prev'), next = d.querySelector('.rail-btn.next');
    var step = function () { var c = rail.querySelector('.card'); return c ? c.getBoundingClientRect().width + 16 : 300; };
    var ends = function () { prev.disabled = rail.scrollLeft < 4; next.disabled = rail.scrollLeft + rail.clientWidth > rail.scrollWidth - 4; };
    prev.addEventListener('click', function () { rail.scrollBy({ left: -step(), behavior: still ? 'auto' : 'smooth' }); });
    next.addEventListener('click', function () { rail.scrollBy({ left: step(), behavior: still ? 'auto' : 'smooth' }); });
    rail.addEventListener('scroll', ends, { passive: true }); addEventListener('resize', ends); ends();
  }

  // Fly any run again: one replay at a time. It plays while in view, moves on
  // to the next place when it ends, and a tab picks the place. With reduced
  // motion nothing plays until the video is tapped.
  var clip = d.querySelector('.player video'), tabs = [].slice.call(d.querySelectorAll('.tabs button'));
  var seen = false;
  var pick = function (i, play) {
    tabs.forEach(function (t, j) { t.setAttribute('aria-selected', j === i ? 'true' : 'false'); });
    var t = tabs[i];
    clip.poster = t.getAttribute('data-poster'); clip.setAttribute('data-src', t.getAttribute('data-src'));
    clip.setAttribute('aria-label', t.getAttribute('data-label'));
    clip.removeAttribute('src'); clip.load();
    if (play) { clip.src = t.getAttribute('data-src'); clip.play().catch(function () {}); }
  };
  if (clip) {
    tabs.forEach(function (t, i) { t.addEventListener('click', function () { pick(i, seen && !still); }); });
    clip.addEventListener('ended', function () {
      var i = tabs.findIndex(function (t) { return t.getAttribute('aria-selected') === 'true'; });
      pick((i + 1) % tabs.length, true);
    });
    clip.addEventListener('click', function () {
      if (!clip.src) clip.src = clip.getAttribute('data-src');
      if (clip.paused) clip.play().catch(function () {}); else clip.pause();
    });
  }

  // Route phone: its screens take turns while it is in view.
  var cycle = d.querySelector('.phone.cycle'), turn = null;
  var spin = function (on) {
    if (!cycle || still) return;
    if (on && !turn) {
      var shots = cycle.querySelectorAll('img'), i = 0;
      turn = setInterval(function () {
        shots[i].classList.add('alt'); i = (i + 1) % shots.length; shots[i].classList.remove('alt');
      }, 3200);
    } else if (!on && turn) { clearInterval(turn); turn = null; }
  };

  if (!('IntersectionObserver' in window)) return;
  if (clip && !still) {
    new IntersectionObserver(function (es) {
      seen = es[0].isIntersecting;
      if (seen) { if (!clip.src) clip.src = clip.getAttribute('data-src'); clip.play().catch(function () {}); } else clip.pause();
    }, { threshold: 0.5 }).observe(clip);
  }
  if (cycle) new IntersectionObserver(function (es) { spin(es[0].isIntersecting); }, { threshold: 0.5 }).observe(cycle);
  root.classList.add('js');
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (!e.isIntersecting) return;
      e.target.classList.add('in');
      io.unobserve(e.target);
    });
  }, { rootMargin: '0px 0px -8% 0px' });
  [].forEach.call(d.querySelectorAll('.reveal'), function (el) { io.observe(el); });

})();
