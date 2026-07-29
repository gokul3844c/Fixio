/* ==========================================================================
   FixAI Assistant Chat & Web Speech API Voice Interface
   ========================================================================== */

let activeSessionId = "session_" + Math.random().toString(36).substring(2, 9);
let isRecording = false;
let recognition = null;

// Initialize Speech Recognition if supported
if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  recognition = new SpeechRecognition();
  recognition.continuous = false;
  recognition.interimResults = false;
  recognition.lang = 'en-US';

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    document.getElementById('chatInput').value = transcript;
    toggleVoiceInput(); // stop recording state
    sendChatMessage(); // auto send spoken prompt
  };

  recognition.onerror = (event) => {
    showToast('Voice recognition error: ' + event.error, 'warning');
    toggleVoiceInput();
  };
}

function toggleVoiceInput() {
  const micBtn = document.getElementById('voiceMicBtn');
  if (!recognition) {
    showToast('Speech recognition not supported in current browser engine', 'warning');
    return;
  }

  if (!isRecording) {
    isRecording = true;
    micBtn.classList.add('recording');
    recognition.start();
    showToast('Listening... Speak your technical question.', 'info');
  } else {
    isRecording = false;
    micBtn.classList.remove('recording');
    recognition.stop();
  }
}

function handleChatKeyDown(e) {
  if (e.key === 'Enter') {
    sendChatMessage();
  }
}

function sendSuggestedQuery(text) {
  document.getElementById('chatInput').value = text;
  sendChatMessage();
}

async function sendChatMessage() {
  const input = document.getElementById('chatInput');
  const query = input.value.trim();
  if (!query) return;

  const messagesContainer = document.getElementById('chatMessages');

  // Render User Message Bubble
  const userBubble = document.createElement('div');
  userBubble.className = 'chat-bubble user';
  userBubble.innerText = query;
  messagesContainer.appendChild(userBubble);

  input.value = '';
  messagesContainer.scrollTop = messagesContainer.scrollHeight;

  // Render Loading indicator
  const loadingBubble = document.createElement('div');
  loadingBubble.className = 'chat-bubble ai';
  loadingBubble.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Analyzing circuit schematics & datasheets...';
  messagesContainer.appendChild(loadingBubble);
  messagesContainer.scrollTop = messagesContainer.scrollHeight;

  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        session_id: activeSessionId,
        message: query
      })
    });

    if (response.ok) {
      const data = await response.json();
      loadingBubble.innerHTML = formatMarkdownResponse(data.reply);

      // Optional text to speech output
      speakResponse(data.reply);
    } else {
      throw new Error('Chat API returned error');
    }
  } catch (err) {
    // Local fallback responder
    setTimeout(() => {
      loadingBubble.innerHTML = formatMarkdownResponse(
        `**FixAI Assistant Diagnostic Response for "${query}":**\n\n` +
        "1. Check the standby voltage rail with a digital multimeter DC range.\n" +
        "2. If an LM7805 regulator or MOSFET feels hot, desolder and check for short circuits.\n" +
        "3. Replace dried or bulging electrolytic capacitors with low-ESR equivalents."
      );
    }, 600);
  }

  messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function formatMarkdownResponse(text) {
  return text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/\n/g, '<br>');
}

function speakResponse(text) {
  if ('speechSynthesis' in window) {
    const cleanText = text.replace(/<[^>]*>?/gm, '').replace(/\*/g, '');
    const utterance = new SpeechSynthesisUtterance(cleanText.substring(0, 200));
    utterance.rate = 1.0;
    window.speechSynthesis.speak(utterance);
  }
}

function startNewChatSession() {
  activeSessionId = "session_" + Math.random().toString(36).substring(2, 9);
  const container = document.getElementById('chatMessages');
  container.innerHTML = `
    <div class="chat-bubble ai">
      New session started. Ask me anything about electronics troubleshooting, IC datasheets, or repair guidance!
    </div>
  `;
  showToast('New chat session initialized', 'info');
}
