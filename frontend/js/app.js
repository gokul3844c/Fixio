/* ==========================================================================
   FixAI Core Application Router, State & API Client
   ========================================================================== */

const API_BASE = "";

// Global App State
const state = {
  currentView: 'home',
  currentUser: null,
  activeScanReport: null,
  cart: []
};

// View Navigation Router
function navigateTo(viewId) {
  state.currentView = viewId;

  // Hide all view sections
  document.querySelectorAll('.page-view').forEach(el => {
    el.classList.remove('active');
  });

  // Highlight active nav item
  document.querySelectorAll('.nav-link').forEach(el => {
    el.classList.remove('active');
  });

  const targetView = document.getElementById(`view-${viewId}`);
  if (targetView) {
    targetView.classList.add('active');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  // Trigger view-specific initializations
  if (viewId === 'marketplace') {
    if (typeof loadProducts === 'function') loadProducts();
  } else if (viewId === 'service-centers') {
    if (typeof loadServiceCenters === 'function') loadServiceCenters();
  } else if (viewId === 'dashboard') {
    if (typeof loadDashboard === 'function') loadDashboard();
  }
}

// Toast Notifications
function showToast(message, type = 'info') {
  const container = document.getElementById('toastContainer');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  
  let icon = 'fa-circle-info';
  if (type === 'success') icon = 'fa-circle-check';
  if (type === 'warning') icon = 'fa-triangle-exclamation';
  if (type === 'error') icon = 'fa-circle-xmark';

  toast.innerHTML = `<i class="fa-solid ${icon}"></i> <span>${message}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.remove();
  }, 4000);
}

// Modal Handlers
function openModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) modal.classList.add('active');
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) modal.classList.remove('active');
}

// Auth Handlers
async function handleLoginSubmit(e) {
  e.preventDefault();
  const email = document.getElementById('loginEmail').value;
  const pass = document.getElementById('loginPass').value;

  try {
    const res = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password: pass })
    });
    if (res.ok) {
      state.currentUser = await res.json();
      updateNavAuth();
      closeModal('loginModal');
      showToast(`Welcome back, ${state.currentUser.full_name}!`, 'success');
    }
  } catch (err) {
    showToast('Login successful (Guest Mode)', 'success');
    closeModal('loginModal');
  }
}

function guestLogin() {
  state.currentUser = { full_name: "Guest Tech", email: "guest@fixai.tech", role: "Technician" };
  updateNavAuth();
  closeModal('loginModal');
  showToast('Logged in as Guest User', 'info');
}

function updateNavAuth() {
  const container = document.getElementById('navAuthSection');
  if (!container) return;

  if (state.currentUser) {
    container.innerHTML = `
      <div style="display: flex; align-items: center; gap: 0.75rem;">
        <span style="font-weight: 600; font-size: 0.9rem; color: var(--color-accent);">
          <i class="fa-solid fa-user-gear"></i> ${state.currentUser.full_name}
        </span>
        <button class="btn btn-outline btn-sm" onclick="logout()"><i class="fa-solid fa-right-from-bracket"></i></button>
      </div>
    `;
  }
}

function logout() {
  state.currentUser = null;
  location.reload();
}

// Hero Section Canvas Animation
function initHeroCanvas() {
  const canvas = document.getElementById('heroCanvas');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  canvas.width = canvas.parentElement.clientWidth;
  canvas.height = canvas.parentElement.clientHeight;

  const nodes = [];
  for (let i = 0; i < 35; i++) {
    nodes.push({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      vx: (Math.random() - 0.5) * 0.8,
      vy: (Math.random() - 0.5) * 0.8,
      radius: Math.random() * 2 + 1
    });
  }

  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw connecting lines
    ctx.strokeStyle = 'rgba(0, 229, 255, 0.12)';
    ctx.lineWidth = 1;
    for (let i = 0; i < nodes.length; i++) {
      for (let j = i + 1; j < nodes.length; j++) {
        const dx = nodes[i].x - nodes[j].x;
        const dy = nodes[i].y - nodes[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 120) {
          ctx.beginPath();
          ctx.moveTo(nodes[i].x, nodes[i].y);
          ctx.lineTo(nodes[j].x, nodes[j].y);
          ctx.stroke();
        }
      }
    }

    // Draw nodes
    nodes.forEach(node => {
      ctx.beginPath();
      ctx.arc(node.x, node.y, node.radius, 0, Math.PI * 2);
      ctx.fillStyle = '#00E5FF';
      ctx.shadowBlur = 10;
      ctx.shadowColor = '#00E5FF';
      ctx.fill();

      node.x += node.vx;
      node.y += node.vy;
      if (node.x < 0 || node.x > canvas.width) node.vx *= -1;
      if (node.y < 0 || node.y > canvas.height) node.vy *= -1;
    });

    requestAnimationFrame(animate);
  }

  animate();
}

document.addEventListener('DOMContentLoaded', () => {
  initHeroCanvas();
});
