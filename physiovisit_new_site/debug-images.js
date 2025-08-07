/**
 * Silent Image Handler for PhysioVisit
 * Production version without console logging for crawler compatibility
 */

// Silent function to check images without logging
function checkImages() {
    const images = document.querySelectorAll('img');
    let stats = {
        total: images.length,
        loaded: 0,
        failed: 0,
        pending: 0
    };
    
    images.forEach((img) => {
        if (img.complete) {
            if (img.naturalWidth > 0) {
                stats.loaded++;
            } else {
                stats.failed++;
            }
        } else {
            stats.pending++;
        }
    });
    
    return stats;
}

// Silent initialization
document.addEventListener('DOMContentLoaded', function() {
    // Initialize without logging
    setTimeout(checkImages, 100);
    
    window.addEventListener('load', function() {
        setTimeout(checkImages, 500);
    });
});

// Make function available globally for debugging if needed
window.checkImages = checkImages;