// v3 composer (6 Nov). Craft study + brand study applied:
// - one 13,200 x 2,868 field (contours + one route) sliced into ten 1320 x 2868 frames, so lines cross the seams
// - a fixed 3-line headline box, the phone top locked on every frame, one headline size for frames 2-10, frame 1 bigger
// - 7 Nov: phoneTop 803 -> 779 (headline moves with it), so the replay's figures show whole above the bottom edge; the frame shows the top 88.7% of each screen (to y 2327 of 2622 px)
// - headline cap height set in px (9.3% of width; frame 1 11%); HU/DE narrow the width axis before the type shrinks
// - two-tone headlines: the setup dim, the point bright ("~" starts the bright part, "^" ends it)
// node frames3.js <look> <lang> [frames]  -> ../frames3/<look>/<lang>-N.png
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const D = '/mnt/project-files/mocks/store-3.4-dream-2026-11-06/src', OUTD = process.env.OUTD, W = 1320, H = 2868, N = 10;
const T = JSON.parse(fs.readFileSync(path.join(D, 'topo.json')));
// 7 Nov evening: COPY3 / OUT3 let a draft build from its own copy file into its own folder, so the finals stay as they are
const COPY = JSON.parse(fs.readFileSync(path.join(D, 'copy3-v2.json')));
const FEATS = fs.existsSync(path.join(D, 'feats.json')) ? JSON.parse(fs.readFileSync(path.join(D, 'feats.json'))) : {};
const LOOKS = JSON.parse(fs.readFileSync(path.join(D, 'looks.json')));
const [lookName = 'night', lang = 'en', only = ''] = process.argv.slice(2);
const L = LOOKS[lookName], OUT = OUTD; fs.mkdirSync(OUT, { recursive: true });
const G = Object.assign({ file: 'archivo.ttf', wght: 760, wdth: 87.5, wdthMin: 72, track: -0.015, lh: 0.95, capRatio: 0.686,
  cap1: 146, cap: 122, subCap: 60, subGap: 1.15, headSubGap: 0.6, left: 100, phoneTop: 779, pw: 1180, gap: 1.25, gap1: 0.95, routeY: 1960, routeW: 22, fx: 600, fpw: 1000, ftop: 30, lth: 138, ltgap: 150, lx: 600, lpw: 1040 }, L.grid || {}, { pw: +(process.env.PW || 940), phoneTop: +(process.env.PTOP || 779) });

// The route: out of each phone's right side, across the seam at one height, into the next phone.
function routePath() {
  let d = '';
  for (let i = 0; i < N; i++) {
    const x0 = i * W, l = x0 + (W - G.pw) / 2, r = l + G.pw, y = G.routeY;
    if (i === 0) d += `M${l + 300} ${y + 180} C${l + 700} ${y + 160} ${r - 220} ${y + 60} ${r - 40} ${y + 30}`;
    else d += ` C${l + 300} ${y - 40} ${r - 300} ${y + 40} ${r - 40} ${y + 30}`;
    if (i < N - 1) d += ` C${r + 40} ${y + 20} ${x0 + W - 30} ${y} ${x0 + W} ${y} S${x0 + W + 110} ${y - 10} ${x0 + W + 110} ${y - 30}`;
  }
  return d;
}
function field(i, f) {
  const k = 6600 / 1024;
  const half = `<g fill="none" stroke="${f.line}" stroke-linejoin="round" vector-effect="non-scaling-stroke">
    <path d="${T.minor.join(' ')}" stroke-width="${f.lw / k}" opacity="${f.mo}"/><path d="${T.major.join(' ')}" stroke-width="${f.lwI / k}" opacity="${f.Mo}"/></g>`;
  const svg = `<svg class=topo width="${N * W}" height="${H}" style="left:${-i * W}px" viewBox="0 0 ${N * W} ${H}">
    <g transform="scale(${k})">${half}</g><g transform="translate(${N * W},0) scale(${-k},${k})">${half}</g></svg>`;
  const rp = routePath();
  const route = f.route === false ? '' : `<svg class=route width="${N * W}" height="${H}" style="left:${-i * W}px" viewBox="0 0 ${N * W} ${H}">
    <path d="${rp}" fill="none" stroke="${f.casing}" stroke-width="${G.routeW + 8}" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="${rp}" fill="none" stroke="${f.routeC}" stroke-width="${G.routeW}" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
  const light = f.light ? `<div class=light style="background:${f.light}"></div>` : '';
  const grain = `<svg class=grain style="opacity:${f.grain};mix-blend-mode:${f.dark ? 'soft-light' : 'multiply'}" width=100% height=100%><filter id=g><feTurbulence type=fractalNoise baseFrequency=".85" numOctaves=2 seed="${i + 3}" stitchTiles=stitch /><feColorMatrix type=saturate values="0"/></filter><rect width=100% height=100% filter="url(#g)"/></svg>`;
  return light + svg + route + grain;
}
const phone = (scr, x, y, w) => { const k = w / 1350, sx = 74 * k, sy = 71 * k, sw = 1202 * k, sh = 2618 * k;
  return `<div class=ph style="left:${x}px;top:${y}px;width:${w}px;height:${(2760 * k).toFixed(0)}px"><div class=s style="left:${sx.toFixed(1)}px;top:${sy.toFixed(1)}px;width:${sw.toFixed(1)}px;height:${sh.toFixed(1)}px;border-radius:${(.128 * sw).toFixed(0)}px"><img src="file://${D}/../screens/${lang}/${scr}.png"></div><img class=f src="phone-silver-frame.png"></div>`; };

function headHTML(h) {
  // dim setup, bright point; "~" opens the bright part, "^" closes it; "|" breaks the line
  let out = '', bright = !h.includes('~');
  for (const ch of h) {
    if (ch === '~') { out += '</span><span class=b>'; bright = true; }
    else if (ch === '^') { out += '</span><span class=d>'; bright = false; }
    else if (ch === '|') out += '<br>';
    else out += ch;
  }
  return `<span class=${h.includes('~') ? 'd' : 'b'}>` + out + '</span>';
}
const GLY = {
  file: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2.8h8l4 4V21.2H6z"/><path d="M14 2.8v4h4"/><path d="M12 10v7M9 14l3 3 3-3"/></svg>',
  loop: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M5 19c-2-4 0-9 4-11s9-1 10 3-3 7-7 6-4-5-1-6"/><circle cx="5" cy="19" r="1.6" fill="currentColor"/></svg>',
  clock: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="13" r="8"/><path d="M12 9v4l3 2M10 2.8h4"/></svg>',
  cloud: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M7 15a4 4 0 0 1-.6-7.95A5.5 5.5 0 0 1 17 8a3.5 3.5 0 0 1 .5 7z"/><path d="M8 18.5l-1 2.5M12 18.5l-1 2.5M16 18.5l-1 2.5"/></svg>',
  watch: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><rect x="6" y="6" width="12" height="12" rx="3.5"/><path d="M8.5 6l1-3.2h5l1 3.2M8.5 18l1 3.2h5l1-3.2"/><path d="M10.5 13.5l3-3M11 10.5h2.5V13"/></svg>',
  doc: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linejoin="round"><path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4"/><path d="M9 13h6M9 17h6"/></svg>',
  rain: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M7 15a4 4 0 0 1-.6-7.95A5.5 5.5 0 0 1 17 8a3.5 3.5 0 0 1 .5 7z"/><path d="M8 18l-1 3M12 18l-1 3M16 18l-1 3"/></svg>',
  chev: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M9 5l7 7-7 7"/></svg>',
  quiet: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M4 20c5-1 7-6 8-10s4-6 8-6"/><circle cx="18" cy="17" r="2.5"/></svg>',
  trails: '<svg viewBox="0 0 24 24" fill="currentColor"><ellipse cx="8" cy="7" rx="2.6" ry="3.6"/><ellipse cx="15" cy="15" rx="2.6" ry="3.6"/></svg>',
  hills: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linejoin="round"><path d="M2 19l7-10 4 5 3-3 6 8z"/></svg>'
};
// A drawn cut-out: the app's light rows and chips, at 3x like a capture, till the real crop exists
function cutHTML(c) {
  if (c.img) return `<img src="${c.img}" style="width:100%;height:100%;object-fit:${c.fit || 'contain'};object-position:${c.pos || 'center'}">`;
  if (c.row) return `<div class=r><i class=g style="background:${c.tile || '#E4EEE7'};color:${c.ink || '#2F6B4C'}">${GLY[c.glyph]}</i><div class=t><b>${c.row}</b><span>${c.sub}</span></div>${c.chev ? `<i class=ch>${GLY.chev}</i>` : ''}</div>`;
  if (c.rows) return c.rows.map(([a, b]) => `<div class="r rr"><div class=t><b>${a}</b><span>${b}</span></div><i class=ch>${GLY.chev}</i></div>`).join('');
  if (c.chips) return `<div class=cs>${c.chips.map(([g, t, on]) => `<span class="c${on ? ' on' : ''}"><i>${GLY[g]}</i>${t}</span>`).join('')}</div>`;
  return '';
}
function featsHTML(list, top, f) {
  return `<div class=fl style="top:${top + G.ftop}px">${list.map(it => `<div class=fi><p class=fc>${it.cap}</p><div class=fx style="background:${it.cut.bg || '#FFFFFF'}">${cutHTML(it.cut)}</div></div>`).join('')}</div>`;
}
function frame(i, [h, scr, lay, sub], set, measure) {
  const f = Object.assign({}, L.base, (L.frames || {})[i + 1] || {}, { light: 'linear-gradient(180deg, rgba(52,104,76,0) 22%, rgba(52,104,76,.42) 52%, rgba(52,104,76,.12) 88%)' });
  const first = i === 0, big = first && !sub, cap = big ? G.cap1 : G.cap, size = cap / G.capRatio;
  const wdth = big ? set.wdth1 : set.wdth, scale = big ? set.scale1 : set.scale;
  const top = G.phoneTop;
  let devs = phone(scr, (W - G.pw) / 2, top, G.pw);
  // 7 Nov: picture 9 is the real Watch capture alone in the watch case (watch-real-<lang>.png, 1000 px wide)
  if (lay === 'watch') devs = `<img class=w src="watch-real-${lang}.png" style="left:${(W - 1000) / 2}px;top:${top + 40}px;width:1000px">`;
  // 7 Nov evening: the routes picture, a feature list. The phone sits right and runs off the edge; down the left, a caption
  // over a small cut-out from the app for each feature (feats.json). Real crops are images; the rest are drawn till captured.
  if (lay === 'features') devs = phone(scr, G.fx, top, G.fpw) + featsHTML(FEATS[lang] || [], top, f);
  // Typeset feature lists, no boxes or crops: 'list-top' puts the lines under the headline and the phone below them;
  // 'list-left' puts two-line items down the left beside a phone that runs off the right edge.
  if (lay === 'list-top') { const L2 = FEATS[lang + ':list'] || [], lh = G.lth;
    devs = `<div class=lt style="top:${top - 10}px">${L2.map(([g, t]) => `<p><i>${GLY[g] || ''}</i><span>${t}</span></p>`).join('')}</div>` + phone(scr, (W - G.pw) / 2, top + L2.length * lh + G.ltgap, G.pw); }
  if (lay === 'list-left') { const L2 = FEATS[lang + ':list2'] || [];
    devs = phone(scr, G.lx, top, G.lpw) + `<div class=ll style="top:${top + 40}px">${L2.map(([g, a, b]) => `<div class=li><i>${GLY[g] || ''}</i><p>${a}<br>${b}</p></div>`).join('')}</div>`; }
  // Structured's zoom: the whole phone scaled up (never a lens), anchored at a fraction across, bleeding off the edges
  if (lay && lay.startsWith('zoom:') && process.env.ZOOM) { const [, z, ax] = lay.split(':').map(Number), w = G.pw * z;
    devs = phone(scr, (W - G.pw) / 2 - ax * (w - G.pw), top, w); }
  if (lay === 'pair') devs = phone(scr, W - G.pw + 190, top, G.pw) + `<img class=w src="watch-nav-${lang}.png" style="left:${G.left - 60}px;top:${top + 980}px;width:660px">`;
  const css = `@font-face{font-family:HF;src:url(${G.file});font-weight:100 900;font-stretch:62% 125%}@font-face{font-family:IF;src:url(InterVariable.woff2);font-weight:100 900}
*{margin:0;padding:0;box-sizing:border-box}body{width:${W}px;height:${H}px;overflow:hidden;position:relative;background:${f.bg};color:${f.ink}}
h1{position:absolute;z-index:9;left:${G.left}px;right:56px;top:0;text-align:left;white-space:nowrap;font-family:HF;font-size:${(size * scale).toFixed(1)}px;line-height:${G.lh};
  letter-spacing:${G.track}em;font-variation-settings:'wght' ${G.wght},'wdth' ${wdth};font-kerning:normal}
.sub{position:absolute;z-index:9;left:${G.left}px;top:0;white-space:nowrap;font-family:HF;font-size:${(G.subCap / G.capRatio).toFixed(1)}px;line-height:1;color:${f.subC || f.dim};font-variation-settings:'wght' 560,'wdth' 87.5;letter-spacing:-.005em}
h1 .b{color:${f.ink}}h1 .d{color:${f.dim}}h1 i.bl{display:inline-block;width:0;height:0;vertical-align:baseline}
.light{position:absolute;inset:0;z-index:0}
.topo{position:absolute;top:0;z-index:1;-webkit-mask-image:linear-gradient(rgba(0,0,0,${f.headFade}) 0,rgba(0,0,0,${f.headFade}) 23%,#000 29%)}
.route{position:absolute;top:0;z-index:3}
.ph{position:absolute;z-index:5;filter:${f.shadow}}.ph .s{position:absolute;overflow:hidden;background:#000}.ph .s img{width:100%;display:block}.ph .f{position:absolute;inset:0;width:100%;height:100%}
.w{position:absolute;z-index:6;filter:${f.shadowW || f.shadow}}
.lt{position:absolute;z-index:7;left:${G.left}px;right:40px}.lt p{display:flex;align-items:center;gap:34px;height:${G.lth}px;font-family:HF;font-size:92px;color:${f.ink};font-variation-settings:'wght' 640,'wdth' 87.5;letter-spacing:-.01em;white-space:nowrap}
.lt i,.ll i{display:block;width:86px;height:86px;color:${f.routeC};flex:none}.lt i svg,.ll i svg{width:100%;height:100%}
.ll{position:absolute;z-index:7;left:${G.left}px;width:${G.lx - G.left + 20}px}.li{margin-bottom:86px}.li i{margin-bottom:22px;width:92px;height:92px}
.li p{font-family:HF;font-size:80px;line-height:1.02;color:${f.ink};font-variation-settings:'wght' 640,'wdth' 87.5;letter-spacing:-.012em;white-space:nowrap}
.fl{position:absolute;z-index:7;left:${G.left - 40}px;width:600px}.fi{margin-bottom:40px}
.fc{font-family:HF;font-size:74px;line-height:1;color:${f.ink};font-variation-settings:'wght' 720,'wdth' 87.5;letter-spacing:-.012em;margin:0 0 18px 6px;white-space:nowrap}
.fx{width:600px;height:200px;border-radius:40px;overflow:hidden;display:flex;flex-direction:column;justify-content:center;filter:${f.shadow}}
.fx .r{display:flex;align-items:center;gap:26px;padding:0 32px;font-family:IF}.fx .rr{flex:1;border-bottom:2px solid #ECE9E2}.fx .rr:last-child{border:0}
.fx .g{width:112px;height:112px;border-radius:30px;display:flex;align-items:center;justify-content:center;flex:none}.fx .g svg{width:62px;height:62px}
.fx .t{display:flex;flex-direction:column;gap:6px;flex:1;min-width:0}.fx .t b{font-size:41px;font-weight:650;color:#1C1C1E;letter-spacing:-.01em;white-space:nowrap}
.fx .t span{font-size:33px;color:#6E6E73;white-space:nowrap}.fx .rr .t b{font-size:38px}.fx .rr .t span{font-size:31px}
.fx .ch{width:34px;height:34px;color:#B5B2AA;flex:none}.fx .ch svg{width:100%;height:100%}
.fx .cs{display:flex;gap:18px;padding:0 30px;font-family:IF}.fx .c{display:flex;align-items:center;gap:12px;height:96px;padding:0 28px;border-radius:48px;background:#EEECE6;color:#1C1C1E;font-size:38px;font-weight:560;white-space:nowrap}
.fx .c i{width:40px;height:40px;display:block}.fx .c i svg{width:100%;height:100%}.fx .c.on{background:#1C1C1E;color:#fff}.grain{position:absolute;inset:0;z-index:8;pointer-events:none}`;
  return `<!doctype html><html><head><meta charset=utf-8><base href="file://${D}/"><style>${css}</style></head><body>${measure ? '' : field(i, f)}<h1>${headHTML(h)}<i class=bl></i></h1>${sub ? `<p class=sub>${sub}<i class=bl2 style="display:inline-block;width:0;height:0;vertical-align:baseline"></i></p>` : ''}${measure ? '' : devs}
<script>document.fonts.ready.then(()=>{const lt=document.querySelector('.lt');if(lt){let fz=92;const ps=[...lt.querySelectorAll('p')];while(fz>72&&ps.some(p=>p.scrollWidth>p.clientWidth+1)){fz-=2;ps.forEach(p=>p.style.fontSize=fz+'px');}window.LISTFZ=fz;}const h=document.querySelector('h1');window.OVER=h.scrollWidth/h.clientWidth;
const b=document.querySelector('i.bl').getBoundingClientRect().top, capPx=${(cap * scale).toFixed(1)}; let want=${top}-${big ? G.gap1 : G.gap}*capPx;
const sp=document.querySelector('.sub'); if(sp){ let w=87.5, fz=parseFloat(getComputedStyle(sp).fontSize); const room=${W - G.left - 56};
  while(sp.scrollWidth>room&&w>70){w-=2.5;sp.style.fontVariationSettings="'wght' 560,'wdth' "+w;}
  while(sp.scrollWidth>room&&fz>${(0.043 * W / G.capRatio).toFixed(1)}){fz-=1;sp.style.fontSize=fz+'px';}
  const sc=fz*${G.capRatio}, sb=${top}-${G.subGap}*sc, b2=document.querySelector('i.bl2').getBoundingClientRect().top; sp.style.top=(sb-b2)+'px';
  window.SUB={w,fz,over:sp.scrollWidth/room}; want=sb-sc-${G.headSubGap}*capPx; }
h.style.top=(want-b)+'px'; window.CAPTOP=want-b-capPx; document.title='ok';});</script></body></html>`;
}
async function render(pg, i, p, set, file) {
  const f = path.join(OUT, `_w_${lang}_${i + 1}.html`); fs.writeFileSync(f, frame(i, p, set, !file));
  await pg.goto('file://' + f); await pg.waitForFunction('document.title=="ok"');
  if (file) { await pg.waitForTimeout(150); await pg.screenshot({ path: file }); const sb = await pg.evaluate('window.SUB'); if (sb) console.log('  frame', i + 1, 'subline', JSON.stringify(sb), 'caps top', Math.round(await pg.evaluate('window.CAPTOP'))); }
  return pg.evaluate('window.OVER');
}
(async () => {
  const b = await chromium.launch(); const pg = await b.newPage({ viewport: { width: W, height: H } });
  pg.on('pageerror', e => console.log('ERR', e.message));
  const list = COPY[lang];
  // fit: narrow the width axis first (one value for frames 2-10), then, only if that is not enough, shrink the type
  const fit = async (idx) => { let wdth = G.wdth, scale = 1;
    for (;;) { let worst = 0; for (const i of idx) worst = Math.max(worst, await render(pg, i, list[i], { wdth, scale, wdth1: wdth, scale1: scale }));
      if (worst <= 1.001) return { wdth, scale };
      if (wdth > G.wdthMin) wdth = Math.max(G.wdthMin, wdth - 2.5); else scale = Math.floor(scale / worst * 100) / 100; } };
  const rest = await fit([...Array(N).keys()].slice(1)), one = await fit([0]);
  const set = { wdth: rest.wdth, scale: rest.scale, wdth1: one.wdth, scale1: one.scale };
  console.log(lang, 'frames 2-10: wdth', rest.wdth, 'scale', rest.scale, 'cap', (G.cap * rest.scale / W * 100).toFixed(1) + '% W', '| frame 1: wdth', one.wdth, 'scale', one.scale);
  for (const [i, p] of list.entries()) {
    if (only && !only.split(',').includes(String(i + 1))) continue;
    await render(pg, i, p, set, path.join(OUT, `${lang}-${i + 1}.png`));
  }
  await b.close();
})();
