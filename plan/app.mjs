// The route planner page: the map, the points, and sending the route to Aera.
import * as maplibregl from './maplibre/maplibre-gl.mjs';
import { Tiles, routeLeg, joinLegs, gpx, encodeLink, decodeLink, MAX_POINTS, MAX_METRES } from './planner.mjs';
import { qrSvg } from './qr.mjs';

const $ = id => document.getElementById(id);
const touch = matchMedia('(pointer: coarse)').matches;
const phone = touch && (() => {
  try {
    return !!navigator.canShare && navigator.canShare({ files: [new File(['x'], 'route.gpx', { type: 'application/gpx+xml' })] });
  } catch { return false; }
})();
const tap = touch ? 'Tap' : 'Click';
const MESSAGES = {
  start: `${tap} the map to place your start.`,
  next: `${tap} where you want to go next.`,
  ready: `Drag a point to move it, or ${tap.toLowerCase()} to add more.`,
  zoom: 'Zoom in closer to place a point.',
  finding: 'Finding a path',
  far: 'These points are too far apart. Add one in between.',
  snap: 'No road or trail near this point.',
  nopath: 'No path between these points. Try nearer a road or trail.',
  sport: 'No path for that activity between these points.',
  offline: 'The map didn’t load. Check your connection and try again.',
  full: 'That’s the most points a route can have.',
  long: 'Aera takes routes up to 200 km. Remove a point to send it.',
  fromLink: 'Your route from the computer. Open it in Aera to keep it.',
};
const SPORT_NAME = { run: 'Run', walk: 'Walk', hike: 'Hike', ride: 'Ride' };
let zone = '';
try { zone = Intl.DateTimeFormat().resolvedOptions().timeZone || ''; } catch { /* no zone */ }
// Miles only for a US English browser in an American time zone; everyone else gets kilometres.
const miles = (navigator.language || '').toLowerCase() === 'en-us' && zone.startsWith('America/');
const number = new Intl.NumberFormat(navigator.language || 'en', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
const distance = m => number.format(m / (miles ? 1609.344 : 1000)) + (miles ? ' mi' : ' km');

// Where the map opens: the city of the browser's time zone, read on this device only.
const TIME_ZONE_CITIES = {
  'Europe/Budapest': [19.0402, 47.4979], 'Europe/Vienna': [16.3738, 48.2082], 'Europe/Berlin': [13.405, 52.52],
  'Europe/Zurich': [8.5417, 47.3769], 'Europe/Prague': [14.4378, 50.0755], 'Europe/Warsaw': [21.0122, 52.2297],
  'Europe/London': [-0.1276, 51.5072], 'Europe/Dublin': [-6.2603, 53.3498], 'Europe/Paris': [2.3522, 48.8566],
  'Europe/Amsterdam': [4.9041, 52.3676], 'America/New_York': [-73.9712, 40.7831], 'America/Chicago': [-87.6298, 41.8781],
  'America/Denver': [-104.9903, 39.7392], 'America/Los_Angeles': [-118.2437, 34.0522], 'Australia/Sydney': [151.2093, -33.8688],
};

let sport = 'run';
const points = []; // where each point was placed, [lng, lat]
const legs = []; // legs[i] runs from points[i] to points[i + 1]
const markers = [];
let version = ''; // the week of map tiles the route was found on

// ---------- tiles ----------

const link = decodeLink(location.hash);
let tilesPromise = null;
let wanted = link ? link.version : '';
function tiles() {
  if (!tilesPromise) {
    tilesPromise = Tiles.open(wanted).then(t => { version = t.version; return t; });
    tilesPromise.catch(() => { tilesPromise = null; });
  }
  return tilesPromise;
}

async function leg(from, to, kind) {
  try {
    return await routeLeg(await tiles(), from, to, kind);
  } catch (e) {
    if (e.code !== 'offline' || !wanted) throw e;
    wanted = ''; // that week's tiles are gone: use this week's
    tilesPromise = null;
    return routeLeg(await tiles(), from, to, kind);
  }
}

// One change at a time, in the order they were asked for.
let queue = Promise.resolve();
const enqueue = task => { queue = queue.then(task).catch(e => { console.error(e); update('offline', true); }); };

// ---------- the map ----------

const start = link ? { center: link.points[0], zoom: 13 }
  : TIME_ZONE_CITIES[zone] ? { center: TIME_ZONE_CITIES[zone], zoom: 12 } : { center: [10, 50], zoom: 3.6 };

const map = new maplibregl.Map({
  container: 'map',
  style: 'https://tiles.openfreemap.org/styles/liberty',
  center: start.center,
  zoom: start.zoom,
  attributionControl: { compact: true },
  dragRotate: false,
  pitchWithRotate: false,
  touchPitch: false,
});
map.touchZoomRotate.disableRotation();
map.addControl(new maplibregl.NavigationControl({ showCompass: false }), 'top-right');
map.addControl(new maplibregl.GeolocateControl({ fitBoundsOptions: { maxZoom: 14 } }), 'top-right');

map.on('load', () => {
  map.addSource('route', { type: 'geojson', data: { type: 'FeatureCollection', features: [] } });
  const layout = { 'line-join': 'round', 'line-cap': 'round' };
  map.addLayer({ id: 'route-casing', type: 'line', source: 'route', layout, paint: { 'line-color': '#ffffff', 'line-width': 9 } });
  map.addLayer({ id: 'route-line', type: 'line', source: 'route', layout, paint: { 'line-color': '#0f7a57', 'line-width': 5 } });
  drawRoute();
});

map.on('click', e => {
  if (e.originalEvent.target.closest && e.originalEvent.target.closest('.pin')) return;
  if (map.getZoom() < 11) {
    map.easeTo({ center: e.lngLat, zoom: Math.min(13, map.getZoom() + 3) });
    say('zoom');
    return;
  }
  addPoint([e.lngLat.lng, e.lngLat.lat]);
});

function makeMarker(p) {
  const el = document.createElement('div');
  el.className = 'pin';
  const marker = new maplibregl.Marker({ element: el, draggable: true }).setLngLat(p).addTo(map);
  marker.on('dragend', () => moved(marker));
  return marker;
}

// A point shows where its leg starts or ends: on the path, not where it was placed.
function shownAt(i) {
  if (legs[i]) return legs[i].coords[0];
  if (i > 0 && legs[i - 1]) return legs[i - 1].coords[legs[i - 1].coords.length - 1];
  return points[i];
}

function drawRoute() {
  const source = map.getSource('route');
  if (source) {
    source.setData({ type: 'FeatureCollection', features: legs.map(l => ({
      type: 'Feature', properties: {}, geometry: { type: 'LineString', coordinates: l.coords },
    })) });
  }
}

// ---------- state on screen ----------

function say(key, error = false) {
  const status = $('status');
  status.textContent = MESSAGES[key];
  status.classList.toggle('error', error);
}

const metres = () => legs.reduce((sum, l) => sum + l.metres, 0);
const routeName = () => $('name').value.trim() || `${SPORT_NAME[sport]} ${distance(metres())}`;

function linkHash() {
  return encodeLink({ sport, points, name: $('name').value.trim(), version });
}

function update(key, error = false) {
  markers.forEach((m, i) => {
    m.setLngLat(shownAt(i));
    const el = m.getElement();
    el.classList.toggle('start', i === 0);
    el.classList.toggle('end', i > 0 && i === markers.length - 1);
  });
  drawRoute();
  const total = metres(), tooLong = total > MAX_METRES;
  $('dist').textContent = distance(total);
  $('send').disabled = $('download').disabled = !legs.length || tooLong;
  $('undo').disabled = $('clear').disabled = !points.length;
  if (!key) key = tooLong ? 'long' : ['start', 'next'][points.length] || 'ready';
  say(key, error || tooLong);
  history.replaceState(null, '', location.pathname + location.search + (points.length ? '#' + linkHash() : ''));
}

function fail(e) {
  update(e && MESSAGES[e.code] ? e.code : 'offline', true);
}

// ---------- editing ----------

function addPoint(p) {
  enqueue(async () => {
    if (points.length >= MAX_POINTS) return update('full', true);
    points.push(p);
    markers.push(makeMarker(p));
    if (points.length === 1) return update();
    say('finding');
    try {
      legs.push(await leg(points[points.length - 2], p, sport));
    } catch (e) {
      points.pop();
      markers.pop().remove();
      return fail(e);
    }
    update();
  });
}

function moved(marker) {
  enqueue(async () => {
    const i = markers.indexOf(marker);
    if (i < 0) return;
    const old = points[i], ll = marker.getLngLat();
    points[i] = [ll.lng, ll.lat];
    say('finding');
    try {
      const before = i > 0 ? await leg(points[i - 1], points[i], sport) : null;
      const after = i < points.length - 1 ? await leg(points[i], points[i + 1], sport) : null;
      if (before) legs[i - 1] = before;
      if (after) legs[i] = after;
    } catch (e) {
      points[i] = old;
      return fail(e);
    }
    update();
  });
}

$('undo').addEventListener('click', () => enqueue(() => {
  if (!points.length) return;
  points.pop();
  markers.pop().remove();
  legs.length = Math.max(0, points.length - 1);
  update();
}));

$('clear').addEventListener('click', () => enqueue(() => {
  points.length = 0;
  legs.length = 0;
  markers.splice(0).forEach(m => m.remove());
  update();
}));

document.querySelectorAll('input[name="sport"]').forEach(input => input.addEventListener('change', () => enqueue(async () => {
  const next = input.value;
  if (next === sport) return;
  if (points.length < 2) { sport = next; return update(); }
  say('finding');
  try {
    const fresh = [];
    for (let i = 0; i + 1 < points.length; i++) fresh.push(await leg(points[i], points[i + 1], next));
    legs.splice(0, legs.length, ...fresh);
    sport = next;
  } catch (e) {
    $('s-' + sport).checked = true;
    return fail(e.code === 'nopath' ? { code: 'sport' } : e);
  }
  update();
})));

$('name').addEventListener('input', () => { if (points.length) update(); });

// ---------- sending ----------

const fileName = () => routeName().replace(/[\\/:*?"<>|]+/g, '-') + '.gpx';
const gpxText = () => gpx(routeName(), sport, joinLegs(legs));

function download() {
  const url = URL.createObjectURL(new Blob([gpxText()], { type: 'application/gpx+xml' }));
  const a = document.createElement('a');
  a.href = url;
  a.download = fileName();
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 10000);
}

async function share() {
  const file = new File([gpxText()], fileName(), { type: 'application/gpx+xml' });
  try {
    await navigator.share({ files: [file] });
  } catch (e) {
    if (e.name !== 'AbortError') download();
  }
}

function showCode() {
  $('qr-code').innerHTML = qrSvg(location.origin + location.pathname + '#' + linkHash());
  $('qr').showModal();
}

if (phone) $('send').textContent = 'Open in Aera';
$('send').addEventListener('click', () => (phone ? share() : showCode()));
$('download').addEventListener('click', download);

// ---------- a route that came in a link ----------

if (link) {
  sport = link.sport;
  $('s-' + sport).checked = true;
  $('name').value = link.name;
  enqueue(async () => {
    link.points.forEach(p => { points.push(p); markers.push(makeMarker(p)); });
    say('finding');
    let failure = null;
    try {
      for (let i = 0; i + 1 < points.length; i++) legs.push(await leg(points[i], points[i + 1], sport));
    } catch (e) {
      failure = e;
      points.splice(legs.length + 1).forEach(() => markers.pop().remove());
    }
    const box = new maplibregl.LngLatBounds();
    (legs.length ? legs.flatMap(l => l.coords) : points).forEach(p => box.extend(p));
    const wide = matchMedia('(min-width: 721px)').matches;
    map.fitBounds(box, { padding: wide ? { top: 48, bottom: 48, left: 400, right: 72 } : 36, maxZoom: 16, duration: 0 });
    if (failure) fail(failure); else update(phone && legs.length ? 'fromLink' : undefined);
  });
} else {
  update();
}
