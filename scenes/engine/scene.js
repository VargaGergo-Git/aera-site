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
    var ticking = false, step = 0, isWord = false, isLanded = false, wordCss = '', wordW = 0, wordH = 0, headBottom = 0;
    // Plays once, like a film, when the stage is half in view, then holds on the last frame.
    var DUR = 7000, t0 = 0, done = false;
    // Where "Good to go" sits on the 400 x 870 capture: centre and width.
    var TX = 144 / 400, TY = 284 / 870, TW = 248 / 400;
    function c01(v) { return v < 0 ? 0 : v > 1 ? 1 : v; }
    function seg(p, a, b) { return c01((p - a) / (b - a)); }
    function ease(t) { return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; }
    // Only changed values are written: an unchanged write still restyles the whole scene.
    var vals = {};
    function set(k, v) { var s = typeof v === 'number' ? v.toFixed(3) : v; if (vals[k] !== s) { vals[k] = s; sec.style.setProperty(k, s); } }
    // Geometry for the film, read once (and on resize) so no frame ever forces a layout.
    // G.dev*: the phone at rest; G.img*: the capture inside it; G.orb*: the orb relative
    // to the board's centre at full size. Frames map these through the current transforms.
    var G = null;
    function measure() {
      wordW = word.offsetWidth; wordH = word.offsetHeight;
      head.style.transform = 'none';
      headBottom = head.offsetTop + head.offsetHeight;
      head.style.transform = '';
      set('--dev-top', (headBottom + 18) + 'px');
      var vh0 = stage.clientHeight || window.innerHeight, vw0 = window.innerWidth;
      var room = vh0 - headBottom - 18 - (vw0 < 900 ? 44 : 28);
      set('--dev-w', Math.max(150, Math.min(vw0 * .66, 360, room / 2.2)) + 'px');
      var caps = sec.querySelector('.eng-caps');
      var capsTop = vh0 - (caps ? caps.offsetHeight : 90) - Math.max(22, vh0 * .03);
      var avail = capsTop - headBottom - 28;
      var bw = Math.max(240, Math.min(vw0 - 32, 600, (avail - 44) / 1.05 + 44));
      set('--board-w', bw + 'px');
      set('--board-y', ((headBottom + capsTop) / 2) + 'px');
      // Read the resting frame: board risen, nothing faded, phone in place.
      var keep = ['--rise', '--fade', '--dev'].map(function (k) { return sec.style.getPropertyValue(k); });
      sec.style.setProperty('--rise', '1'); sec.style.setProperty('--fade', '0'); sec.style.setProperty('--dev', '1');
      var st = stage.getBoundingClientRect(), dev = sec.querySelector('.eng-device').getBoundingClientRect();
      var bd = sec.querySelector('.eng-board').getBoundingClientRect();
      var ir = img ? img.getBoundingClientRect() : dev, o = orb ? orb.getBoundingClientRect() : bd;
      G = {
        w: st.width, h: st.height,
        dcx: dev.left - st.left + dev.width / 2, dcy: dev.top - st.top + dev.height / 2,
        tx: ir.left - st.left + ir.width * TX, ty: ir.top - st.top + ir.height * TY, tw: ir.width * TW,
        bcx: bd.left - st.left + bd.width / 2, bcy: bd.top - st.top + bd.height / 2,
        ox: o.left + o.width / 2 - (bd.left + bd.width / 2), oy: o.top + o.height / 2 - (bd.top + bd.height / 2)
      };
      ['--rise', '--fade', '--dev'].forEach(function (k, i) { if (keep[i]) sec.style.setProperty(k, keep[i]); else sec.style.removeProperty(k); });
    }
    function clear() {
      ['--a', '--b', '--c', '--d', '--hy', '--rise', '--fade', '--dev', '--bx', '--by', '--bs', '--bo', '--glow', '--mk', '--dev-top', '--dev-w', '--board-w', '--board-y'].forEach(function (k) { sec.style.removeProperty(k); });
      sec.removeAttribute('data-step'); sec.classList.remove('is-word', 'is-landed');
      word.style.transform = ''; word.style.opacity = '';
      step = 0; isWord = false; isLanded = false; wordCss = ''; vals = {};
    }
    function update() {
      ticking = false;
      if (!root.classList.contains('motion')) { if (step) clear(); return; }
      if (!wordW || !G) measure();
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
      var landed = p > .88;
      if (landed !== isLanded) { isLanded = landed; sec.classList.toggle('is-landed', landed); }

      // Bloom: a burst of light where the three streams meet.
      var bl = seg(p, .55, .78);
      if (bl > 0 && bl < 1) {
        var bsc = 1 - .14 * ease(seg(p, .56, .68));
        set('--bx', (G.bcx + G.ox * bsc) + 'px');
        set('--by', (G.bcy + G.oy * bsc) + 'px');
      }
      set('--bs', bl <= 0 ? 0 : .05 + Math.sin(Math.min(bl, 1) * Math.PI * .5) * 2.4);
      set('--bo', bl <= 0 || bl >= 1 ? 0 : Math.sin(bl * Math.PI) * .9);

      // The word: appears big in the middle, then lands on the real screen.
      var wa = ease(seg(p, .6, .7));
      set('--glow', Math.sin(seg(p, .62, .82) * Math.PI));
      var cx = G.w / 2, cy = G.h * .52;
      var k = ease(seg(p, .74, .9));
      var s0 = .82 + .18 * wa, x = cx, y = cy, sc = s0, op = wa;
      if (k > 0) {
        if (flip) {
          // Where "Good to go" sits on the capture right now: the resting spot mapped
          // through the phone's current rise and scale (about its own centre).
          var ds = .9 + dev * .1, dy = (1 - dev) * .7 * G.h;
          var tx = G.dcx + (G.tx - G.dcx) * ds, ty = G.dcy + (G.ty - G.dcy) * ds + dy;
          var ts = (G.tw * ds) / wordW;
          x = cx + (tx - cx) * k; y = cy + (ty - cy) * k; sc = s0 + (ts - s0) * k;
          op = wa * (1 - seg(p, .9, .95));
        } else {
          y = cy - k * G.h * .08; sc = s0 * (1 - .3 * k); op = wa * (1 - k);
        }
      }
      set('--mk', 1 - seg(p, .895, .93));
      var css = op.toFixed(3) + '|translate3d(' + (x - wordW * sc / 2).toFixed(1) + 'px,' + (y - wordH * sc / 2).toFixed(1) + 'px,0) scale(' + sc.toFixed(4) + ')';
      if (css !== wordCss) { wordCss = css; var cut = css.indexOf('|'); word.style.opacity = css.slice(0, cut); word.style.transform = css.slice(cut + 1); }
    }
    function frame() { update(); if (t0 && !done) requestAnimationFrame(frame); }
    function play() { if (t0 || done) return; t0 = performance.now(); requestAnimationFrame(frame); }
    function redraw() { if (!ticking) { ticking = true; requestAnimationFrame(update); } }
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es) { if (es[0].isIntersecting) play(); }, { threshold: .5 }).observe(stage);
      // Scrolled away mid-film: jump to the last frame instead of animating off screen.
      new IntersectionObserver(function (es) { if (!es[0].isIntersecting && t0 && !done) { done = true; redraw(); } }).observe(stage);
    } else { done = true; }
    window.addEventListener('resize', function () { wordW = 0; redraw(); }, { passive: true });
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { wordW = 0; redraw(); });
    update();
  } catch (e) {
    try { var s2 = document.getElementById('engine'); s2.removeAttribute('style'); s2.classList.add('eng-off'); } catch (e2) {}
  }
})();
