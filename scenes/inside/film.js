/* Inside film: a 27-second real-time 3D sequence of how today's session is made.
   Last night's three sleeps, seven mornings of heart against 28 nights, a week of
   training against the four before, four checks, a length from your own runs,
   and the card. Every number on screen follows the app's engine rules
   (TrainingReadinessEngine, TodaysSessionEngine). Loaded only near view by
   scene.js; the poster stands in for it under reduced motion or without WebGL. */
import * as THREE from '../../assets/vendor/three-0.160.0.module.min.js';

var END = 27.4;

function clamp(x, a, b) { return x < a ? a : x > b ? b : x; }
function ease(p) { return p < .5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2; }
function out(p) { return 1 - Math.pow(1 - p, 3); }
function back(p) { var c = 1.6; return 1 + (c + 1) * Math.pow(p - 1, 3) + c * Math.pow(p - 1, 2); }
function prog(T, t0, t1) { return clamp((T - t0) / (t1 - t0), 0, 1); }

// A small fixed random, so the film is identical every play.
function rng(seed) { return function () { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; }; }
function gauss(r) { return Math.sqrt(-2 * Math.log(r() + 1e-9)) * Math.cos(2 * Math.PI * r()); }

export function start(host, S) {
  var R = rng(11);
  var canvas = document.createElement('canvas');
  canvas.className = 'ix-canvas';
  host.appendChild(canvas);
  var renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, powerPreference: 'default' });
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.NoToneMapping; // flat, painted colours, like the homepage valley

  // Aera's valley: the film runs from last night to this morning, so the sky
  // moves from night through dawn to a clear morning (colours from home.css).
  var scene = new THREE.Scene();
  var fogCol = new THREE.Color('#57395b');
  scene.fog = new THREE.FogExp2(fogCol, 0.0075);
  var camera = new THREE.PerspectiveCamera(34, 16 / 9, 0.1, 400);
  var hemi = new THREE.HemisphereLight(0xf4f1e6, 0x9aa57a, 1.5); scene.add(hemi);
  var sunLight = new THREE.DirectionalLight(0xfff1cf, .2); sunLight.position.set(40, 30, -30); scene.add(sunLight);
  var fill = new THREE.DirectionalLight(0xffffff, .5); fill.position.set(-10, 12, 20); scene.add(fill);

  var C = { sleep: new THREE.Color('#7b79ff'), heart: new THREE.Color('#e2335f'), load: new THREE.Color('#e46f22'),
            ok: new THREE.Color('#23966f'), gold: new THREE.Color('#d8b25e'), white: new THREE.Color('#ffffff'),
            ink: new THREE.Color('#26252b'), wood: new THREE.Color('#9c7a52'), stone: new THREE.Color('#d9d0bb') };

  // Soft round light, used for every glow, bokeh and dust mote.
  var gc = document.createElement('canvas'); gc.width = gc.height = 128;
  var g = gc.getContext('2d'), gr = g.createRadialGradient(64, 64, 0, 64, 64, 64);
  gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(.25, 'rgba(255,255,255,.55)');
  gr.addColorStop(.6, 'rgba(255,255,255,.12)'); gr.addColorStop(1, 'rgba(255,255,255,0)');
  g.fillStyle = gr; g.fillRect(0, 0, 128, 128);
  var glowTex = new THREE.CanvasTexture(gc); glowTex.colorSpace = THREE.SRGBColorSpace;

  var disposables = [];
  function track(o) { disposables.push(o); return o; }
  function glow(color, size, opacity) {
    var m = track(new THREE.SpriteMaterial({ map: glowTex, color: color, transparent: true, opacity: opacity, blending: THREE.AdditiveBlending, depthWrite: false, fog: true }));
    var s = new THREE.Sprite(m); s.scale.set(size, size, 1); s.userData.o = opacity; return s;
  }
  function lam(color, o) { o = o || {}; o.color = color; return track(new THREE.MeshLambertMaterial(o)); }
  function basic(color, opacity, additive) {
    return track(new THREE.MeshBasicMaterial({ color: color, transparent: opacity < 1, opacity: opacity, depthWrite: !additive && opacity >= 1,
      blending: THREE.NormalBlending }));
  }
  // A field-guide tag: ink on a paper pill, so it reads at night and by day.
  function label(text, color, h, bare) {
    var c = document.createElement('canvas'), x = c.getContext('2d');
    var px = 64, pad = bare ? 12 : 40, f = '700 ' + px + 'px ui-rounded, "SF Pro Rounded", system-ui, -apple-system, sans-serif';
    x.font = f; var w = Math.ceil(x.measureText(text).width) + pad * 2; c.width = w; c.height = px + (bare ? 28 : 56);
    if (!bare) {
      var r = c.height / 2; x.beginPath(); x.moveTo(r, 2); x.lineTo(w - r, 2); x.arc(w - r, r, r - 2, -Math.PI / 2, Math.PI / 2); x.lineTo(r, c.height - 2); x.arc(r, r, r - 2, Math.PI / 2, Math.PI * 1.5); x.closePath();
      x.fillStyle = 'rgba(251,247,238,.94)'; x.fill(); x.lineWidth = 3; x.strokeStyle = 'rgba(38,37,43,.14)'; x.stroke();
    }
    x.font = f; x.fillStyle = color; x.textBaseline = 'middle'; x.fillText(text, pad, c.height / 2 + 3);
    var t = track(new THREE.CanvasTexture(c)); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4;
    var m = track(new THREE.SpriteMaterial({ map: t, transparent: true, depthWrite: false, fog: false }));
    var s = new THREE.Sprite(m); s.scale.set(h * c.width / c.height, h, 1); s.center.set(0, .5); return s;
  }
  // A glowing line drawn on along its length: a core tube and a wide soft one.
  function strand(curve, color, r, segs, bright) {
    var grp = new THREE.Group();
    var core = new THREE.Mesh(track(new THREE.TubeGeometry(curve, segs, r, 8, false)), lam(color, { emissive: color, emissiveIntensity: .35, transparent: bright < 1, opacity: bright }));
    var halo = new THREE.Mesh(track(new THREE.TubeGeometry(curve, segs, r * 3.2, 8, false)), track(new THREE.MeshBasicMaterial({ color: color, transparent: true, opacity: .12 * bright, depthWrite: false })));
    grp.add(halo, core);
    var head = glow(C.white, r * 26, .85 * bright); grp.add(head);
    grp.userData = { curve: curve, parts: [core, halo], head: head };
    return grp;
  }
  function drawTo(st, p) {
    st.userData.parts.forEach(function (m) {
      var n = m.geometry.index.count; m.geometry.setDrawRange(0, Math.floor(n * p / 6) * 6); m.visible = p > 0;
    });
    var h = st.userData.head; h.visible = p > 0 && p < 1;
    if (h.visible) h.position.copy(st.userData.curve.getPointAt(clamp(p, 0, 1)));
  }
  function fade(obj, a) {
    obj.traverse(function (o) {
      if (!o.material) return;
      if (o.userData.o === undefined) o.userData.o = o.material.opacity;
      o.material.opacity = o.userData.o * a; o.visible = a > 0.001;
    });
  }

  // Sky dome: three colours, night to dawn to morning.
  var skyU = { top: { value: new THREE.Color() }, mid: { value: new THREE.Color() }, low: { value: new THREE.Color() } };
  var sky = new THREE.Mesh(track(new THREE.SphereGeometry(300, 32, 16)), track(new THREE.ShaderMaterial({
    uniforms: skyU, side: THREE.BackSide, depthWrite: false, fog: false,
    vertexShader: 'varying float h; void main(){ h = normalize(position).y; gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }',
    fragmentShader: 'uniform vec3 top; uniform vec3 mid; uniform vec3 low; varying float h; void main(){ float t = clamp(h*2.2, 0.0, 1.0); vec3 c = mix(low, mid, smoothstep(0.0, .45, t)); c = mix(c, top, smoothstep(.45, 1.0, t)); gl_FragColor = vec4(c, 1.0); }'
  })));
  sky.renderOrder = -10; scene.add(sky);
  var SKY = [ // time, top, mid, horizon, fog, sun light, sky light
    [0, '#1a2147', '#4a4677', '#8a6f8c', '#6f6683', .2, 1.25],
    [6, '#3d5788', '#b08aa0', '#efb48a', '#c7a9a4', .9, 1.7],
    [11, '#8db4dc', '#cadff0', '#f6e3c8', '#e3e0d4', 1.8, 2.3],
    [17, '#9fc3e6', '#d4e4f0', '#f6f1e4', '#e9ebe4', 2.1, 2.6],
    [24, '#a8c6e4', '#e4ddd6', '#f9e4c8', '#efe6d6', 2.2, 2.7]
  ].map(function (r) { return { t: r[0], top: new THREE.Color(r[1]), mid: new THREE.Color(r[2]), low: new THREE.Color(r[3]), fog: new THREE.Color(r[4]), sun: r[5], hemi: r[6] }; });
  var stars = (function () {
    var n = 500, p = new Float32Array(n * 3), r2 = rng(3);
    for (var i = 0; i < n; i++) { var a = r2() * Math.PI * 2, e = .15 + r2() * 1.2; p[i * 3] = Math.cos(a) * Math.cos(e) * 280; p[i * 3 + 1] = Math.sin(e) * 280; p[i * 3 + 2] = Math.sin(a) * Math.cos(e) * 280; }
    var gm = track(new THREE.BufferGeometry()); gm.setAttribute('position', new THREE.BufferAttribute(p, 3));
    return new THREE.Points(gm, track(new THREE.PointsMaterial({ size: 1.6, color: 0xfff6e0, transparent: true, opacity: .8, fog: false, depthWrite: false })));
  })();
  scene.add(stars);
  var sun = glow(new THREE.Color('#fff1cf'), 60, 1); sun.material.fog = false; scene.add(sun);
  var sunCore = glow(new THREE.Color('#ffffff'), 16, 1); sunCore.material.fog = false; scene.add(sunCore);

  // The valley: a flat meadow, rolling hills behind it, and two
  // far ridges that fade into the sky like the homepage hero.
  function hills(w, d, segX, segZ, fn, colFn) {
    var gm = track(new THREE.PlaneGeometry(w, d, segX, segZ)); gm.rotateX(-Math.PI / 2);
    var pos = gm.attributes.position, col = new Float32Array(pos.count * 3), c = new THREE.Color();
    for (var i = 0; i < pos.count; i++) {
      var x = pos.getX(i), z = pos.getZ(i), y = fn(x, z); pos.setY(i, y); colFn(x, y, z, c); col[i * 3] = c.r; col[i * 3 + 1] = c.g; col[i * 3 + 2] = c.b;
    }
    gm.setAttribute('color', new THREE.BufferAttribute(col, 3)); gm.computeVertexNormals();
    return new THREE.Mesh(gm, lam(0xffffff, { vertexColors: true }));
  }
  function n2(x, z) { return Math.sin(x * .11 + Math.sin(z * .07) * 2) * .5 + Math.sin(x * .043 - z * .09) * .7 + Math.sin(x * .23 + z * .17) * .18; }
  function groundY(x, z) {
    var back = Math.max(0, -z - 24), front = Math.max(0, z - 12);
    return -0.72 + n2(x, z) * .12 + Math.pow(back, 1.25) * .07 * (1.2 + n2(x * .7, z) * .5) + front * .08 * (1 + n2(x, z));
  }
  var meadowC = new THREE.Color('#c9c58f'), grassC = new THREE.Color('#a3b39b'), hillC = new THREE.Color('#6f8c63'), fieldC = new THREE.Color('#a9b47f');
  var ground = hills(220, 120, 220, 80, function (x, z) { return groundY(x + 14, z - 8); }, function (x, y, z, c) {
    var k = clamp((y + .5) / 5, 0, 1), m = n2(x * .33 + 7, z * .41) * .5 + .5;
    c.copy(meadowC).lerp(fieldC, m * .55).lerp(grassC, clamp(k * 2.2, 0, 1)).lerp(hillC, clamp(k * 1.4 - .5, 0, 1));
  });
  ground.position.set(14, 0, -8); scene.add(ground);
  var ridgeA = hills(360, 60, 120, 8, function (x, z) { return 6 + n2(x * .4, 3) * 5 + Math.sin(x * .021) * 6 - z * .1; }, function (x, y, z, c) { c.set('#a7b5a0'); });
  ridgeA.position.set(14, -2, -95); scene.add(ridgeA);
  var ridgeB = hills(420, 60, 120, 8, function (x, z) { return 16 + n2(x * .25, 9) * 9 + Math.sin(x * .013 + 1) * 10; }, function (x, y, z, c) { c.set('#b8c3d1'); });
  ridgeB.position.set(14, -4, -160); scene.add(ridgeB);
  // Firs on the hills and at the edges of frame; hay bales in the meadow.
  var firGeo = track(new THREE.ConeGeometry(1, 3.2, 7)); firGeo.translate(0, 1.6, 0);
  var firs = new THREE.InstancedMesh(firGeo, lam('#3d5a3c'), 260), fr = rng(17), m4 = new THREE.Matrix4(), q = new THREE.Quaternion(), sc = new THREE.Vector3(), ps = new THREE.Vector3();
  // Firs grow in groves: twelve centres behind the meadow, a few behind the camera.
  var groves = []; for (var gI = 0; gI < 14; gI++) groves.push([-66 + gI * 12 + fr() * 6, gI % 3 === 1 ? -16 - fr() * 4 : -26 - fr() * 18]);
  for (var i = 0; i < 260; i++) {
    var gv = groves[i % groves.length], fx = i < 220 ? gv[0] + gauss(fr) * 3.2 : -60 + fr() * 150, fz = i < 220 ? gv[1] + gauss(fr) * 2.4 : 26 + fr() * 10, s2 = .5 + fr() * .9;
    m4.compose(ps.set(fx, groundY(fx, fz) - .1, fz), q, sc.set(s2 * .55, s2, s2 * .55)); firs.setMatrixAt(i, m4);
  }
  scene.add(firs);
  var baleGeo = track(new THREE.CylinderGeometry(1, 1, 1, 18)); baleGeo.rotateZ(Math.PI / 2);
  var bales = new THREE.InstancedMesh(baleGeo, lam('#d8b25e'), 10), br = rng(29), up = new THREE.Vector3(0, 1, 0);
  for (i = 0; i < 10; i++) { var bx = -55 + i * 13 + br() * 3, bz = -10 - br() * 6; m4.compose(ps.set(bx, groundY(bx, bz) + .35, bz), q.setFromAxisAngle(up, br() * 3), sc.set(.75, .42, .42)); bales.setMatrixAt(i, m4); }
  q.identity();
  scene.add(bales);
  // A few seeds of light drifting in the morning air.
  var motesN = 220, mp = new Float32Array(motesN * 3);
  for (i = 0; i < motesN; i++) { mp[i * 3] = -50 + R() * 130; mp[i * 3 + 1] = R() * 7; mp[i * 3 + 2] = -6 + R() * 16; }
  var mg = track(new THREE.BufferGeometry()); mg.setAttribute('position', new THREE.BufferAttribute(mp, 3));
  var dust = new THREE.Points(mg, track(new THREE.PointsMaterial({ size: .09, map: glowTex, color: 0xfff1cf, transparent: true, opacity: .7, blending: THREE.AdditiveBlending, depthWrite: false })));
  scene.add(dust);
  var tmpA = new THREE.Color(), tmpB = new THREE.Color();
  function skyAt(T) {
    var k = 0; while (k < SKY.length - 2 && T >= SKY[k + 1].t) k++;
    var a = SKY[k], b = SKY[k + 1], p = ease(clamp((T - a.t) / (b.t - a.t), 0, 1));
    skyU.top.value.copy(a.top).lerp(b.top, p); skyU.mid.value.copy(a.mid).lerp(b.mid, p); skyU.low.value.copy(a.low).lerp(b.low, p);
    fogCol.copy(a.fog).lerp(b.fog, p); scene.fog.color.copy(fogCol);
    sunLight.intensity = a.sun + (b.sun - a.sun) * p; hemi.intensity = a.hemi + (b.hemi - a.hemi) * p;
    stars.material.opacity = .6 * (1 - clamp(T / 5, 0, 1)); stars.visible = stars.material.opacity > .01;
    var rise = clamp((T - 3) / 14, 0, 1), sy = -14 + out(rise) * 42;
    sun.position.set(camera.position.x + 70, sy, -230); sunCore.position.copy(sun.position);
    sun.material.opacity = .25 + .55 * rise; sunCore.material.opacity = clamp(rise * 3, 0, 1);
    sunLight.position.set(70, Math.max(4, sy), -200);
    sunLight.color.copy(tmpA.set('#ffb37a')).lerp(tmpB.set('#fff6e6'), rise);
    dust.material.opacity = .25 + .5 * rise;
    sky.position.copy(camera.position); stars.position.copy(camera.position);
  }

  var tracks = [];
  function at(t0, t1, fn) { tracks.push({ t0: t0, t1: t1, fn: fn }); }

  // ---- 1. Last night: three nights as hypnograms against the sleep need --------
  var MIN = 16 / 480, X0 = -34, LV = [2.5, 1.85, 1.2, 0.5]; // awake, REM, core, deep
  function hypnogram(minutes, z, r) {
    var path = new THREE.CurvePath(), x = X0, y = LV[0], t = 0, cyc = 0;
    function to(nx, ny) {
      if (ny !== y) { path.add(new THREE.LineCurve3(new THREE.Vector3(x, y, z), new THREE.Vector3(x, ny, z))); y = ny; }
      if (nx !== x) { path.add(new THREE.LineCurve3(new THREE.Vector3(x, y, z), new THREE.Vector3(nx, y, z))); x = nx; }
    }
    to(X0 + 12 * MIN, LV[0]);
    while (t < minutes - 20) {
      var deep = Math.max(4, 38 - cyc * 11) * (0.7 + r() * .6), rem = (10 + cyc * 7) * (0.7 + r() * .6), core = 22 + r() * 18;
      var seq = [[LV[2], core * .5], [LV[3], deep], [LV[2], core * .5], [LV[1], rem]];
      if (r() < .35) seq.push([LV[0], 2 + r() * 4]);
      for (var k = 0; k < seq.length && t < minutes - 20; k++) { var d = Math.min(seq[k][1], minutes - 20 - t); t += d; to(X0 + (12 + t) * MIN, seq[k][0]); }
      cyc++;
    }
    to(X0 + minutes * MIN, LV[0]);
    return path;
  }
  var nights = [[455, -2.6, .38], [440, 0, .6], [468, 2.6, 1]]; // oldest to newest; the newest counts most
  var sleepStrands = nights.map(function (n, k) {
    var st = strand(hypnogram(n[0], n[1], rng(40 + k)), C.sleep, .045, 600, n[2]);
    scene.add(st); drawTo(st, 0); at(0.4 + k * .45, 2.9 + k * .45, function (p) { drawTo(st, out(p)); }); return st;
  });
  var needX = X0 + 470 * MIN;
  var need = new THREE.Group();
  var needPane = new THREE.Mesh(track(new THREE.PlaneGeometry(7, 3.1)), basic(C.white, .06, true));
  needPane.rotation.y = Math.PI / 2; needPane.position.set(needX, 1.45, 0); need.add(needPane);
  var needEdge = new THREE.Mesh(track(new THREE.BoxGeometry(.03, 3.1, .03)), basic(C.white, .8, true));
  needEdge.position.set(needX, 1.45, 3.4); need.add(needEdge);
  var needLab = label(S.lb_need, '#3b3a8f', .5); needLab.position.set(needX + .25, 3.25, 3.4); need.add(needLab);
  scene.add(need); fade(need, 0); at(3.0, 4.0, function (p) { fade(need, out(p)); });

  // ---- 2. Heart: seven mornings land inside the range of the last 28 nights -----
  var HY = 1.5, SD = .9, HX = -12;
  var band = new THREE.Group();
  var bandBox = new THREE.Mesh(track(new THREE.BoxGeometry(12.6, SD, 3.2)), basic(C.ok, .14, true));
  bandBox.position.set(HX + 6, HY, 0); band.add(bandBox);
  var bandEdges = new THREE.LineSegments(track(new THREE.EdgesGeometry(bandBox.geometry)), track(new THREE.LineBasicMaterial({ color: C.ok, transparent: true, opacity: .6 })));
  bandEdges.position.copy(bandBox.position); band.add(bandEdges);
  var rangeLab = label(S.lb_range, '#1d6e52', .5); rangeLab.position.set(HX + 2.2, HY + SD / 2 + .4, 1.6); band.add(rangeLab);
  scene.add(band); fade(band, 0); at(5.0, 5.9, function (p) { fade(band, out(p)); });
  var sph = track(new THREE.SphereGeometry(1, 20, 14));
  var nightsHR = new THREE.Group(), hr = rng(5);
  for (i = 0; i < 28; i++) {
    var d = new THREE.Mesh(sph, lam(C.heart, { transparent: true, opacity: .5 }));
    d.scale.setScalar(.09); d.position.set(HX + .2 + i * .3, HY + clamp(gauss(hr), -2.2, 2.2) * SD, (hr() - .5) * 2); nightsHR.add(d);
  }
  scene.add(nightsHR);
  nightsHR.children.forEach(function (d, k) { d.visible = false; at(5.1 + k * .025, 5.6 + k * .025, function (p) { d.visible = p > 0; d.scale.setScalar(.09 * out(p)); }); });
  var mornings = [], mz = [.2, .55, -.1, .35, .6, .15, .4];
  mz.forEach(function (z, k) {
    var grp = new THREE.Group();
    var m = new THREE.Mesh(sph, lam(C.heart, { emissive: C.heart, emissiveIntensity: .25 }));
    m.scale.setScalar(.17); grp.add(m);
    var x = HX + 9 + k * .52, y = HY + z * SD * .9;
    grp.userData.home = new THREE.Vector3(x, y, (k % 2 ? .5 : -.5));
    grp.visible = false; scene.add(grp); mornings.push(grp);
    at(5.9 + k * .17, 6.9 + k * .17, function (p) {
      grp.visible = p > 0; var q = out(p);
      grp.position.set(x, y + (1 - q) * 5.5, grp.userData.home.z + (1 - q) * 3);
    });
  });
  var meanY = HY + (mz.reduce(function (a, b) { return a + b; }, 0) / 7) * SD * .9;
  var meanBar = new THREE.Mesh(track(new THREE.BoxGeometry(4, .035, .035)), basic(C.ink, .9));
  meanBar.position.set(HX + 10.6, meanY, 0); scene.add(meanBar); meanBar.scale.x = 0.001;
  at(7.3, 8.0, function (p) { meanBar.scale.x = Math.max(.001, out(p)); });

  // ---- 3. Your week: recent days against the four weeks before ------------------
  var WX = 6, lr = rng(23), loads = [];
  for (i = 0; i < 35; i++) loads.push(lr() < .3 ? 0 : clamp(42 + gauss(lr) * 20, 6, 95));
  var chronic = loads.slice(0, 28).reduce(function (a, b) { return a + b; }, 0) / 28, LK = .036;
  var colGeo = track(new THREE.BoxGeometry(.26, 1, .9)); colGeo.translate(0, .5, 0);
  var cols = [];
  loads.forEach(function (v, k) {
    if (!v) return;
    var recent = k >= 28;
    var mat = recent ? lam(C.load, { emissive: C.load, emissiveIntensity: .15 }) : lam(C.wood, { transparent: true, opacity: .55 });
    var c = new THREE.Mesh(colGeo, mat); c.position.set(WX + k * .36, -0.7, 0); c.scale.y = .001; scene.add(c); cols.push(c);
    at(8.8 + k * .035, 9.8 + k * .035, function (p) { c.scale.y = Math.max(.001, v * LK * out(p)); });
  });
  function level(y, op, txt, col) {
    var grp = new THREE.Group();
    var pl = new THREE.Mesh(track(new THREE.PlaneGeometry(10.4, 2.2)), basic(C.ink, op));
    pl.rotation.x = -Math.PI / 2; pl.position.set(WX + 5, -0.7 + y, 0); grp.add(pl);
    var ed = new THREE.Mesh(track(new THREE.BoxGeometry(10.4, .025, .025)), basic(C.ink, Math.min(1, op * 8))); ed.position.set(WX + 5, -0.7 + y, 1.1); grp.add(ed);
    var lb = label(txt, col, .38); lb.position.set(WX - .1 - 0, -0.7 + y + .32, 1.1); grp.add(lb);
    scene.add(grp); fade(grp, 0); return grp;
  }
  var usual = level(chronic * LK, .08, S.lb_weeks, '#8a4413');
  var ceil12 = level(chronic * 1.2 * LK, .05, S.lb_x12, '#26252b'); ceil12.children[2].position.x = WX + 10.6;
  at(10.1, 10.9, function (p) { fade(usual, out(p)); });
  at(10.5, 11.3, function (p) { fade(ceil12, out(p)); });

  // ---- 4. Four checks: the three signals run through four rings -----------------
  var GX = [27, 30.5, 34, 37.5], GY = 1.6;
  var gates = GX.map(function (x, k) {
    var grp = new THREE.Group();
    var ring = new THREE.Mesh(track(new THREE.TorusGeometry(1.25, .085, 12, 72)), lam(C.wood.clone(), { transparent: true }));
    ring.rotation.y = Math.PI / 2; grp.add(ring);
    var halo = glow(C.ok, 4.2, 0); grp.add(halo);
    grp.position.set(x, GY, 0); scene.add(grp);
    grp.userData = { ring: ring, halo: halo };
    fade(ring, 0); at(12.2 + k * .12, 13.0 + k * .12, function (p) { fade(ring, out(p)); });
    return grp;
  });
  function curve(pts) { return new THREE.CatmullRomCurve3(pts.map(function (p) { return new THREE.Vector3(p[0], p[1], p[2]); }), false, 'centripetal'); }
  var lanes = [
    { c: C.sleep, pts: [[-18, 1.2, 1.8], [-8, 6.5, 4.5], [10, 6.8, 4], [22, 2.6, .9], [27, 1.75, .14], [38.5, 1.75, .14]] },
    { c: C.heart, pts: [[-.2, 1.6, 0], [10, 4.6, -3.8], [21, 2.4, -1.2], [27, 1.5, -.12], [38.5, 1.5, -.12]] },
    { c: C.load, pts: [[19, 1.9, 0], [23, 1.5, .5], [27, 1.45, .05], [38.5, 1.45, .05]] }
  ];
  var streams = lanes.map(function (l, k) {
    var st = strand(curve(l.pts), l.c, .035, 500, 1); scene.add(st); drawTo(st, 0);
    at(12.6 + k * .2, 15.4, function (p) { drawTo(st, ease(p)); });
    return st;
  });
  // A ring lights when the signals have passed through it: no check holds today back.
  gates.forEach(function (gt, k) {
    var tp = 13.7 + k * .42;
    at(tp, tp + .9, function (p) {
      var f = p < .25 ? p / .25 : 1 - (p - .25) / .75 * .45;
      gt.userData.ring.material.color.copy(C.wood).lerp(C.ok, out(Math.min(1, p * 2)));
      gt.userData.halo.material.opacity = .55 * f; gt.userData.halo.visible = p > 0;
    });
  });
  var okLab = label(S.lb_clear, '#1d6e52', .48); okLab.position.set(GX[3] + .3, GY + 1.75, 0); scene.add(okLab); fade(okLab, 0);
  at(15.4, 16.0, function (p) { fade(okLab, out(p)); });

  // ---- 5. Your own length: easy runs on a ruler, the 60th percentile marked ------
  var RX = 44, RW = 12; function mx(m) { return RX + (m - 20) / 60 * RW; }
  var runs = [32, 35, 38, 40, 40, 42, 44, 45, 46, 48, 50, 55, 62, 70];
  var sorted = runs.slice().sort(function (a, b) { return a - b; }), rk = .6 * (sorted.length - 1), lo = Math.floor(rk);
  var p60 = sorted[lo] + (sorted[lo + 1] - sorted[lo]) * (rk - lo), med = (sorted[6] + sorted[7]) / 2;
  var shown = 5 * Math.round(Math.min(p60, med * 1.3) / 5); // 45
  var merged = strand(curve([[38.5, 1.55, 0], [41, 1.1, 0], [RX, .8, 0], [RX + RW, .8, 0]]), C.ok, .04, 300, 1);
  scene.add(merged); drawTo(merged, 0); at(15.6, 17.4, function (p) { drawTo(merged, ease(p)); });
  [20, 40, 60, 80].forEach(function (m) {
    var tk = new THREE.Mesh(track(new THREE.BoxGeometry(.03, .35, .03)), basic(C.ink, .6)); tk.position.set(mx(m), .62, 0); scene.add(tk);
    fade(tk, 0); at(17.0, 17.5, function (p) { fade(tk, p); });
    var lb = label(m + '', '#4a4943', .3, true); lb.position.set(mx(m) - .14, .2, .2); scene.add(lb); fade(lb, 0); at(17.0, 17.5, function (p) { fade(lb, p); });
  });
  var seen = {}, baleMat = lam(C.gold);
  runs.forEach(function (m, k) {
    var n = seen[m] || 0; seen[m] = n + 1;
    var grp = new THREE.Group();
    var s = new THREE.Mesh(baleGeo, baleMat); s.scale.set(.26, .2, .2); s.rotation.y = .5; grp.add(s);
    var y = 1.08 + n * .44; scene.add(grp); grp.visible = false;
    at(16.9 + k * .07, 17.7 + k * .07, function (p) { grp.visible = p > 0; grp.position.set(mx(m), y + (1 - back(p)) * 3.2, 0); });
  });
  var capBar = new THREE.Mesh(track(new THREE.BoxGeometry(.025, 2.6, .025)), basic(C.ink, .35));
  capBar.position.set(mx(med * 1.3), 1.9, 0); scene.add(capBar); fade(capBar, 0); at(18.2, 18.8, function (p) { fade(capBar, p); });
  var mark = new THREE.Group();
  var markBar = new THREE.Mesh(track(new THREE.CylinderGeometry(.035, .035, 2.7, 8)), lam(C.wood)); markBar.position.y = 1.35; mark.add(markBar);
  var flagShape = new THREE.Shape(); flagShape.moveTo(0, 0); flagShape.lineTo(.7, -.22); flagShape.lineTo(0, -.44); flagShape.closePath();
  var flag = new THREE.Mesh(track(new THREE.ShapeGeometry(flagShape)), lam(new THREE.Color('#e8742e'), { side: THREE.DoubleSide })); flag.position.set(.03, 2.7, 0); mark.add(flag);
  var markLab = label(shown + ' ' + S.c_min, '#26252b', .62); markLab.position.set(.85, 2.5, 0); mark.add(markLab);
  mark.position.set(mx(shown), .8, 0); scene.add(mark); mark.scale.y = .001; fade(markLab, 0);
  at(18.0, 18.9, function (p) { mark.scale.y = Math.max(.001, out(p)); });
  at(18.6, 19.2, function (p) { fade(markLab, p); });

  // ---- 6. Today's session: the card ------------------------------------------
  function cardTexture() {
    var c = document.createElement('canvas'); c.width = 1024; c.height = 640; var x = c.getContext('2d');
    var f = 'ui-rounded, "SF Pro Rounded", system-ui, -apple-system, sans-serif';
    function rr(a, b, w, h, r) { x.beginPath(); x.moveTo(a + r, b); x.arcTo(a + w, b, a + w, b + h, r); x.arcTo(a + w, b + h, a, b + h, r); x.arcTo(a, b + h, a, b, r); x.arcTo(a, b, a + w, b, r); x.closePath(); }
    var bgr = x.createLinearGradient(0, 0, 0, 640); bgr.addColorStop(0, '#fdfaf2'); bgr.addColorStop(1, '#f1e9d6');
    rr(4, 4, 1016, 632, 64); x.fillStyle = bgr; x.fill(); x.lineWidth = 3; x.strokeStyle = 'rgba(38,37,43,.14)'; x.stroke();
    x.fillStyle = '#23966f'; x.font = '700 34px ' + f; x.fillText(S.c_today.split('').join(String.fromCharCode(8202)), 72, 112);
    x.fillStyle = '#26252b'; x.font = '800 76px ' + f; x.fillText(S.c_name, 70, 208);
    x.font = '800 150px ' + f; x.fillText(String(shown), 66, 372);
    var w = x.measureText(String(shown)).width; x.fillStyle = '#7a776c'; x.font = '600 48px ' + f; x.fillText(S.c_min, 66 + w + 16, 372);
    // The app's own read line for a normal day, wrapped to the card.
    x.fillStyle = '#4d4b44'; x.font = '600 36px ' + f;
    var words = S.c_read.split(' '), line = '', y = 452;
    words.forEach(function (w) {
      var t2 = line ? line + ' ' + w : w;
      if (x.measureText(t2).width > 880 && line) { x.fillText(line, 70, y); y += 50; line = w; } else line = t2;
    });
    if (line) x.fillText(line, 70, y);
    var t = track(new THREE.CanvasTexture(c)); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; return t;
  }
  var card = new THREE.Group();
  var cardMesh = new THREE.Mesh(track(new THREE.PlaneGeometry(5.12, 3.2)), track(new THREE.MeshBasicMaterial({ map: cardTexture(), transparent: true, alphaTest: .5, depthWrite: true, fog: false })));
  var stack = new THREE.Group(); card.add(stack); stack.add(cardMesh);
  card.position.set(64, 2.2, 0); scene.add(card); fade(card, 0);
  var toCard = strand(curve([[RX + RW, .8, 0], [59, 1.1, 0], [61.3, 2.2, 0]]), C.ok, .04, 200, 1);
  scene.add(toCard); drawTo(toCard, 0); at(19.3, 20.4, function (p) { drawTo(toCard, ease(p)); });
  toCard.userData.parts.forEach(function (m) { m.material.transparent = true; });
  at(22.4, 23.2, function (p) { if (p > 0) fade(toCard, 1 - p); });
  at(20.0, 21.6, function (p) {
    var q = out(p); fade(card, q); card.scale.setScalar(.86 + .14 * q); card.rotation.y = -.55 * (1 - q) - .1;
  });

  // ---- 7. Finale: the card tips back and opens into the layers it is made of ----
  function layerTexture(kind) {
    var c = document.createElement('canvas'); c.width = 1024; c.height = 640; var x = c.getContext('2d');
    function rr(a, b, w, h, r) { x.beginPath(); x.moveTo(a + r, b); x.arcTo(a + w, b, a + w, b + h, r); x.arcTo(a + w, b + h, a, b + h, r); x.arcTo(a, b + h, a, b, r); x.arcTo(a, b, a + w, b, r); x.closePath(); }
    rr(4, 4, 1016, 632, 64); x.fillStyle = 'rgba(251,247,238,.86)'; x.fill(); x.lineWidth = 3; x.strokeStyle = 'rgba(38,37,43,.16)'; x.stroke();
    var lr2 = rng(70 + kind);
    if (kind === 1) {           // last night and this week
      for (var i = 0; i < 13; i++) { var h = 120 + lr2() * 120; x.fillStyle = i > 9 ? '#5b59d6' : 'rgba(91,89,214,.3)'; x.fillRect(70 + i * 22, 470 - h, 14, h); }
      for (i = 0; i < 35; i++) { x.fillStyle = i > 27 ? '#c42a50' : 'rgba(196,42,80,.3)'; x.beginPath(); x.arc(410 + i * 6.4, 330 + gauss(lr2) * 50, i > 27 ? 8 : 5, 0, 7); x.fill(); }
      for (i = 0; i < 35; i++) { var v = lr2() < .3 ? 0 : 40 + lr2() * 160; x.fillStyle = i > 27 ? '#d0631c' : 'rgba(156,122,82,.4)'; x.fillRect(700 + i * 7.6, 470 - v, 5, v); }
    } else if (kind === 2) {    // against your own usual
      x.fillStyle = 'rgba(35,150,111,.16)'; x.strokeStyle = 'rgba(35,150,111,.8)'; x.lineWidth = 3;
      [[70, 290, 300, 44], [400, 290, 240, 70], [700, 300, 260, 50]].forEach(function (b) { rr(b[0], b[1], b[2], b[3], 22); x.fill(); x.stroke(); });
      x.setLineDash([12, 14]); x.strokeStyle = 'rgba(38,37,43,.7)';
      [[70, 312, 370], [400, 325, 640], [700, 325, 960]].forEach(function (l) { x.beginPath(); x.moveTo(l[0], l[1]); x.lineTo(l[2], l[1]); x.stroke(); });
    } else if (kind === 3) {    // four checks
      for (i = 0; i < 4; i++) {
        var cx = 190 + i * 215; x.lineWidth = 8; x.strokeStyle = '#23966f'; x.beginPath(); x.arc(cx, 320, 76, 0, 7); x.stroke();
        x.fillStyle = '#23966f'; x.beginPath(); x.arc(cx + 54, 266, 26, 0, 7); x.fill();
        x.strokeStyle = '#ffffff'; x.lineWidth = 7; x.beginPath(); x.moveTo(cx + 42, 267); x.lineTo(cx + 51, 277); x.lineTo(cx + 67, 257); x.stroke();
      }
    } else {                    // your own length
      x.strokeStyle = 'rgba(38,37,43,.5)'; x.lineWidth = 4; x.beginPath(); x.moveTo(80, 440); x.lineTo(944, 440); x.stroke();
      var seen2 = {};
      runs.forEach(function (m) { var n = seen2[m] || 0; seen2[m] = n + 1; x.fillStyle = '#c99a3e'; x.beginPath(); x.arc(80 + (m - 20) / 60 * 864, 410 - n * 40, 17, 0, 7); x.fill(); });
      var mxp = 80 + (shown - 20) / 60 * 864; x.strokeStyle = '#26252b'; x.lineWidth = 7; x.beginPath(); x.moveTo(mxp, 170); x.lineTo(mxp, 470); x.stroke();
      x.fillStyle = '#e8742e'; x.beginPath(); x.moveTo(mxp, 160); x.lineTo(mxp + 64, 182); x.lineTo(mxp, 204); x.closePath(); x.fill();
    }
    var t = track(new THREE.CanvasTexture(c)); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; return t;
  }
  var GAP = 1.6, LIFT = 6, layerNames = [S.ly1, S.ly2, S.ly3, S.ly4], layers = [];
  [4, 3, 2, 1].forEach(function (kind, k) {
    var grp = new THREE.Group();
    var m = new THREE.Mesh(track(new THREE.PlaneGeometry(5.12, 3.2)), track(new THREE.MeshBasicMaterial({ map: layerTexture(kind), transparent: true, depthWrite: false, side: THREE.DoubleSide, fog: false })));
    grp.add(m);
    var lb = label(layerNames[kind - 1], '#3b3a36', .36); lb.position.set(2.85, 0, 0); grp.add(lb);
    lb.renderOrder = 20; lb.material.depthTest = false; stack.add(grp); grp.renderOrder = -1 - k; fade(grp, 0); grp.visible = false;
    layers.push(grp);
    at(23.4 + k * .22, 25.0 + k * .22, function (p) { grp.visible = p > 0; fade(grp, out(Math.min(1, p * 1.6))); grp.position.z = -(k + 1) * GAP * out(p); });
  });
  var topLab = label(S.ly5, '#1d6e52', .4); topLab.position.set(2.85, 0, .02); topLab.renderOrder = 20; topLab.material.depthTest = false; stack.add(topLab); fade(topLab, 0);
  at(24.6, 25.4, function (p) { fade(topLab, p); });
  var spine = new THREE.Mesh(track(new THREE.CylinderGeometry(.025, .025, 4 * GAP, 8)), basic(C.ok, .9));
  spine.rotation.x = Math.PI / 2; spine.position.set(2.35, 1.35, -2 * GAP); stack.add(spine); fade(spine, 0);
  var spineGlow = new THREE.Mesh(track(new THREE.CylinderGeometry(.12, .12, 4 * GAP, 10)), basic(C.ok, .16));
  spineGlow.rotation.x = Math.PI / 2; spineGlow.position.copy(spine.position); stack.add(spineGlow); fade(spineGlow, 0);
  at(25.0, 26.0, function (p) { fade(spine, p); fade(spineGlow, p); spine.scale.y = spineGlow.scale.y = Math.max(.001, out(p)); });
  // The card rises clear of the meadow so its layers have room to open beneath it.
  at(22.4, 24.2, function (p) { card.position.y = 2.2 + LIFT * ease(p); if (p <= 0) { stack.rotation.x = 0; return; } stack.rotation.x = -1.12 * ease(p); card.rotation.y = -.1 - .42 * ease(p); });

  // ---- Camera: one continuous tracking shot -----------------------------------
  // Arrival times: the camera reaches each station at its time, holds while the
  // station plays, then glides on over MOVE seconds.
  var shots = [
    [0.0, [-46, 3.4, 20], [-27, 2.6, 0]],
    [2.4, [-25.2, 4.6, 13.2], [-25.6, 2.1, 0]],
    [5.6, [-5.4, 3.6, 12.8], [-5.6, 2.2, 0]],
    [9.2, [12.2, 4.2, 13.4], [12.2, 1.7, 0]],
    [13.0, [21.8, 2.9, 4.6], [37, 1.6, 0]],
    [17.0, [50, 3.4, 10.6], [50.2, 2.3, 0]],
    [21.0, [60.4, 3.0, 11.2], [62.4, 1.35, 0]],
    [24.6, [61.6, 4.6 + LIFT, 11.6], [64.4, -.6 + LIFT, -2.4]]
  ];
  var MOVE = 2.1;
  var P = new THREE.Vector3(), L = new THREE.Vector3(), A = new THREE.Vector3(), B = new THREE.Vector3();
  var portrait = false;
  function placeCamera(T) {
    var k = 0; while (k < shots.length - 1 && T >= shots[k + 1][0]) k++;
    var a = shots[k], b = shots[Math.min(k + 1, shots.length - 1)], p = 0;
    if (b !== a) { var mv = k === 0 ? b[0] : Math.min(MOVE, b[0] - a[0]); p = ease(clamp((T - (b[0] - mv)) / mv, 0, 1)); }
    P.fromArray(a[1]).lerp(B.fromArray(b[1]), p);
    L.fromArray(a[2]).lerp(A.fromArray(b[2]), p);
    var dr = Math.max(0, T - 24.6);
    P.x += Math.sin(T * .31) * .16 - Math.sin(dr * .2) * .9; P.y += Math.sin(T * .23) * .1; P.z += Math.sin(dr * .2) * .5;
    if (portrait) {
      var fin = clamp((T - 19) / 3, 0, 1), v = P.clone().sub(L);
      P.copy(L).add(v.multiplyScalar(1.1 - .05 * fin)); L.y += .7 - .7 * fin; L.x += 1.7 * fin; P.x += 1.3 * fin;
    }
    camera.position.copy(P); camera.lookAt(L);
  }

  function render(T) {
    for (var k = 0; k < tracks.length; k++) tracks[k].fn(prog(T, tracks[k].t0, tracks[k].t1));
    placeCamera(T);
    skyAt(T);
    renderer.render(scene, camera);
  }

  function resize() {
    var w = host.clientWidth, h = host.clientHeight; if (!w || !h) return;
    var dpr = Math.min(window.devicePixelRatio || 1, 1.5);
    renderer.setPixelRatio(dpr); renderer.setSize(w, h, false);
    camera.aspect = w / h; portrait = w / h < 1; camera.fov = portrait ? 48 : 34; camera.updateProjectionMatrix();
  }
  resize();
  var ro = 'ResizeObserver' in window ? new ResizeObserver(resize) : null; if (ro) ro.observe(host);

  // Frame guard: if this device cannot keep up (slow frames after warm-up) or
  // drops the GL context, hand back to the poster instead of janking the page.
  var T = 0, last = 0, running = false, raf = 0, onTime = null, onSlow = null, gaps = [], gave = false;
  function giveUp() { if (gave) return; gave = true; running = false; if (raf) cancelAnimationFrame(raf); raf = 0; if (onSlow) onSlow(); }
  canvas.addEventListener('webglcontextlost', function (e) { e.preventDefault(); giveUp(); });
  function frame(now) {
    raf = 0; if (!running) return;
    if (last) {
      gaps.push(now - last);
      if (gaps.length === 40) {
        var g = gaps.slice(8).sort(function (a, b) { return a - b; });
        if (g[g.length >> 1] > 45) { giveUp(); return; }
      }
    }
    var dt = last ? Math.min(.05, (now - last) / 1000) : 0; last = now;
    T += dt; render(T); if (onTime) onTime(T);
    raf = requestAnimationFrame(frame);
  }
  render(0);
  return {
    end: END,
    play: function () { if (running || gave) return; running = true; last = 0; if (gaps.length < 40) gaps = []; raf = requestAnimationFrame(frame); },
    pause: function () { running = false; if (raf) cancelAnimationFrame(raf); raf = 0; },
    seek: function (t) { T = t; render(T); if (onTime) onTime(T); },
    onTime: function (fn) { onTime = fn; },
    onSlow: function (fn) { onSlow = fn; },
    dispose: function () { this.pause(); if (ro) ro.disconnect(); disposables.forEach(function (d) { d.dispose && d.dispose(); }); renderer.dispose(); canvas.remove(); }
  };
}
