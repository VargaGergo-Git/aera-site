// Route finding for the Aera route planner.
// It reads OpenFreeMap's zoom-14 map tiles (the OpenMapTiles "transportation" layer, from
// OpenStreetMap) in the browser and finds a path along real roads and trails. The only
// requests it makes are for those tiles.

export const ZOOM = 14;
const EXTENT = 4096;
const WORLD = 2 ** ZOOM * EXTENT; // world width in tile units at zoom 14
const EARTH = 40075016.686; // metres around the equator

const SNAP_METRES = 250; // a placed point moves onto the nearest usable path within this
const JOIN_METRES = 2; // a dead end joins a line this close: tile seams and simplified junctions
// Riding against a one-way street costs this many times more. The tiles don't say which one-ways let
// bikes go both ways, and a rider can walk the bike a few metres, so it's never ruled out.
const WRONG_WAY = 5;
const MAX_TILES = 90; // per leg, about 15 km by 15 km
export const MAX_POINTS = 60;
export const MAX_METRES = 200000; // the most Aera imports
export const MAX_GPX_POINTS = 4096; // the most Aera keeps without thinning

export const SPORTS = ['run', 'walk', 'hike', 'ride'];
const GPX_TYPE = { run: 'running', walk: 'walking', hike: 'hiking', ride: 'cycling' };
const LINK_CODE = { run: 'r', walk: 'w', hike: 'h', ride: 'b' };

// ---------- projection ----------

export function project(lng, lat) {
  const s = Math.sin(Math.max(-85.0511, Math.min(85.0511, lat)) * Math.PI / 180);
  return [(lng + 180) / 360 * WORLD, (0.5 - Math.log((1 + s) / (1 - s)) / (4 * Math.PI)) * WORLD];
}

export function unproject(x, y) {
  return [x / WORLD * 360 - 180, Math.atan(Math.sinh(Math.PI - 2 * Math.PI * y / WORLD)) * 180 / Math.PI];
}

// Metres on the ground per tile unit at a given height in the world.
function unitMetres(y) {
  return EARTH * Math.cos(Math.atan(Math.sinh(Math.PI - 2 * Math.PI * y / WORLD))) / WORLD;
}

// ---------- reading a vector tile (protocol buffers) ----------

const utf8 = new TextDecoder();

class Reader {
  constructor(b, p, end) { this.b = b; this.p = p; this.end = end; }
  varint() {
    let v = 0, mul = 1, byte;
    do { byte = this.b[this.p++]; v += (byte & 0x7f) * mul; mul *= 128; } while (byte & 0x80);
    return v;
  }
  int64() {
    let v = 0n, shift = 0n, byte;
    do { byte = this.b[this.p++]; v |= BigInt(byte & 0x7f) << shift; shift += 7n; } while (byte & 0x80);
    return Number(BigInt.asIntN(64, v));
  }
  string() {
    const len = this.varint(), s = utf8.decode(this.b.subarray(this.p, this.p + len));
    this.p += len;
    return s;
  }
  skip(wire) {
    if (wire === 0) { while (this.b[this.p++] & 0x80); }
    else if (wire === 1) this.p += 8;
    else if (wire === 2) { const len = this.varint(); this.p += len; }
    else if (wire === 5) this.p += 4;
    else throw new Error('Unreadable tile');
  }
}

function readValue(b, start, end) {
  const r = new Reader(b, start, end), view = new DataView(b.buffer, b.byteOffset);
  let v = null;
  while (r.p < end) {
    const tag = r.varint(), field = tag >> 3, wire = tag & 7;
    if (field === 1 && wire === 2) v = r.string();
    else if (field === 2 && wire === 5) { v = view.getFloat32(r.p, true); r.p += 4; }
    else if (field === 3 && wire === 1) { v = view.getFloat64(r.p, true); r.p += 8; }
    else if (field === 4 && wire === 0) v = r.int64();
    else if (field === 5 && wire === 0) v = r.varint();
    else if (field === 6 && wire === 0) { const n = r.varint(); v = n % 2 ? -(n + 1) / 2 : n / 2; }
    else if (field === 7 && wire === 0) v = r.varint() !== 0;
    else r.skip(wire);
  }
  return v;
}

function readFeature(b, start, end) {
  const r = new Reader(b, start, end);
  let type = 0, tags = [], geom = [];
  while (r.p < end) {
    const tag = r.varint(), field = tag >> 3, wire = tag & 7;
    if (field === 2 && wire === 2) { const len = r.varint(), e = r.p + len; tags = []; while (r.p < e) tags.push(r.varint()); }
    else if (field === 3 && wire === 0) type = r.varint();
    else if (field === 4 && wire === 2) { const len = r.varint(), e = r.p + len; geom = []; while (r.p < e) geom.push(r.varint()); }
    else r.skip(wire);
  }
  return { type, tags, geom };
}

// One named layer of a tile, or null.
export function readLayer(b, wanted) {
  const r = new Reader(b, 0, b.length);
  while (r.p < r.end) {
    const tag = r.varint(), field = tag >> 3, wire = tag & 7;
    if (field !== 3 || wire !== 2) { r.skip(wire); continue; }
    const size = r.varint(), end = r.p + size, l = new Reader(b, r.p, end);
    let name = null, extent = 4096;
    const keys = [], values = [], features = [];
    while (l.p < end) {
      const t = l.varint(), f = t >> 3, w = t & 7;
      if (f === 1 && w === 2) { name = l.string(); if (name !== wanted) break; }
      else if (f === 2 && w === 2) { const len = l.varint(); features.push([l.p, l.p + len]); l.p += len; }
      else if (f === 3 && w === 2) keys.push(l.string());
      else if (f === 4 && w === 2) { const len = l.varint(); values.push(readValue(b, l.p, l.p + len)); l.p += len; }
      else if (f === 5 && w === 0) extent = l.varint();
      else l.skip(w);
    }
    if (name === wanted) return { extent, keys, values, features: features.map(([s, e]) => readFeature(b, s, e)) };
    r.p = end;
  }
  return null;
}

function decodeLines(geom) {
  const out = [];
  let x = 0, y = 0, cur = null, i = 0;
  while (i < geom.length) {
    const cmd = geom[i] & 7, count = geom[i] >>> 3;
    i++;
    if (cmd === 1 || cmd === 2) {
      for (let k = 0; k < count; k++) {
        const dx = geom[i++], dy = geom[i++];
        x += (dx >>> 1) ^ -(dx & 1);
        y += (dy >>> 1) ^ -(dy & 1);
        if (cmd === 1) { cur = []; out.push(cur); }
        cur.push(x, y);
      }
    } else if (cmd === 7 && cur && cur.length >= 2) cur.push(cur[0], cur[1]);
  }
  return out;
}

// Cuts a line (flat x,y list) to a square, so each tile keeps only its own part and the
// cut points of two neighbours are computed from the same numbers.
function clipSegment(x0, y0, x1, y1, minX, minY, maxX, maxY) {
  let t0 = 0, t1 = 1;
  const dx = x1 - x0, dy = y1 - y0;
  const p = [-dx, dx, -dy, dy], q = [x0 - minX, maxX - x0, y0 - minY, maxY - y0];
  for (let i = 0; i < 4; i++) {
    if (p[i] === 0) { if (q[i] < 0) return null; continue; }
    const r = q[i] / p[i];
    if (p[i] < 0) { if (r > t1) return null; if (r > t0) t0 = r; }
    else { if (r < t0) return null; if (r < t1) t1 = r; }
  }
  if (t0 >= t1) return null;
  return [t0 === 0 ? x0 : x0 + t0 * dx, t0 === 0 ? y0 : y0 + t0 * dy,
    t1 === 1 ? x1 : x0 + t1 * dx, t1 === 1 ? y1 : y0 + t1 * dy];
}

function clipLine(pts, minX, minY, maxX, maxY) {
  const out = [];
  let cur = null;
  for (let i = 0; i + 3 < pts.length; i += 2) {
    const s = clipSegment(pts[i], pts[i + 1], pts[i + 2], pts[i + 3], minX, minY, maxX, maxY);
    if (!s) { cur = null; continue; }
    if (!cur || cur[cur.length - 2] !== s[0] || cur[cur.length - 1] !== s[1]) { cur = [s[0], s[1]]; out.push(cur); }
    cur.push(s[2], s[3]);
  }
  return out;
}

// ---------- what each kind of way costs ----------

const ROAD_CLASSES = new Set(['motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'minor', 'service',
  'track', 'path', 'pier', 'busway', 'raceway']);
const KEPT_KEYS = new Set(['class', 'subclass', 'oneway', 'access', 'foot', 'bicycle', 'brunnel', 'indoor']);
const ALLOWED = new Set(['yes', 'designated', 'permissive']);
const NO = Infinity;

// Lower is preferred; NO means never.
const PROFILES = {
  run: { motorway: NO, trunk: NO, primary: 1.7, secondary: 1.45, tertiary: 1.2, minor: 1, service: 1.1, track: 1.05,
    path: 1, footway: 0.95, pedestrian: 0.95, cycleway: 1.05, bridleway: 1.1, steps: 1.6, platform: 1.5,
    corridor: 2.5, pier: 1, busway: NO, raceway: NO },
  walk: { motorway: NO, trunk: NO, primary: 1.7, secondary: 1.45, tertiary: 1.2, minor: 1, service: 1.1, track: 1.05,
    path: 1, footway: 0.95, pedestrian: 0.95, cycleway: 1.1, bridleway: 1.1, steps: 1.2, platform: 1.5,
    corridor: 2.5, pier: 1, busway: NO, raceway: NO },
  hike: { motorway: NO, trunk: NO, primary: 2.2, secondary: 1.8, tertiary: 1.5, minor: 1.25, service: 1.3, track: 0.9,
    path: 0.85, footway: 1, pedestrian: 1.1, cycleway: 1.2, bridleway: 0.9, steps: 1.15, platform: 2,
    corridor: 3, pier: 1.2, busway: NO, raceway: NO },
  ride: { motorway: NO, trunk: NO, primary: 2, secondary: 1.4, tertiary: 1.15, minor: 1, service: 1.2, track: 1.5,
    path: 2.2, footway: 2.6, pedestrian: 2.6, cycleway: 0.75, bridleway: 2.6, steps: NO, platform: NO,
    corridor: NO, pier: 2.5, busway: NO, raceway: NO },
};
const CHEAPEST = Object.fromEntries(SPORTS.map(s => [s, Math.min(...Object.values(PROFILES[s]).filter(isFinite))]));

const INFO = [];
const INFO_INDEX = new Map();
const MULTIPLIERS = Object.fromEntries(SPORTS.map(s => [s, []]));

function infoIndex(p) {
  const key = [p.class, p.subclass, p.oneway, p.access, p.foot, p.bicycle, p.brunnel, p.indoor].join('|');
  let i = INFO_INDEX.get(key);
  if (i === undefined) {
    i = INFO.length;
    INFO.push({ ...p });
    INFO_INDEX.set(key, i);
  }
  return i;
}

function multiplier(info, sport) {
  const P = PROFILES[sport], ride = sport === 'ride';
  const own = ride ? info.bicycle : info.foot;
  if (own === 'no') return NO;
  if (info.access === 'no' && !ALLOWED.has(own)) return NO;
  let m = info.class === 'path' ? (P[info.subclass] ?? P.path) : P[info.class];
  if (m === undefined) return NO;
  if (ride && info.class === 'path' && info.subclass !== 'steps' && ALLOWED.has(info.bicycle)) m = Math.min(m, 1.1);
  if (info.indoor === 1 || info.indoor === true) m *= ride ? NO : 2;
  if (info.brunnel === 'ford') m *= ride ? 4 : 3;
  return m;
}

function multipliersFor(sport) {
  const list = MULTIPLIERS[sport];
  for (let i = list.length; i < INFO.length; i++) list.push(multiplier(INFO[i], sport));
  return list;
}

// ---------- tiles ----------

function readTile(bytes, tx, ty) {
  const layer = readLayer(bytes, 'transportation');
  const out = [];
  if (!layer) return out;
  const scale = EXTENT / layer.extent, ox = tx * EXTENT, oy = ty * EXTENT;
  for (const f of layer.features) {
    if (f.type !== 2 && f.type !== 3) continue;
    const p = {};
    for (let i = 0; i + 1 < f.tags.length; i += 2) {
      const k = layer.keys[f.tags[i]];
      if (KEPT_KEYS.has(k)) p[k] = layer.values[f.tags[i + 1]];
    }
    if (!ROAD_CLASSES.has(p.class)) continue; // leaves out rail, transit, ferry and building sites
    // Squares and piers drawn as areas: their edge is walkable, so paths ending on it connect.
    if (f.type === 3 && p.class !== 'path' && p.class !== 'pier') continue;
    const info = infoIndex(p);
    for (const line of decodeLines(f.geom)) {
      const g = new Array(line.length);
      for (let i = 0; i < line.length; i += 2) { g[i] = ox + line[i] * scale; g[i + 1] = oy + line[i + 1] * scale; }
      for (const piece of clipLine(g, ox, oy, ox + EXTENT, oy + EXTENT)) out.push({ info, pts: piece });
    }
  }
  return out;
}

const OFM_INDEX = 'https://tiles.openfreemap.org/planet';

export class Tiles {
  constructor(template, fetcher = fetch) {
    this.template = template;
    this.fetcher = url => fetcher(url); // browsers refuse fetch called as a method of another object
    this.cache = new Map();
  }

  // The tiles OpenFreeMap serves this week, or a given week's tiles named in a link.
  static async open(version, fetcher = fetch) {
    if (version && /^[0-9A-Za-z_.-]{4,48}$/.test(version)) {
      return new Tiles(`${OFM_INDEX}/${version}/{z}/{x}/{y}.pbf`, fetcher);
    }
    const res = await fetcher(OFM_INDEX);
    if (!res.ok) throw new PlanError('offline');
    const json = await res.json();
    return new Tiles(json.tiles[0], fetcher);
  }

  get version() {
    const m = this.template.match(/\/planet\/([^/]+)\//);
    return m ? m[1] : '';
  }

  get(tx, ty) {
    const key = tx + '/' + ty;
    let p = this.cache.get(key);
    if (!p) {
      const url = this.template.replace('{z}', ZOOM).replace('{x}', tx).replace('{y}', ty);
      p = this.fetcher(url)
        .then(r => { if (!r.ok) throw new PlanError('offline'); return r.arrayBuffer(); })
        .then(buf => readTile(new Uint8Array(buf), tx, ty));
      p.catch(() => this.cache.delete(key));
      this.cache.set(key, p);
    }
    return p;
  }
}

export class PlanError extends Error {
  constructor(code, index) { super(code); this.code = code; this.index = index; }
}

// ---------- the graph for one leg ----------

const CELL = 64; // tile units per grid cell

class Graph {
  constructor(minTX, minTY) {
    this.bx = minTX * EXTENT; this.by = minTY * EXTENT;
    this.xs = []; this.ys = []; this.adj = []; this.keys = new Map();
    this.ea = []; this.eb = []; this.el = []; this.ei = []; this.alive = [];
    this.grid = new Map();
  }

  node(x, y) {
    const k = (Math.round((x - this.bx) * 4) + 8) * 4194304 + Math.round((y - this.by) * 4) + 8;
    let n = this.keys.get(k);
    if (n === undefined) {
      n = this.xs.length;
      this.xs.push(x); this.ys.push(y); this.adj.push([]);
      this.keys.set(k, n);
    }
    return n;
  }

  edge(a, b, info) {
    if (a === b) return;
    const e = this.ea.length, xs = this.xs, ys = this.ys;
    this.ea.push(a); this.eb.push(b); this.ei.push(info); this.alive.push(true);
    this.el.push(Math.hypot(xs[b] - xs[a], ys[b] - ys[a]) * unitMetres((ys[a] + ys[b]) / 2));
    this.adj[a].push(e); this.adj[b].push(e);
    const x0 = Math.floor((Math.min(xs[a], xs[b]) - this.bx) / CELL), x1 = Math.floor((Math.max(xs[a], xs[b]) - this.bx) / CELL);
    const y0 = Math.floor((Math.min(ys[a], ys[b]) - this.by) / CELL), y1 = Math.floor((Math.max(ys[a], ys[b]) - this.by) / CELL);
    for (let cx = x0; cx <= x1; cx++) {
      for (let cy = y0; cy <= y1; cy++) {
        const k = (cx + 8) * 65536 + cy + 8;
        const cell = this.grid.get(k);
        if (cell) cell.push(e); else this.grid.set(k, [e]);
      }
    }
  }

  degree(v) {
    let d = 0;
    for (const e of this.adj[v]) if (this.alive[e]) d++;
    return d;
  }

  // The closest point on a usable line to (x, y), within `radius` tile units.
  nearest(x, y, radius, usable) {
    const r = Math.ceil(radius / CELL), cx0 = Math.floor((x - this.bx) / CELL), cy0 = Math.floor((y - this.by) / CELL);
    let best = null;
    const seen = new Set();
    for (let cx = cx0 - r; cx <= cx0 + r; cx++) {
      for (let cy = cy0 - r; cy <= cy0 + r; cy++) {
        const cell = this.grid.get((cx + 8) * 65536 + cy + 8);
        if (!cell) continue;
        for (const e of cell) {
          if (!this.alive[e] || seen.has(e)) continue;
          seen.add(e);
          if (!usable(e)) continue;
          const ax = this.xs[this.ea[e]], ay = this.ys[this.ea[e]], bx = this.xs[this.eb[e]], by = this.ys[this.eb[e]];
          const dx = bx - ax, dy = by - ay, len2 = dx * dx + dy * dy;
          const t = len2 === 0 ? 0 : Math.max(0, Math.min(1, ((x - ax) * dx + (y - ay) * dy) / len2));
          const px = ax + t * dx, py = ay + t * dy, d = Math.hypot(x - px, y - py);
          if (d <= radius && (!best || d < best.d)) best = { e, t, x: px, y: py, d };
        }
      }
    }
    return best;
  }

  // Connected pieces of the network, counting only usable ways.
  pieces(usable) {
    const n = this.xs.length, piece = new Int32Array(n).fill(-1);
    let id = 0;
    for (let s = 0; s < n; s++) {
      if (piece[s] >= 0) continue;
      piece[s] = id;
      const stack = [s];
      while (stack.length) {
        const v = stack.pop();
        for (const e of this.adj[v]) {
          if (!this.alive[e] || !usable(e)) continue;
          const w = this.ea[e] === v ? this.eb[e] : this.ea[e];
          if (piece[w] < 0) { piece[w] = id; stack.push(w); }
        }
      }
      id++;
    }
    return piece;
  }

  // The closest usable point in each piece of network within `radius`.
  nearestPerPiece(x, y, radius, usable, piece) {
    const best = new Map();
    this.nearest(x, y, radius, e => {
      if (!usable(e)) return false;
      const id = piece[this.ea[e]], ax = this.xs[this.ea[e]], ay = this.ys[this.ea[e]];
      const dx = this.xs[this.eb[e]] - ax, dy = this.ys[this.eb[e]] - ay, len2 = dx * dx + dy * dy;
      const t = len2 === 0 ? 0 : Math.max(0, Math.min(1, ((x - ax) * dx + (y - ay) * dy) / len2));
      const px = ax + t * dx, py = ay + t * dy, d = Math.hypot(x - px, y - py);
      const old = best.get(id);
      if (d <= radius && (!old || d < old.d)) best.set(id, { e, t, x: px, y: py, d });
      return false;
    });
    return best;
  }

  // A node at a point on a line: one of its ends when the point is that close, else a new one.
  splitAt(hit) {
    const { e } = hit, a = this.ea[e], b = this.eb[e], len = this.el[e];
    if (hit.t * len < 0.25) return a;
    if ((1 - hit.t) * len < 0.25) return b;
    const s = this.node(hit.x, hit.y);
    if (s === a || s === b) return s;
    this.alive[e] = false;
    this.edge(a, s, this.ei[e]);
    this.edge(s, b, this.ei[e]);
    return s;
  }

  // Joins each dead end to a line within `radius`, when both are at the same level
  // (a bridge never meets the road under it).
  joinDeadEnds(radius) {
    const count = this.xs.length;
    for (let v = 0; v < count; v++) {
      if (this.degree(v) !== 1) continue;
      const own = this.adj[v].find(e => this.alive[e]);
      const level = INFO[this.ei[own]].brunnel || '';
      const hit = this.nearest(this.xs[v], this.ys[v], radius, e =>
        this.ea[e] !== v && this.eb[e] !== v && (INFO[this.ei[e]].brunnel || '') === level);
      if (!hit) continue;
      const target = this.splitAt(hit);
      // The join goes both ways: copying a one-way flag would make the start of a one-way street unreachable.
      const { oneway, ...kind } = INFO[this.ei[own]];
      if (target !== v) this.edge(v, target, infoIndex(kind));
    }
  }

  // Cheapest path between two nodes, or null.
  path(s, t, sport) {
    const mult = multipliersFor(sport), ride = sport === 'ride';
    const n = this.xs.length, xs = this.xs, ys = this.ys;
    const tx = xs[t], ty = ys[t];
    // Never overestimate: the smallest ground size of a unit in the area, times the cheapest way.
    let far = WORLD / 2;
    for (let i = 0; i < n; i++) if (Math.abs(ys[i] - WORLD / 2) > Math.abs(far - WORLD / 2)) far = ys[i];
    const hScale = unitMetres(far) * CHEAPEST[sport] * 0.999;
    const g = new Float64Array(n).fill(Infinity), via = new Int32Array(n).fill(-1), done = new Uint8Array(n);
    const heap = new Heap();
    g[s] = 0;
    heap.push(Math.hypot(xs[s] - tx, ys[s] - ty) * hScale, s);
    while (heap.size) {
      const v = heap.pop();
      if (done[v]) continue;
      done[v] = 1;
      if (v === t) break;
      for (const e of this.adj[v]) {
        if (!this.alive[e]) continue;
        const info = INFO[this.ei[e]], m = mult[this.ei[e]];
        if (m === NO) continue;
        const forward = this.ea[e] === v, w = forward ? this.eb[e] : this.ea[e];
        const wrongWay = ride && ((info.oneway === 1 && !forward) || (info.oneway === -1 && forward));
        const c = g[v] + this.el[e] * m * (wrongWay ? WRONG_WAY : 1);
        if (c < g[w]) {
          g[w] = c; via[w] = e;
          heap.push(c + Math.hypot(xs[w] - tx, ys[w] - ty) * hScale, w);
        }
      }
    }
    if (!done[t]) return null;
    const nodes = [t];
    let metres = 0;
    for (let v = t; v !== s;) {
      const e = via[v];
      metres += this.el[e];
      v = this.ea[e] === v ? this.eb[e] : this.ea[e];
      nodes.push(v);
    }
    nodes.reverse();
    return { coords: nodes.map(v => unproject(xs[v], ys[v])), metres };
  }
}

class Heap {
  constructor() { this.k = []; this.v = []; }
  get size() { return this.k.length; }
  push(key, val) {
    const k = this.k, v = this.v;
    let i = k.length;
    k.push(key); v.push(val);
    while (i > 0) {
      const p = (i - 1) >> 1;
      if (k[p] <= key) break;
      k[i] = k[p]; v[i] = v[p]; i = p;
    }
    k[i] = key; v[i] = val;
  }
  pop() {
    const k = this.k, v = this.v, top = v[0], lastK = k.pop(), lastV = v.pop();
    if (k.length) {
      let i = 0;
      for (;;) {
        let c = 2 * i + 1;
        if (c >= k.length) break;
        if (c + 1 < k.length && k[c + 1] < k[c]) c++;
        if (k[c] >= lastK) break;
        k[i] = k[c]; v[i] = v[c]; i = c;
      }
      k[i] = lastK; v[i] = lastV;
    }
    return top;
  }
}

// ---------- one leg ----------

// The tiles within `margin` tile units of the straight line from a to b.
function corridor(a, b, margin) {
  const minX = Math.floor((Math.min(a[0], b[0]) - margin) / EXTENT), maxX = Math.floor((Math.max(a[0], b[0]) + margin) / EXTENT);
  const minY = Math.floor((Math.min(a[1], b[1]) - margin) / EXTENT), maxY = Math.floor((Math.max(a[1], b[1]) + margin) / EXTENT);
  const dx = b[0] - a[0], dy = b[1] - a[1], len2 = dx * dx + dy * dy, reach = margin + EXTENT * Math.SQRT1_2;
  const out = [];
  for (let tx = minX; tx <= maxX; tx++) {
    for (let ty = minY; ty <= maxY; ty++) {
      const cx = (tx + 0.5) * EXTENT, cy = (ty + 0.5) * EXTENT;
      const t = len2 === 0 ? 0 : Math.max(0, Math.min(1, ((cx - a[0]) * dx + (cy - a[1]) * dy) / len2));
      if (Math.hypot(cx - a[0] - t * dx, cy - a[1] - t * dy) <= reach) out.push([tx, ty]);
    }
  }
  return out;
}

async function buildGraph(tiles, list) {
  const minTX = Math.min(...list.map(t => t[0])), minTY = Math.min(...list.map(t => t[1]));
  const pieces = await Promise.all(list.map(([x, y]) => tiles.get(x, y)));
  const graph = new Graph(minTX, minTY);
  for (const tile of pieces) {
    for (const { info, pts } of tile) {
      let prev = graph.node(pts[0], pts[1]);
      for (let i = 2; i < pts.length; i += 2) {
        const next = graph.node(pts[i], pts[i + 1]);
        graph.edge(prev, next, info);
        prev = next;
      }
    }
  }
  return graph;
}

// The path for one leg between two placed points ([lng, lat]). Throws PlanError:
// 'far' (points too far apart), 'snap' (no usable way near a point), 'nopath'.
export async function routeLeg(tiles, from, to, sport) {
  const a = project(from[0], from[1]), b = project(to[0], to[1]);
  const mpu = unitMetres((a[1] + b[1]) / 2), span = Math.hypot(b[0] - a[0], b[1] - a[1]);
  const margins = [Math.max(0.25 * span, 800 / mpu), Math.max(0.6 * span, 2500 / mpu)];
  let lastError = null;
  for (const margin of margins) {
    const list = corridor(a, b, margin);
    if (list.length > MAX_TILES) {
      if (lastError) break;
      throw new PlanError('far');
    }
    const graph = await buildGraph(tiles, list);
    graph.joinDeadEnds(JOIN_METRES / mpu);
    const mult = multipliersFor(sport);
    const usable = e => mult[graph.ei[e]] !== NO;
    // Both ends go onto the same connected piece of network, the pair closest to the two points,
    // so a stray fragment of path next to a point never strands the leg.
    const piece = graph.pieces(usable), radius = SNAP_METRES / mpu;
    const nearA = graph.nearestPerPiece(a[0], a[1], radius, usable, piece);
    const nearB = graph.nearestPerPiece(b[0], b[1], radius, usable, piece);
    if (!nearA.size || !nearB.size) throw new PlanError('snap', nearA.size ? 1 : 0);
    let pick = null;
    for (const [id, ha] of nearA) {
      const hb = nearB.get(id);
      if (hb && (!pick || ha.d + hb.d < pick.d)) pick = { id, d: ha.d + hb.d, ha };
    }
    if (!pick) { lastError = new PlanError('nopath'); continue; }
    const s = graph.splitAt(pick.ha);
    const old = piece.length;
    const inPiece = e => usable(e) && [graph.ea[e], graph.eb[e]].some(v => v < old && piece[v] === pick.id);
    const t = graph.splitAt(graph.nearest(b[0], b[1], radius, inPiece));
    const found = graph.path(s, t, sport);
    if (found) return found;
    lastError = new PlanError('nopath');
  }
  throw lastError || new PlanError('nopath');
}

// ---------- the finished route ----------

// Fewer points along the same line: drops points within `tolerance` metres of it.
export function simplify(coords, tolerance) {
  if (coords.length < 3) return coords.slice();
  const pts = coords.map(([lng, lat]) => project(lng, lat));
  const mpu = unitMetres(pts[Math.floor(pts.length / 2)][1]), tol = tolerance / mpu;
  const keep = new Uint8Array(pts.length);
  keep[0] = keep[pts.length - 1] = 1;
  const stack = [[0, pts.length - 1]];
  while (stack.length) {
    const [i, j] = stack.pop();
    const [ax, ay] = pts[i], [bx, by] = pts[j], dx = bx - ax, dy = by - ay, len = Math.hypot(dx, dy);
    let far = -1, farD = tol;
    for (let k = i + 1; k < j; k++) {
      const d = len === 0 ? Math.hypot(pts[k][0] - ax, pts[k][1] - ay)
        : Math.abs(dy * (pts[k][0] - ax) - dx * (pts[k][1] - ay)) / len;
      if (d > farD) { far = k; farD = d; }
    }
    if (far >= 0) { keep[far] = 1; stack.push([i, far], [far, j]); }
  }
  return coords.filter((_, k) => keep[k]);
}

// The legs joined into one line, with as few points as Aera keeps whole.
export function joinLegs(legs) {
  const line = [];
  for (const leg of legs) {
    for (const c of leg.coords) {
      const last = line[line.length - 1];
      if (!last || Math.abs(last[0] - c[0]) > 1e-9 || Math.abs(last[1] - c[1]) > 1e-9) line.push(c);
    }
  }
  let tolerance = 1, out = simplify(line, tolerance);
  while (out.length > MAX_GPX_POINTS) { tolerance *= 2; out = simplify(line, tolerance); }
  return out;
}

function escapeXML(s) {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

// A GPX course (<rte>): Aera keeps a course whole and names it from <name>.
export function gpx(name, sport, line) {
  const pts = line.map(([lng, lat]) => `    <rtept lat="${lat.toFixed(6)}" lon="${lng.toFixed(6)}"/>`).join('\n');
  return `<?xml version="1.0" encoding="UTF-8"?>
<gpx version="1.1" creator="Aera route planner, aerahealth.app/plan" xmlns="http://www.topografix.com/GPX/1/1">
  <rte>
    <name>${escapeXML(name)}</name>
    <type>${GPX_TYPE[sport]}</type>
${pts}
  </rte>
</gpx>
`;
}

// ---------- the link (everything after the #) ----------

const B64 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_';

function pushNumber(n, out) {
  let v = n < 0 ? ~(n << 1) : n << 1;
  while (v >= 32) { out.push(B64[32 | (v & 31)]); v >>>= 5; }
  out.push(B64[v]);
}

export function encodeLink({ sport, points, name, version }) {
  const out = [];
  let lat0 = 0, lng0 = 0;
  for (const [lng, lat] of points) {
    const la = Math.round(lat * 1e5), lo = Math.round(lng * 1e5);
    pushNumber(la - lat0, out); pushNumber(lo - lng0, out);
    lat0 = la; lng0 = lo;
  }
  let s = `v=1&s=${LINK_CODE[sport]}&p=${out.join('')}`;
  if (version) s += `&t=${version}`;
  if (name) s += `&n=${encodeURIComponent(name)}`;
  return s;
}

export function decodeLink(hash) {
  const q = new URLSearchParams(hash.replace(/^#/, ''));
  if (q.get('v') !== '1') return null;
  const sport = Object.keys(LINK_CODE).find(k => LINK_CODE[k] === q.get('s')) || 'run';
  const nums = [];
  let v = 0, shift = 0;
  for (const ch of q.get('p') || '') {
    const c = B64.indexOf(ch);
    if (c < 0) return null;
    v |= (c & 31) << shift;
    if (c & 32) { shift += 5; continue; }
    nums.push(v & 1 ? ~(v >>> 1) : v >>> 1);
    v = 0; shift = 0;
  }
  const points = [];
  let lat = 0, lng = 0;
  for (let i = 0; i + 1 < nums.length && points.length < MAX_POINTS; i += 2) {
    lat += nums[i]; lng += nums[i + 1];
    if (Math.abs(lat) > 85e5 || Math.abs(lng) > 180e5) return null;
    points.push([lng / 1e5, lat / 1e5]);
  }
  if (!points.length) return null;
  return { sport, points, name: (q.get('n') || '').slice(0, 80), version: q.get('t') || '' };
}
