/* Inside scene: arm the play-once motion, start it when the stack is in view,
   and pause the slow sway while it is off screen. No scroll reads. */
(function () {
  try {
    var s = document.querySelector('.scene-inside');
    if (!s || !('IntersectionObserver' in window)) return;
    if (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    var stage = s.querySelector('.ix-stage');
    s.classList.add('armed');
    new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting) { s.classList.add('play'); s.classList.remove('off'); }
        else if (s.classList.contains('play')) s.classList.add('off');
      });
    }, { threshold: 0.45 }).observe(stage);
  } catch (err) {
    var x = document.querySelector('.scene-inside');
    if (x) x.classList.remove('armed');
  }
})();
