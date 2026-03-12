// Service Worker self-destruct: clears all caches and unregisters itself
// This fixes cross-origin CSS issues caused by domain redirect changes

self.addEventListener('install', event => {
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => caches.delete(cacheName))
      );
    }).then(() => {
      return self.registration.unregister();
    }).then(() => {
      return self.clients.matchAll();
    }).then(clients => {
      clients.forEach(client => client.navigate(client.url));
    })
  );
});
