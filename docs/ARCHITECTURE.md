# ARCHITECTURE.md - Arquitetura do Sistema J.O.S.E

**Versão:** 0.1  
**Data:** 2026-02-11

---

## 🏗️ Visão Geral

J.O.S.E segue uma arquitetura modular em camadas, separando responsabilidades entre **core** (lógica), **kb** (conhecimento), **io** (entrada/saída), **api** (backend web) e **apps** (interfaces).

```
┌─────────────────────────────────────────────────┐
│                   APPS LAYER                    │
│  ┌──────────────┐  ┌──────────────────────────┐ │
│  │  CLI (main)  │  │  Web Frontend (kiosk)    │ │
│  └──────────────┘  └──────────────────────────┘ │
└─────────────────────────────────────────────────┘
                      ▲
                      │ HTTP/WebSocket
                      ▼
┌─────────────────────────────────────────────────┐
│                   API LAYER                     │
│  ┌──────────────────────────────────────────┐   │
│  │  FastAPI (REST + WebSocket)              │   │
│  │  - GET /health                           │   │
│  │  - POST /ask                             │   │
│  └──────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
                      ▲
                      │
                      ▼
┌─────────────────────────────────────────────────┐
│                  CORE LAYER                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────────┐  │
│  │  Brain   │  │   NLP    │  │   Config     │  │
│  │ (orquest)│  │ (process)│  │  (settings)  │  │
│  └──────────┘  └──────────┘  └──────────────┘  │
└─────────────────────────────────────────────────┘
         ▲                            ▲
         │                            │
         ▼                            ▼
┌──────────────────┐        ┌──────────────────────┐
│    KB LAYER      │        │     IO LAYER         │
│  ┌────────────┐  │        │  ┌────────────────┐  │
│  │  Loader    │  │        │  │  Voice (STT)   │  │
│  │  Matcher   │  │        │  │  Audio (TTS)   │  │
│  │  Learner   │  │        │  │  Serial (HW)   │  │
│  └────────────┘  │        │  └────────────────┘  │
└──────────────────┘        └──────────────────────┘
         ▲
         │
         ▼
┌─────────────────────────────────────────────────┐
│                  DATA LAYER                     │
│  data/cerebro_nied.json                         │
│  logs/telemetry.log                             │
└─────────────────────────────────────────────────┘
```

---

## 📦 Módulos

### `src/core/` - Lógica de Negócio

#### `brain.py`
**Responsabilidade:** Orquestração central do sistema

**Funções principais:**
- `process_question(text: str) -> dict` - Processa pergunta e retorna resposta
- `learn_new_answer(question: str, answer: str)` - Modo aprendizado
- `get_system_status() -> dict` - Status do sistema

**Dependências:** `kb.matcher`, `io.voice`, `io.audio`, `io.serial`

#### `nlp.py`
**Responsabilidade:** Processamento de linguagem natural

**Funções principais:**
- `normalize_text(text: str) -> str` - Normaliza texto (lowercase, remove acentos)
- `extract_intent(text: str) -> str` - Extrai intenção da pergunta
- `calculate_similarity(text1: str, text2: str) -> float` - Similaridade entre textos

#### `config.py`
**Responsabilidade:** Configurações globais

**Variáveis (com env vars e defaults):**
```python
import os

WAKE_WORD = os.getenv("WAKE_WORD", "josé")
KB_PATH = os.getenv("KB_PATH", "data/cerebro_nied.json")
SERIAL_PORT = os.getenv("SERIAL_PORT", "COM3")
SERIAL_BAUD = int(os.getenv("SERIAL_BAUD", "9600"))
TTS_VOICE = os.getenv("TTS_VOICE", "pt-BR-AntonioNeural")
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.7"))
```

**Nota:** Configurações podem ser sobrescritas via variáveis de ambiente.

**Nota sobre Nomes de Arquivos:** Os nomes de arquivos listados acima (`brain.py`, `nlp.py`, `config.py`) são sugestões baseadas nas responsabilidades. A estrutura real pode variar - consulte `src/` para implementação atual.

---

### `src/kb/` - Knowledge Base

#### `loader.py`
**Responsabilidade:** Carregar e salvar KB

**Funções principais:**
- `load_kb(path: str) -> list[dict]` - Carrega KB do JSON
- `save_kb(path: str, kb: list[dict])` - Salva KB no JSON
- `validate_kb(kb: list[dict]) -> bool` - Valida estrutura do KB

#### `matcher.py`
**Responsabilidade:** Buscar respostas no KB

**Funções principais:**
- `find_answer(question: str, kb: list[dict]) -> dict` - Busca resposta
- `calculate_confidence(question: str, triggers: list[str]) -> float` - Calcula confiança
- `get_best_match(question: str, kb: list[dict]) -> dict` - Melhor match

**Retorno:**
```python
{
    "answer": "texto da resposta",
    "sources": {
        "kb_entry_id": 42,
        "matched_triggers": ["o que é o nied", "nied"]
    },
    "confidence": 0.95
}
```

#### `learner.py`
**Responsabilidade:** Aprendizado interativo

**Funções principais:**
- `add_entry(question: str, answer: str, kb: list[dict]) -> list[dict]` - Adiciona entrada
- `suggest_triggers(question: str) -> list[str]` - Sugere gatilhos
- `merge_similar_entries(kb: list[dict]) -> list[dict]` - Mescla entradas similares

---

### `src/io/` - Entrada/Saída

#### `voice.py`
**Responsabilidade:** Reconhecimento de voz (STT)

**Funções principais:**
- `listen() -> str` - Captura áudio e converte para texto
- `detect_wake_word(text: str) -> bool` - Detecta wake word
- `calibrate_microphone()` - Calibra microfone para ruído ambiente

**Tecnologia:** `speech_recognition` (Google STT)

#### `audio.py`
**Responsabilidade:** Síntese de voz (TTS)

**Funções principais:**
- `speak(text: str)` - Converte texto em áudio e reproduz
- `generate_audio_file(text: str, path: str)` - Gera arquivo MP3
- `format_text_for_speech(text: str) -> str` - Formata texto para fala natural

**Tecnologia:** `edge-tts` (Microsoft Edge TTS)

#### `serial_comm.py`
**Responsabilidade:** Comunicação com Arduino

**Funções principais:**
- `connect(port: str, baud: int) -> Serial` - Conecta ao Arduino
- `send_command(cmd: str)` - Envia comando lógico (OPEN/CLOSE)
- `sync_mouth_with_audio(audio_path: str)` - Sincroniza boca com áudio

**Protocolo:**
- **Contrato lógico:** `OPEN` (abrir boca), `CLOSE` (fechar boca)
- **Implementação:** Pode enviar `"OPEN"`/`"CLOSE"` (strings) ou `1`/`0` (binário) dependendo do firmware Arduino
- Timing baseado em sílabas do texto

---

### `src/api/` - Backend Web

#### `main.py`
**Responsabilidade:** Servidor FastAPI

**Endpoints:**

##### `GET /health`
**Descrição:** Status do sistema

**Resposta:**
```json
{
  "status": "healthy",
  "kb_loaded": true,
  "kb_entries": 42,
  "version": "1.0.0"
}
```

##### `POST /ask`
**Descrição:** Enviar pergunta

**Request:**
```json
{
  "question": "o que é o NIED?"
}
```

**Response:**
```json
{
  "answer": "O NIED é o Núcleo de Informática Aplicada à Educação...",
  "sources": {
    "kb_entry_id": 42,
    "matched_triggers": ["o que é o nied", "nied"]
  },
  "confidence": 0.95,
  "timestamp": "2026-02-11T12:00:00Z"
}
```

#### `websocket.py` ⚠️ **FUTURO / FORA DO MVP**
**Responsabilidade:** WebSocket para streaming de áudio

**Nota:** Não implementar na Etapa 2. Apenas modo texto e push-to-talk via HTTP no MVP.

---

### `src/frontend/` - Interface Web

#### `index.html`
**Descrição:** Página principal (modo kiosk)

**Componentes:**
- Input de texto
- Botão push-to-talk
- Área de resposta
- Indicador de confiança

#### `app.js`
**Descrição:** Lógica do frontend

**Funções:**
- `sendQuestion(text)` - Envia pergunta para API
- `displayAnswer(response)` - Exibe resposta
- `startPushToTalk()` - Inicia gravação de áudio

---

## 🔄 Fluxos Principais

### Fluxo 1: Pergunta via CLI

```
1. Usuário fala: "José, o que é o NIED?"
   ↓
2. voice.listen() captura áudio
   ↓
3. voice.detect_wake_word() verifica "josé"
   ↓
4. nlp.normalize_text() normaliza pergunta
   ↓
5. matcher.find_answer() busca no KB
   ↓
6. brain.process_question() orquestra resposta
   ↓
7. audio.speak() reproduz resposta
   ↓
8. serial_comm.sync_mouth_with_audio() move boca
```

### Fluxo 2: Pergunta via API

```
1. Frontend envia POST /ask {"question": "..."}
   ↓
2. API recebe request
   ↓
3. brain.process_question() processa
   ↓
4. matcher.find_answer() busca no KB
   ↓
5. API retorna JSON {answer, sources, confidence}
   ↓
6. Frontend exibe resposta
```

### Fluxo 3: Modo Aprendizado

```
1. Usuário pergunta algo desconhecido
   ↓
2. matcher.find_answer() retorna confidence < 0.7
   ↓
3. brain.process_question() detecta baixa confiança
   ↓
4. Sistema pergunta: "Eu não sei. O que devo responder?"
   ↓
5. Usuário fornece resposta
   ↓
6. learner.add_entry() adiciona ao KB
   ↓
7. loader.save_kb() persiste no JSON
```

---

## 📊 Diagrama de Dependências

```
apps/main_cli.py
    ├── core/brain.py
    │   ├── kb/matcher.py
    │   │   └── kb/loader.py
    │   ├── io/voice.py
    │   ├── io/audio.py
    │   └── io/serial_comm.py
    └── core/config.py

api/main.py
    ├── core/brain.py
    │   └── (mesmas dependências)
    └── core/config.py

frontend/app.js
    └── api/main.py (HTTP)
```

---

## 🔐 Segurança

- **API:** CORS configurado para domínios permitidos
- **KB:** Validação de entrada antes de salvar
- **Serial:** Timeout para evitar travamento
- **Logs:** Não registrar dados sensíveis

---

**Desenvolvido em parceria: Amado Maker × NIED/Unicamp**
