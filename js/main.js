// ===============================
// RBV-STUDIO MAIN JS
// ===============================

const siteHeader = document.querySelector('.site-header');
const navToggle = document.querySelector('.nav-toggle');
const navMenu = document.getElementById('nav-menu');
const navLinks = navMenu ? navMenu.querySelectorAll('a[href]') : [];
const isDesktop = window.matchMedia('(min-width: 901px)');

const getHeaderOffset = () => (siteHeader?.offsetHeight || 0) + 14;

const setMenuState = (open) => {
  if (!navMenu || !navToggle) return;
  navMenu.classList.toggle('open', open);
  navToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
  document.body.classList.toggle('menu-open', open);
};

if (navToggle && navMenu) {
  navToggle.addEventListener('click', () => {
    const isOpen = navToggle.getAttribute('aria-expanded') === 'true';
    setMenuState(!isOpen);
  });

  navLinks.forEach((link) => {
    link.addEventListener('click', () => setMenuState(false));
  });

  document.addEventListener('click', (event) => {
    const target = event.target;
    if (!(target instanceof Element)) return;
    if (!navMenu.classList.contains('open')) return;
    const clickedInside = navMenu.contains(target) || navToggle.contains(target);
    if (!clickedInside) setMenuState(false);
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') setMenuState(false);
  });

  isDesktop.addEventListener('change', (event) => {
    if (event.matches) setMenuState(false);
  });
}

// Sticky Header Style
const syncHeaderScrollState = () => {
  if (!siteHeader) return;
  siteHeader.classList.toggle('scrolled', window.scrollY > 12);
};
syncHeaderScrollState();
window.addEventListener('scroll', syncHeaderScrollState, { passive: true });

// Anchor Navigation with Fixed Header Compensation
document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener('click', (event) => {
    const href = anchor.getAttribute('href');
    if (!href || href.length <= 1) return;

    const target = document.querySelector(href);
    if (!target) return;

    event.preventDefault();
    const top = target.getBoundingClientRect().top + window.scrollY - getHeaderOffset();
    window.scrollTo({ top, behavior: 'smooth' });
  });
});

// If page loads with hash, correct scroll after layout settles
if (window.location.hash && window.location.hash.length > 1) {
  window.addEventListener('load', () => {
    const target = document.querySelector(window.location.hash);
    if (!target) return;
    const top = target.getBoundingClientRect().top + window.scrollY - getHeaderOffset();
    window.scrollTo({ top });
  });
}

// Scroll Reveal Animation
const revealElements = document.querySelectorAll('.reveal');
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

if (reducedMotion) {
  revealElements.forEach((el) => el.classList.add('is-visible'));
} else if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver(
    (entries, obs) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-visible');
        obs.unobserve(entry.target);
      });
    },
    {
      threshold: 0.16,
      rootMargin: '0px 0px -8% 0px'
    }
  );

  revealElements.forEach((el) => observer.observe(el));
} else {
  revealElements.forEach((el) => el.classList.add('is-visible'));
}