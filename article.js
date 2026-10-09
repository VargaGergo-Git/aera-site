// Aera articles: fade blocks up once as they arrive. Opacity and transform only.
(function () {
  if (!('IntersectionObserver' in window) || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var els = document.querySelectorAll('.legal > .fig, .legal > .shot, .legal > .keys, .legal > .pull, .legal > .note');
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -12% 0px' });
  els.forEach(function (el) {
    if (el.getBoundingClientRect().top < innerHeight * 0.9) return;
    el.classList.add('rv'); io.observe(el);
    el.querySelectorAll('.dot').forEach(function (d, i) { d.style.transitionDelay = (i * 18) + 'ms'; });
  });
})();
