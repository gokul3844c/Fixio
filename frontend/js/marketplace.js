/* ==========================================================================
   FixAI Replacement Parts Marketplace & E-Commerce Logic
   ========================================================================== */

let productsList = [
  {
    id: 1,
    name: "LM7805 Voltage Regulator IC (5V 1.5A)",
    part_number: "LM7805-TO220",
    category: "IC",
    price: 0.25,
    price_formatted: "$0.25 / ₹20",
    stock_status: "In Stock",
    stock_quantity: 450,
    compatibility_info: "Universal replacement for 5V power rails",
    rating: 4.9,
    image_url: "/assets/products/lm7805_part.jpg"
  },
  {
    id: 2,
    name: "10uF 25V Radial Electrolytic Capacitor (105°C)",
    part_number: "ECE-10UF25V",
    category: "Capacitor",
    price: 0.10,
    price_formatted: "$0.10 / ₹8",
    stock_status: "In Stock",
    stock_quantity: 1200,
    compatibility_info: "Low-ESR power filtering capacitor",
    rating: 4.8,
    image_url: "/assets/products/capacitor_part.jpg"
  },
  {
    id: 3,
    name: "IRFZ44N N-Channel Power MOSFET (55V 49A)",
    part_number: "IRFZ44N-TO220",
    category: "MOSFET",
    price: 0.45,
    price_formatted: "$0.45 / ₹35",
    stock_status: "In Stock",
    stock_quantity: 320,
    compatibility_info: "SMPS power stage & inverter drives",
    rating: 4.9,
    image_url: "/assets/products/mosfet_part.jpg"
  },
  {
    id: 4,
    name: "1N5819 Schottky Barrier Diode (40V 1A)",
    part_number: "1N5819-DO41",
    category: "Diode",
    price: 0.05,
    price_formatted: "$0.05 / ₹4",
    stock_status: "In Stock",
    stock_quantity: 2000,
    compatibility_info: "High-speed flyback diode protection",
    rating: 4.7,
    image_url: "/assets/products/diode_part.jpg"
  }
];

async function loadProducts() {
  try {
    const res = await fetch('/api/marketplace');
    if (res.ok) {
      const data = await res.json();
      if (data && data.length > 0) productsList = data;
    }
  } catch (err) {
    // Keep local list
  }
  renderProductCatalog(productsList);
}

function renderProductCatalog(items) {
  const container = document.getElementById('marketProductGrid');
  if (!container) return;

  container.innerHTML = '';
  items.forEach(prod => {
    const card = document.createElement('div');
    card.className = 'glass-card product-card';

    card.innerHTML = `
      <div style="background: rgba(0,0,0,0.3); height: 140px; border-radius: var(--radius-sm); display: flex; align-items: center; justify-content: center; font-size: 2.5rem; color: var(--color-accent);">
        <i class="${getCategoryIcon(prod.category)}"></i>
      </div>
      <div>
        <div style="font-size: 0.78rem; color: var(--color-text-muted); text-transform: uppercase;">${prod.category}</div>
        <h4 style="font-size: 1rem; margin-top: 0.15rem;">${prod.name}</h4>
        <p style="font-size: 0.82rem; color: var(--color-text-muted); margin-top: 0.25rem;">Part #: ${prod.part_number}</p>
      </div>

      <div style="display: flex; justify-content: space-between; align-items: center; margin-top: auto;">
        <div class="product-price">${prod.price_formatted}</div>
        <button class="btn btn-accent btn-sm" onclick="addToCart(${prod.id})">
          <i class="fa-solid fa-cart-plus"></i> Add
        </button>
      </div>
    `;
    container.appendChild(card);
  });
}

function getCategoryIcon(cat) {
  if (cat === 'IC') return 'fa-solid fa-microchip';
  if (cat === 'Capacitor') return 'fa-solid fa-atom';
  if (cat === 'MOSFET') return 'fa-solid fa-bolt-lightning';
  if (cat === 'Diode') return 'fa-solid fa-arrows-left-right';
  return 'fa-solid fa-cubes';
}

function filterMarketplace() {
  const search = document.getElementById('marketSearchInput').value.toLowerCase();
  const category = document.getElementById('marketCategorySelect').value;

  const filtered = productsList.filter(p => {
    const matchesSearch = p.name.toLowerCase().includes(search) || p.part_number.toLowerCase().includes(search);
    const matchesCategory = category === 'All' || p.category.toLowerCase() === category.toLowerCase();
    return matchesSearch && matchesCategory;
  });

  renderProductCatalog(filtered);
}

function addToCart(productId) {
  const prod = productsList.find(p => p.id === productId);
  if (prod) {
    state.cart.push(prod);
    document.getElementById('cartCount').innerText = state.cart.length;
    showToast(`Added ${prod.name} to cart!`, 'success');
  }
}

function toggleCartDrawer() {
  if (state.cart.length === 0) {
    showToast('Your shopping cart is empty. Add parts from the marketplace.', 'info');
    return;
  }
  showToast(`Cart Checkout: ${state.cart.length} item(s) ready for instant dispatch!`, 'success');
}
