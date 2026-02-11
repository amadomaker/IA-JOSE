const API_URL = "http://localhost:8000";

const chatHistory = document.getElementById('chat-history');
const questionInput = document.getElementById('question-input');
const askBtn = document.getElementById('ask-btn');
const micBtn = document.getElementById('mic-btn');
const micStatus = document.getElementById('mic-status');
const repeatBtn = document.getElementById('repeat-btn');
const ttsSwitch = document.getElementById('tts-switch');
const toggleStatus = document.querySelector('.toggle-status');

// Estado
let lastAnswer = "";
let isTtsEnabled = true;

// Configuração TTS (Backend)
const audioPlayer = new Audio();

async function speakText(text) {
    if (!isTtsEnabled || !text) return;

    // Parar áudio anterior
    audioPlayer.pause();

    try {
        console.log("Solicitando áudio ao backend...");
        const response = await fetch(`${API_URL}/tts`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: text })
        });

        if (!response.ok) throw new Error("Erro ao gerar áudio");

        const data = await response.json();
        const audioUrl = `${API_URL}${data.audio_url}`;

        console.log("Reproduzindo:", audioUrl);
        // Adicionar timestamp para evitar cache
        audioPlayer.src = `${audioUrl}?t=${new Date().getTime()}`;
        audioPlayer.play();

    } catch (error) {
        console.error("Erro no TTS Backend:", error);
    }
}

// Handler do Toggle TTS
ttsSwitch.addEventListener('change', (e) => {
    isTtsEnabled = e.target.checked;
    toggleStatus.textContent = isTtsEnabled ? "ON" : "OFF";
    if (!isTtsEnabled) audioPlayer.pause();
});

// Handler do Botão Repetir
repeatBtn.addEventListener('click', () => {
    if (lastAnswer) speakText(lastAnswer);
});


// Verificação de suporte a Web Speech API
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
let recognition = null;

if (SpeechRecognition) {
    recognition = new SpeechRecognition();
    recognition.lang = 'pt-BR';
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onstart = () => {
        micBtn.classList.add('listening');
        micStatus.classList.remove('hidden');
        micStatus.textContent = "Ouvindo... 👂";
    };

    recognition.onend = () => {
        micBtn.classList.remove('listening');
        micStatus.classList.add('hidden');
    };

    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        if (transcript) {
            questionInput.value = transcript;
            askQuestion(); // Auto-enviar ao terminar de falar
        }
    };

    recognition.onerror = (event) => {
        console.error("Erro no reconhecimento de voz:", event.error);
        micStatus.textContent = `Erro: ${event.error}`;
        micStatus.classList.remove('hidden');
        setTimeout(() => micStatus.classList.add('hidden'), 3000);
    };
} else {
    micBtn.style.display = 'none'; // Esconder se não suportado
    console.warn("Web Speech API não suportada neste navegador.");
}

// Função para adicionar mensagem ao chat
function addMessage(text, sender) {
    const div = document.createElement('div');
    div.classList.add('message', sender);
    div.textContent = text;
    chatHistory.appendChild(div);
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

// Função para enviar pergunta
async function askQuestion() {
    const question = questionInput.value.trim();
    if (!question) return;

    // Desabilitar UI
    questionInput.value = '';
    questionInput.disabled = true;
    askBtn.disabled = true;

    // Mostrar mensagem do usuário
    addMessage(question, 'user');

    // Mostrar "digitando..." (opcional, por enquanto direto)

    try {
        const response = await fetch(`${API_URL}/ask`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question: question })
        });

        if (!response.ok) {
            throw new Error(`Erro na API: ${response.status}`);
        }

        const data = await response.json();


        // Simular um pequeno delay natural se a resposta for muito rápida
        // setTimeout(() => addMessage(data.answer, 'system'), 300);
        addMessage(data.answer, 'system');

        // Salvar resposta para repetição e falar
        lastAnswer = data.answer;
        repeatBtn.classList.remove('hidden');
        speakText(data.answer);

        // Log de fontes para debug no console
        console.log("Sources:", data.sources);
        console.log("Confidence:", data.confidence);

    } catch (error) {
        console.error("Erro:", error);
        addMessage("Desculpe, ocorreu um erro ao se comunicar com o cérebro.", 'system');
    } finally {
        // Reabilitar UI
        questionInput.disabled = false;
        askBtn.disabled = false;
        questionInput.focus();
    }
}

// Event Listeners
askBtn.addEventListener('click', askQuestion);

if (recognition) {
    // Push-to-Talk logic (Segurar para falar)
    micBtn.addEventListener('mousedown', () => recognition.start());
    micBtn.addEventListener('mouseup', () => recognition.stop());

    // Suporte a toque (Mobile/Tablet)
    micBtn.addEventListener('touchstart', (e) => { e.preventDefault(); recognition.start(); });
    micBtn.addEventListener('touchend', (e) => { e.preventDefault(); recognition.stop(); });
}

questionInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        askQuestion();
    }
});

// Foco inicial
window.onload = () => {
    questionInput.focus();
};
