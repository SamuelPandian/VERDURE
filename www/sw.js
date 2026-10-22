// VERDURE Service Worker for Offline In-Field Execution
const CACHE_NAME = 'verdure-cache-v2';
const ASSETS_TO_CACHE = [
  './',
  './index.html',
  './manifest.json',
  './samples/potato_early_blight.jpg',
  './samples/field_rice_canopy.jpg',
  './samples/motion_blur_leaf.jpg',
  './samples/hand_occlusion_leaf.jpg',
  './samples/soil_non_foliage.jpg',
  './samples/confocal_stomata.jpg'
];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS_TO_CACHE))
  );
  self.skipWaiting();
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            return caches.delete(key);
          }
        })
      );
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', (e) => {
  e.respondWith(
    caches.match(e.request).then((res) => res || fetch(e.request))
  );
});
