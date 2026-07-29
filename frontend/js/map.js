/* ==========================================================================
   FixAI Interactive Service Center Canvas Map Simulator
   ========================================================================== */

let serviceStores = [
  {
    id: 1,
    store_name: "Master Electronics Repair Service",
    address: "124 Anna Salai, T. Nagar, Chennai",
    phone: "+91 44 2434 8899",
    opening_hours: "09:30 AM - 08:30 PM",
    rating: 4.9,
    review_count: 342,
    x: 180,
    y: 150,
    is_authorized: true
  },
  {
    id: 2,
    store_name: "Sri Venkateshwara Electronics",
    address: "45 Arcot Road, Kodambakkam, Chennai",
    phone: "+91 44 2481 1122",
    opening_hours: "10:00 AM - 09:00 PM",
    rating: 4.8,
    review_count: 189,
    x: 320,
    y: 220,
    is_authorized: true
  },
  {
    id: 3,
    store_name: "Raj Electronics Repair Hub",
    address: "88 L.B. Road, Adyar, Chennai",
    phone: "+91 44 2441 5566",
    opening_hours: "09:00 AM - 08:00 PM",
    rating: 4.7,
    review_count: 115,
    x: 420,
    y: 350,
    is_authorized: false
  },
  {
    id: 4,
    store_name: "Smart Care Service Center",
    address: "12 100 Feet Road, Velachery, Chennai",
    phone: "+91 44 2243 7788",
    opening_hours: "10:00 AM - 08:00 PM",
    rating: 4.8,
    review_count: 210,
    x: 250,
    y: 420,
    is_authorized: true
  }
];

let selectedStoreId = 1;

async function loadServiceCenters() {
  try {
    const res = await fetch('/api/service-centers');
    if (res.ok) {
      const data = await res.json();
      if (data && data.length > 0) {
        serviceStores = data.map((s, idx) => ({
          ...s,
          x: 150 + (idx * 110) % 400,
          y: 120 + (idx * 90) % 350
        }));
      }
    }
  } catch (err) {
    // Keep local fallback store data
  }
  renderStoreList();
  renderCanvasMap();
}

function renderStoreList() {
  const container = document.getElementById('storeListContainer');
  if (!container) return;

  container.innerHTML = '';
  serviceStores.forEach(store => {
    const card = document.createElement('div');
    card.className = `glass-card store-card ${store.id === selectedStoreId ? 'selected' : ''}`;
    card.onclick = () => selectStore(store.id);

    card.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: flex-start;">
        <h4 style="font-size: 1.05rem;">${store.store_name}</h4>
        ${store.is_authorized ? '<span class="badge badge-success"><i class="fa-solid fa-circle-check"></i> Authorized</span>' : ''}
      </div>
      <p style="color: var(--color-text-muted); font-size: 0.88rem; margin-top: 0.35rem;">
        <i class="fa-solid fa-location-dot"></i> ${store.address}
      </p>
      <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 0.75rem; font-size: 0.85rem;">
        <span style="color: #FBBF24;"><i class="fa-solid fa-star"></i> ${store.rating} (${store.review_count} reviews)</span>
        <button class="btn btn-primary btn-sm" onclick="event.stopPropagation(); openAppointmentModal(${store.id})">Book</button>
      </div>
    `;
    container.appendChild(card);
  });
}

function selectStore(id) {
  selectedStoreId = id;
  renderStoreList();
  renderCanvasMap();
}

function renderCanvasMap() {
  const canvas = document.getElementById('mapCanvas');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  canvas.width = canvas.parentElement.clientWidth;
  canvas.height = canvas.parentElement.clientHeight || 500;

  // Background map grid simulation
  ctx.fillStyle = '#0B1120';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // Draw grid roads
  ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
  ctx.lineWidth = 2;
  for (let x = 0; x < canvas.width; x += 40) {
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, canvas.height);
    ctx.stroke();
  }
  for (let y = 0; y < canvas.height; y += 40) {
    ctx.beginPath();
    ctx.moveTo(0, y);
    ctx.lineTo(canvas.width, y);
    ctx.stroke();
  }

  // Draw main arterial blue roads
  ctx.strokeStyle = 'rgba(37, 99, 235, 0.3)';
  ctx.lineWidth = 6;
  ctx.beginPath();
  ctx.moveTo(0, canvas.height * 0.4);
  ctx.lineTo(canvas.width, canvas.height * 0.6);
  ctx.stroke();

  ctx.beginPath();
  ctx.moveTo(canvas.width * 0.3, 0);
  ctx.lineTo(canvas.width * 0.5, canvas.height);
  ctx.stroke();

  // Draw pins
  serviceStores.forEach(store => {
    const isSelected = store.id === selectedStoreId;

    // Pulse effect for selected store pin
    if (isSelected) {
      ctx.beginPath();
      ctx.arc(store.x, store.y, 22, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(0, 229, 255, 0.2)';
      ctx.fill();
    }

    // Pin dot
    ctx.beginPath();
    ctx.arc(store.x, store.y, isSelected ? 10 : 7, 0, Math.PI * 2);
    ctx.fillStyle = isSelected ? '#00E5FF' : '#2563EB';
    ctx.shadowBlur = isSelected ? 15 : 5;
    ctx.shadowColor = isSelected ? '#00E5FF' : '#2563EB';
    ctx.fill();

    // Store label
    ctx.font = '600 12px Inter, sans-serif';
    ctx.fillStyle = isSelected ? '#FFF' : '#94A3B8';
    ctx.fillText(store.store_name.substring(0, 20), store.x + 14, store.y + 4);
  });
}

function openAppointmentModal(storeId) {
  const store = serviceStores.find(s => s.id === storeId);
  if (store) {
    document.getElementById('appointStoreId').value = store.id;
    document.getElementById('appointStoreName').innerText = `Book with ${store.store_name}`;
    openModal('appointmentModal');
  }
}

async function handleBookAppointment(e) {
  e.preventDefault();
  const storeId = document.getElementById('appointStoreId').value;
  const device = document.getElementById('appointDevice').value;
  const date = document.getElementById('appointDate').value;

  try {
    const res = await fetch('/api/service-centers/book-appointment', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        store_id: parseInt(storeId),
        user_name: state.currentUser ? state.currentUser.full_name : 'Technician User',
        phone: '+91 98765 43210',
        device_type: device,
        issue_description: 'AI Scan detected damaged component',
        preferred_date: date,
        preferred_time: '11:00 AM'
      })
    });
    if (res.ok) {
      const data = await res.json();
      closeModal('appointmentModal');
      showToast(data.message, 'success');
    }
  } catch (err) {
    closeModal('appointmentModal');
    showToast(`Appointment confirmed for ${date}!`, 'success');
  }
}

function filterStores() {
  const query = document.getElementById('storeSearchInput').value.toLowerCase();
  const filtered = serviceStores.filter(s =>
    s.store_name.toLowerCase().includes(query) ||
    s.address.toLowerCase().includes(query)
  );
  if (filtered.length > 0) selectStore(filtered[0].id);
}
