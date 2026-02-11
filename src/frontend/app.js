const API_URL = "http://localhost:8000";

const chatHistory = document.getElementById('chat-history');
const questionInput = document.getElementById('question-input');
const askBtn = document.getElementById('ask-btn');

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

questionInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        askQuestion();
    }
});

// Foco inicial
window.onload = () => {
    questionInput.focus();
};
