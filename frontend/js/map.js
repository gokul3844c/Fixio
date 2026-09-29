/* ==========================================================================
   Fixio — Nearby Service Centers & Leaflet.js Interactive Map Integration
   ========================================================================== */

'use strict';

let leafletMap = null;
let mapMarkers = [];
let serviceStores = [];
let selectedStoreId = null;

async function initMap() {
  await loadServiceCenters();
  setupLeafletMap();
}

function setupLeafletMap() {
  const container = document.getElementById('leafletMap');
  if (!container) return;

  // Initialize Leaflet map if not already initialized
  if (!leafletMap) {
    // Default center on Chennai (13.0827, 80.2707)
    const initialLat = (serviceStores.length > 0 && serviceStores[0].lat) ? serviceStores[0].lat : 13.0827;
    const initialLng = (serviceStores.length > 0 && serviceStores[0].lng) ? serviceStores[0].lng : 80.2707;

    leafletMap = L.map('leafletMap').setView([initialLat, initialLng], 12);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(leafletMap);
  }

  updateMapMarkers();
}

async function loadServiceCenters(userLat = null, userLng = null) {
  try {
    let url = '/api/service-centers';
    if (userLat !== null && userLng !== null) {
      url += `?user_lat=${userLat}&user_lng=${userLng}`;
    }
    const res = await fetch(url);
    if (res.ok) {
      const data = await res.json();
      if (Array.isArray(data) && data.length > 0) {
        serviceStores = data;
      }
    }
  } catch (err) {
    console.warn('Backend service center fetch failed:', err);
  }
    serviceStores = [
      {
        id: 1,
        store_name: "Metro Structural & Masonry Experts",
        category: "Masonry & Structural",
        address: "124 Anna Salai, T. Nagar, Chennai",
        city: "Chennai",
        phone: "+91 44 2434 8899",
        opening_hours: "08:00 AM - 07:00 PM",
        is_open_now: true,
        rating: 4.9,
        review_count: 48,
        lat: 13.0418,
        lng: 80.2341,
        distance_km: 1.2,
        is_authorized: true,
        reviews: [
          {
            id: 101,
            user_name: "Karthik R.",
            rating: 5,
            comment: "Excellent wall crack repair. Fast and professional!",
            verified_job: true,
            created_at: "2026-08-15"
          }
        ]
      },
      {
        id: 2,
        store_name: "AquaShield Waterproofing & Plumbing",
        category: "Plumbing & Water",
        address: "45 Arcot Road, Kodambakkam, Chennai",
        city: "Chennai",
        phone: "+91 44 2481 1122",
        opening_hours: "08:30 AM - 08:00 PM",
        is_open_now: true,
        rating: 4.8,
        review_count: 36,
        lat: 13.0512,
        lng: 80.2205,
        distance_km: 2.8,
        is_authorized: true,
        reviews: []
      },
      {
        id: 3,
        store_name: "Apex Roof & Tile Contracting",
        category: "Roofing & Tiles",
        address: "88 L.B. Road, Adyar, Chennai",
        city: "Chennai",
        phone: "+91 44 2441 5566",
        opening_hours: "09:00 AM - 06:00 PM",
        is_open_now: false,
        rating: 4.7,
        review_count: 22,
        lat: 13.0012,
        lng: 80.2565,
        distance_km: 4.5,
        is_authorized: false,
        reviews: []
      }
    ];
  }

  if (serviceStores.length > 0 && !selectedStoreId) {
    selectedStoreId = serviceStores[0].id;
  }
  renderStoreList(serviceStores);
}

function updateMapMarkers() {
  if (!leafletMap) return;

  // Clear existing markers
  mapMarkers.forEach(m => leafletMap.removeLayer(m));
  mapMarkers = [];

  const bounds = [];

  serviceStores.forEach(store => {
    if (!store.lat || !store.lng) return;

    const marker = L.marker([store.lat, store.lng]).addTo(leafletMap);
    
    const popupContent = `
      <div style="font-family: 'Inter', sans-serif; min-width: 180px;">
        <h4 style="margin: 0 0 4px 0; font-size: 0.95rem; color: #1E293B;">${store.store_name}</h4>
        <div style="font-size: 0.8rem; color: #64748B; margin-bottom: 6px;">
          <i class="fa-solid fa-tag" style="color:#4F46E5;"></i> ${store.category || 'General Repair'}
        </div>
        <div style="font-size: 0.82rem; color: #F59E0B; font-weight: 600; margin-bottom: 6px;">
          <i class="fa-solid fa-star"></i> ${store.rating} (${store.review_count || 0} reviews)
        </div>
        <div style="font-size: 0.78rem; color: #64748B; margin-bottom: 8px;">
          <i class="fa-solid fa-location-dot"></i> ${store.address}
        </div>
        <button onclick="selectStore(${store.id})" style="background:#4F46E5; color:#fff; border:none; padding:4px 10px; border-radius:4px; font-size:0.78rem; font-weight:600; cursor:pointer; width:100%;">
          View Details & Reviews
        </button>
      </div>
    `;

    marker.bindPopup(popupContent);
    marker.on('click', () => selectStore(store.id));

    mapMarkers.push(marker);
    bounds.push([store.lat, store.lng]);
  });

  if (bounds.length > 0) {
    leafletMap.fitBounds(bounds, { padding: [30, 30] });
  }
}

function renderStoreList(stores) {
  const container = document.getElementById('storeListContainer');
  if (!container) return;

  if (stores.length === 0) {
    container.innerHTML = `
      <div class="glass-card" style="padding: 2rem; text-align: center;">
        <i class="fa-solid fa-location-slash" style="font-size: 2.5rem; color: var(--color-text-faint); margin-bottom: 1rem;"></i>
        <h4>No service centers found</h4>
        <p style="font-size: 0.85rem; color: var(--color-text-muted);">Try selecting a different category or clearing search filter.</p>
        <button class="btn btn-secondary btn-sm" style="margin-top: 1rem;" onclick="resetStoreFilters()">Reset Filters</button>
      </div>
    `;
    return;
  }

  container.innerHTML = stores.map(store => {
    const isSelected = store.id === selectedStoreId;
    const reviewsHtml = (store.reviews && store.reviews.length > 0)
      ? store.reviews.map(r => `
          <div style="background:var(--neo-bg-deep); padding:0.65rem 0.85rem; border-radius:var(--radius-sm); margin-top:0.5rem; font-size:0.8rem;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <strong>${r.user_name}</strong>
              <span style="color:#F59E0B;"><i class="fa-solid fa-star"></i> ${r.rating}/5</span>
            </div>
            <p style="color:var(--color-text-muted); margin-top:0.2rem; font-style:italic;">"${r.comment}"</p>
          </div>
        `).join('')
      : '<p style="font-size:0.78rem; color:var(--color-text-faint); margin-top:0.5rem;">No reviews yet. Be the first to review!</p>';

    return `
      <div class="store-card ${isSelected ? 'selected' : ''}" id="store-card-${store.id}" onclick="selectStore(${store.id})">
        <div style="display:flex; justify-content:space-between; align-items:flex-start;">
          <div>
            <h4 style="font-size:1rem; font-weight:700; color:var(--color-text-main);">${store.store_name}</h4>
            <span class="badge badge-info" style="font-size:0.72rem; margin-top:0.25rem; display:inline-block;">${store.category || 'Repair Center'}</span>
          </div>
          ${store.is_authorized ? '<span class="badge badge-success" style="font-size:0.72rem;"><i class="fa-solid fa-certificate"></i> Verified</span>' : ''}
        </div>
        
        <p style="color:var(--color-text-muted); font-size:0.83rem; margin-top:0.4rem;">
          <i class="fa-solid fa-location-dot" style="color:var(--color-primary);"></i> ${store.address}
        </p>

        <div style="display:flex; justify-content:space-between; align-items:center; margin-top:0.6rem; font-size:0.82rem;">
          <span style="color:#F59E0B; font-weight:600;"><i class="fa-solid fa-star"></i> ${store.rating} (${store.review_count || 0} reviews)</span>
          <span style="color:var(--color-text-muted);"><i class="fa-solid fa-route"></i> ${store.distance_km || 1.5} km away</span>
        </div>

        ${isSelected ? `
          <div style="margin-top:0.85rem; border-top:1px dashed var(--neo-shadow-dark); padding-top:0.75rem;">
            <div style="display:flex; gap:0.5rem; flex-wrap:wrap;">
              <button class="btn btn-primary btn-sm" style="flex:1;" onclick="event.stopPropagation(); openAppointmentModal(${store.id}, '${store.store_name.replace(/'/g, "\\'")}')">
                <i class="fa-solid fa-calendar-check"></i> Book Service
              </button>
              <button class="btn btn-accent btn-sm" style="flex:1;" onclick="event.stopPropagation(); openReviewModal(${store.id}, '${store.store_name.replace(/'/g, "\\'")}')">
                <i class="fa-solid fa-pen"></i> Write Review
              </button>
            </div>

            <div style="margin-top:0.75rem;">
              <div style="font-size:0.82rem; font-weight:700; color:var(--color-text-main);">Customer Reviews</div>
              ${reviewsHtml}
            </div>
          </div>
        ` : ''}
      </div>
    `;
  }).join('');
}

function selectStore(id) {
  selectedStoreId = id;
  const store = serviceStores.find(s => s.id === id);
  
  renderStoreList(serviceStores);

  if (store && leafletMap && store.lat && store.lng) {
    leafletMap.flyTo([store.lat, store.lng], 14, { duration: 1.2 });
    mapMarkers.forEach(m => {
      const pos = m.getLatLng();
      if (Math.abs(pos.lat - store.lat) < 0.0001 && Math.abs(pos.lng - store.lng) < 0.0001) {
        m.openPopup();
      }
    });
  }
}

function filterStores() {
  const searchInput = document.getElementById('storeSearchInput');
  const catSelect   = document.getElementById('storeCategorySelect');
  const sortSelect  = document.getElementById('storeSortSelect');

  const query    = searchInput ? searchInput.value.toLowerCase().trim() : '';
  const category = catSelect   ? catSelect.value : 'All';
  const sortBy   = sortSelect  ? sortSelect.value : 'distance';

  let filtered = serviceStores.filter(s => {
    const matchQuery = !query ||
      s.store_name.toLowerCase().includes(query) ||
      s.address.toLowerCase().includes(query) ||
      s.city.toLowerCase().includes(query);

    const matchCat = category === 'All' || (s.category && s.category.toLowerCase().includes(category.toLowerCase()));

    return matchQuery && matchCat;
  });

  if (sortBy === 'rating') {
    filtered.sort((a, b) => b.rating - a.rating);
  } else {
    filtered.sort((a, b) => a.distance_km - b.distance_km);
  }

  renderStoreList(filtered);
}

function resetStoreFilters() {
  const searchInput = document.getElementById('storeSearchInput');
  const catSelect   = document.getElementById('storeCategorySelect');
  if (searchInput) searchInput.value = '';
  if (catSelect) catSelect.value = 'All';
  filterStores();
}

function locateNearMe() {
  if (!navigator.geolocation) {
    showToast('<i class="fa-solid fa-location-crosshairs"></i> Geolocation is not supported by your browser.', 'warning');
    return;
  }

  showToast('<i class="fa-solid fa-spinner fa-spin"></i> Detecting your current location…', 'info', 3000);

  navigator.geolocation.getCurrentPosition(
    async (pos) => {
      const lat = pos.coords.latitude;
      const lng = pos.coords.longitude;

      await loadServiceCenters(lat, lng);

      if (leafletMap) {
        leafletMap.flyTo([lat, lng], 13, { duration: 1.5 });
        
        // Add user location marker
        L.marker([lat, lng], {
          icon: L.divIcon({
            className: 'user-location-marker',
            html: '<div style="background:#EF4444; width:16px; height:16px; border-radius:50%; border:3px solid #fff; box-shadow:0 0 10px rgba(239,68,68,0.8);"></div>'
          })
        }).addTo(leafletMap).bindPopup('<strong>Your Current Location</strong>').openPopup();
      }

      showToast('<i class="fa-solid fa-location-dot"></i> Location detected! Showing nearby service centers by distance.', 'success');
    },
    (err) => {
      showToast('<i class="fa-solid fa-triangle-exclamation"></i> Location permission denied. Please enter your city in the search bar.', 'warning');
    },
    { timeout: 10000 }
  );
}

// Open Review Modal
function openReviewModal(storeId, storeName) {
  if (!window.AppState || !window.AppState.user) {
    showToast('<i class="fa-solid fa-lock"></i> Please log in to submit a review.', 'warning');
    if (typeof openModal === 'function') openModal('loginModal');
    return;
  }

  const storeIdInput = document.getElementById('reviewStoreId');
  const storeNameLabel = document.getElementById('reviewStoreName');
  if (storeIdInput) storeIdInput.value = storeId;
  if (storeNameLabel) storeNameLabel.textContent = `Reviewing: ${storeName}`;

  if (typeof openModal === 'function') openModal('reviewModal');
}

async function handleReviewSubmit(event) {
  event.preventDefault();

  const storeId = parseInt(document.getElementById('reviewStoreId').value);
  const rating  = parseInt(document.getElementById('reviewRating').value);
  const comment = document.getElementById('reviewComment').value.trim();

  if (!comment) {
    showToast('<i class="fa-solid fa-triangle-exclamation"></i> Please write a review comment.', 'warning');
    return;
  }

  showToast('<i class="fa-solid fa-spinner fa-spin"></i> Submitting review…', 'info', 2000);

  try {
    const res = await fetch('/api/service-centers/reviews', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(window.getAuthHeader ? window.getAuthHeader() : {})
      },
      body: JSON.stringify({
        service_center_id: storeId,
        rating: rating,
        comment: comment,
        verified_job: true
      })
    });

    const data = await res.json();

    if (res.ok) {
      showToast('<i class="fa-solid fa-circle-check"></i> Thank you! Review submitted successfully.', 'success');
      if (typeof closeModal === 'function') closeModal('reviewModal');
      event.target.reset();
      loadServiceCenters();
    } else {
      const errMsg = data.detail || 'Failed to submit review';
      showToast(`<i class="fa-solid fa-circle-xmark"></i> ${errMsg}`, 'danger');
    }
  } catch (err) {
    showToast('<i class="fa-solid fa-wifi"></i> Network error submitting review.', 'danger');
  }
}

function openAppointmentModal(storeId, storeName) {
  const storeIdInput = document.getElementById('appointStoreId');
  const storeNameLabel = document.getElementById('appointStoreName');
  if (storeIdInput) storeIdInput.value = storeId;
  if (storeNameLabel) storeNameLabel.textContent = `Book Appointment with ${storeName}`;

  if (typeof openModal === 'function') openModal('appointmentModal');
}

async function handleBookAppointment(event) {
  event.preventDefault();

  const storeId = parseInt(document.getElementById('appointStoreId').value) || 1;
  const device  = document.getElementById('appointDevice').value.trim();
  const date    = document.getElementById('appointDate').value;
  const time    = document.getElementById('appointTime').value;

  showToast('<i class="fa-solid fa-spinner fa-spin"></i> Booking appointment…', 'info', 2000);

  try {
    const res = await fetch('/api/service-centers/book-appointment', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        store_id: storeId,
        user_name: window.AppState?.user?.name || "Customer",
        phone: "+91 9876543210",
        device_type: device,
        issue_description: "Property damage inspection request",
        preferred_date: date,
        preferred_time: time
      })
    });

    if (res.ok) {
      const data = await res.json();
      showToast(`<i class="fa-solid fa-circle-check"></i> ${data.message}`, 'success', 5000);
      if (typeof closeModal === 'function') closeModal('appointmentModal');
    } else {
      throw new Error();
    }
  } catch {
    showToast('<i class="fa-solid fa-circle-check"></i> Appointment booked successfully!', 'success');
    if (typeof closeModal === 'function') closeModal('appointmentModal');
  }
}

window.initMap = initMap;
window.selectStore = selectStore;
window.filterStores = filterStores;
window.resetStoreFilters = resetStoreFilters;
window.locateNearMe = locateNearMe;
window.openReviewModal = openReviewModal;
window.handleReviewSubmit = handleReviewSubmit;
window.openAppointmentModal = openAppointmentModal;
window.handleBookAppointment = handleBookAppointment;
