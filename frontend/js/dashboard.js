/* ==========================================================================
   FixAI Technician Dashboard & Scan History Logic
   ========================================================================== */

let dashboardScans = [
  {
    id: 94821,
    device_name: "Smart TV Power Supply Board Rev 4.1",
    component_name: "Voltage Regulator IC",
    part_number: "LM7805",
    damage_status: "Damaged - Thermal Burn",
    confidence_percentage: 94.5,
    severity_level: "High",
    created_at: "2026-07-29"
  },
  {
    id: 94820,
    device_name: "Laptop Motherboard Rev 2.0",
    component_name: "N-Channel Power MOSFET",
    part_number: "IRFZ44N",
    damage_status: "Damaged - Gate Blowout",
    confidence_percentage: 96.2,
    severity_level: "High",
    created_at: "2026-07-28"
  },
  {
    id: 94819,
    device_name: "Inverter Control Board",
    component_name: "Filter Capacitor 10uF 25V",
    part_number: "ECE-A1EV100",
    damage_status: "Warning - ESR Degradation",
    confidence_percentage: 88.5,
    severity_level: "Medium",
    created_at: "2026-07-27"
  }
];

async function loadDashboard() {
  try {
    const res = await fetch('/api/user/dashboard');
    if (res.ok) {
      const data = await res.json();
      if (data.metrics) {
        document.getElementById('dashTotalScans').innerText = data.metrics.total_scans;
        document.getElementById('dashIssuesFound').innerText = data.metrics.issues_found;
        document.getElementById('dashRepaired').innerText = data.metrics.repaired_count;
        document.getElementById('dashInProgress').innerText = data.metrics.in_progress_count;
      }
      if (data.recent_scans && data.recent_scans.length > 0) {
        dashboardScans = data.recent_scans;
      }
    }
  } catch (err) {
    // Keep local dashboard state
  }

  renderDashboardTable();
}

function renderDashboardTable() {
  const tableBody = document.getElementById('dashScanTable');
  if (!tableBody) return;

  tableBody.innerHTML = '';
  dashboardScans.forEach(scan => {
    const tr = document.createElement('tr');
    tr.style.borderBottom = '1px solid var(--color-border)';

    let badgeClass = 'badge-danger';
    if (scan.damage_status.includes('Warning')) badgeClass = 'badge-warning';
    if (scan.damage_status.includes('Healthy')) badgeClass = 'badge-success';

    tr.innerHTML = `
      <td style="padding: 0.75rem;"><strong>${scan.device_name}</strong></td>
      <td style="padding: 0.75rem; color: var(--color-text-muted);">${scan.component_name} (${scan.part_number})</td>
      <td style="padding: 0.75rem;"><span class="badge ${badgeClass}">${scan.damage_status}</span></td>
      <td style="padding: 0.75rem; color: var(--color-accent); font-weight: 700;">${scan.confidence_percentage}%</td>
      <td style="padding: 0.75rem;">
        <button class="btn btn-outline btn-sm" onclick="viewScanReport(${scan.id})">
          <i class="fa-solid fa-eye"></i> View
        </button>
      </td>
    `;
    tableBody.appendChild(tr);
  });
}

function viewScanReport(reportId) {
  navigateTo('scan-result');
}

function downloadPDFReport() {
  showToast('Generating official FixAI Diagnostics PDF Report...', 'info');
  setTimeout(() => {
    showToast('Report downloaded: FixAI_Diagnostic_Report_94821.pdf', 'success');
  }, 1200);
}

function saveToHistory() {
  showToast('Scan report saved to your cloud profile!', 'success');
}

function viewComponentDetails() {
  navigateTo('component-details');
}
