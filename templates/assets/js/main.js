/**
 * Website Migration Tool - Main JavaScript
 * Handles mobile navigation and interactive features
 */

// Mobile Menu Toggle
function toggleMobileMenu() {
    const navMenu = document.getElementById('navMenu');
    if (navMenu) {
        navMenu.classList.toggle('active');
    }
}

// Close mobile menu when clicking outside
document.addEventListener('click', function(event) {
    const navMenu = document.getElementById('navMenu');
    const toggle = document.querySelector('.mobile-menu-toggle');

    if (navMenu && toggle) {
        if (!navMenu.contains(event.target) && !toggle.contains(event.target)) {
            navMenu.classList.remove('active');
        }
    }
});

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href !== '#' && href !== '#main-content') {
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        }
    });
});

// Add active class to current page in navigation
document.addEventListener('DOMContentLoaded', function() {
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    const navLinks = document.querySelectorAll('.nav-menu a');

    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPage) {
            link.classList.add('active');
        }
    });
});

// Accessible keyboard navigation
document.addEventListener('keydown', function(e) {
    // Close mobile menu on Escape
    if (e.key === 'Escape') {
        const navMenu = document.getElementById('navMenu');
        if (navMenu && navMenu.classList.contains('active')) {
            navMenu.classList.remove('active');
        }
    }
});

// Print friendly
window.addEventListener('beforeprint', function() {
    // Expand any collapsed content before printing
    const collapsibles = document.querySelectorAll('.collapsed');
    collapsibles.forEach(el => el.classList.remove('collapsed'));
});
