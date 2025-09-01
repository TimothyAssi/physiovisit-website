(function () {
  function trackCallAndNavigate(url) {
    var go = function() { if (url) window.location.href = url; };
    try {
      if (typeof gtag === 'function') {
        gtag('event', 'conversion', {
          send_to: 'AW-620935990/HnVxCJ2N2JEbELb2iqgC',
          value: 1.0,
          currency: 'EUR',
          event_callback: go
        });
        // fallback als callback niet vuurt binnen 800ms
        setTimeout(go, 800);
      } else {
        go();
      }
    } catch(e) { go(); }
  }

  function bindTelLinks() {
    var links = document.querySelectorAll('a[href^="tel:"]');
    links.forEach(function(link){
      if (link.dataset.gadsBound) return;
      link.addEventListener('click', function(e){
        e.preventDefault();
        trackCallAndNavigate(link.getAttribute('href'));
      }, {passive:true});
      link.dataset.gadsBound = '1';
    });
  }

  if (document.readyState !== 'loading') bindTelLinks();
  else document.addEventListener('DOMContentLoaded', bindTelLinks);
})();