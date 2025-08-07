/**
 * PhysioVisit Website JavaScript
 * Handles form validation, interactivity, and user experience enhancements
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all functionality
    initImageErrorHandling();
    initFormValidation();
    initSmoothScrolling();
    initLazyLoading();
    initFAQAccordion();
    initPriceCalculator();
    initAnimations();
    initMobileOptimizations();
});

/**
 * Image Error Handling and Fallbacks
 */
function initImageErrorHandling() {
    const images = document.querySelectorAll('img');
    
    images.forEach(img => {
        // Add error handling
        img.addEventListener('error', function() {
            // Image failed to load - handled gracefully
            
            // Try different fallback strategies
            if (this.src.includes('assets/img/')) {
                // Try without assets prefix
                const newSrc = this.src.replace('assets/img/', 'img/');
                this.src = newSrc;
            } else if (this.src.includes('img/')) {
                // Try with assets prefix
                const newSrc = this.src.replace('img/', 'assets/img/');
                this.src = newSrc;
            } else {
                // Create a fallback div
                this.style.display = 'none';
                const fallback = document.createElement('div');
                fallback.className = 'img-fallback';
                fallback.style.width = this.width || '200px';
                fallback.style.height = this.height || '200px';
                this.parentNode.insertBefore(fallback, this.nextSibling);
            }
        });
        
        // Check if image is already loaded (for cached images)
        if (img.complete && img.naturalHeight !== 0) {
            // Image already loaded
        }
    });
}

/**
 * Form Validation for Contact Form
 */
function initFormValidation() {
    const contactForm = document.getElementById('contactForm');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(event) {
            // Only prevent default if validation fails
            if (!validateForm(contactForm)) {
                event.preventDefault();
                event.stopPropagation();
                contactForm.classList.add('was-validated');
                return false;
            }
            
            // If validation passes, let Netlify handle the submission
            // Show loading state but don't prevent submission
            const submitButton = contactForm.querySelector('button[type="submit"]');
            const loadingSpinner = submitButton.querySelector('.loading-spinner');
            
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.innerHTML = '<i class="bi bi-hourglass-split me-2"></i>Verzenden...';
            }
            
            if (loadingSpinner) {
                loadingSpinner.classList.remove('d-none');
            }
            
            // Let the form submit naturally to Netlify
            return true;
        });
        
        // Real-time validation
        const inputs = contactForm.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(this);
            });
            
            input.addEventListener('input', function() {
                if (this.classList.contains('is-invalid')) {
                    validateField(this);
                }
            });
        });
    }
}

/**
 * Validate individual form field
 */
function validateField(field) {
    const isValid = field.checkValidity();
    
    if (isValid) {
        field.classList.remove('is-invalid');
        field.classList.add('is-valid');
    } else {
        field.classList.remove('is-valid');
        field.classList.add('is-invalid');
    }
    
    return isValid;
}

/**
 * Validate entire form
 */
function validateForm(form) {
    let isValid = true;
    const requiredFields = form.querySelectorAll('[required]');
    
    requiredFields.forEach(field => {
        if (!validateField(field)) {
            isValid = false;
        }
    });
    
    // Custom email validation
    const emailField = form.querySelector('input[type="email"]');
    if (emailField && emailField.value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(emailField.value)) {
            emailField.classList.add('is-invalid');
            isValid = false;
        }
    }
    
    // Custom phone validation (Belgian format)
    const phoneField = form.querySelector('input[type="tel"]');
    if (phoneField && phoneField.value) {
        const phoneRegex = /^(\+32|0)[1-9][0-9]{7,8}$/;
        if (!phoneRegex.test(phoneField.value.replace(/\s/g, ''))) {
            phoneField.setCustomValidity('Vul een geldig Belgisch telefoonnummer in');
            phoneField.classList.add('is-invalid');
            isValid = false;
        } else {
            phoneField.setCustomValidity('');
            phoneField.classList.remove('is-invalid');
            phoneField.classList.add('is-valid');
        }
    }
    
    return isValid;
}

/**
 * Handle form submission (now only used for fallback scenarios)
 * Netlify handles the actual form submission
 */
function handleFormSubmission(form) {
    // This function is now only used as a fallback
    // The main form submission is handled by Netlify
}

/**
 * Smooth scrolling for anchor links
 */
function initSmoothScrolling() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                e.preventDefault();
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

/**
 * Lazy loading for images
 */
function initLazyLoading() {
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src || img.src;
                    img.classList.remove('img-lazy');
                    observer.unobserve(img);
                }
            });
        });
        
        const lazyImages = document.querySelectorAll('.img-lazy');
        lazyImages.forEach(img => imageObserver.observe(img));
    }
}

/**
 * FAQ Accordion functionality (custom implementation)
 */
function initFAQAccordion() {
    const faqItems = document.querySelectorAll('.faq-item');
    
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        const answer = item.querySelector('.faq-answer');
        
        if (question && answer) {
            question.addEventListener('click', function() {
                const isActive = answer.classList.contains('active');
                
                // Close all other FAQ items
                faqItems.forEach(otherItem => {
                    const otherAnswer = otherItem.querySelector('.faq-answer');
                    if (otherAnswer && otherAnswer !== answer) {
                        otherAnswer.classList.remove('active');
                    }
                });
                
                // Toggle current item
                answer.classList.toggle('active', !isActive);
            });
        }
    });
}

/**
 * Price Calculator for Equipment Rental
 */
function initPriceCalculator() {
    const apparaatSelect = document.getElementById('apparaatSelect');
    const aantalDagen = document.getElementById('aantalDagen');
    const totalePrijs = document.getElementById('totalePrijs');
    
    if (apparaatSelect && aantalDagen && totalePrijs) {
        function updatePrice() {
            const prijsPerDag = parseFloat(apparaatSelect.value) || 0;
            const dagen = parseInt(aantalDagen.value) || 0;
            const totaal = prijsPerDag * dagen;
            
            totalePrijs.textContent = '€' + totaal.toFixed(0);
            
            // Add visual feedback for calculations
            if (totaal > 0) {
                totalePrijs.classList.add('text-primary');
                totalePrijs.style.transform = 'scale(1.1)';
                setTimeout(() => {
                    totalePrijs.style.transform = 'scale(1)';
                }, 150);
            }
        }
        
        apparaatSelect.addEventListener('change', updatePrice);
        aantalDagen.addEventListener('input', updatePrice);
        
        // Initialize calculation
        updatePrice();
    }
}

/**
 * Scroll animations and effects
 */
function initAnimations() {
    // Animate elements on scroll
    if ('IntersectionObserver' in window) {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const animationObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                }
            });
        }, observerOptions);
        
        // Observe elements that should animate
        const animateElements = document.querySelectorAll('.service-card, .icon-box, .testimonial-card, .team-photo');
        animateElements.forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(20px)';
            el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            animationObserver.observe(el);
        });
    }
    
    // Add CSS for animations
    const style = document.createElement('style');
    style.textContent = `
        .animate-in {
            opacity: 1 !important;
            transform: translateY(0) !important;
        }
        
        .service-card:hover {
            transform: translateY(-5px);
            transition: transform 0.3s ease;
        }
        
        .team-photo:hover {
            transform: scale(1.02);
            transition: transform 0.3s ease;
        }
    `;
    document.head.appendChild(style);
}

/**
 * Mobile-specific optimizations
 */
function initMobileOptimizations() {
    // Improve mobile navigation
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
        // Close mobile menu when clicking on a link
        const navLinks = navbarCollapse.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                if (navbarCollapse.classList.contains('show')) {
                    navbarToggler.click();
                }
            });
        });
        
        // Close mobile menu when clicking outside
        document.addEventListener('click', (e) => {
            if (navbarCollapse.classList.contains('show') && 
                !navbarCollapse.contains(e.target) && 
                !navbarToggler.contains(e.target)) {
                navbarToggler.click();
            }
        });
    }
    
    // Touch-friendly interactions
    if ('ontouchstart' in window) {
        document.body.classList.add('touch-device');
        
        // Add touch-specific styles
        const touchStyle = document.createElement('style');
        touchStyle.textContent = `
            .touch-device .btn {
                min-height: 44px;
                padding: 12px 24px;
            }
            
            .touch-device .form-control {
                min-height: 44px;
            }
            
            .touch-device .service-card:hover {
                transform: none;
            }
        `;
        document.head.appendChild(touchStyle);
    }
    
    // Optimize form inputs for mobile
    const phoneInputs = document.querySelectorAll('input[type="tel"]');
    phoneInputs.forEach(input => {
        input.setAttribute('pattern', '[0-9+\\-\\s]+');
        input.setAttribute('inputmode', 'tel');
    });
    
    const emailInputs = document.querySelectorAll('input[type="email"]');
    emailInputs.forEach(input => {
        input.setAttribute('inputmode', 'email');
    });
}

/**
 * Utility Functions
 */

// Debounce function to limit rapid function calls
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Check if element is in viewport
function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}

// Format phone number for display
function formatPhoneNumber(phone) {
    // Simple Belgian phone number formatting
    const cleaned = phone.replace(/\D/g, '');
    if (cleaned.startsWith('32')) {
        return '+32 ' + cleaned.substring(2, 3) + ' ' + cleaned.substring(3, 5) + ' ' + cleaned.substring(5, 7) + ' ' + cleaned.substring(7);
    } else if (cleaned.startsWith('0')) {
        return cleaned.substring(0, 4) + ' ' + cleaned.substring(4, 6) + ' ' + cleaned.substring(6, 8) + ' ' + cleaned.substring(8);
    }
    return phone;
}

// Error handling for failed network requests
window.addEventListener('unhandledrejection', function(event) {
    // Unhandled promise rejection handled
    // Could show user-friendly error message here
});

// Performance monitoring
if ('performance' in window) {
    window.addEventListener('load', function() {
        setTimeout(() => {
            const perfData = performance.getEntriesByType('navigation')[0];
            if (perfData) {
                // Performance data available but not logged for crawler compatibility
            }
        }, 0);
    });
}