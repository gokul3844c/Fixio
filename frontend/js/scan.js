/* ==========================================================================
   Fixio — Electronic Component Identification & Repair Assistant Scanner (scan.js)
   ========================================================================== */

'use strict';

let selectedFile = null;
let currentScanMode = 'datasheet'; // Always default to electronic component scanner mode
const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/webp', 'image/bmp'];
const MAX_SIZE_BYTES = 10 * 1024 * 1024; // 10MB

function setScanMode(mode) {
  currentScanMode = 'datasheet';
  const propBtn = document.getElementById('modePropertyBtn');
  const dsBtn   = document.getElementById('modeDatasheetBtn');
  const manualSec = document.getElementById('manualSearchSection');
  const mainTitle = document.getElementById('scannerMainTitle');
  const mainSub   = document.getElementById('scannerMainSubtitle');
  const dzTitle   = document.getElementById('dropzoneTitle');
  const dzIcon    = document.getElementById('dropzoneIcon');

  if (propBtn)   { propBtn.style.display = 'none'; }
  if (dsBtn)     { dsBtn.className   = 'btn btn-primary'; }
  if (manualSec) manualSec.style.display = 'block';
  if (mainTitle) mainTitle.textContent = 'Electronic Component Scanner';
  if (mainSub)   mainSub.textContent = 'Upload a photo of an electronic component or motherboard, or search by part number manually below.';
  if (dzTitle)   dzTitle.textContent = 'Drag & Drop Electronic Component Image Here';
  if (dzIcon)    dzIcon.innerHTML = '<i class="fa-solid fa-microchip"></i>';
}

function triggerFileInput() {
  const el = document.getElementById('fileInput');
  if (el) el.click();
}

function handleFileSelect(e) {
  const file = e.target.files[0];
  if (file) {
    validateAndPreviewFile(file);
  }
}

function validateAndPreviewFile(file) {
  if (!ALLOWED_TYPES.includes(file.type)) {
    showToast(`<i class="fa-solid fa-circle-xmark"></i> Unsupported file format. Please upload JPG, PNG, WEBP, or BMP images.`, 'danger');
    return;
  }

  if (file.size > MAX_SIZE_BYTES) {
    showToast(`<i class="fa-solid fa-circle-xmark"></i> File size exceeds 10MB limit. Please select a smaller image.`, 'danger');
    return;
  }

  selectedFile = file;
  showImagePreview(file);
}

// Drag & drop initialization
document.addEventListener('DOMContentLoaded', () => {
  setScanMode('datasheet');
  const dropzone = document.getElementById('dropzone');
  if (!dropzone) return;

  ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(evtName => {
    dropzone.addEventListener(evtName, (e) => {
      e.preventDefault();
      e.stopPropagation();
    }, false);
  });

  ['dragenter', 'dragover'].forEach(evtName => {
    dropzone.addEventListener(() => dropzone.classList.add('dragover'), false);
  });

  ['dragleave', 'drop'].forEach(evtName => {
    dropzone.addEventListener(() => dropzone.classList.remove('dragover'), false);
  });

  dropzone.addEventListener('drop', (e) => {
    const dt = e.dataTransfer;
    const file = dt ? dt.files[0] : null;
    if (file) {
      validateAndPreviewFile(file);
    }
  });
});

function showImagePreview(file) {
  const previewArea  = document.getElementById('scanPreviewArea');
  const previewImage = document.getElementById('previewImage');
  if (previewArea && previewImage) {
    previewImage.src = URL.createObjectURL(file);
    previewArea.style.display = 'block';
    showToast('<i class="fa-solid fa-microchip"></i> Component image loaded! Click <strong>"Start Analysis"</strong> to proceed.', 'info');
  }
}

async function searchPartNumberManual() {
  const inputEl = document.getElementById('manualPartInput');
  const partNum = inputEl ? inputEl.value.trim() : '';

  if (!partNum) {
    showToast('<i class="fa-solid fa-circle-exclamation"></i> Please enter a part number to search.', 'warning');
    return;
  }

  showToast(`<i class="fa-solid fa-spinner fa-spin"></i> Searching component database for <strong>${partNum}</strong>...`, 'info');

  try {
    const response = await fetch(`/api/components/search?part_number=${encodeURIComponent(partNum)}`, {
      headers: window.getAuthHeader ? window.getAuthHeader() : {}
    });

    if (response.ok) {
      const data = await response.json();
      renderDatasheetSearchResult(data, partNum);
      if (window.navigateTo) navigateTo('scan-result');
    } else {
      throw new Error('Datasheet search API error');
    }
  } catch (err) {
    showToast(`<i class="fa-solid fa-circle-xmark"></i> Failed to query component API. Please check part number.`, 'danger');
  }
}

async function executeScanProcess() {
  const previewArea = document.getElementById('scanPreviewArea');
  const laserBeam   = document.getElementById('laserBeam');
  const progressMsg = document.getElementById('scanProgressMsg');
  const scanBtn     = document.getElementById('startScanBtn');

  if (!selectedFile) {
    showToast('<i class="fa-solid fa-triangle-exclamation"></i> Please select an electronic component image first.', 'warning');
    triggerFileInput();
    return;
  }

  if (previewArea) previewArea.style.display = 'block';
  if (laserBeam)   laserBeam.style.display   = 'block';
  if (scanBtn)     scanBtn.disabled = true;
  if (progressMsg) progressMsg.textContent  = 'Analyzing electronic component marking via OpenCV & Vision OCR...';

  const formData = new FormData();
  formData.append('file', selectedFile);
  formData.append('device_name', 'Electronic Component');
  formData.append('mode', 'datasheet');

  try {
    const response = await fetch('/api/scan', {
      method: 'POST',
      headers: window.getAuthHeader ? window.getAuthHeader() : {},
      body: formData
    });

    if (response.ok) {
      const result = await response.json();
      if (window.AppState) AppState.activeScanReport = result;

      setTimeout(() => {
        if (laserBeam) laserBeam.style.display = 'none';
        if (scanBtn)   scanBtn.disabled = false;
        renderScanResults(result);
        if (window.navigateTo) navigateTo('scan-result');
        if (result.success && result.status === 'confirmed') {
          showToast(`<i class="fa-solid fa-microchip"></i> Component Identified: <strong>${result.identification.part_number}</strong>`, 'success');
        } else if (result.status === 'possible') {
          showToast('<i class="fa-solid fa-circle-question"></i> Component Detected (Marking Unconfirmed)', 'warning');
        } else {
          showToast('<i class="fa-solid fa-circle-xmark"></i> Unable to identify component marking.', 'danger');
        }
      }, 1000);
    } else {
      const err = await response.json();
      throw new Error(err.detail || 'Scan request failed');
    }
  } catch (err) {
    if (laserBeam) laserBeam.style.display = 'none';
    if (scanBtn)   scanBtn.disabled = false;
    showToast(`<i class="fa-solid fa-triangle-exclamation"></i> Component analysis failed: ${err.message}`, 'danger');
    renderScanResults({
      success: false,
      status: "analysis_failed",
      message: "Unable to identify the component from this image.",
      ocr_text: [],
      components: []
    });
    if (window.navigateTo) navigateTo('scan-result');
  }
}

function renderDatasheetSearchResult(data, searchedPart) {
  const result = {
    success: data.found,
    status: data.found ? "confirmed" : "analysis_failed",
    image_url: data.original_image_url || null,
    identification: {
      status: data.found ? "confirmed" : "unknown",
      part_number: data.part_number || searchedPart,
      component_type: data.category || "Electronic Component",
      manufacturer: data.manufacturer || "Semiconductor Manufacturer",
      confidence: null
    },
    ocr: {
      raw_text: [searchedPart],
      cleaned_text: searchedPart
    },
    component_data: {
      name: data.name || (data.found ? `Part #${data.part_number}` : `Part #${searchedPart}`),
      part_number: data.part_number || searchedPart,
      manufacturer: data.manufacturer || "Semiconductor Manufacturer",
      category: data.category || "Electronic Component",
      purpose: data.message || `Manual search for part ${searchedPart}`,
      specifications: data.specifications || {},
      datasheet_url: data.datasheet_url
    },
    damage_analysis: {
      status: "not_available",
      findings: []
    },
    recommendations: []
  };

  if (window.AppState) AppState.activeScanReport = result;
  renderScanResults(result);
}

function renderScanResults(result) {
  const setTxt = (id, txt) => {
    const el = document.getElementById(id);
    if (el) el.textContent = txt;
  };

  // 1. Display ACTUAL uploaded image with cache-busting timestamp
  const resultImage = document.getElementById('resultImage');
  if (resultImage) {
    let imgUrl = result.image_url;
    if (!imgUrl && selectedFile) {
      imgUrl = URL.createObjectURL(selectedFile);
    }
    if (imgUrl) {
      const cacheBust = imgUrl.includes('?') ? `&t=${Date.now()}` : `?t=${Date.now()}`;
      resultImage.src = imgUrl + (imgUrl.startsWith('blob:') ? '' : cacheBust);
    }
  }

  const ident = result.identification || {};
  const compData = result.component_data || {};
  const ocrData = result.ocr || {};
  const status = result.status || (result.success ? "confirmed" : "analysis_failed");

  // Title and breadcrumb updates
  setTxt('resultDeviceName', compData.name || (ident.part_number ? `Component Part #${ident.part_number}` : 'Electronic Component'));
  setTxt('resultComponentName', ident.part_number ? `Part #: ${ident.part_number}` : 'Component Marking Unreadable');
  setTxt('resultPartNumber', `Scan ID: ${result.scan_id || 'N/A'}`);
  setTxt('resultConfidence', ident.part_number ? 'Identified' : 'Unconfirmed');
  setTxt('resultSeverity', 'INFO');
  setTxt('resultRepairCost', 'N/A');
  setTxt('resultRepairTime', 'N/A');
  setTxt('resultDisclaimer', "Component specifications retrieved from component database. Verify pinouts before soldering.");

  // Electronics Vision Engine Label
  const engineEl = document.getElementById('resultEngineName');
  if (engineEl) engineEl.textContent = 'Fixio Electronics Vision';

  // Status Badge
  const statusBadge = document.getElementById('resultDamageStatus');
  if (statusBadge) {
    if (status === 'confirmed') {
      statusBadge.innerHTML = `<i class="fa-solid fa-microchip"></i> CONFIRMED: ${ident.part_number}`;
      statusBadge.className = 'badge badge-success';
    } else if (status === 'possible') {
      statusBadge.innerHTML = `<i class="fa-solid fa-circle-question"></i> POSSIBLE: Marking Unconfirmed`;
      statusBadge.className = 'badge badge-warning';
    } else {
      statusBadge.innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i> UNKNOWN: Identification Failed`;
      statusBadge.className = 'badge badge-danger';
    }
  }

  // Content Area
  const issuesContainer = document.getElementById('resultIssuesList');
  if (!issuesContainer) return;

  if (!result.success || status === 'analysis_failed') {
    issuesContainer.innerHTML = `
      <div class="glass-card" style="padding:1.75rem; border-left:4px solid #EF4444; background:rgba(239,68,68,0.05);">
        <div style="display:flex; align-items:flex-start; gap:1rem;">
          <i class="fa-solid fa-circle-xmark" style="font-size:2.2rem; color:#EF4444; margin-top:0.2rem;"></i>
          <div>
            <h3 style="font-size:1.2rem; color:#DC2626; margin:0 0 0.5rem 0;">Unable to Identify Component</h3>
            <p style="font-size:0.92rem; color:var(--color-text-muted); margin:0; line-height:1.5;">
              ${result.message || 'No visible part number or supported electronic component marking could be detected from this image. Please upload a clearer photo or enter the part number manually.'}
            </p>
            <div style="margin-top:1.25rem; display:flex; gap:0.75rem; flex-wrap:wrap;">
              <button class="btn btn-primary" onclick="if(window.navigateTo){ navigateTo('scanner'); }">
                <i class="fa-solid fa-magnifying-glass"></i> Use Manual Part Search
              </button>
              <button class="btn btn-secondary" onclick="triggerFileInput()">
                <i class="fa-solid fa-camera"></i> Upload Clearer Photo
              </button>
            </div>
          </div>
        </div>
      </div>
    `;
    return;
  }

  if (status === 'possible') {
    issuesContainer.innerHTML = `
      <div class="glass-card" style="padding:1.75rem; border-left:4px solid #F59E0B; background:rgba(245,158,11,0.05);">
        <div style="display:flex; align-items:flex-start; gap:1rem;">
          <i class="fa-solid fa-circle-question" style="font-size:2.2rem; color:#F59E0B; margin-top:0.2rem;"></i>
          <div>
            <h3 style="font-size:1.2rem; color:#D97706; margin:0 0 0.5rem 0;">Component Marking Unconfirmed</h3>
            <p style="font-size:0.92rem; color:var(--color-text-muted); margin:0 0 0.75rem 0;">
              An electronic component was detected in the photo, but the printed part number could not be validated with high certainty.
            </p>
            ${ocrData.cleaned_text ? `
              <div style="background:rgba(255,255,255,0.1); padding:0.75rem 1rem; border-radius:var(--radius-sm); font-family:monospace; font-size:0.9rem; margin-bottom:1rem;">
                <strong>OCR Extracted Text:</strong> ${ocrData.cleaned_text}
              </div>
            ` : ''}
            <div style="display:flex; gap:0.75rem; flex-wrap:wrap;">
              <button class="btn btn-primary" onclick="if(window.navigateTo){ navigateTo('scanner'); }">
                <i class="fa-solid fa-search"></i> Manual Search
              </button>
              <button class="btn btn-secondary" onclick="triggerFileInput()">
                <i class="fa-solid fa-camera"></i> Upload Better Photo
              </button>
            </div>
          </div>
        </div>
      </div>
    `;
    return;
  }

  // Confirmed identification specs rendering
  const specsObj = compData.specifications || {};
  const specsHtml = Object.entries(specsObj).map(([k, v]) => `
    <div style="padding:0.75rem 1rem; background:rgba(255,255,255,0.05); border-radius:var(--radius-sm); border:1px solid rgba(255,255,255,0.1);">
      <div style="font-size:0.78rem; color:var(--color-text-muted); text-transform:uppercase; letter-spacing:0.05em;">${k}</div>
      <div style="font-size:0.95rem; font-weight:700; color:var(--color-text-main); margin-top:0.2rem;">${v}</div>
    </div>
  `).join('');

  const recs = result.recommendations || [];
  const recsHtml = recs.length ? `
    <div style="margin-top:1.25rem;">
      <h4 style="font-size:0.95rem; color:var(--color-text-main); margin-bottom:0.5rem;"><i class="fa-solid fa-wrench" style="color:var(--color-primary);"></i> Handling & Solder Recommendations</h4>
      <ul style="margin:0 0 0 1.25rem; font-size:0.88rem; color:var(--color-text-muted); line-height:1.6;">
        ${recs.map(r => `<li>${r}</li>`).join('')}
      </ul>
    </div>
  ` : '';

  issuesContainer.innerHTML = `
    <div class="glass-card" style="padding:1.75rem; border-left:4px solid #10B981; margin-bottom:1.5rem;">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem; margin-bottom:1.25rem;">
        <div>
          <span class="badge badge-success" style="margin-bottom:0.5rem;"><i class="fa-solid fa-certificate"></i> Verified Semiconductor Component</span>
          <h2 style="font-size:1.5rem; margin:0.25rem 0;">${compData.part_number || ident.part_number} — ${compData.name}</h2>
          <div style="font-size:0.9rem; color:var(--color-text-muted);">
            <strong>Manufacturer:</strong> ${compData.manufacturer || ident.manufacturer || 'OEM Semiconductor'} &nbsp;|&nbsp; <strong>Category:</strong> ${compData.category || 'Integrated Circuit'}
          </div>
        </div>
        ${compData.datasheet_url ? `
          <a href="${compData.datasheet_url}" target="_blank" class="btn btn-primary btn-lg" style="box-shadow: 0 4px 14px rgba(79,70,229,0.4);">
            <i class="fa-solid fa-file-pdf"></i> View Official Datasheet PDF
          </a>
        ` : ''}
      </div>

      ${compData.purpose ? `
        <div style="margin-bottom:1.25rem; font-size:0.92rem; color:var(--color-text-muted); line-height:1.5; background:rgba(255,255,255,0.03); padding:0.85rem 1.1rem; border-radius:var(--radius-sm);">
          <strong>Description:</strong> ${compData.purpose}
        </div>
      ` : ''}

      <h3 style="font-size:1.05rem; margin:1.25rem 0 0.75rem 0;"><i class="fa-solid fa-sliders" style="color:var(--color-primary);"></i> Component Technical Specifications</h3>
      <div style="display:grid; grid-template-columns:repeat(auto-fill, minmax(200px, 1fr)); gap:0.85rem;">
        ${specsHtml}
      </div>

      ${ocrData.cleaned_text ? `
        <div style="margin-top:1.25rem; font-size:0.82rem; color:var(--color-text-muted);">
          <strong>OCR Raw Output:</strong> <code style="background:rgba(255,255,255,0.1); padding:0.2rem 0.5rem; border-radius:4px;">${ocrData.cleaned_text}</code>
        </div>
      ` : ''}

      ${recsHtml}

      <!-- Damage Analysis Status (Requirement #11) -->
      <div style="margin-top:1.5rem; padding:1rem; background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08); border-radius:var(--radius-sm);">
        <div style="font-size:0.88rem; font-weight:700; color:var(--color-text-muted); margin-bottom:0.25rem;">
          <i class="fa-solid fa-microscope" style="color:var(--color-primary);"></i> Component Damage Analysis
        </div>
        <div style="font-size:0.85rem; color:var(--color-text-muted);">
          Damage Analysis: <strong>Not available</strong> — requires additional thermal or electrical circuit testing.
        </div>
      </div>
    </div>
  `;
}

function openCameraModal() {
  showToast('<i class="fa-solid fa-camera"></i> Camera capture initiated.', 'info');
  triggerFileInput();
}

window.setScanMode           = setScanMode;
window.triggerFileInput       = triggerFileInput;
window.handleFileSelect       = handleFileSelect;
window.executeScanProcess     = executeScanProcess;
window.searchPartNumberManual = searchPartNumberManual;
window.openCameraModal        = openCameraModal;
