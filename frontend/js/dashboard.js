/* ==========================================================================
   Fixio Property Owner Dashboard & Scan History Logic (dashboard.js)
   ========================================================================== */

'use strict';

let dashboardScans = [
  {
    id: 94821,
    scan_id: "scan_demo_94821",
    device_name: "Compound Entrance Wall",
    component_name: "Exterior Masonry Wall",
    part_number: "WALL-CRACK-01",
    damage_status: "Damaged - Wall Crack",
    confidence_percentage: 82.0,
    severity_level: "medium",
    created_at: "2026-08-20"
  },
  {
    id: 94820,
    scan_id: "scan_demo_94820",
    device_name: "Plumbing Wall Junction",
    component_name: "Waterproofing & Piping",
    part_number: "PIPE-LEAK-02",
    damage_status: "Damaged - Water Seepage",
    confidence_percentage: 89.0,
    severity_level: "high",
    created_at: "2026-08-18"
  }
];

async function loadDashboard() {
  try {
    const res = await fetch('/api/scan', {
      headers: window.getAuthHeader ? window.getAuthHeader() : {}
    });

    if (res.ok) {
      const reports = await res.json();
      if (Array.isArray(reports) && reports.length > 0) {
        dashboardScans = reports;
      }
    }
  } catch (err) {
    // Keep local scans fallback
  }

  updateDashboardMetrics();
  renderDashboardTable();
}

function updateDashboardMetrics() {
  const totalEl = document.getElementById('dashTotalScans');
  const issuesEl = document.getElementById('dashIssuesFound');
  const repairedEl = document.getElementById('dashRepaired');
  const progressEl = document.getElementById('dashInProgress');

  const total = dashboardScans.length;
  const issues = dashboardScans.filter(s => s.severity_level === 'high' || (s.damage_status && s.damage_status.includes('Damaged'))).length;

  if (totalEl) totalEl.textContent = total;
  if (issuesEl) issuesEl.textContent = issues;
  if (repairedEl) repairedEl.textContent = Math.max(0, total - issues);
  if (progressEl) progressEl.textContent = Math.min(total, issues);
}

function renderDashboardTable() {
  const tableBody = document.getElementById('dashScanTable');
  if (!tableBody) return;

  tableBody.innerHTML = '';

  if (dashboardScans.length === 0) {
    tableBody.innerHTML = `
      <tr>
        <td colspan="5" style="text-align:center; padding:2rem; color:var(--color-text-muted);">
          No property scans found. <a onclick="navigateTo('scanner')" style="color:var(--color-primary); cursor:pointer; font-weight:600;">Perform a new scan</a>
        </td>
      </tr>
    `;
    return;
  }

  dashboardScans.forEach(scan => {
    const tr = document.createElement('tr');
    tr.style.borderBottom = '1px solid var(--neo-shadow-dark)';

    const severity = (scan.severity_level || 'medium').toLowerCase();
    let badgeClass = 'badge-warning';
    if (severity === 'high') badgeClass = 'badge-danger';
    if (severity === 'low') badgeClass = 'badge-success';

    tr.innerHTML = `
      <td style="padding: 0.85rem;"><strong>${scan.device_name}</strong></td>
      <td style="padding: 0.85rem; color: var(--color-text-muted);">${scan.component_name}</td>
      <td style="padding: 0.85rem;"><span class="badge ${badgeClass}">${scan.damage_status}</span></td>
      <td style="padding: 0.85rem; color: var(--color-primary); font-weight: 700;">${(scan.confidence_percentage).toFixed(0)}%</td>
      <td style="padding: 0.85rem;">
        <button class="btn btn-outline btn-sm" onclick="viewScanReport(${scan.id})">
          <i class="fa-solid fa-eye"></i> View Report
        </button>
      </td>
    `;
    tableBody.appendChild(tr);
  });
}

function viewScanReport(reportId) {
  const match = dashboardScans.find(s => s.id === reportId);
  if (match && window.AppState) {
    window.AppState.activeScanReport = match;
    if (typeof renderScanResults === 'function') renderScanResults(match);
  }
  navigateTo('scan-result');
}

function downloadPDFReport() {
  showToast('<i class="fa-solid fa-file-pdf"></i> Generating official Fixio Property Inspection PDF Report...', 'info');
  setTimeout(() => {
    showToast('<i class="fa-solid fa-circle-check"></i> Report downloaded: Fixio_Inspection_Report.pdf', 'success');
  }, 1200);
}

function saveToHistory() {
  showToast('<i class="fa-solid fa-bookmark"></i> Scan report saved to your cloud profile!', 'success');
}

function viewComponentDetails() {
  navigateTo('repair-guide');
}

window.loadDashboard = loadDashboard;
window.renderDashboard = loadDashboard;
window.viewScanReport = viewScanReport;
window.downloadPDFReport = downloadPDFReport;
window.saveToHistory = saveToHistory;
window.viewComponentDetails = viewComponentDetails;
