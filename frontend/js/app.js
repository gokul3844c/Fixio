/* ==========================================================================
   NeoShop — app.js
   Core: Navigation, Auth, Modals, Cart, Toast, Hero Canvas, Countdown
   ========================================================================== */

'use strict';

// ============================================================
// STATE
// ============================================================
const AppState = {
  currentView: 'home',
  cart: JSON.parse(localStorage.getItem('fixio_cart') || '[]'),
  user: JSON.parse(localStorage.getItem('fixio_user') || 'null'),
  wishlist: JSON.parse(localStorage.getItem('fixio_wishlist') || '[]'),
  cartDrawerOpen: false,
  navSearchOpen: false,
  mobileMenuOpen: false,
};

// ============================================================
// PAGE LOADER
// ============================================================
window.addEventListener('load', () => {
  setTimeout(() => {
    const loader = document.getElementById('pageLoader');
    if (loader) { loader.classList.add('done'); }
  }, 1800);

  initApp();
});

function initApp() {
  restoreAuthState();
  initGoogleSignIn();
  updateCartUI();
  startCountdownTimer();
  drawHeroCanvas();
  initCategoriesGrid();
  initFeaturedProducts();
  initDashboard();

  // Set today as min date for appointment booking
  const apptDate = document.getElementById('appointDate');
  if (apptDate) apptDate.min = new Date().toISOString().split('T')[0];

  // Keyboard shortcuts
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') { closeAllModals(); closeCartDrawer(); }
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') { e.preventDefault(); toggleNavSearch(); }
  });
}

// ============================================================
// NAVIGATION
// ============================================================
function navigateTo(view) {
  if ((view === 'dashboard' || view === 'scan') && !AppState.user) {
    showToast('<i class="fa-solid fa-lock"></i> Please log in or register to access this feature.', 'warning');
    openModal('loginModal');
    return;
  }

  // Hide all views
  document.querySelectorAll('.page-view').forEach(el => el.classList.remove('active'));

  // Show target
  const target = document.getElementById(`view-${view}`);
  if (target) {
    target.classList.add('active');
    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  // Update nav links
  document.querySelectorAll('.nav-link').forEach(el => {
    el.classList.remove('active');
    if (el.id === `nav-${view}`) el.classList.add('active');
  });

  AppState.currentView = view;
  closeMobileMenu();

  // View-specific init
  if (view === 'shop' || view === 'marketplace') {
    if (typeof initShop === 'function') initShop();
  }
  if (view === 'service-centers') {
    if (typeof initMap === 'function') initMap();
    if (typeof filterStores === 'function') filterStores();
  }
  if (view === 'dashboard') {
    if (typeof renderDashboard === 'function') renderDashboard();
  }
  if (view === 'home') {
    drawHeroCanvas();
  }

  // Close cart drawer on navigation
  closeCartDrawer();

  // Scroll to top after short delay
  setTimeout(() => window.scrollTo({ top: 0, behavior: 'smooth' }), 50);
}

// ============================================================
// MOBILE MENU
// ============================================================
function toggleMobileMenu() {
  AppState.mobileMenuOpen = !AppState.mobileMenuOpen;
  const links = document.getElementById('navLinks');
  const toggle = document.getElementById('navToggle');
  if (links) links.classList.toggle('open', AppState.mobileMenuOpen);
  if (toggle) {
    toggle.setAttribute('aria-expanded', AppState.mobileMenuOpen);
    toggle.classList.toggle('open', AppState.mobileMenuOpen);
  }
}

function closeMobileMenu() {
  AppState.mobileMenuOpen = false;
  const links = document.getElementById('navLinks');
  const toggle = document.getElementById('navToggle');
  if (links) links.classList.remove('open');
  if (toggle) { toggle.setAttribute('aria-expanded', 'false'); toggle.classList.remove('open'); }
}

// ============================================================
// NAV SEARCH
// ============================================================
function toggleNavSearch() {
  AppState.navSearchOpen = !AppState.navSearchOpen;
  const bar = document.getElementById('navSearchBar');
  if (bar) {
    bar.style.display = AppState.navSearchOpen ? 'block' : 'none';
    if (AppState.navSearchOpen) {
      setTimeout(() => document.getElementById('globalSearchInput')?.focus(), 80);
    }
  }
}

function handleGlobalSearch(val) {
  if (!val.trim()) return;
  if (val.trim().length > 1) {
    navigateTo('shop');
    setTimeout(() => {
      const el = document.getElementById('marketSearchInput');
      if (el) { el.value = val; if (typeof filterMarketplace === 'function') filterMarketplace(); }
    }, 200);
  }
}

function handleSearchKey(e) {
  if (e.key === 'Escape') { toggleNavSearch(); }
  if (e.key === 'Enter') { handleGlobalSearch(e.target.value); toggleNavSearch(); }
}

// ============================================================
// MODAL SYSTEM
// ============================================================
function openModal(id) {
  const modal = document.getElementById(id);
  if (modal) { modal.classList.add('open'); document.body.style.overflow = 'hidden'; }
}

function closeModal(id) {
  const modal = document.getElementById(id);
  if (modal) modal.classList.remove('open');
  // Re-enable scroll only if no other modals are open
  if (!document.querySelector('.modal-backdrop.open')) document.body.style.overflow = '';
}

function closeAllModals() {
  document.querySelectorAll('.modal-backdrop').forEach(m => m.classList.remove('open'));
  document.body.style.overflow = '';
}

// ============================================================
// CART SYSTEM
// ============================================================
function addToCart(product) {
  const existing = AppState.cart.find(i => i.id === product.id);
  if (existing) {
    existing.qty = Math.min(existing.qty + 1, 99);
  } else {
    AppState.cart.push({ ...product, qty: 1 });
  }
  saveCart();
  updateCartUI();
  showToast(`<i class="fa-solid fa-cart-plus"></i> <strong>${product.name}</strong> added to cart!`, 'success');
  animateCartBadge();
}

function removeFromCart(productId) {
  AppState.cart = AppState.cart.filter(i => i.id !== productId);
  saveCart();
  updateCartUI();
  renderCartDrawer();
}

function updateCartQty(productId, delta) {
  const item = AppState.cart.find(i => i.id === productId);
  if (!item) return;
  item.qty = Math.max(1, Math.min(99, item.qty + delta));
  saveCart();
  updateCartUI();
  renderCartDrawer();
}

function saveCart() {
  localStorage.setItem('neoshop_cart', JSON.stringify(AppState.cart));
}

function getCartTotal() {
  return AppState.cart.reduce((sum, i) => sum + i.price * i.qty, 0);
}

function getCartItemCount() {
  return AppState.cart.reduce((sum, i) => sum + i.qty, 0);
}

function updateCartUI() {
  const count = getCartItemCount();
  const total = getCartTotal();

  // Navbar badge
  const badge = document.getElementById('cartBadge');
  if (badge) {
    badge.textContent = count;
    badge.style.display = count > 0 ? 'flex' : 'none';
  }

  // Shop page cart count
  const countEl = document.getElementById('cartCount');
  if (countEl) countEl.textContent = count;

  // Cart total in drawer
  const totalEl = document.getElementById('cartTotalPrice');
  if (totalEl) totalEl.textContent = `$${total.toFixed(2)}`;

  const totalItemsEl = document.getElementById('cartTotalItems');
  if (totalItemsEl) totalItemsEl.textContent = count;

  const itemCountLabel = document.getElementById('cartItemCountLabel');
  if (itemCountLabel) itemCountLabel.textContent = count > 0 ? `(${count})` : '';

  // Checkout button state
  const checkoutBtn = document.getElementById('checkoutBtn');
  if (checkoutBtn) checkoutBtn.disabled = count === 0;

  // Checkout modal totals
  const checkSub = document.getElementById('checkSubtotal');
  const checkTot = document.getElementById('checkTotal');
  if (checkSub) checkSub.textContent = `$${total.toFixed(2)}`;
  if (checkTot) checkTot.textContent = `$${total.toFixed(2)}`;
}

function animateCartBadge() {
  const badge = document.getElementById('cartBadge');
  if (!badge) return;
  badge.style.transform = 'scale(1.5)';
  setTimeout(() => badge.style.transform = '', 300);
}

// ============================================================
// CART DRAWER
// ============================================================
function toggleCartDrawer() {
  AppState.cartDrawerOpen = !AppState.cartDrawerOpen;
  const drawer = document.getElementById('cartDrawer');
  const overlay = document.getElementById('cartOverlay');
  if (drawer) drawer.classList.toggle('open', AppState.cartDrawerOpen);
  if (overlay) overlay.classList.toggle('open', AppState.cartDrawerOpen);
  document.body.style.overflow = AppState.cartDrawerOpen ? 'hidden' : '';
  if (AppState.cartDrawerOpen) renderCartDrawer();
}

function closeCartDrawer() {
  AppState.cartDrawerOpen = false;
  const drawer = document.getElementById('cartDrawer');
  const overlay = document.getElementById('cartOverlay');
  if (drawer) drawer.classList.remove('open');
  if (overlay) overlay.classList.remove('open');
  if (!document.querySelector('.modal-backdrop.open')) document.body.style.overflow = '';
}

function renderCartDrawer() {
  const listEl = document.getElementById('cartItemsList');
  const emptyEl = document.getElementById('cartEmptyMsg');
  if (!listEl) return;

  if (AppState.cart.length === 0) {
    listEl.innerHTML = '';
    if (emptyEl) emptyEl.style.display = 'block';
    return;
  }

  if (emptyEl) emptyEl.style.display = 'none';

  listEl.innerHTML = AppState.cart.map(item => `
    <div class="cart-item" id="cart-item-${item.id}">
      <div class="cart-item-img" style="background:var(--neo-bg-deep);">
        ${item.image_url
          ? `<img src="${item.image_url}" alt="${item.name}" style="width:44px; height:44px; object-fit:contain;" />`
          : `<i class="fa-solid fa-microchip" style="font-size:1.4rem; color:var(--color-primary);"></i>`
        }
      </div>
      <div class="cart-item-details">
        <div class="cart-item-name" title="${item.name}">${item.name}</div>
        <div class="cart-item-price">$${(item.price * item.qty).toFixed(2)}</div>
      </div>
      <div class="cart-qty-control">
        <button class="cart-qty-btn" onclick="updateCartQty(${item.id}, -1)" aria-label="Decrease quantity">−</button>
        <span class="cart-qty-val">${item.qty}</span>
        <button class="cart-qty-btn" onclick="updateCartQty(${item.id}, 1)" aria-label="Increase quantity">+</button>
      </div>
      <button class="cart-item-remove" onclick="removeFromCart(${item.id})" aria-label="Remove ${item.name} from cart">
        <i class="fa-solid fa-xmark"></i>
      </button>
    </div>
  `).join('');
}

// ============================================================
// WISHLIST
// ============================================================
function toggleWishlist(productId, btn) {
  const idx = AppState.wishlist.indexOf(productId);
  if (idx === -1) {
    AppState.wishlist.push(productId);
    if (btn) { btn.classList.add('active'); btn.innerHTML = '<i class="fa-solid fa-heart"></i>'; }
    showToast('<i class="fa-solid fa-heart" style="color:#EF4444;"></i> Added to wishlist', 'info');
  } else {
    AppState.wishlist.splice(idx, 1);
    if (btn) { btn.classList.remove('active'); btn.innerHTML = '<i class="fa-regular fa-heart"></i>'; }
  }
  localStorage.setItem('neoshop_wishlist', JSON.stringify(AppState.wishlist));
}

// ============================================================
// TOAST NOTIFICATION
// ============================================================
function showToast(message, type = 'info', duration = 3500) {
  const container = document.getElementById('toastContainer');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `
    <span style="flex:1;">${message}</span>
    <button onclick="this.parentElement.remove()" style="background:none; border:none; cursor:pointer; color:var(--color-text-faint); font-size:1rem; padding:0; margin-left:0.5rem;">&times;</button>
  `;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(20px)';
    toast.style.transition = 'opacity 0.3s, transform 0.3s';
    setTimeout(() => toast.remove(), 320);
  }, duration);
}

// ============================================================
// AUTH
// ============================================================
function getAuthHeader() {
  const token = (AppState.user && AppState.user.token) || localStorage.getItem('fixio_token');
  if (token) {
    return { 'Authorization': `Bearer ${token}` };
  }
  return {};
}

async function restoreAuthState() {
  const stored = localStorage.getItem('fixio_user');
  if (stored) {
    try {
      AppState.user = JSON.parse(stored);
      if (AppState.user && AppState.user.token) {
        const res = await fetch('/api/auth/me', {
          headers: getAuthHeader()
        });
        if (res.ok) {
          const uData = await res.json();
          AppState.user.name = uData.full_name || AppState.user.name;
          AppState.user.email = uData.email || AppState.user.email;
          localStorage.setItem('fixio_user', JSON.stringify(AppState.user));
          localStorage.setItem('fixio_token', AppState.user.token);
        } else if (res.status === 401) {
          AppState.user = null;
          localStorage.removeItem('fixio_user');
          localStorage.removeItem('fixio_token');
          showToast('<i class="fa-solid fa-clock"></i> Session expired. Please log in again.', 'warning');
        }
      }
    } catch (e) {
      console.warn('Auth restoration issue:', e);
    }
  }
  updateAuthUI(AppState.user);
}

function updateAuthUI(user) {
  const loginBtn   = document.getElementById('navLoginBtn');
  const registerBtn= document.getElementById('navRegisterBtn');
  const avatar     = document.getElementById('navUserAvatar');
  const initials   = document.getElementById('navAvatarInitials');

  if (user) {
    if (loginBtn)    loginBtn.style.display   = 'none';
    if (registerBtn) registerBtn.style.display = 'none';
    if (avatar)      avatar.style.display      = 'flex';
    if (initials)    initials.textContent       = user.name ? user.name[0].toUpperCase() : 'U';
  } else {
    if (loginBtn)    loginBtn.style.display   = '';
    if (registerBtn) registerBtn.style.display = '';
    if (avatar)      avatar.style.display      = 'none';
  }
}

async function handleLoginSubmit(event) {
  event.preventDefault();
  const emailInput = document.getElementById('loginEmail');
  const passInput  = document.getElementById('loginPass');
  const email = emailInput ? emailInput.value.trim() : '';
  const pass  = passInput  ? passInput.value.trim()  : '';

  if (!email || !pass) {
    showToast('<i class="fa-solid fa-triangle-exclamation"></i> Please enter both email and password.', 'warning');
    return;
  }

  showToast('<i class="fa-solid fa-spinner fa-spin"></i> Authenticating…', 'info', 2000);

  try {
    const res = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password: pass })
    });

    const data = await res.json();

    if (res.ok && data.access_token) {
      AppState.user = {
        id: data.user.id,
        name: data.user.full_name || email,
        email: data.user.email,
        token: data.access_token
      };
      localStorage.setItem('fixio_user', JSON.stringify(AppState.user));
      localStorage.setItem('fixio_token', data.access_token);
      updateAuthUI(AppState.user);
      closeModal('loginModal');
      showToast(`<i class="fa-solid fa-circle-check"></i> Welcome back, <strong>${AppState.user.name}</strong>!`, 'success');
      if (typeof renderDashboard === 'function') renderDashboard();
    } else {
      const errMsg = data.detail || 'Invalid email or password';
      showToast(`<i class="fa-solid fa-circle-xmark"></i> ${errMsg}`, 'danger');
    }
  } catch (err) {
    showToast('<i class="fa-solid fa-wifi"></i> Connection error. Please check server status.', 'danger');
  }
}

async function handleRegisterSubmit(event) {
  event.preventDefault();
  const name  = document.getElementById('regName').value.trim();
  const email = document.getElementById('regEmail').value.trim();
  const pass  = document.getElementById('regPass').value.trim();

  if (!name || !email || !pass) {
    showToast('<i class="fa-solid fa-triangle-exclamation"></i> All fields are required for registration.', 'warning');
    return;
  }

  showToast('<i class="fa-solid fa-spinner fa-spin"></i> Creating account…', 'info', 2000);

  try {
    const res = await fetch('/api/auth/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ full_name: name, email, password: pass })
    });

    const data = await res.json();

    if (res.ok && data.access_token) {
      AppState.user = {
        id: data.user.id,
        name: data.user.full_name || name,
        email: data.user.email,
        token: data.access_token
      };
      localStorage.setItem('fixio_user', JSON.stringify(AppState.user));
      localStorage.setItem('fixio_token', data.access_token);
      updateAuthUI(AppState.user);
      closeModal('registerModal');
      showToast(`<i class="fa-solid fa-party-horn"></i> Account registered! Welcome, <strong>${name}</strong>!`, 'success');
      if (typeof renderDashboard === 'function') renderDashboard();
    } else {
      const errMsg = data.detail || 'Registration failed.';
      showToast(`<i class="fa-solid fa-circle-xmark"></i> ${errMsg}`, 'danger');
    }
  } catch (err) {
    showToast('<i class="fa-solid fa-wifi"></i> Registration server error.', 'danger');
  }
}

function guestLogin() {
  showToast('<i class="fa-solid fa-info-circle"></i> Guest access is read-only. Please create an account to save scan reports.', 'info');
  closeModal('loginModal');
}

function handleLogout() {
  AppState.user = null;
  localStorage.removeItem('fixio_user');
  localStorage.removeItem('fixio_token');
  if (window.google && window.google.accounts && window.google.accounts.id) {
    try { window.google.accounts.id.disableAutoSelect(); } catch(e){}
  }
  updateAuthUI(null);
  navigateTo('home');
  showToast('<i class="fa-solid fa-sign-out-alt"></i> Logged out successfully', 'info');
}

// ============================================================
// GOOGLE SIGN IN API INTEGRATION
// ============================================================
async function handleGoogleCallback(response) {
  if (!response || !response.credential) {
    showToast('<i class="fa-solid fa-circle-xmark"></i> Google authorization was cancelled or failed.', 'danger');
    return;
  }

  showToast('<i class="fa-solid fa-spinner fa-spin"></i> Authenticating with Google…', 'info', 3000);

  try {
    const res = await fetch('/api/auth/google', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ token: response.credential })
    });

    const data = await res.json();

    if (res.ok && data.access_token) {
      AppState.user = {
        id: data.user.id,
        name: data.user.full_name || data.user.email,
        email: data.user.email,
        token: data.access_token
      };
      localStorage.setItem('neoshop_user', JSON.stringify(AppState.user));
      updateAuthUI(AppState.user);
      closeModal('loginModal');
      closeModal('registerModal');
      showToast(`<i class="fa-solid fa-circle-check"></i> Signed in via Google as <strong>${AppState.user.name}</strong>!`, 'success');
      if (typeof renderDashboard === 'function') renderDashboard();
    } else {
      const errMsg = data.detail || 'Google Login failed.';
      showToast(`<i class="fa-solid fa-circle-xmark"></i> ${errMsg}`, 'danger');
    }
  } catch (err) {
    console.error('Google Auth Error:', err);
    showToast('<i class="fa-solid fa-wifi"></i> Google Login server communication error.', 'danger');
  }
}

function triggerGoogleSignIn() {
  if (window.google && window.google.accounts && window.google.accounts.id) {
    window.google.accounts.id.prompt((notification) => {
      if (notification.isNotDisplayed()) {
        showToast('<i class="fa-solid fa-info-circle"></i> Opening Google Sign-In prompt...', 'info');
      }
    });
  } else {
    // Demo / standard fallback when offline or GIS script blocked
    const demoEmail = 'user.google@example.com';
    showToast('<i class="fa-solid fa-spinner fa-spin"></i> Simulating Google OAuth Sign-In…', 'info', 2000);
    fetch('/api/auth/google', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ token: `mock_google_id_token_${Date.now()}` })
    })
    .then(r => r.json())
    .then(data => {
      if (data.access_token) {
        AppState.user = {
          id: data.user.id,
          name: data.user.full_name || 'Google User',
          email: data.user.email,
          token: data.access_token
        };
        localStorage.setItem('neoshop_user', JSON.stringify(AppState.user));
        updateAuthUI(AppState.user);
        closeModal('loginModal');
        closeModal('registerModal');
        showToast(`<i class="fa-solid fa-circle-check"></i> Google Sign-In successful! Welcome <strong>${AppState.user.name}</strong>`, 'success');
        if (typeof renderDashboard === 'function') renderDashboard();
      }
    })
    .catch(() => {
      showToast('<i class="fa-solid fa-circle-xmark"></i> Google auth endpoint failed.', 'danger');
    });
  }
}

function initGoogleSignIn() {
  if (window.google && window.google.accounts && window.google.accounts.id) {
    try {
      window.google.accounts.id.initialize({
        client_id: "109876543210-exampleclientid.apps.googleusercontent.com",
        callback: handleGoogleCallback,
        auto_select: false,
        cancel_on_tap_outside: true
      });
    } catch (err) {
      console.warn("GSI init warning:", err);
    }
  }
}

window.getAuthHeader = getAuthHeader;
window.handleGoogleCallback = handleGoogleCallback;
window.triggerGoogleSignIn = triggerGoogleSignIn;

// ============================================================
// CHECKOUT
// ============================================================
function handleCheckoutSubmit(event) {
  event.preventDefault();
  const name = document.getElementById('checkFirstName').value + ' ' + document.getElementById('checkLastName').value;

  closeModal('checkoutModal');
  closeCartDrawer();

  // Simulate order placement
  setTimeout(() => {
    showToast(`<i class="fa-solid fa-circle-check"></i> Order placed successfully! Thank you, <strong>${name}</strong>. Expect delivery in 2–3 days.`, 'success', 6000);
    AppState.cart = [];
    saveCart();
    updateCartUI();
    renderCartDrawer();
  }, 500);
}

// ============================================================
// COUNTDOWN TIMER
// ============================================================
function startCountdownTimer() {
  let totalSeconds = 23 * 3600 + 47 * 60 + 12;

  function tick() {
    const h = String(Math.floor(totalSeconds / 3600)).padStart(2, '0');
    const m = String(Math.floor((totalSeconds % 3600) / 60)).padStart(2, '0');
    const s = String(totalSeconds % 60).padStart(2, '0');
    const el = document.getElementById('countdownTimer');
    if (el) el.textContent = `${h}:${m}:${s}`;
    if (totalSeconds > 0) {
      totalSeconds--;
      setTimeout(tick, 1000);
    } else {
      if (el) el.textContent = 'SALE ENDED';
    }
  }
  tick();
}

// ============================================================
// HERO CANVAS — Animated Circuit Board Drawing
// ============================================================
function drawHeroCanvas() {
  const canvas = document.getElementById('heroCanvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  function resize() {
    const rect = canvas.parentElement.getBoundingClientRect();
    canvas.width  = rect.width  || 400;
    canvas.height = rect.height || 300;
  }

  resize();
  window.addEventListener('resize', () => { resize(); drawFrame(0); });

  const W = () => canvas.width;
  const H = () => canvas.height;

  // Color palette — light neomorphic pastels
  const colors = {
    bg:      '#EEF2F7',
    track:   'rgba(79, 70, 229, 0.18)',
    trackHi: 'rgba(79, 70, 229, 0.55)',
    node:    '#4F46E5',
    nodeGlow:'rgba(79, 70, 229, 0.35)',
    chip:    'rgba(79, 70, 229, 0.08)',
    chipBorder: 'rgba(79, 70, 229, 0.28)',
    pulse:   '#7C74FF',
    label:   'rgba(79, 70, 229, 0.6)',
  };

  // Generate stable circuit nodes
  const nodes = [];
  const seed = 42;
  function seededRand(i) { return ((Math.sin(seed + i) * 9301 + 49297) % 233280) / 233280; }

  for (let i = 0; i < 18; i++) {
    nodes.push({
      x: 0.06 + seededRand(i * 3)     * 0.88,
      y: 0.06 + seededRand(i * 3 + 1) * 0.88,
      r: 3.5 + seededRand(i * 3 + 2) * 4,
      pulse: seededRand(i) * Math.PI * 2,
      speed: 0.02 + seededRand(i * 2) * 0.04,
    });
  }

  // Build edges (connect nearby nodes)
  const edges = [];
  for (let i = 0; i < nodes.length; i++) {
    for (let j = i + 1; j < nodes.length; j++) {
      const dx = nodes[i].x - nodes[j].x;
      const dy = nodes[i].y - nodes[j].y;
      const dist = Math.sqrt(dx * dx + dy * dy);
      if (dist < 0.32 && edges.length < 28) {
        edges.push({ a: i, b: j, progress: 0, speed: 0.004 + seededRand(i + j) * 0.008 });
      }
    }
  }

  // IC Chips
  const chips = [
    { x: 0.35, y: 0.28, w: 0.22, h: 0.18, label: 'MCU' },
    { x: 0.12, y: 0.55, w: 0.18, h: 0.14, label: 'PWR' },
    { x: 0.65, y: 0.55, w: 0.20, h: 0.15, label: 'RF' },
  ];

  // Animated pulses along edges
  const pulses = edges.map(e => ({
    edge: e,
    t: seededRand(edges.indexOf(e)),
    speed: 0.006 + seededRand(edges.indexOf(e)) * 0.01,
  }));

  let frame = 0;

  function drawFrame(ts) {
    frame++;
    const w = W(), h = H();
    ctx.clearRect(0, 0, w, h);

    // Background
    ctx.fillStyle = colors.bg;
    ctx.fillRect(0, 0, w, h);

    // Draw IC chips
    chips.forEach(chip => {
      const cx = chip.x * w, cy = chip.y * h;
      const cw = chip.w * w, ch = chip.h * h;

      ctx.beginPath();
      ctx.roundRect(cx, cy, cw, ch, 6);
      ctx.fillStyle = colors.chip;
      ctx.fill();
      ctx.strokeStyle = colors.chipBorder;
      ctx.lineWidth = 1.5;
      ctx.stroke();

      // IC legs
      const legCount = 6;
      const legSpacing = cw / (legCount + 1);
      for (let i = 1; i <= legCount; i++) {
        ctx.beginPath();
        ctx.moveTo(cx + legSpacing * i, cy);
        ctx.lineTo(cx + legSpacing * i, cy - 8);
        ctx.strokeStyle = colors.chipBorder;
        ctx.lineWidth = 1.5;
        ctx.stroke();

        ctx.beginPath();
        ctx.moveTo(cx + legSpacing * i, cy + ch);
        ctx.lineTo(cx + legSpacing * i, cy + ch + 8);
        ctx.stroke();
      }

      // Label
      ctx.font = `bold ${Math.max(9, cw * 0.2)}px Outfit, sans-serif`;
      ctx.fillStyle = colors.label;
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(chip.label, cx + cw / 2, cy + ch / 2);
    });

    // Draw edges (tracks)
    edges.forEach(edge => {
      const na = nodes[edge.a], nb = nodes[edge.b];
      const ax = na.x * w, ay = na.y * h;
      const bx = nb.x * w, by = nb.y * h;

      // Manhattan routing (L-shape)
      ctx.beginPath();
      ctx.moveTo(ax, ay);
      ctx.lineTo(bx, ay);
      ctx.lineTo(bx, by);
      ctx.strokeStyle = colors.track;
      ctx.lineWidth = 1.5;
      ctx.stroke();
    });

    // Draw pulsing glows along tracks
    pulses.forEach(p => {
      p.t += p.speed;
      if (p.t > 1) p.t = 0;
      const na = nodes[p.edge.a], nb = nodes[p.edge.b];
      const ax = na.x * w, ay = na.y * h;
      const bx = nb.x * w, by = nb.y * h;

      // Pulse goes along L-shape
      const totalLen = Math.abs(bx - ax) + Math.abs(by - ay);
      const seg1 = Math.abs(bx - ax) / totalLen;
      let px, py;
      if (p.t < seg1) {
        px = ax + (p.t / seg1) * (bx - ax);
        py = ay;
      } else {
        px = bx;
        py = ay + ((p.t - seg1) / (1 - seg1)) * (by - ay);
      }

      const grad = ctx.createRadialGradient(px, py, 0, px, py, 10);
      grad.addColorStop(0, colors.pulse);
      grad.addColorStop(1, 'rgba(124,116,255,0)');
      ctx.beginPath();
      ctx.arc(px, py, 10, 0, Math.PI * 2);
      ctx.fillStyle = grad;
      ctx.fill();
    });

    // Draw nodes
    nodes.forEach((node, i) => {
      node.pulse += node.speed;
      const glowSize = node.r * (1.5 + 0.4 * Math.sin(node.pulse));
      const nx = node.x * w, ny = node.y * h;

      // Glow
      const grad = ctx.createRadialGradient(nx, ny, 0, nx, ny, glowSize * 2.5);
      grad.addColorStop(0, colors.nodeGlow);
      grad.addColorStop(1, 'rgba(79,70,229,0)');
      ctx.beginPath();
      ctx.arc(nx, ny, glowSize * 2.5, 0, Math.PI * 2);
      ctx.fillStyle = grad;
      ctx.fill();

      // Core dot
      ctx.beginPath();
      ctx.arc(nx, ny, node.r * 0.7, 0, Math.PI * 2);
      ctx.fillStyle = colors.node;
      ctx.fill();

      // Inner highlight
      ctx.beginPath();
      ctx.arc(nx - node.r * 0.2, ny - node.r * 0.2, node.r * 0.25, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(255,255,255,0.6)';
      ctx.fill();
    });

    // Subtle grid lines
    ctx.globalAlpha = 0.04;
    ctx.strokeStyle = '#4F46E5';
    ctx.lineWidth = 0.5;
    const gridStep = 28;
    for (let x = 0; x < w; x += gridStep) {
      ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, h); ctx.stroke();
    }
    for (let y = 0; y < h; y += gridStep) {
      ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(w, y); ctx.stroke();
    }
    ctx.globalAlpha = 1;

    requestAnimationFrame(drawFrame);
  }

  requestAnimationFrame(drawFrame);
}

// ============================================================
// CATEGORIES GRID (Home page)
// ============================================================
const CATEGORIES = [
  { icon: 'fa-microchip',        label: 'ICs & MCUs',      count: '3,200+', color: '#4F46E5', filter: 'IC' },
  { icon: 'fa-plug-circle-bolt', label: 'Capacitors',       count: '1,850+', color: '#7C74FF', filter: 'Capacitor' },
  { icon: 'fa-wave-square',      label: 'Resistors',        count: '2,100+', color: '#10B981', filter: 'Resistor' },
  { icon: 'fa-bolt',             label: 'MOSFETs',          count: '980+',   color: '#F59E0B', filter: 'MOSFET' },
  { icon: 'fa-code-fork',        label: 'Diodes',           count: '740+',   color: '#EF4444', filter: 'Diode' },
  { icon: 'fa-screwdriver-wrench',label: 'Repair Tools',    count: '560+',   color: '#3B82F6', filter: 'Tool' },
];

function initCategoriesGrid() {
  const grid = document.getElementById('categoriesGrid');
  if (!grid) return;

  grid.innerHTML = CATEGORIES.map(cat => `
    <div class="feature-card" onclick="navigateTo('shop'); setTimeout(() => filterByCategory('${cat.filter}'), 250);"
         style="cursor:pointer;" tabindex="0" role="button" aria-label="Browse ${cat.label}">
      <div class="feature-icon" style="color:${cat.color};">
        <i class="fa-solid ${cat.icon}"></i>
      </div>
      <h3>${cat.label}</h3>
      <p style="font-size:0.82rem; color:var(--color-text-faint); margin-top:0.25rem;">${cat.count} products</p>
    </div>
  `).join('');
}

function filterByCategory(cat) {
  const sel = document.getElementById('marketCategorySelect');
  if (sel) { sel.value = cat; }
  if (typeof filterMarketplace === 'function') filterMarketplace();
}

// ============================================================
// FEATURED PRODUCTS (Home page — first 8 products)
// ============================================================
function initFeaturedProducts() {
  const grid = document.getElementById('featuredProductsGrid');
  if (!grid) return;

  // Wait for shop products to be available
  const tryRender = (attempts = 0) => {
    if (typeof ALL_PRODUCTS !== 'undefined' && ALL_PRODUCTS.length) {
      const featured = ALL_PRODUCTS.slice(0, 8);
      grid.innerHTML = featured.map(p => buildProductCard(p)).join('');
    } else if (attempts < 20) {
      setTimeout(() => tryRender(attempts + 1), 150);
    }
  };
  tryRender();
}

// ============================================================
// SCAN RESULT HELPERS
// ============================================================
function switchTab(tabId, btn) {
  document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
  const tab = document.getElementById(tabId);
  if (tab) tab.classList.add('active');
  if (btn) btn.classList.add('active');
}

function viewComponentDetails() { navigateTo('component-details'); }
function downloadPDFReport() { showToast('<i class="fa-solid fa-file-pdf"></i> Preparing PDF report…', 'info', 2500); }
function saveToHistory() { showToast('<i class="fa-solid fa-bookmark"></i> Scan saved to your history!', 'success'); }

// ============================================================
// APPOINTMENT BOOKING
// ============================================================
function handleBookAppointment(event) {
  event.preventDefault();
  const device = document.getElementById('appointDevice').value;
  const date   = document.getElementById('appointDate').value;
  closeModal('appointmentModal');
  showToast(`<i class="fa-solid fa-calendar-check"></i> Appointment booked for <strong>${device}</strong> on <strong>${date}</strong>!`, 'success', 5000);
}

function openAppointmentModal(storeId, storeName) {
  document.getElementById('appointStoreId').value = storeId;
  document.getElementById('appointStoreName').textContent = `Book at ${storeName}`;
  openModal('appointmentModal');
}

// ============================================================
// PRODUCT QUICK VIEW
// ============================================================
function openProductModal(product) {
  const content = document.getElementById('productModalContent');
  if (!content) return;

  const isWishlisted = AppState.wishlist.includes(product.id);

  content.innerHTML = `
    <div class="product-detail-gallery" style="min-height:260px; border-radius:var(--radius-lg); box-shadow:var(--neo-shadow);">
      ${product.image_url
        ? `<img src="${product.image_url}" alt="${product.name}" class="product-detail-img" />`
        : `<div style="font-size:4rem; color:var(--color-primary);"><i class="fa-solid fa-microchip"></i></div>`
      }
    </div>
    <div class="product-detail-info">
      <div>
        <span class="product-category">${product.category}</span>
        <h2 class="product-detail-title" style="font-size:1.5rem; margin-top:0.4rem;">${product.name}</h2>
        <p style="font-size:0.85rem; color:var(--color-text-faint); margin-top:0.25rem;">Part# ${product.part_number}</p>
        <div class="product-rating" style="margin-top:0.6rem;">
          <div class="stars">${renderStars(product.rating)}</div>
          <span class="rating-count">${product.rating} · ${product.stock_quantity} in stock</span>
        </div>
        <p style="margin-top:1rem; font-size:0.88rem; color:var(--color-text-muted); line-height:1.7;">${product.compatibility_info || 'Compatible with standard electronics applications.'}</p>
        <div style="font-family:'Outfit',sans-serif; font-size:2rem; font-weight:800; color:var(--color-primary); margin-top:1rem;">
          ${product.price_formatted || '$' + product.price.toFixed(2)}
        </div>
        <div style="display:flex; align-items:center; gap:0.75rem; margin-top:0.5rem;">
          <span class="badge badge-success"><i class="fa-solid fa-circle-check"></i> ${product.stock_status || 'In Stock'}</span>
          <span style="font-size:0.8rem; color:var(--color-text-faint);">Free shipping over ₹500</span>
        </div>
      </div>
      <div style="display:flex; gap:0.75rem; margin-top:1.5rem; flex-wrap:wrap;">
        <button class="btn btn-primary" style="flex:1;" onclick="addToCart(${JSON.stringify(product).replace(/"/g,'&quot;')}); closeModal('productModal');">
          <i class="fa-solid fa-cart-plus"></i> Add to Cart
        </button>
        <button class="btn btn-secondary btn-icon" onclick="toggleWishlist(${product.id}, this)" aria-label="Add to wishlist">
          <i class="${isWishlisted ? 'fa-solid' : 'fa-regular'} fa-heart" style="${isWishlisted ? 'color:var(--color-danger);' : ''}"></i>
        </button>
      </div>
    </div>
  `;

  openModal('productModal');
}

// ============================================================
// RENDER HELPERS
// ============================================================
function renderStars(rating) {
  const full = Math.floor(rating);
  const half = rating % 1 >= 0.5 ? 1 : 0;
  const empty = 5 - full - half;
  return '<i class="fa-solid fa-star"></i>'.repeat(full) +
         '<i class="fa-solid fa-star-half-stroke"></i>'.repeat(half) +
         '<i class="fa-regular fa-star"></i>'.repeat(empty);
}

function buildProductCard(p) {
  const isWishlisted = AppState.wishlist.includes(p.id);
  const discount = p.original_price ? Math.round((1 - p.price / p.original_price) * 100) : 0;

  return `
    <div class="product-card" role="listitem" tabindex="0"
         aria-label="${p.name}"
         onkeydown="if(event.key==='Enter') openProductModal(${JSON.stringify(p).replace(/"/g,'&quot;')})">
      <div class="product-img-wrap">
        ${discount >= 10 ? `<span class="product-badge badge-sale">-${discount}%</span>` : ''}
        ${!discount && p.is_new ? `<span class="product-badge badge-new">NEW</span>` : ''}
        ${p.is_hot ? `<span class="product-badge badge-hot">🔥 HOT</span>` : ''}
        <button class="wishlist-btn ${isWishlisted ? 'active' : ''}"
                onclick="event.stopPropagation(); toggleWishlist(${p.id}, this)"
                aria-label="Add ${p.name} to wishlist">
          <i class="${isWishlisted ? 'fa-solid' : 'fa-regular'} fa-heart"></i>
        </button>
        ${p.image_url
          ? `<img src="${p.image_url}" alt="${p.name}" class="product-img" loading="lazy" />`
          : `<div class="product-icon-placeholder"><i class="fa-solid fa-microchip"></i></div>`
        }
      </div>
      <div class="product-info" onclick="openProductModal(${JSON.stringify(p).replace(/"/g,'&quot;')})">
        <span class="product-category">${p.category}</span>
        <div class="product-name">${p.name}</div>
        <div class="product-part">${p.part_number}</div>
        <div class="product-rating">
          <div class="stars">${renderStars(p.rating)}</div>
          <span class="rating-count">(${p.stock_quantity})</span>
        </div>
        <div class="product-price-row">
          <div>
            <div class="product-price">${p.price_formatted || '$' + p.price.toFixed(2)}</div>
            ${p.original_price ? `<div class="product-price-old">$${p.original_price.toFixed(2)}</div>` : ''}
          </div>
          <button class="product-add-btn"
                  onclick="event.stopPropagation(); addToCart(${JSON.stringify(p).replace(/"/g,'&quot;')})"
                  aria-label="Add ${p.name} to cart"
                  title="Add to cart">
            <i class="fa-solid fa-plus"></i>
          </button>
        </div>
      </div>
    </div>
  `;
}

// ============================================================
// DASHBOARD
// ============================================================
function renderDashboard() {
  const greeting = document.getElementById('dashUserGreeting');
  if (greeting && AppState.user) {
    greeting.textContent = `👋 Hello, ${AppState.user.name}`;
  }

  const table = document.getElementById('dashScanTable');
  if (!table) return;

  const rows = [
    { device: 'LM317 Power Supply Module', comp: 'Linear Voltage Regulator', status: 'Identified', conf: 'Confirmed', date: '2026-09-28' },
    { device: 'NE555 Timer Circuit PCB', comp: 'Precision Timing IC', status: 'Identified', conf: 'Confirmed', date: '2026-09-25' },
    { device: 'IRFZ44N Motor Drive Board', comp: 'N-Channel Power MOSFET', status: 'Identified', conf: 'Confirmed', date: '2026-09-20' },
    { device: 'STM32 Main Control Board', comp: '32-Bit ARM Microcontroller', status: 'Identified', conf: 'Confirmed', date: '2026-09-15' },
  ];

  const statusBadge = (s) => {
    if (s === 'Identified') return `<span class="badge badge-success">${s}</span>`;
    return `<span class="badge badge-info">${s}</span>`;
  };

  table.innerHTML = rows.map(r => `
    <tr>
      <td style="font-weight:600;">${r.device}</td>
      <td>${r.comp}</td>
      <td>${statusBadge(r.status)}</td>
      <td style="color:var(--color-primary); font-weight:600;">${r.conf}</td>
      <td style="color:var(--color-text-faint);">${r.date}</td>
      <td>
        <button class="btn btn-outline btn-sm" onclick="navigateTo('scan-result')">
          <i class="fa-solid fa-eye"></i> View
        </button>
      </td>
    </tr>
  `).join('');
}

function initDashboard() {
  // Animate metric counters
  const animate = (id, target, suffix='', color='') => {
    const el = document.getElementById(id);
    if (!el) return;
    let current = 0;
    const step = Math.ceil(target / 30);
    const interval = setInterval(() => {
      current = Math.min(current + step, target);
      el.textContent = current + suffix;
      if (current >= target) clearInterval(interval);
    }, 40);
    if (color) el.style.color = color;
  };

  setTimeout(() => {
    animate('dashTotalScans', 24);
    animate('dashIssuesFound', 18);
    animate('dashRepaired', 12);
    animate('dashInProgress', 4);
    animate('dashOrders', 7);
  }, 300);
}

// ============================================================
// CAMERA MODAL (stub — uses scan.js)
// ============================================================
function openCameraModal() {
  showToast('<i class="fa-solid fa-camera"></i> Camera access requires HTTPS. Using file upload instead.', 'warning');
  document.getElementById('fileInput')?.click();
}

// Expose globals
window.navigateTo    = navigateTo;
window.openModal     = openModal;
window.closeModal    = closeModal;
window.showToast     = showToast;
window.addToCart     = addToCart;
window.removeFromCart= removeFromCart;
window.updateCartQty = updateCartQty;
window.toggleCartDrawer = toggleCartDrawer;
window.toggleWishlist   = toggleWishlist;
window.openProductModal = openProductModal;
window.buildProductCard = buildProductCard;
window.renderStars   = renderStars;
window.switchTab     = switchTab;
window.AppState      = AppState;
window.handleLoginSubmit   = handleLoginSubmit;
window.handleRegisterSubmit= handleRegisterSubmit;
window.handleLogout        = handleLogout;
window.guestLogin          = guestLogin;
window.handleCheckoutSubmit= handleCheckoutSubmit;
window.handleBookAppointment = handleBookAppointment;
window.filterByCategory  = filterByCategory;
window.toggleMobileMenu  = toggleMobileMenu;
window.toggleNavSearch   = toggleNavSearch;
window.handleGlobalSearch= handleGlobalSearch;
window.handleSearchKey   = handleSearchKey;
window.openAppointmentModal = openAppointmentModal;
window.downloadPDFReport = downloadPDFReport;
window.saveToHistory     = saveToHistory;
window.openCameraModal   = openCameraModal;
