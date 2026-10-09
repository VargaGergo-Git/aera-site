/* Route planner scene: one scroll-scrubbed timeline through the pinned stage.
   Beat 1 (0 to .46): taps, the line follows the paths to each tap, distance counts.
   Beat 2 (.46 to .64): what you will meet pops up along the line.
   Beat 3 (.64 to 1): the map tilts away, the phone and the watch rise, the arrow turns.
   Without .motion, or on any error, the markup's final frame stays. */
(function () {
  try {
    var sec = document.getElementById('planner');
    if (!sec) return;
    var root = document.documentElement;
    var run = sec.querySelector('.pl-run');
    var paths = ['planner-route', 'planner-case', 'planner-glow'].map(function (id) { return document.getElementById(id); });
    var route = paths[0];
    var head = document.getElementById('planner-head');
    var comet = document.getElementById('planner-comet');
    var pins = [].slice.call(sec.querySelectorAll('.pl-pin'));
    var finger = document.getElementById('planner-finger');
    var rips = [].slice.call(sec.querySelectorAll('.pl-rip'));
    var dots = [].slice.call(sec.querySelectorAll('.pl-wp'));
    var guides = [].slice.call(sec.querySelectorAll('.pl-g'));
    var says = [].slice.call(sec.querySelectorAll('.pl-say'));
    var beats = [].slice.call(sec.querySelectorAll('.pl-rail li'));
    var num = sec.querySelector('.pl-num');
    if (!run || !route || !num) return;

    var KM = parseFloat(num.getAttribute('data-km')) || 6.4;
    var finalText = num.textContent;
    var lang = (root.getAttribute('lang') || 'en').slice(0, 2);
    var nf;
    try { nf = new Intl.NumberFormat(lang, { minimumFractionDigits: 1, maximumFractionDigits: 1 }); }
    catch (e) { nf = { format: function (v) { return v.toFixed(1); } }; }

    var L = route.getTotalLength();
    var wp = rips.map(function (c) { return { x: +c.getAttribute('cx'), y: +c.getAttribute('cy') }; });
    // Where each tap sits along the line, by nearest sample.
    function near(px, py) {
      var best = 0, bd = Infinity;
      for (var i = 0; i <= 500; i++) {
        var q = route.getPointAtLength(L * i / 500);
        var d = (q.x - px) * (q.x - px) + (q.y - py) * (q.y - py);
        if (d < bd) { bd = d; best = i / 500; }
      }
      return best;
    }
    var fr = wp.map(function (p) { return near(p.x, p.y); });
    fr[0] = 0; fr[fr.length - 1] = 1;
    // Pins pop as the light travelling along the line reaches them.
    var pf = pins.map(function (el) {
      var x = parseFloat(el.style.left) * 6, y = parseFloat(el.style.top) * 6.4;
      return near(x, y);
    });

    function clamp(v) { return v < 0 ? 0 : v > 1 ? 1 : v; }
    function out(v) { return 1 - Math.pow(1 - v, 3); }
    function inOut(v) { return v < 0.5 ? 4 * v * v * v : 1 - Math.pow(-2 * v + 2, 3) / 2; }
    function back(v) { if (v <= 0) return 0; if (v >= 1) return 1; var c = 1.7, c3 = c + 1; return 1 + c3 * Math.pow(v - 1, 3) + c * Math.pow(v - 1, 2); }
    function set(k, v) { sec.style.setProperty(k, v.toFixed(4)); }

    var VARS = ['--k', '--w', '--ph', '--turn', '--p0', '--p1', '--p2', '--b1', '--b2', '--b3'];
    var dead = false, live = false, shown = 0, target = 0, lastText = '', lastBeat = -1, buzz = false;

    function reset() {
      VARS.forEach(function (k) { sec.style.removeProperty(k); });
      paths.forEach(function (p) { if (p) { p.style.strokeDasharray = ''; p.style.strokeDashoffset = ''; } });
      [head, finger, comet].concat(rips, dots, guides).forEach(function (el) { if (el) el.removeAttribute('style'); });
      num.textContent = finalText;
      says.forEach(function (s, i) { s.classList.toggle('on', i === 0); });
      sec.classList.remove('pl-buzz');
      live = false; lastText = ''; lastBeat = -1;
    }

    function paint(t) {
      // Beat 1: the first tap, then three segments, each: finger travels, tap, line follows the paths.
      var d = 0, fx = wp[0].x, fy = wp[0].y;
      var fo = clamp(t / 0.04) * (1 - clamp((t - 0.46) / 0.04));
      var rip = [clamp((t - 0.035) / 0.06)];
      var gd = [];
      for (var j = 0; j < 3; j++) {
        var s = clamp((t - (0.08 + j * 0.125)) / 0.125);
        var m = inOut(clamp(s / 0.24));
        if (s > 0) { fx = wp[j].x + (wp[j + 1].x - wp[j].x) * m; fy = wp[j].y + (wp[j + 1].y - wp[j].y) * m; }
        rip.push(clamp((s - 0.2) / 0.28));
        gd.push(clamp((s - 0.18) / 0.08) * (1 - clamp((s - 0.86) / 0.14)));
        if (s > 0.3) d = fr[j] + (fr[j + 1] - fr[j]) * inOut(clamp((s - 0.3) / 0.7));
      }
      var dash = (L * (1 - d)).toFixed(1);
      paths.forEach(function (p) { if (p) { p.style.strokeDasharray = L.toFixed(1) + ' ' + (L + 2).toFixed(1); p.style.strokeDashoffset = dash; } });
      if (head) {
        var hp = route.getPointAtLength(L * d);
        head.setAttribute('cx', hp.x.toFixed(1));
        head.setAttribute('cy', hp.y.toFixed(1));
        head.style.opacity = d > 0.002 && t < 0.47 ? 1 : 0;
      }
      if (finger) {
        finger.setAttribute('transform', 'translate(' + fx.toFixed(1) + ' ' + fy.toFixed(1) + ')');
        finger.style.opacity = fo.toFixed(3);
      }
      rips.forEach(function (c, i) {
        var r = rip[i] || 0;
        c.setAttribute('r', (6 + r * 24).toFixed(1));
        c.style.opacity = r > 0 && r < 1 ? (1 - r).toFixed(3) : 0;
        if (dots[i]) dots[i].style.opacity = clamp(r * 4).toFixed(3);
      });
      guides.forEach(function (g, i) { g.style.opacity = (gd[i] * 0.85).toFixed(3); });
      var text = nf.format(Math.round(KM * d * 10) / 10);
      if (text !== lastText) { num.textContent = text; lastText = text; }

      // Beat 2: what you will meet.
      var c = clamp((t - 0.465) / 0.15);
      if (comet) {
        var cp = route.getPointAtLength(L * c);
        comet.setAttribute('cx', cp.x.toFixed(1));
        comet.setAttribute('cy', cp.y.toFixed(1));
        comet.style.opacity = (clamp(c * 12) * (1 - clamp((c - 0.97) / 0.03))).toFixed(3);
      }
      pf.forEach(function (f, i) {
        var at = 0.465 + 0.15 * f - 0.01;
        set('--p' + i, back(clamp((t - at) / 0.06)));
      });

      // Beat 3: to your wrist.
      set('--k', inOut(clamp((t - 0.64) / 0.22)));
      set('--ph', out(clamp((t - 0.68) / 0.16)));
      set('--w', out(clamp((t - 0.72) / 0.16)));
      set('--turn', inOut(clamp((t - 0.87) / 0.08)));
      var bz = t > 0.93;
      if (bz !== buzz) { buzz = bz; sec.classList.toggle('pl-buzz', bz); }

      set('--b1', clamp(t / 0.46));
      set('--b2', clamp((t - 0.46) / 0.18));
      set('--b3', clamp((t - 0.64) / 0.31));
      var beat = t < 0.46 ? 0 : t < 0.64 ? 1 : 2;
      if (beat !== lastBeat) {
        lastBeat = beat;
        says.forEach(function (s, i) { s.classList.toggle('on', i === beat); });
        beats.forEach(function (s, i) { s.classList.toggle('on', i === beat); });
      }
    }

    function progress() {
      var r = run.getBoundingClientRect();
      var vh = window.innerHeight;
      var span = r.height - vh;
      if (span < 10) return 1;
      return clamp(-r.top / span);
    }

    var ticking = false, easing = false;
    function step() {
      easing = false;
      try {
        if (!root.classList.contains('motion')) { if (live) reset(); return; }
        var delta = target - shown;
        shown = Math.abs(delta) < 0.0008 ? target : shown + delta * 0.16;
        live = true;
        paint(shown);
        if (shown !== target) { easing = true; requestAnimationFrame(step); }
      } catch (e) { dead = true; reset(); }
    }
    function frame() {
      ticking = false;
      if (dead) return;
      try {
        if (!root.classList.contains('motion')) { if (live) reset(); return; }
        var r = run.getBoundingClientRect(), vh = window.innerHeight;
        if (r.bottom < -vh * 0.3 || r.top > vh * 1.3) return;   // far away: rest
        target = progress();
        if (!live) shown = target;
        if (!easing) { easing = true; requestAnimationFrame(step); }
      } catch (e) { dead = true; reset(); }
    }
    function request() {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(frame);
    }
    window.addEventListener('scroll', request, { passive: true });
    window.addEventListener('resize', request, { passive: true });
    window.addEventListener('load', request);
    request();
  } catch (e) { /* the final frame in the markup stays */ }
})();
