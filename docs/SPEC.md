# SPEC.md - Especificação Técnica do J.O.S.E

**Versão:** 0.1  
**Data:** 2026-02-11

---

## 🎯 Objetivo

J.O.S.E (Jovem Orientador de Soluções Educacionais) é um assistente virtual interativo desenvolvido para o **Espaço Maker de Robótica Pedagógica do NIED/Unicamp**.

**Missão:** Auxiliar visitantes e estudantes com informações sobre o laboratório, projetos, equipamentos e atividades educacionais através de interação por voz e interface web.

---

## 📋 Casos de Uso (Laboratório)

### UC1: Visitante Pergunta Sobre o NIED
**Ator:** Visitante do laboratório  
**Fluxo:**
1. Visitante clica em push-to-talk (ou diz "José" se wake-name ativo)
2. Visitante pergunta: "O que é o NIED?"
3. Sistema reconhece voz e busca resposta no knowledge base
4. Sistema responde com voz natural
5. (Opcional) Boca do robô se move sincronizada

**Resultado:** Visitante recebe informação clara sobre o NIED

### UC2: Estudante Pergunta Sobre Equipamento
**Ator:** Estudante do Espaço Maker  
**Fluxo:**
1. Estudante pergunta: "José, como usar a impressora 3D?"
2. Sistema busca instruções no KB
3. Sistema fornece passo a passo por voz
4. Sistema pode exibir informações na tela (modo web)

**Resultado:** Estudante aprende a usar equipamento

### UC3: Aprendizado de Nova Informação
**Ator:** Educador/Administrador  
**Fluxo:**
1. Educador diz: "José, quem é o coordenador do NIED?"
2. Sistema não encontra resposta
3. Sistema pergunta: "Eu não sei. O que devo responder?"
4. Educador fornece resposta
5. Sistema confirma e salva no KB

**Resultado:** KB é expandido com nova informação

### UC4: Acesso Web (Kiosk)
**Ator:** Visitante usando terminal web  
**Fluxo:**
1. Visitante acessa interface web em tablet/kiosk
2. Clica em botão push-to-talk
3. Faz pergunta
4. Recebe resposta em texto + áudio
5. Pode ver fontes e confiança da resposta

**Resultado:** Interação multimodal (voz + texto)

---

## 📊 Requisitos Funcionais

### RF1: Reconhecimento de Voz
- **Descrição:** Sistema deve reconhecer comandos de voz em português brasileiro
- **Tecnologia:** Google Speech Recognition
- **Ativação:**
  - **Push-to-Talk:** Obrigatório no MVP (botão para ativar microfone)
  - **Wake-Name:** Opcional ("josé", pode ser desabilitado em ambientes ruidosos)
- **Ambiente:** Laboratório com ruído moderado

### RF2: Síntese de Voz
- **Descrição:** Sistema deve responder com voz natural
- **Tecnologia:** Microsoft Edge TTS
- **Voz:** Antonio (pt-BR, masculina)
- **Qualidade:** Alta fidelidade, natural

### RF3: Knowledge Base
- **Formato:** JSON estruturado
- **Localização:** `data/kb/nied_kb.json`
- **Conteúdo:** Perguntas/respostas sobre NIED, equipamentos, projetos
- **Versionamento:** Controle de versão do KB

### RF4: Modo Aprendizado
- **Descrição:** Sistema pode aprender novas respostas interativamente
- **Fluxo:** Pergunta desconhecida → Solicita resposta → Confirma → Salva
- **Persistência:** Salvar em `data/kb/nied_kb.json`

### RF5: API REST
- **Tecnologia:** FastAPI
- **Endpoints:**
  - `GET /health` - Status do sistema
  - `POST /ask` - Enviar pergunta, receber resposta
- **Formato de Resposta:**
  ```json
  {
    "answer": "texto da resposta",
    "sources": {
      "kb_entry_id": 42,
      "matched_triggers": ["o que é o nied", "nied"]
    },
    "confidence": 0.95,
    "timestamp": "2026-02-11T12:00:00Z"
  }
  ```

### RF6: Interface Web (Kiosk)
- **Descrição:** Página web para interação em terminais/tablets
- **Modos:**
  - **Texto:** Digitar pergunta e receber resposta (sempre disponível)
  - **Push-to-Talk:** Clicar botão, falar, receber resposta (MVP)
  - **Wake-Name:** Opcional, pode ser desabilitado em ambientes ruidosos
- **Design:** Modo kiosk (fullscreen, sem distrações)

### RF7: Controle de Hardware (Arduino)
- **Descrição:** Sincronizar movimento da boca do robô com fala
- **Protocolo:** Serial (COM3, 9600 baud)
- **Comandos Lógicos:** `OPEN` (abrir boca), `CLOSE` (fechar boca)
- **Implementação:** Pode ser `OPEN`/`CLOSE` (strings) ou `1`/`0` (binário) - adaptável ao firmware
- **Modo Simulação:** Funciona sem Arduino conectado

---

## 🔧 Requisitos Não-Funcionais

### RNF1: Disponibilidade
- Sistema deve funcionar durante horário de operação do laboratório
- Modo degradado:
  - Se API cair, CLI continua funcionando
  - Se STT/TTS falhar (rede), modo texto continua disponível
- Objetivo: 95% uptime durante horário do lab

### RNF2: Performance
- **Modo Texto (API):** Resposta em < 500ms (pergunta conhecida, sem rede externa)
- **Modo Voz (STT + TTS):** Latência total < 3 segundos (dependente de rede Google/Microsoft)
  - STT (Google): ~1-2s
  - Processamento local: < 100ms
  - TTS (Edge): ~1-2s

### RNF3: Escalabilidade
- Suportar múltiplos usuários simultâneos (web)
- KB pode crescer até 1000+ entradas

### RNF4: Manutenibilidade
- Código modular (src/core, src/kb, src/io, src/api)
- Documentação completa em `docs/`
- Testes automatizados (pytest)

### RNF5: Portabilidade
- **Atual:** Windows (desenvolvimento)
- **Futuro:** Raspberry Pi (produção no robô)
- Python 3.8+ compatível

---

## 🚀 Evolução Futura

### Fase 1: MVP (Atual)
- ✅ CLI com voz
- ✅ KB JSON
- ✅ Arduino (opcional)

### Fase 2: Web (Em Desenvolvimento)
- 🔧 API FastAPI
- 🔧 Frontend kiosk
- 🔧 Push-to-talk

### Fase 3: Robô Físico
- 🔮 Deploy em Raspberry Pi
- 🔮 Wake-name contínuo
- 🔮 Visão computacional (reconhecer visitantes)
- 🔮 Movimentos corporais (servo motores)

### Fase 4: IA Avançada
- 🔮 LLM local (respostas generativas)
- 🔮 RAG (Retrieval-Augmented Generation)
- 🔮 Multimodalidade (visão + voz + gestos)

---

## 📝 Glossário

- **KB:** Knowledge Base (base de conhecimento)
- **STT:** Speech-to-Text (reconhecimento de voz)
- **TTS:** Text-to-Speech (síntese de voz)
- **Wake Word:** Palavra de ativação ("josé")
- **Push-to-Talk:** Apertar botão para falar
- **Kiosk:** Terminal de autoatendimento
- **RAG:** Retrieval-Augmented Generation

---

**Desenvolvido em parceria: Amado Maker × NIED/Unicamp**
