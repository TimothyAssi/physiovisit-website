// Service Worker for PhysioVisit - Aggressive caching for performance
const CACHE_NAME = 'physiovisit-cache-v2';
const STATIC_ASSETS = [
  '/',
  '/index.html',
  '/kinesitherapie.html',
  '/kinetec-huren.html', 
  '/contact.html',
  '/styles.min.css',
  '/script.min.js',
  '/assets/img/physiovisit logo.png',
  '/assets/img/ik en charlotte.jpg',
  '/manifest.json'
];

// Install event - cache static assets
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(STATIC_ASSETS))
      .then(() => self.skipWaiting())
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames
          .filter(cacheName => cacheName !== CACHE_NAME)
          .map(cacheName => caches.delete(cacheName))
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch event - serve from cache, fallback to network
self.addEventListener('fetch', event => {
  // Only handle GET requests
  if (event.request.method !== 'GET') return;
  
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        if (response) {
          return response; // Return cached version
        }
        
        return fetch(event.request)
          .then(response => {
            // Don't cache non-successful responses
            if (!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }
            
            const responseToCache = response.clone();
            
            // Cache images and fonts for longer
            if (event.request.url.includes('/assets/img/') || 
                event.request.url.includes('fonts.googleapis.com') ||
                event.request.url.includes('fonts.gstatic.com')) {
              
              caches.open(CACHE_NAME + '-assets')
                .then(cache => cache.put(event.request, responseToCache));
            }
            
            return response;
          })
          .catch(() => {
            // Fallback for HTML pages
            if (event.request.headers.get('accept').includes('text/html')) {
              return caches.match('/index.html');
            }
          });
      })
  );
});