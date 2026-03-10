// Mobile nav toggle
const navToggle = document.querySelector('.nav-toggle');
const navLinks = document.querySelector('.nav-links');

navToggle.addEventListener('click', () => {
  const isOpen = navLinks.classList.toggle('nav-links--open');
  navToggle.setAttribute('aria-expanded', String(isOpen));
});

// Smooth scroll for anchor links & close mobile nav
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    const href = this.getAttribute('href');
    if (href === '#') return;
    e.preventDefault();
    const target = document.querySelector(href);
    if (target) {
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    navLinks.classList.remove('nav-links--open');
    navToggle.setAttribute('aria-expanded', 'false');
  });
});

// Scroll fade-in with IntersectionObserver
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.project-card, .project-card-compact, .skill-group, .timeline-item').forEach(el => {
  el.classList.add('fade-in');
  observer.observe(el);
});

// Active nav highlight on scroll
const sections = document.querySelectorAll('section[id]');
const navAnchors = document.querySelectorAll('.nav-links a');

window.addEventListener('scroll', () => {
  const scrollY = window.scrollY + 100;
  sections.forEach(section => {
    const top = section.offsetTop;
    const height = section.offsetHeight;
    const id = section.getAttribute('id');
    if (scrollY >= top && scrollY < top + height) {
      navAnchors.forEach(a => {
        a.classList.toggle('active', a.getAttribute('href') === '#' + id);
      });
    }
  });
});

// Placeholder link interception
document.querySelectorAll('[data-placeholder="true"]').forEach(link => {
  link.addEventListener('click', (e) => {
    e.preventDefault();
    const original = link.textContent;
    link.textContent = 'Coming soon';
    link.classList.add('btn--disabled');
    setTimeout(() => {
      link.textContent = original;
      link.classList.remove('btn--disabled');
    }, 2000);
  });
});
