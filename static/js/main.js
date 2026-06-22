/* ── main.js — Teja Labs Frontend Logic ──────────────────────────────────── */

/* ── Scroll Reveal ────────────────────────────────────────────────────────── */
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.remove('section-hidden');
      entry.target.classList.add('section-visible');
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.08 });

document.querySelectorAll('section').forEach(section => {
  section.classList.add('section-hidden');
  revealObserver.observe(section);
});


/* ── Navbar Shrink on Scroll ──────────────────────────────────────────────── */
const header = document.querySelector('header');
window.addEventListener('scroll', () => {
  if (window.scrollY > 60) {
    header.classList.remove('mt-6', 'w-[90%]');
    header.classList.add('mt-0', 'w-full', 'rounded-none', 'shadow-md');
  } else {
    header.classList.add('mt-6', 'w-[90%]');
    header.classList.remove('mt-0', 'w-full', 'rounded-none', 'shadow-md');
  }
}, { passive: true });


/* ── Mobile Menu Toggle ───────────────────────────────────────────────────── */
function toggleMobileMenu() {
  const menu = document.getElementById('mobile-menu');
  menu.classList.toggle('hidden');
  menu.classList.toggle('flex');
}


/* ── Counter Animation ────────────────────────────────────────────────────── */
function animateCounter(el) {
  const target = parseInt(el.dataset.target);
  const suffix = el.dataset.suffix || '+';
  let current = 0;
  const step = Math.max(1, Math.floor(target / 60));
  const timer = setInterval(() => {
    current = Math.min(current + step, target);
    el.textContent = current + (current === target ? suffix : '');
    if (current >= target) clearInterval(timer);
  }, 25);
}

const counterObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      animateCounter(entry.target);
      counterObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.5 });

document.querySelectorAll('.counter').forEach(el => counterObserver.observe(el));


/* ── Toast Notifications ──────────────────────────────────────────────────── */
let toastTimer;

function showToast(type, title, message) {
  const toast = document.getElementById('toast');
  const icon  = document.getElementById('toast-icon');
  const titleEl = document.getElementById('toast-title');
  const msgEl   = document.getElementById('toast-msg');

  titleEl.textContent = title;
  msgEl.textContent   = message;

  if (type === 'success') {
    icon.className = 'w-10 h-10 rounded-full flex items-center justify-center shrink-0 bg-green-100 text-green-600';
    icon.innerHTML = '<span class="material-symbols-outlined text-xl">check_circle</span>';
  } else {
    icon.className = 'w-10 h-10 rounded-full flex items-center justify-center shrink-0 bg-red-100 text-red-600';
    icon.innerHTML = '<span class="material-symbols-outlined text-xl">error</span>';
  }

  toast.classList.remove('hidden');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(hideToast, 6000);
}

function hideToast() {
  document.getElementById('toast').classList.add('hidden');
}


/* ── Contact Form Submission ──────────────────────────────────────────────── */
async function submitContactForm(event) {
  event.preventDefault();

  const form   = document.getElementById('contact-form-el');
  const btn    = document.getElementById('cf-submit');
  const text   = document.getElementById('cf-submit-text');
  const icon   = document.getElementById('cf-submit-icon');
  const spinner = document.getElementById('cf-spinner');

  // Basic client-side validation
  const name    = document.getElementById('cf-name').value.trim();
  const email   = document.getElementById('cf-email').value.trim();
  const message = document.getElementById('cf-message').value.trim();

  if (!name || name.length < 2) {
    showToast('error', 'Validation Error', 'Please enter your full name (at least 2 characters).');
    document.getElementById('cf-name').focus();
    return;
  }
  if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    showToast('error', 'Validation Error', 'Please enter a valid email address.');
    document.getElementById('cf-email').focus();
    return;
  }
  if (!message || message.length < 10) {
    showToast('error', 'Validation Error', 'Please describe your project (at least 10 characters).');
    document.getElementById('cf-message').focus();
    return;
  }

  // Set loading state
  btn.disabled = true;
  text.textContent = 'Sending…';
  icon.classList.add('hidden');
  spinner.classList.remove('hidden');
  btn.classList.add('opacity-75');

  const payload = {
    name,
    email,
    phone:   document.getElementById('cf-phone').value.trim() || null,
    service: document.getElementById('cf-service').value || null,
    budget:  document.getElementById('cf-budget').value || null,
    message,
  };

  try {
    const res = await fetch('/api/contact', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify(payload),
    });

    const data = await res.json();

    if (res.ok && data.success) {
      showToast('success', '🎉 Message Sent!', data.message);
      form.reset();
    } else {
      const detail = data.detail || data.message || 'Something went wrong. Please try again.';
      showToast('error', 'Submission Failed', typeof detail === 'string' ? detail : JSON.stringify(detail));
    }
  } catch (err) {
    showToast('error', 'Network Error', 'Could not reach the server. Please check your connection.');
    console.error('Contact form error:', err);
  } finally {
    btn.disabled = false;
    text.textContent = 'Send Message';
    icon.classList.remove('hidden');
    spinner.classList.add('hidden');
    btn.classList.remove('opacity-75');
  }
}


/* ── Active Nav Link on Scroll ────────────────────────────────────────────── */
const navLinks = document.querySelectorAll('nav a[href^="#"]');
const sectionIds = [...navLinks].map(a => a.getAttribute('href').slice(1)).filter(Boolean);

window.addEventListener('scroll', () => {
  let current = '';
  sectionIds.forEach(id => {
    const section = document.getElementById(id);
    if (section && window.scrollY >= section.offsetTop - 120) current = id;
  });
  navLinks.forEach(a => {
    a.classList.toggle('text-secondary', a.getAttribute('href') === `#${current}`);
    a.classList.toggle('text-primary', a.getAttribute('href') === `#${current}`);
  });
}, { passive: true });
