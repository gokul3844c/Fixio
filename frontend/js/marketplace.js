/* ==========================================================================
   NeoShop — Marketplace & Catalog Logic (marketplace.js)
   ========================================================================== */

'use strict';

const ALL_PRODUCTS = [
  {
    id: 1,
    name: "LM7805 Voltage Regulator IC (5V 1.5A)",
    part_number: "LM7805-TO220",
    category: "IC",
    price: 0.25,
    original_price: 0.40,
    price_formatted: "$0.25",
    stock_status: "In Stock",
    stock_quantity: 450,
    compatibility_info: "Universal replacement for 5V power rails in TVs, routers, & mainboards.",
    rating: 4.9,
    is_new: false,
    is_hot: true,
    image_url: ""
  },
  {
    id: 2,
    name: "1000µF 25V Low-ESR Radial Electrolytic Capacitor",
    part_number: "ECE-1000UF25V",
    category: "Capacitor",
    price: 0.15,
    original_price: 0.25,
    price_formatted: "$0.15",
    stock_status: "In Stock",
    stock_quantity: 1200,
    compatibility_info: "High-frequency power filter capacitor for SMPS & audio circuits.",
    rating: 4.8,
    is_new: true,
    is_hot: false,
    image_url: ""
  },
  {
    id: 3,
    name: "IRFZ44N N-Channel Power MOSFET (55V 49A)",
    part_number: "IRFZ44N-TO220",
    category: "MOSFET",
    price: 0.45,
    original_price: 0.60,
    price_formatted: "$0.45",
    stock_status: "In Stock",
    stock_quantity: 320,
    compatibility_info: "Ideal for power inverters, motor controllers, and DC-DC converters.",
    rating: 4.9,
    is_new: false,
    is_hot: true,
    image_url: ""
  },
  {
    id: 4,
    name: "1N5819 Schottky Barrier Diode (40V 1A)",
    part_number: "1N5819-DO41",
    category: "Diode",
    price: 0.05,
    original_price: 0.10,
    price_formatted: "$0.05",
    stock_status: "In Stock",
    stock_quantity: 2000,
    compatibility_info: "High-speed flyback diode protection for inductive switching.",
    rating: 4.7,
    is_new: false,
    is_hot: false,
    image_url: ""
  },
  {
    id: 5,
    name: "ESP32-WROOM-32D Dual-Core WiFi+BT MCU Module",
    part_number: "ESP32-WROOM-32D",
    category: "IC",
    price: 3.80,
    original_price: 5.00,
    price_formatted: "$3.80",
    stock_status: "In Stock",
    stock_quantity: 650,
    compatibility_info: "IoT development, smart home controllers, and automation boards.",
    rating: 4.95,
    is_new: true,
    is_hot: true,
    image_url: ""
  },
  {
    id: 6,
    name: "Precision Soldering Iron Kit 60W Adjustable Temp",
    part_number: "TL-SOL-60W",
    category: "Tool",
    price: 18.50,
    original_price: 24.99,
    price_formatted: "$18.50",
    stock_status: "In Stock",
    stock_quantity: 85,
    compatibility_info: "ESD-safe ceramic heater with 5 interchangeable tips.",
    rating: 4.85,
    is_new: false,
    is_hot: true,
    image_url: ""
  },
  {
    id: 7,
    name: "NE555P Precision Single Timer IC Dip-8",
    part_number: "NE555P-DIP8",
    category: "IC",
    price: 0.18,
    original_price: 0.30,
    price_formatted: "$0.18",
    stock_status: "In Stock",
    stock_quantity: 1800,
    compatibility_info: "Standard clock generation, pulse generators, and timing circuits.",
    rating: 4.9,
    is_new: false,
    is_hot: false,
    image_url: ""
  },
  {
    id: 8,
    name: "0.1µF 50V Ceramic Disc Capacitor (100-Pack)",
    part_number: "CC-104-50V",
    category: "Capacitor",
    price: 1.20,
    original_price: 1.80,
    price_formatted: "$1.20",
    stock_status: "In Stock",
    stock_quantity: 500,
    compatibility_info: "High-frequency decoupling capacitors for microcontroller power pins.",
    rating: 4.8,
    is_new: false,
    is_hot: false,
    image_url: ""
  },
  {
    id: 9,
    name: "2N2222A NPN Bipolar Transistor (40V 600mA)",
    part_number: "2N2222A-TO92",
    category: "Transistor",
    price: 0.08,
    original_price: 0.15,
    price_formatted: "$0.08",
    stock_status: "In Stock",
    stock_quantity: 3500,
    compatibility_info: "General purpose amplification and high-speed switching.",
    rating: 4.75,
    is_new: false,
    is_hot: false,
    image_url: ""
  },
  {
    id: 10,
    name: "Digital Multimeter Auto-Ranging 6000 Counts TRMS",
    part_number: "TL-DMM-6000",
    category: "Tool",
    price: 32.00,
    original_price: 45.00,
    price_formatted: "$32.00",
    stock_status: "In Stock",
    stock_quantity: 110,
    compatibility_info: "Measures Voltage, Current, Resistance, Capacitance, & Frequency.",
    rating: 4.92,
    is_new: true,
    is_hot: true,
    image_url: ""
  },
  {
    id: 11,
    name: "10K Ohm 1/4W 1% Metal Film Resistors (100-Pack)",
    part_number: "RES-10K-1/4W",
    category: "Resistor",
    price: 1.50,
    original_price: 2.20,
    price_formatted: "$1.50",
    stock_status: "In Stock",
    stock_quantity: 800,
    compatibility_info: "Precision low-noise pull-up & current limiting resistors.",
    rating: 4.9,
    is_new: false,
    is_hot: false,
    image_url: ""
  },
  {
    id: 12,
    name: "AMS1117-3.3V SMD LDO Voltage Regulator SOT-223",
    part_number: "AMS1117-3.3",
    category: "IC",
    price: 0.12,
    original_price: 0.20,
    price_formatted: "$0.12",
    stock_status: "In Stock",
    stock_quantity: 2400,
    compatibility_info: "Compact 3.3V step-down regulator for 3.3V logic supply.",
    rating: 4.88,
    is_new: false,
    is_hot: false,
    image_url: ""
  },
  {
    id: 13,
    name: "Thermal Compound / Heatsink Paste (10g Syringe)",
    part_number: "HY510-10G",
    category: "Compound",
    price: 4.50,
    original_price: 6.50,
    price_formatted: "$4.50",
    stock_status: "In Stock",
    stock_quantity: 850,
    compatibility_info: "High thermal conductivity silicone paste for ICs, MOSFETs, and CPU/GPU heatsinks.",
    rating: 4.9,
    is_new: true,
    is_hot: true,
    image_url: ""
  },
  {
    id: 14,
    name: "Arctic MX-4 High Performance Thermal Compound Paste (4g)",
    part_number: "ACTCP00002B",
    category: "Compound",
    price: 8.99,
    original_price: 11.99,
    price_formatted: "$8.99",
    stock_status: "In Stock",
    stock_quantity: 420,
    compatibility_info: "Premium carbon-microparticle thermal paste for maximum heat dissipation in electronic repairs.",
    rating: 4.95,
    is_new: true,
    is_hot: true,
    image_url: ""
  }
];

let filteredProducts = [...ALL_PRODUCTS];

function buildProductCard(p) {
  const isWishlisted = (window.AppState && window.AppState.wishlist && window.AppState.wishlist.includes(p.id)) || false;
  const ratingVal = p.rating || 5.0;
  const fullStars = Math.floor(ratingVal);
  const halfStar = (ratingVal % 1) >= 0.5;
  let starsHtml = '';
  for (let i = 0; i < 5; i++) {
    if (i < fullStars) {
      starsHtml += '<i class="fa-solid fa-star"></i>';
    } else if (i === fullStars && halfStar) {
      starsHtml += '<i class="fa-solid fa-star-half-stroke"></i>';
    } else {
      starsHtml += '<i class="fa-regular fa-star"></i>';
    }
  }

  const pObj = {
    id: p.id,
    name: p.name,
    price: p.price,
    image_url: p.image_url || ''
  };
  const pJson = JSON.stringify(pObj).replace(/'/g, "&#39;").replace(/"/g, "&quot;");

  return `
    <div class="product-card neo-card" id="product-card-${p.id}">
      ${p.is_new ? '<span class="product-badge badge-new">NEW</span>' : ''}
      ${p.is_hot ? '<span class="product-badge badge-hot">HOT</span>' : ''}
      <button class="wishlist-btn ${isWishlisted ? 'active' : ''}" onclick="toggleWishlist(${p.id}, this)" title="Add to Wishlist">
        <i class="${isWishlisted ? 'fa-solid' : 'fa-regular'} fa-heart"></i>
      </button>
      <div class="product-img-wrap">
        ${p.image_url 
          ? `<img src="${p.image_url}" alt="${p.name}" class="product-img" loading="lazy" />`
          : `<div class="product-icon-placeholder"><i class="fa-solid ${p.category === 'Compound' ? 'fa-fill-drip' : 'fa-microchip'}" style="font-size:2rem; color:var(--color-primary);"></i></div>`
        }
      </div>
      <div class="product-info">
        <span class="product-category">${p.category || 'Component'}</span>
        <h4 class="product-name" title="${p.name}">${p.name}</h4>
        <span class="product-part">${p.part_number || ''}</span>
        <div class="product-rating">
          <div class="stars">${starsHtml}</div>
          <span class="rating-count">(${ratingVal.toFixed(1)})</span>
        </div>
        <div class="product-price-row">
          <div>
            <span class="product-price">${p.price_formatted || '$' + Number(p.price).toFixed(2)}</span>
            ${p.original_price ? `<span class="product-price-old">$${Number(p.original_price).toFixed(2)}</span>` : ''}
          </div>
          <button class="product-add-btn" onclick="addToCart(${pJson})" title="Add to Cart">
            <i class="fa-solid fa-cart-plus"></i>
          </button>
        </div>
      </div>
    </div>
  `;
}
window.buildProductCard = buildProductCard;

function initShop() {
  loadProductsFromAPI();
}

async function loadProductsFromAPI() {
  try {
    const res = await fetch('/api/marketplace');
    if (res.ok) {
      const data = await res.json();
      if (Array.isArray(data) && data.length > 0) {
        ALL_PRODUCTS.length = 0;
        ALL_PRODUCTS.push(...data);
      }
    }
  } catch {
    // Keep local dataset if backend endpoint unavailable
  }
  filterMarketplace();
}

function filterMarketplace() {
  const searchInput = document.getElementById('marketSearchInput');
  const catSelect   = document.getElementById('marketCategorySelect');
  const sortSelect  = document.getElementById('marketSortSelect');

  const query    = searchInput ? searchInput.value.trim().toLowerCase() : '';
  const category = catSelect   ? catSelect.value : 'All';
  const sortBy   = sortSelect  ? sortSelect.value : 'featured';

  filteredProducts = ALL_PRODUCTS.filter(prod => {
    const matchQuery = !query ||
      prod.name.toLowerCase().includes(query) ||
      prod.part_number.toLowerCase().includes(query) ||
      prod.category.toLowerCase().includes(query) ||
      (prod.compatibility_info && prod.compatibility_info.toLowerCase().includes(query));

    const matchCat = category === 'All' || prod.category.toLowerCase() === category.toLowerCase();

    return matchQuery && matchCat;
  });

  // Sorting
  if (sortBy === 'price-low') {
    filteredProducts.sort((a, b) => a.price - b.price);
  } else if (sortBy === 'price-high') {
    filteredProducts.sort((a, b) => b.price - a.price);
  } else if (sortBy === 'rating') {
    filteredProducts.sort((a, b) => b.rating - a.rating);
  } else if (sortBy === 'newest') {
    filteredProducts.sort((a, b) => (b.is_new ? 1 : 0) - (a.is_new ? 1 : 0));
  }

  renderMarketplaceGrid(filteredProducts);
}

function renderMarketplaceGrid(products) {
  const container = document.getElementById('marketProductGrid');
  const counter   = document.getElementById('marketProductCount');

  if (counter) counter.textContent = products.length;

  if (!container) return;

  if (products.length === 0) {
    container.innerHTML = `
      <div style="grid-column: 1 / -1; text-align: center; padding: 4rem 1rem;">
        <div style="font-size: 3rem; color: var(--color-text-faint); margin-bottom: 1rem;">
          <i class="fa-solid fa-magnifying-glass-minus"></i>
        </div>
        <h3 style="font-size: 1.2rem; color: var(--color-text-muted);">No products found</h3>
        <p style="font-size: 0.9rem; color: var(--color-text-faint); margin-top: 0.4rem;">
          Try adjusting your search terms or category filter.
        </p>
        <button class="btn btn-secondary btn-sm" style="margin-top: 1.2rem;" onclick="resetShopFilters()">
          Reset Filters
        </button>
      </div>
    `;
    return;
  }

  container.innerHTML = products.map(p => window.buildProductCard ? window.buildProductCard(p) : '').join('');
}

function resetShopFilters() {
  const searchInput = document.getElementById('marketSearchInput');
  const catSelect   = document.getElementById('marketCategorySelect');
  const sortSelect  = document.getElementById('marketSortSelect');

  if (searchInput) searchInput.value = '';
  if (catSelect)   catSelect.value   = 'All';
  if (sortSelect)  sortSelect.value  = 'featured';

  filterMarketplace();
}

async function handleAddProductSubmit(event) {
  event.preventDefault();

  const name        = document.getElementById('newProdName').value.trim();
  const partNumber  = document.getElementById('newProdPartNumber').value.trim();
  const category    = document.getElementById('newProdCategory').value;
  const price       = parseFloat(document.getElementById('newProdPrice').value);
  const stockQty    = parseInt(document.getElementById('newProdStock').value) || 100;
  const compatInfo  = document.getElementById('newProdCompat').value.trim();
  const imageUrl    = document.getElementById('newProdImage').value.trim();

  const payload = {
    name,
    part_number: partNumber,
    category,
    price,
    price_formatted: `$${price.toFixed(2)}`,
    stock_status: 'In Stock',
    stock_quantity: stockQty,
    compatibility_info: compatInfo || 'Standard electronics application component.',
    rating: 5.0,
    image_url: imageUrl || ''
  };

  showToast('<i class="fa-solid fa-spinner fa-spin"></i> Adding new product…', 'info', 2000);

  try {
    const res = await fetch('/api/marketplace', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (res.ok) {
      const created = await res.json();
      ALL_PRODUCTS.unshift(created);
    } else {
      throw new Error();
    }
  } catch {
    // Local fallback creation
    const localProduct = {
      id: Date.now(),
      ...payload,
      is_new: true,
      is_hot: true
    };
    ALL_PRODUCTS.unshift(localProduct);
  }

  filterMarketplace();
  closeModal('addProductModal');
  event.target.reset();

  showToast(`<i class="fa-solid fa-circle-check"></i> Product <strong>"${name}"</strong> added successfully!`, 'success', 5000);
}

window.ALL_PRODUCTS          = ALL_PRODUCTS;
window.initShop              = initShop;
window.filterMarketplace     = filterMarketplace;
window.resetShopFilters      = resetShopFilters;
window.handleAddProductSubmit = handleAddProductSubmit;

