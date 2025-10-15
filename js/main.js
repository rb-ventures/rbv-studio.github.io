// ===============================
// RBV-STUDIO MAIN JS
// ===============================

// Mobile Navigation
const btn = document.querySelector('.nav-toggle');
const menu = document.getElementById('nav-menu');
if (btn && menu) {
  btn.addEventListener('click', () => {
    const open = menu.classList.toggle('open');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
}

// Smooth Scroll
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const id = a.getAttribute('href');
    if (id.length > 1) {
      e.preventDefault();
      document.querySelector(id)?.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });
    }
  });
});

// Sticky Header
const header = document.querySelector('.site-header');
const onScroll = () => header.classList.toggle('scrolled', window.scrollY > 10);
onScroll();
window.addEventListener('scroll', onScroll);

// ===============================
// Scroll Fade-In Animations
// ===============================

// Add 'fade-in' class to elements you want to animate in CSS.
const fadeEls = document.querySelectorAll('.fade-in');

const appearOptions = {
  threshold: 0.15,
  rootMargin: "0px 0px -10% 0px"
};

const appearOnScroll = new IntersectionObserver(function(entries, observer) {
  entries.forEach(entry => {
    if (!entry.isIntersecting) return;
    entry.target.classList.add('appear');
    observer.unobserve(entry.target);
  });
}, appearOptions);

fadeEls.forEach(el => appearOnScroll.observe(el));

// Optional: Automatically add .fade-in to key sections
document.querySelectorAll('section').forEach(section => {
  section.classList.add('fade-in');
  // Ensure newly-tagged sections are observed so they can transition to 'appear'
  appearOnScroll.observe(section);
});