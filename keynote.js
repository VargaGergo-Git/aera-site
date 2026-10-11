/* The home page's motion (scripts/build_keynote.py): sections fade up once as
   they enter, the header gains a backdrop after the first scroll, and the
   replay film plays once when it comes into view. No scroll-driven scenes. */
(function () {
  var d = document, root = d.documentElement;
  var still = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var dark = matchMedia('(prefers-color-scheme: dark)').matches;

  var bar = d.querySelector('.bar');
  var onScroll = function () { bar.classList.toggle('scrolled', scrollY > 8); };
  addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // The film: the light or dark recording to match the page, with its first
  // frame as the poster. Plays once, then rests on the last frame.
  var film = d.querySelector('.film video');
  if (film) {
    if (dark) film.poster = film.getAttribute('data-poster-dark');
    film.src = film.getAttribute(dark ? 'data-dark' : 'data-light');
  }

  if (!('IntersectionObserver' in window)) { if (film && !still) film.play().catch(function () {}); return; }
  root.classList.add('js');
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (!e.isIntersecting) return;
      e.target.classList.add('in');
      io.unobserve(e.target);
    });
  }, { rootMargin: '0px 0px -8% 0px' });
  [].forEach.call(d.querySelectorAll('.reveal'), function (el) { io.observe(el); });

  if (film && !still) {
    var fo = new IntersectionObserver(function (es) {
      if (!es[0].isIntersecting) return;
      fo.disconnect();
      setTimeout(function () { film.play().catch(function () {}); }, 350);
    }, { threshold: 0.6 });
    fo.observe(film);
  }
})();
