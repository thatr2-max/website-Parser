/**
 * Municipal Website Template - Main JavaScript
 * Minimal, accessible mobile menu functionality
 */

(function() {
  'use strict';

  /**
   * Mobile menu toggle functionality
   */
  function initMobileMenu() {
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');

    if (!navToggle || !navMenu) {
      return;
    }

    navToggle.addEventListener('click', function() {
      const isExpanded = navToggle.getAttribute('aria-expanded') === 'true';

      // Toggle menu visibility
      navMenu.classList.toggle('active');

      // Update ARIA attributes for accessibility
      navToggle.setAttribute('aria-expanded', !isExpanded);

      // Update button text
      navToggle.textContent = isExpanded ? 'Menu' : 'Close';
    });

    // Close menu when clicking outside
    document.addEventListener('click', function(event) {
      const isClickInside = navToggle.contains(event.target) || navMenu.contains(event.target);

      if (!isClickInside && navMenu.classList.contains('active')) {
        navMenu.classList.remove('active');
        navToggle.setAttribute('aria-expanded', 'false');
        navToggle.textContent = 'Menu';
      }
    });

    // Close menu on escape key
    document.addEventListener('keydown', function(event) {
      if (event.key === 'Escape' && navMenu.classList.contains('active')) {
        navMenu.classList.remove('active');
        navToggle.setAttribute('aria-expanded', 'false');
        navToggle.textContent = 'Menu';
        navToggle.focus();
      }
    });

    // Close menu when window is resized above mobile breakpoint
    let resizeTimer;
    window.addEventListener('resize', function() {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(function() {
        if (window.innerWidth > 768 && navMenu.classList.contains('active')) {
          navMenu.classList.remove('active');
          navToggle.setAttribute('aria-expanded', 'false');
          navToggle.textContent = 'Menu';
        }
      }, 250);
    });
  }

  /**
   * Form validation for contact form
   */
  function initFormValidation() {
    const contactForm = document.querySelector('#contact-form');

    if (!contactForm) {
      return;
    }

    contactForm.addEventListener('submit', function(event) {
      event.preventDefault();

      let isValid = true;
      const formElements = contactForm.elements;

      // Clear previous error messages
      const errorMessages = contactForm.querySelectorAll('.error-message');
      errorMessages.forEach(function(msg) {
        msg.remove();
      });

      // Validate required fields
      for (let i = 0; i < formElements.length; i++) {
        const field = formElements[i];

        if (field.hasAttribute('required') && !field.value.trim()) {
          isValid = false;
          showError(field, 'This field is required');
        }

        // Email validation
        if (field.type === 'email' && field.value.trim()) {
          const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
          if (!emailRegex.test(field.value)) {
            isValid = false;
            showError(field, 'Please enter a valid email address');
          }
        }
      }

      if (isValid) {
        // Form is valid - would normally submit here
        // For template purposes, just show success message
        const successMsg = document.createElement('div');
        successMsg.className = 'success-message';
        successMsg.textContent = 'Thank you! Your message has been sent.';
        successMsg.setAttribute('role', 'status');
        successMsg.setAttribute('aria-live', 'polite');
        contactForm.insertBefore(successMsg, contactForm.firstChild);

        // Reset form
        contactForm.reset();
      }
    });
  }

  /**
   * Display error message for form field
   */
  function showError(field, message) {
    const errorMsg = document.createElement('div');
    errorMsg.className = 'error-message';
    errorMsg.textContent = message;
    errorMsg.setAttribute('role', 'alert');

    field.setAttribute('aria-invalid', 'true');
    field.parentNode.appendChild(errorMsg);
  }

  /**
   * Set active navigation link based on current page
   */
  function setActiveNavLink() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-menu a');

    navLinks.forEach(function(link) {
      const linkPath = new URL(link.href).pathname;

      if (currentPath === linkPath ||
          (currentPath === '/' && linkPath.endsWith('index.html'))) {
        link.classList.add('active');
        link.setAttribute('aria-current', 'page');
      }
    });
  }

  /**
   * Initialize all functionality when DOM is ready
   */
  function init() {
    initMobileMenu();
    initFormValidation();
    setActiveNavLink();
  }

  // Wait for DOM to be ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
