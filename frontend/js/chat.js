/* ==========================================================================
   NeoShop — AI Assistant Chat & Voice Logic (chat.js)
   ========================================================================== */

'use strict';

let activeSessionId = "session_" + Math.random().toString(36).substring(2, 9);
let isRecording = false;
let recognition = null;

if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  recognition = new SpeechRecognition();
  recognition.continuous = false;
  recognition.interimResults = false;
  recognition.lang = 'en-US';

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    const input = document.getElementById('chatInput');
    if (input) input.value = transcript;
    toggleVoiceInput();
    sendChatMessage();
  };

  recognition.onerror = (event) => {
    showToast('Voice error: ' + event.error, 'warning');
    toggleVoiceInput();
  };
}

function toggleVoiceInput() {
  const micBtn = document.getElementById('voiceMicBtn');
  if (!recognition) {
    showToast('Speech recognition not supported in browser.', 'warning');
    return;
  }

  if (!isRecording) {
    isRecording = true;
    if (micBtn) micBtn.classList.add('recording');
    recognition.start();
    showToast('<i class="fa-solid fa-microphone"></i> Listening… Speak your question.', 'info');
  } else {
    isRecording = false;
    if (micBtn) micBtn.classList.remove('recording');
    recognition.stop();
  }
}

function handleChatKeyDown(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendChatMessage();
  }
}

function sendSuggestedQuery(text) {
  const input = document.getElementById('chatInput');
  if (input) input.value = text;
  sendChatMessage();
}

async function sendChatMessage() {
  const input = document.getElementById('chatInput');
  if (!input) return;
  const query = input.value.trim();
  if (!query) return;

  const messagesContainer = document.getElementById('chatMessages');
  if (!messagesContainer) return;

  // Render User Message
  const userBubble = document.createElement('div');
  userBubble.className = 'chat-bubble user';
  userBubble.innerHTML = `<div style="font-weight:600; font-size:0.75rem; color:var(--color-primary); margin-bottom:0.25rem;">You</div>${escapeHtml(query)}`;
  messagesContainer.appendChild(userBubble);

  input.value = '';
  messagesContainer.scrollTop = messagesContainer.scrollHeight;

  // Render AI Loading Bubble
  const loadingBubble = document.createElement('div');
  loadingBubble.className = 'chat-bubble ai';
  loadingBubble.innerHTML = `
    <div style="font-weight:600; font-size:0.75rem; color:var(--color-primary); margin-bottom:0.25rem;">NeoAI Assistant</div>
    <div style="display:flex; align-items:center; gap:0.5rem; color:var(--color-text-faint);">
      <i class="fa-solid fa-microchip fa-spin" style="color:var(--color-primary);"></i>
      Analyzing component schematics & datasheets…
    </div>
  `;
  messagesContainer.appendChild(loadingBubble);
  messagesContainer.scrollTop = messagesContainer.scrollHeight;

  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ session_id: activeSessionId, message: query })
    });

    if (response.ok) {
      const data = await response.json();
      loadingBubble.innerHTML = `
        <div style="font-weight:600; font-size:0.75rem; color:var(--color-primary); margin-bottom:0.25rem;">NeoAI Assistant</div>
        <div>${formatMarkdownResponse(data.reply)}</div>
      `;
    } else { throw new Error(); }
  } catch {
    // Intelligent local response fallback
    setTimeout(() => {
      loadingBubble.innerHTML = `
        <div style="font-weight:600; font-size:0.75rem; color:var(--color-primary); margin-bottom:0.25rem;">NeoAI Assistant</div>
        <div>${formatMarkdownResponse(getLocalAiResponse(query))}</div>
      `;
      messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }, 700);
  }
}

function getLocalAiResponse(query) {
  const q = query.toLowerCase();
  if (q.includes('crack') || q.includes('wall') || q.includes('plaster')) {
    return "**Wall Crack Repair Guide:**\n- **Assessment:** Measure crack width. Hairline cracks (<2mm) can be sealed with polymer acrylic filler. Structural cracks (>5mm) require structural epoxy injection.\n- **Preparation:** V-groove the crack edges with a chisel and clean all dust with a wire brush.\n- **Application:** Apply flexible polyurethane sealant, smooth with a putty knife, and finish with exterior paint.";
  }
  if (q.includes('water') || q.includes('damp') || q.includes('leak') || q.includes('seepage')) {
    return "**Water Dampness & Seepage Control:**\n- **Symptoms:** Flaking paint, efflorescence (white salt deposits), mold growth.\n- **Testing:** Check external plumbing joints or roof drainage points above the damp zone.\n- **Remediation:** Seal external water entry points with crystalline waterproofing coat, then apply anti-efflorescence primer internally.";
  }
  if (q.includes('roof') || q.includes('tile') || q.includes('leakage')) {
    return "**Roof Tile & Leakage Repair:**\n- **Inspection:** Look for cracked terracotta/concrete tiles or displaced flashing.\n- **Fix:** Replace damaged tiles or seal overlaps with bituminous waterproofing tape and elastomer sealant.";
  }
  return `**Fixio Assistant Advice for "${query}":**\n\n1. **Visual Damage Assessment:** Capture clear, high-resolution photos of the damaged area.\n2. **AI Scan Tool:** Use our [AI Property Scanner](#) to auto-detect damage severity and estimated repair cost.\n3. **Nearby Experts:** Check our [Service Centers Map](#) to hire top-rated local structural engineers and repair technicians.`;
}

function formatMarkdownResponse(text) {
  return text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/\n/g, '<br>');
}

function escapeHtml(str) {
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function startNewChatSession() {
  activeSessionId = "session_" + Math.random().toString(36).substring(2, 9);
  const container = document.getElementById('chatMessages');
  if (container) {
    container.innerHTML = `
      <div class="chat-bubble ai">
        <div style="font-weight:600; font-size:0.75rem; color:var(--color-primary); margin-bottom:0.25rem;">NeoAI Assistant</div>
        New diagnostic session started! Ask me about IC datasheets, pinouts, component replacements, or repair procedures.
      </div>
    `;
  }
  showToast('<i class="fa-solid fa-rotate-left"></i> New chat session started', 'info');
}

window.toggleVoiceInput   = toggleVoiceInput;
window.handleChatKeyDown  = handleChatKeyDown;
window.sendSuggestedQuery = sendSuggestedQuery;
window.sendChatMessage    = sendChatMessage;
window.startNewChatSession= startNewChatSession;
