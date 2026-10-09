(function () {
  try {
    var sec = document.getElementById('engine');
    if (!sec) return;
    var pin = sec.querySelector('.eng-pin');
    var coach = sec.querySelector('.eng-coach .coach');
    var root = document.documentElement;
    var ticking = false, near = false, shown = false, step = 0;
    function c01(v) { return v < 0 ? 0 : v > 1 ? 1 : v; }
    function f(v) { return v.toFixed(3); }
    function update() {
      ticking = false;
      if (!root.classList.contains('motion')) {
        if (step) { step = 0; shown = false; sec.removeAttribute('style'); sec.removeAttribute('data-step'); sec.classList.remove('is-result'); }
        return;
      }
      var r = pin.getBoundingClientRect(), vh = window.innerHeight;
      var span = r.height - vh;
      var p = span > 0 ? c01(-r.top / span) : 1;
      var d = c01((p - 0.74) / 0.16);
      sec.style.setProperty('--a', f(c01(p / 0.28)));
      sec.style.setProperty('--b', f(c01((p - 0.24) / 0.24)));
      sec.style.setProperty('--c', f(c01((p - 0.48) / 0.26)));
      sec.style.setProperty('--d', f(d));
      var s = p < 0.26 ? 1 : p < 0.5 ? 2 : 3;
      if (s !== step) { step = s; sec.setAttribute('data-step', String(s)); }
      var res = d > 0.25;
      if (res !== shown) {
        shown = res;
        sec.classList.toggle('is-result', res);
        if (res && coach && window.AeraCoach) setTimeout(function () { try { window.AeraCoach.play(coach, 'hello'); } catch (e) {} }, 320);
      }
    }
    function onScroll() { if (near && !ticking) { ticking = true; requestAnimationFrame(update); } }
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es) { near = es[0].isIntersecting; if (near) onScroll(); }, { rootMargin: '50% 0px' }).observe(sec);
    } else { near = true; }
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll, { passive: true });
    update();
  } catch (e) {
    try { document.getElementById('engine').removeAttribute('style'); } catch (e2) {}
  }
})();
