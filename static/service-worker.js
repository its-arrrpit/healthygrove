// Minimal service worker for caching the shell and models
const SHELL_CACHE = 'healthygroove-shell-v1';
const MODELS_CACHE = 'healthygroove-models-v1';
const SHELL_ASSETS = [
  '/',
  '/index.html',
];
self.addEventListener('install', (event) => {
  event.waitUntil(caches.open(SHELL_CACHE).then((c) => c.addAll(SHELL_ASSETS)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', (event) => {
  event.waitUntil(self.clients.claim());
});
self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);
  if (url.pathname.startsWith('/static/models/')) {
    event.respondWith(caches.open(MODELS_CACHE).then(async (cache) => {
      const cached = await cache.match(event.request);
      if (cached) return cached;
      const res = await fetch(event.request);
      if (res.ok) cache.put(event.request, res.clone());
      return res;
    }));
    return;
  }
  if (SHELL_ASSETS.includes(url.pathname)) {
    event.respondWith(caches.open(SHELL_CACHE).then(async (cache) => {
      const cached = await cache.match(event.request);
      if (cached) return cached;
      const res = await fetch(event.request);
      if (res.ok) cache.put(event.request, res.clone());
      return res;
    }));
  }
});
