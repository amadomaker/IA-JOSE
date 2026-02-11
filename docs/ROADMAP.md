# ROADMAP.md - Plano de Entregas J.O.S.E

**Versão:** 0.1  
**Data:** 2026-02-11

---

## 🎯 Visão Geral

Este roadmap define a ordem de implementação das funcionalidades do J.O.S.E, priorizando entregas incrementais e testáveis.

---

## ✅ Milestone 0: Preparação (COMPLETO)

**Status:** ✅ Concluído

### Entregas:
- ✅ Estrutura de diretórios (`src/`, `docs/`, `tests/`, `data/`)
- ✅ Configuração de projeto (`pyproject.toml`, `.gitignore`, `requirements.txt`)
- ✅ Git repository com branches `main` e `dev`
- ✅ README.md atualizado
- ✅ Créditos e parceria Amado Maker × NIED

### Critério de Aceite:
- ✅ Estrutura de pastas criada
- ✅ Git configurado e sincronizado com GitHub

---

## 📝 Etapa 1: Documentação 0.1 (EM ANDAMENTO)

**Status:** 🔧 Em desenvolvimento

### Entregas:
- 🔧 `docs/SPEC.md` - Especificação técnica
- 🔧 `docs/ARCHITECTURE.md` - Arquitetura do sistema
- 🔧 `docs/ROADMAP.md` - Este arquivo
- 🔧 `docs/KB_FORMAT.md` - Formato do knowledge base
- 🔧 `docs/RUNBOOK_WINDOWS.md` - Guia de execução
- 🔧 `docs/SAFETY.md` - Regras de segurança

### Critério de Aceite:
- [ ] Todos os 6 documentos criados
- [ ] Documentos revisados e aprovados
- [ ] Referências cruzadas funcionando

### Próximo Passo:
Após aprovação, iniciar **Etapa 2: API Mínima**

---

## 🚀 Etapa 2: API Mínima

**Status:** ⏳ Aguardando

### Entregas:
- [ ] `src/api/main.py` - Servidor FastAPI
  - [ ] `GET /health` - Status do sistema
  - [ ] `POST /ask` - Endpoint de perguntas
- [ ] `src/kb/loader.py` - Carregar KB de `data/kb/`
- [ ] `src/kb/matcher.py` - Buscar respostas no KB
- [ ] Resposta estruturada: `{answer, sources, confidence}`
- [ ] 1 teste de integração (`tests/integration/test_api.py`)
- [ ] Atualizar `docs/RUNBOOK_WINDOWS.md` com instruções

### Critério de Aceite:
- [ ] `uvicorn src.api.main:app --reload` inicia servidor
- [ ] `GET /health` retorna status 200
- [ ] `POST /ask` retorna resposta válida do KB
- [ ] Teste de integração passa (`pytest tests/integration/`)
- [ ] RUNBOOK tem instruções claras de execução

### Exemplo de Teste:
```powershell
# Iniciar servidor
uvicorn src.api.main:app --reload

# Testar endpoint
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "o que é o NIED?"}'

# Resposta esperada:
{
  "answer": "O NIED é o Núcleo de Informática Aplicada à Educação...",
  "sources": {
    "kb_entry_id": 42,
    "matched_triggers": ["o que é o nied", "nied"]
  },
  "confidence": 0.95
}
```

### Próximo Passo:
Após aprovação, iniciar **Etapa 3**

---

## 🖥️ Etapa 3: Frontend Kiosk

**Status:** ✅ Concluído

### Etapa 3.1: Frontend Básico (Texto)
**Entregas:**
- [ ] `src/frontend/index.html` - Página principal
- [ ] `src/frontend/app.js` - Lógica básica
- [ ] `src/frontend/style.css` - Estilo (modo kiosk)
- [ ] Input texto + botão "Perguntar"
- [ ] Exibir resposta + confiança

**Critério de Aceite 3.1:**
- [ ] Página carrega em `http://localhost:8000/`
- [ ] Digitar pergunta → API responde → Exibe na tela

### Etapa 3.2: Push-to-Talk (Áudio)
**Entregas:**
- [ ] Botão "Segurar para Falar"
- [ ] Captura de microfone no navegador
- [ ] Envio de áudio (ou texto transcrito) para API

**Critério de Aceite 3.2:**
- [ ] Clicar e falar → API responde → Exibe na tela

### Próximo Passo:
Após aprovação, iniciar **Etapa 4: Testes e Qualidade**

---

## 🧪 Etapa 4: Testes e Qualidade

**Status:** ⏳ Aguardando

### Entregas:
- [ ] Testes unitários para `kb/` (`tests/unit/test_kb.py`)
- [ ] Testes unitários para `core/` (`tests/unit/test_core.py`)
- [ ] Testes de integração para API (`tests/integration/test_api.py`)
- [ ] Cobertura de código > 70%
- [ ] Linting (flake8) sem erros
- [ ] Formatação (black) aplicada

### Critério de Aceite:
- [ ] `pytest` passa todos os testes
- [ ] `pytest --cov=src --cov-report=html` mostra > 70%
- [ ] `flake8 src/ tests/` sem erros
- [ ] `black src/ tests/` formatado

### Próximo Passo:
Após aprovação, iniciar **Etapa 5: Deploy Raspberry Pi**

---

## 🤖 Etapa 5: Deploy Raspberry Pi (FUTURO)

**Status:** 🔮 Planejado

### Entregas:
- [ ] Script de instalação para Raspberry Pi
- [ ] Configuração de autostart (systemd)
- [ ] Otimização de performance (CPU/RAM)
- [ ] Teste em hardware real (robô físico)
- [ ] Documentação de deploy

### Critério de Aceite:
- [ ] Sistema inicia automaticamente no boot
- [ ] Responde em < 2 segundos
- [ ] Funciona 24/7 sem travamento

---

## 🔮 Etapa 6: IA Avançada (FUTURO)

**Status:** 🔮 Planejado

### Entregas:
- [ ] Integração com LLM local (Llama, Mistral)
- [ ] RAG (Retrieval-Augmented Generation)
- [ ] Wake-name contínuo (detecção sempre ativa)
- [ ] Visão computacional (reconhecer visitantes)
- [ ] Movimentos corporais (servo motores)

### Critério de Aceite:
- [ ] Respostas generativas funcionam
- [ ] Wake-name detecta "josé" continuamente
- [ ] Robô reconhece rostos

---

## 📊 Resumo de Prioridades

| Etapa | Prioridade | Status |
|-------|-----------|--------|
| **Milestone 0** | Alta | ✅ Completo |
| **Etapa 1: Docs** | Alta | 🔧 Em andamento |
| **Etapa 2: API** | Alta | ⏳ Aguardando |
| **Etapa 3.1: Frontend Txt** | Alta | ✅ Completo |
| **Etapa 3.2: Frontend Talk** | Alta | ✅ Completo |
| **Etapa 4: Testes** | Média | ⏳ Aguardando |
| **Etapa 5: Raspberry** | Média | 🔮 Planejado |
| **Etapa 6: IA Avançada** | Baixa | 🔮 Planejado |

---

## 🎯 Estratégia de Entregas

### Princípios:
1. **Incremental:** Cada etapa adiciona valor
2. **Testável:** Critérios de aceite claros
3. **Revisável:** Pausa após cada etapa para aprovação
4. **Documentado:** Tudo documentado em `docs/`

### Fluxo de Trabalho:
```
1. Implementar etapa
   ↓
2. Testar critérios de aceite
   ↓
3. Commitar em branch dev
   ↓
4. Solicitar revisão
   ↓
5. Aprovado? → Merge para main
   ↓
6. Próxima etapa
```

---

## 📝 Notas

- **Branches:** Trabalhar em `dev`, merge para `main` após aprovação
- **Commits:** Mensagens descritivas (`feat:`, `fix:`, `docs:`)
- **PRs:** Criar PR para cada etapa completa

---

**Desenvolvido em parceria: Amado Maker × NIED/Unicamp**
