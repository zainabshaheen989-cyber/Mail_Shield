/* ═══════════════════════════════════════════════════════
   SpamShield – main.js
   Handles: animated canvas bg, hamburger menu, FAQ accordion,
            char counter, toast notifications, history panel.
   ═══════════════════════════════════════════════════════ */

/* ── Animated particle canvas ───────────────────────────── */
(function initCanvas() {
  const canvas = document.getElementById('bgCanvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  let particles = [];

  function resize() {
    canvas.width  = window.innerWidth;
    canvas.height = window.innerHeight;
  }
  resize();
  window.addEventListener('resize', resize);

  for (let i = 0; i < 60; i++) {
    particles.push({
      x:  Math.random() * window.innerWidth,
      y:  Math.random() * window.innerHeight,
      vx: (Math.random() - 0.5) * 0.3,
      vy: (Math.random() - 0.5) * 0.3,
      r:  Math.random() * 1.5 + 0.3,
      a:  Math.random() * 0.5 + 0.1,
    });
  }

  function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    particles.forEach(p => {
      p.x += p.vx; p.y += p.vy;
      if (p.x < 0) p.x = canvas.width;
      if (p.x > canvas.width)  p.x = 0;
      if (p.y < 0) p.y = canvas.height;
      if (p.y > canvas.height) p.y = 0;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(0,229,255,${p.a})`;
      ctx.fill();
    });

    // Draw connecting lines
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const d = Math.hypot(particles[i].x - particles[j].x, particles[i].y - particles[j].y);
        if (d < 120) {
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.strokeStyle = `rgba(0,100,200,${0.12 * (1 - d / 120)})`;
          ctx.lineWidth = 0.5;
          ctx.stroke();
        }
      }
    }
    requestAnimationFrame(draw);
  }
  draw();
})();


/* ── Hamburger menu ─────────────────────────────────────── */
const hamburger  = document.getElementById('hamburger');
const mobileMenu = document.getElementById('mobileMenu');

function toggleMenu() {
  hamburger.classList.toggle('open');
  mobileMenu.classList.toggle('open');
}

if (hamburger) hamburger.addEventListener('click', toggleMenu);


/* ── Close mobile menu on link click ───────────────────── */
document.querySelectorAll('.mobile-menu a, .mobile-menu button').forEach(el => {
  el.addEventListener('click', () => {
    hamburger.classList.remove('open');
    mobileMenu.classList.remove('open');
  });
});


/* ── Char counter ───────────────────────────────────────── */
const emailInput = document.getElementById('emailInput');
const charCount  = document.getElementById('charCount');
if (emailInput && charCount) {
  emailInput.addEventListener('input', () => {
    charCount.textContent = emailInput.value.length + ' chars';
  });
}


/* ── FAQ accordion ──────────────────────────────────────── */
document.querySelectorAll('.faq-q').forEach(btn => {
  btn.addEventListener('click', () => {
    const answer = btn.nextElementSibling;
    const arrow  = btn.querySelector('.arrow');
    const isOpen = answer.classList.contains('open');

    // Close all
    document.querySelectorAll('.faq-a').forEach(a => a.classList.remove('open'));
    document.querySelectorAll('.arrow').forEach(a => a.classList.remove('open'));

    if (!isOpen) {
      answer.classList.add('open');
      if (arrow) arrow.classList.add('open');
    }
  });
});


/* ── Toast notification ─────────────────────────────────── */
function showToast(msg, type = '') {
  const toast = document.getElementById('toast');
  if (!toast) return;
  toast.textContent = msg;
  toast.className   = 'toast show' + (type ? ' toast-' + type : '');
  setTimeout(() => toast.classList.remove('show'), 3200);
}
window.showToast = showToast;


/* ── Analysis history (session only) ───────────────────── */
let analysisHistory = [];

function addToHistory(preview, type, label) {
  analysisHistory.unshift({ preview, type, label, time: new Date().toLocaleTimeString() });
  if (analysisHistory.length > 8) analysisHistory.pop();
  renderHistory();
}

function renderHistory() {
  const section = document.getElementById('historySection');
  const list    = document.getElementById('historyList');
  if (!section || !list) return;

  if (!analysisHistory.length) { section.style.display = 'none'; return; }
  section.style.display = 'block';

  list.innerHTML = analysisHistory.map(h => `
    <div class="history-item" title="Click to reload">
      <div class="hi-dot ${h.type}"></div>
      <span class="hi-text">${h.preview}</span>
      <span class="hi-label">${h.label}</span>
    </div>`).join('');
}

window.addToHistory = addToHistory;


/* ── Animate score bars on page load (results page) ─────── */
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.sc-fill[data-width]').forEach(bar => {
    setTimeout(() => {
      bar.style.width = bar.dataset.width;
    }, 100);
  });
});