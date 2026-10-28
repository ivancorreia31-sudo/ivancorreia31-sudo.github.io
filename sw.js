/* Bonnet Up: keeps a copy of the game on the phone so it opens instantly and plays offline. */
const VERSION = 'bonnet-up-v19';
const EXT = 'bonnet-up-ext';
const CORE = ['./', './index.html', './game.html', './manifest.webmanifest', './icon-192.png', './icon-512.png', './icon-maskable-192.png', './icon-maskable-512.png', './apple-touch-icon.png', './favicon-48.png', './privacy.html'];
const LIB = 'https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js';
const EXT_HOSTS = ['cdnjs.cloudflare.com', 'fonts.googleapis.com', 'fonts.gstatic.com'];

self.addEventListener('install', e => {
  e.waitUntil((async () => {
    const c = await caches.open(VERSION);
    await c.addAll(CORE);
    /* the 3D engine comes from a CDN: grab it now if we can, otherwise the first run caches it */
    try { const x = await caches.open(EXT); if (!(await x.match(LIB))) await x.add(LIB); } catch (err) { /* offline right now */ }
    await self.skipWaiting();
  })());
});
self.addEventListener('activate', e => {
  e.waitUntil((async () => {
    for (const k of await caches.keys()) if (k.startsWith('bonnet-up-v') && k !== VERSION) await caches.delete(k);
    await self.clients.claim();
  })());
});
const fresh = (req, ms) => new Promise(resolve => {
  const t = setTimeout(() => resolve(null), ms);
  fetch(req).then(r => { clearTimeout(t); resolve(r && r.ok ? r : null); }).catch(() => { clearTimeout(t); resolve(null); });
});
self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin === self.location.origin) {
    const page = req.mode === 'navigate' || /\.html$|\/$/.test(url.pathname);
    e.respondWith((async () => {
      const c = await caches.open(VERSION);
      if (page) {
        /* pages: the newest copy when the network is quick, the saved copy when it isn't */
        const r = await fresh(req, 3000);
        if (r) { c.put(req, r.clone()); return r; }
        return (await c.match(req, { ignoreSearch: true })) || (await c.match('./index.html')) || Response.error();
      }
      /* pictures and the manifest: the saved copy, refreshed in the background */
      const hit = await c.match(req, { ignoreSearch: true });
      const net = fetch(req).then(r => { if (r && r.ok) c.put(req, r.clone()); return r; }).catch(() => null);
      return hit || (await net) || Response.error();
    })());
    return;
  }
  if (EXT_HOSTS.includes(url.hostname)) {
    /* the 3D engine and the fonts never change at these addresses: keep them once fetched */
    e.respondWith((async () => {
      const c = await caches.open(EXT);
      const hit = await c.match(req);
      if (hit) return hit;
      try { const r = await fetch(req); if (r && (r.ok || r.type === 'opaque')) c.put(req, r.clone()); return r; }
      catch (err) { return Response.error(); }
    })());
  }
});
