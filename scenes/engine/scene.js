(function () {
  try {
    var sec = document.getElementById('engine');
    if (!sec) return;
    var root = document.documentElement;
        var stage = sec.querySelector('.eng-stage');
    var head = sec.querySelector('.eng-head');
    var word = sec.querySelector('.eng-word');
    var orb = sec.querySelector('.eng-orb .core');
    var img = sec.querySelector('.eng-device img');
    var flip = sec.getAttribute('data-flip') === '1';
    var ticking = false, step = 0, isWord = false, wordW = 0, wordH = 0, headBottom = 0;
    // Plays once, like a film, when the stage is half in view, then holds on the last frame.
    var DUR = 7000, t0 = 0, done = false;
    // Where "Good to go" sits on the 400 x 870 capture: centre and width.
    var TX = 144 / 400, TY = 284 / 870, TW = 248 / 400;
    function c01(v) { return v < 0 ? 0 : v > 1 ? 1 : v; }
    function seg(p, a, b) { return c01((p - a) / (b - a)); }
    function ease(t) { return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; }
    function set(k, v) { sec.style.setProperty(k, typeof v === 'number' ? v.toFixed(4) : v); }
    function measure() {
      wordW = word.offsetWidth; wordH = word.offsetHeight;
      head.style.transform = 'none';
      headBottom = head.offsetTop + head.offsetHeight;
      head.style.transform = '';
      set('--dev-top', (headBottom + 18) + 'px');
      var vh0 = window.innerHeight, vw0 = window.innerWidth;
      var room = vh0 - headBottom - 18 - (vw0 < 900 ? 44 : 28);
      set('--dev-w', Math.max(150, Math.min(vw0 * .66, 360, room / 2.2)) + 'px');
      var caps = sec.querySelector('.eng-caps');
      var capsTop = vh0 - (caps ? caps.offsetHeight : 90) - Math.max(22, vh0 * .03);
      var avail = capsTop - headBottom - 28;
      var bw = Math.max(240, Math.min(vw0 - 32, 600, (avail - 44) / 1.05 + 44));
      set('--board-w', bw + 'px');
      set('--board-y', ((headBottom + capsTop) / 2) + 'px');
    }
    function clear() {
      ['--a', '--b', '--c', '--d', '--hy', '--rise', '--fade', '--dev', '--bx', '--by', '--bs', '--bo', '--sweep', '--mk', '--dev-top', '--dev-w', '--board-w', '--board-y'].forEach(function (k) { sec.style.removeProperty(k); });
      sec.removeAttribute('data-step'); sec.classList.remove('is-word', 'is-landed');
      word.style.transform = ''; word.style.opacity = '';
      step = 0; isWord = false;
    }
    function update() {
      ticking = false;
      if (!root.classList.contains('motion')) { if (step) clear(); return; }
      if (!wordW) measure();
      var p = done ? 1 : t0 ? c01((performance.now() - t0) / DUR) : 0;
      if (p >= 1) done = true;
      set('--hy', 1 - ease(seg(p, 0, .16)));
      set('--rise', ease(seg(p, .03, .2)));
      set('--a', seg(p, .12, .32));
      set('--b', seg(p, .27, .42));
      set('--c', seg(p, .4, .54));
      set('--d', seg(p, .5, .58));
      set('--fade', ease(seg(p, .56, .68)));
      var dev = ease(seg(p, .7, .86));
      set('--dev', dev);
      var s = p < .27 ? 1 : p < .46 ? 2 : p < .74 ? 3 : 4;
      if (s !== step) { step = s; sec.setAttribute('data-step', String(s)); }
      var w = p > .55;
      if (w !== isWord) { isWord = w; sec.classList.toggle('is-word', w); }
      sec.classList.toggle('is-landed', p > .88);

      var st = stage.getBoundingClientRect();
      // Bloom: a burst of light where the three streams meet.
      var bl = seg(p, .55, .78);
      if (bl > 0 && bl < 1 && orb) {
        var o = orb.getBoundingClientRect();
        set('--bx', (o.left + o.width / 2 - st.left) + 'px');
        set('--by', (o.top + o.height / 2 - st.top) + 'px');
      }
      set('--bs', bl <= 0 ? 0 : .05 + Math.sin(Math.min(bl, 1) * Math.PI * .5) * 2.4);
      set('--bo', bl <= 0 || bl >= 1 ? 0 : Math.sin(bl * Math.PI) * .9);

      // The word: appears big in the middle, then lands on the real screen.
      var wa = ease(seg(p, .6, .7));
      set('--sweep', seg(p, .62, .78));
      var cx = st.width / 2, cy = st.height * .52;
      var k = ease(seg(p, .74, .9));
      var s0 = .82 + .18 * wa, x = cx, y = cy, sc = s0, op = wa;
      if (k > 0 && img) {
        var ir = img.getBoundingClientRect();
        if (flip) {
          var tx = ir.left - st.left + ir.width * TX, ty = ir.top - st.top + ir.height * TY;
          var ts = (ir.width * TW) / wordW;
          x = cx + (tx - cx) * k; y = cy + (ty - cy) * k; sc = s0 + (ts - s0) * k;
          op = wa * (1 - seg(p, .9, .95));
        } else {
          y = cy - k * st.height * .08; sc = s0 * (1 - .3 * k); op = wa * (1 - k);
        }
      }
      set('--mk', 1 - seg(p, .895, .93));
      word.style.opacity = op.toFixed(3);
      word.style.transform = 'translate3d(' + (x - wordW * sc / 2).toFixed(1) + 'px,' + (y - wordH * sc / 2).toFixed(1) + 'px,0) scale(' + sc.toFixed(4) + ')';
    }
    function frame() { update(); if (t0 && !done) requestAnimationFrame(frame); }
    function play() { if (t0 || done) return; t0 = performance.now(); requestAnimationFrame(frame); }
    function redraw() { if (!ticking) { ticking = true; requestAnimationFrame(update); } }
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es) { if (es[0].isIntersecting) play(); }, { threshold: .5 }).observe(stage);
    } else { done = true; }
    window.addEventListener('resize', function () { wordW = 0; redraw(); }, { passive: true });
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { wordW = 0; redraw(); });
    update();
  } catch (e) {
    try { var s2 = document.getElementById('engine'); s2.removeAttribute('style'); s2.classList.add('eng-off'); } catch (e2) {}
  }
})();
