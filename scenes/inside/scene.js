/* Inside film: load the 3D film (film.js, with three.js) once the section is
   near, play it when half in view, pause it off screen. Under reduced motion,
   without WebGL or on any error the poster and caption list stay. No scroll reads. */
(function () {
  var box = document.querySelector('.scene-inside .ix-film');
  if (!box) return;
  function still() { box.classList.add('still'); box.classList.remove('live'); }
  try {
    var reduced = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
    var gl = (function () { try { var c = document.createElement('canvas'); return !!(c.getContext('webgl2') || c.getContext('webgl')); } catch (e) { return false; } })();
    if (reduced || !gl || !('IntersectionObserver' in window)) { still(); return; }
    var caps = [].slice.call(box.querySelectorAll('.ix-cap')).map(function (el) {
      var t = el.getAttribute('data-t').split(' '); return { el: el, a: +t[0], b: +t[1], on: false };
    });
    var replay = box.querySelector('.ix-replay');
    var S = JSON.parse(box.querySelector('.ix-strings').textContent);
    var film = null, loading = false, seen = false, visible = false;
    function tick(T) {
      caps.forEach(function (c) { var on = T >= c.a && T < c.b; if (on !== c.on) { c.on = on; c.el.classList.toggle('on', on); } });
      if (film && T >= film.end) { film.pause(); replay.hidden = false; }
    }
    function load() {
      if (loading) return; loading = true;
      import(new URL('scenes/inside/film.js', document.baseURI).href).then(function (m) {
        film = m.start(box.querySelector('.ix-frame'), S); film.onTime(tick);
        film.onSlow(function () { try { film.dispose(); } catch (e) {} film = null; still(); });
        var h = /ix-t=([\d.]+)/.exec(location.hash);
        box.classList.add('live');
        if (h) { film.seek(+h[1]); return; }
        if (visible) { seen = true; film.play(); }
      }).catch(still);
    }
    new IntersectionObserver(function (es) { if (es[0].isIntersecting) load(); }, { rootMargin: '900px 0px' }).observe(box);
    new IntersectionObserver(function (es) {
      visible = es[0].isIntersecting;
      if (!film) return;
      if (visible && replay.hidden && !document.hidden) { seen = true; film.play(); } else film.pause();
    }, { threshold: 0.5 }).observe(box);
    document.addEventListener('visibilitychange', function () {
      if (!film) return;
      if (document.hidden) film.pause(); else if (visible && replay.hidden) film.play();
    });
    replay.addEventListener('click', function () { if (!film) return; replay.hidden = true; film.seek(0); film.play(); });
  } catch (e) { still(); }
})();
