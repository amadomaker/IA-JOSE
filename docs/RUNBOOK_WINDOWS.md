# RUNBOOK_WINDOWS.md - Guia de Execução (Windows)

**Versão:** 0.1  
**Data:** 2026-02-11

---

## 📊 Status Atual do Projeto

- **✅ Etapa 1 (Docs):** Disponível (este documento)
- **✅ Etapa 2 (API):** Disponível (Instruções abaixo)
- **✅ Etapa 3 (Frontend):** Disponível (Instruções abaixo)

---

## 🎯 Objetivo

Este guia fornece instruções passo a passo para executar o J.O.S.E em ambiente Windows.

---

## 📋 Pré-requisitos

### Software Necessário

- **Python 3.8+** - [Download](https://www.python.org/downloads/)
- **Git** - [Download](https://git-scm.com/downloads)
- **Microfone** funcional
- **Conexão com internet** (para STT e TTS)

### Hardware Opcional

- **Arduino Uno** (para sincronização labial)
  - Porta: COM3 (padrão)
  - Baud rate: 9600

---

## 🚀 Instalação Inicial

### 1. Clonar Repositório

```powershell
# Navegar para diretório desejado
cd C:\

# Clonar repositório
git clone https://github.com/amadomaker/IA-JOSE.git
cd IA-JOSE
```

### 2. Criar Ambiente Virtual

```powershell
# Criar venv
python -m venv venv

# Ativar venv
.\venv\Scripts\Activate.ps1
```

**Nota:** Se encontrar erro de execução de scripts:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3. Instalar Dependências

```powershell
# Com venv ativado
pip install -r requirements.txt
```

**Tempo estimado:** 2-5 minutos

---

## 🚀 Guia Rápido de Testes (Para Usuários Não-Técnicos)

Se você precisa apenas validar se o robô está funcionando, siga estes passos simplificados.

### 1. Iniciar o Sistema
1. Abra o terminal (Prompt de Comando ou PowerShell).
2. Navegue até a pasta do projeto e inicie o servidor com o comando único:
   ```powershell
   .\venv\Scripts\activate; uvicorn src.api.main:app --reload
   ```
3. Aguarde aparecer a mensagem: `Uvicorn running on http://0.0.0.0:8000`

### 2. Abrir a Interface
1. Abra o navegador (Google Chrome ou Microsoft Edge).
2. Clique neste link: [http://localhost:8000/app/index.html](http://localhost:8000/app/index.html)

### 3. Testar Conversa
1. **Verifique o som:** Garanta que suas caixas de som estão ligadas.
2. **Ative a voz:** No canto superior direito da tela, verifique se o botão diz **"Voz: ON"** (verde).
3. **Fale:**
   * Clique e **segure** o botão do microfone (🎙️).
   * Faça **qualquer pergunta** que você quiser (ex: cumprimente o robô, pergunte sobre o projeto, etc).
   * Solte o botão.
4. **Resultado Esperado:**
   * O robô deve escrever o que você falou.
   * O robô deve responder em texto de forma coerente.
   * O robô deve **falar** essa resposta em voz alta.

### 4. Dicas de Uso
* **Explore:** Tente perguntas variadas para ver como o robô reage.
* **Repetição:** Se não ouvir bem, use o botão "Repetir" abaixo da resposta.
* **Voz:** Se a voz estiver desligada, use o botão "Toggle" no canto superior para ativar.

---

## 🎬 Modos de Execução

### Modo 2: API (FastAPI) - DISPONÍVEL
 
**Status:** ✅ Implementado na Etapa 2.
 
**Quando usar:** Para rodar o "cérebro" do sistema.
 
#### Iniciar Servidor
 
```powershell
# Com venv ativado:
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

#### Testar Endpoints (Futuro)

**GET /health**
```powershell
# PowerShell
Invoke-RestMethod -Uri http://localhost:8000/health -Method GET
```

**Exemplo de Resposta:**
```json
{
  "status": "healthy",
  "kb_loaded": true,
  "kb_entries": 42,
  "version": "0.1.0"
}
```

**POST /ask**
```powershell
# PowerShell
$body = @{
    question = "o que é o NIED?"
} | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:8000/ask `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

**Exemplo de Resposta (Contrato):**
```json
{
  "answer": "O NIED é o Núcleo de Informática Aplicada à Educação...",
  "sources": {
    "kb_entry_id": 42,
    "matched_triggers": ["o que é o nied", "nied"]
  },
  "confidence": 0.95
}
```

#### Acessar Documentação Interativa (Futuro)

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

### Modo 3: Frontend Web (Kiosk) - DISPONÍVEL

**Status:** ✅ Implementado na Etapa 3.

**Quando usar:** Para interação visual e por voz via navegador.

#### Iniciar Frontend

```powershell
# 1. Certifique-se que o servidor (Modo 2) está rodando
# 2. Abra o navegador (Chrome/Edge recomendados) em:
start http://localhost:8000/app/index.html
```

#### Funcionalidades
- **Modo Texto:** Digite sua pergunta e tecle Enter ou clique em "Perguntar".
- **Push-to-Talk:** Segure o botão de microfone (🎙️), fale a pergunta e solte para enviar.
  - *Nota:* O navegador pedirá permissão de microfone na primeira vez.

---

## 🧪 Testes

### Executar Testes Unitários

```powershell
# Ativar venv
.\venv\Scripts\Activate.ps1

# Todos os testes
pytest

# Apenas testes unitários
pytest tests/unit/

# Com cobertura
pytest --cov=src --cov-report=html
```

**Saída esperada:**
```
============================= test session starts =============================
collected 15 items

tests/unit/test_kb.py ........                                          [ 53%]
tests/unit/test_core.py .......                                         [100%]

============================== 15 passed in 2.34s ==============================
```

### Executar Testes de Integração

```powershell
# Apenas testes de integração
pytest tests/integration/

# Teste específico
pytest tests/integration/test_api.py::test_health_endpoint
```

---

## 🔧 Troubleshooting

### Problema 1: Microfone Não Funciona

**Sintoma:** `OSError: No Default Input Device Available`

**Solução:**
1. Verificar se microfone está conectado
2. Configurações do Windows → Privacidade → Microfone → Permitir apps
3. Testar microfone em outro app (Gravador de Voz)

### Problema 2: Arduino Não Conecta

**Sintoma:** `Serial port COM3 not found`

**Solução:**
1. Verificar porta no Gerenciador de Dispositivos
2. Atualizar `src/core/config.py`:
   ```python
   SERIAL_PORT = "COM5"  # Trocar para porta correta
   ```
3. Sistema funciona em modo simulação sem Arduino

### Problema 3: Erro ao Ativar venv

**Sintoma:** `cannot be loaded because running scripts is disabled`

**Solução:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Problema 4: Dependências Não Instalam

**Sintoma:** `ERROR: Could not find a version that satisfies the requirement...`

**Solução:**
```powershell
# Atualizar pip
python -m pip install --upgrade pip

# Reinstalar dependências
pip install -r requirements.txt --upgrade
```

### Problema 5: API Não Inicia

**Sintoma:** `ModuleNotFoundError: No module named 'fastapi'`

**Motivo:** FastAPI ainda não foi instalado (será na Etapa 2).

**Solução (Futura):**
```powershell
# Verificar se venv está ativado
.\venv\Scripts\Activate.ps1

# Reinstalar FastAPI (após Etapa 2)
pip install fastapi uvicorn[standard]
```

---

## 📊 Logs e Telemetria

### Localização dos Logs

```
logs/
├── app.log          # Log geral da aplicação
├── api.log          # Log da API
└── kb_changes.log   # Log de mudanças no KB
```

### Visualizar Logs em Tempo Real

```powershell
# PowerShell
Get-Content logs\app.log -Wait -Tail 50
```

### Níveis de Log

- **DEBUG:** Informações detalhadas para debug
- **INFO:** Eventos normais (perguntas, respostas)
- **WARNING:** Situações inesperadas (baixa confiança)
- **ERROR:** Erros que não param o sistema
- **CRITICAL:** Erros críticos que param o sistema

---

## 🔄 Atualização do Sistema

### Atualizar Código

```powershell
# Parar servidor (Ctrl+C)

# Atualizar código
git pull origin dev

# Reinstalar dependências (se necessário)
pip install -r requirements.txt --upgrade

# Reiniciar servidor
uvicorn src.api.main:app --reload
```

### Atualizar Knowledge Base

```powershell
# Editar KB
notepad data\cerebro_nied.json

# Validar JSON
python -m json.tool data\cerebro_nied.json

# Reiniciar sistema para recarregar KB
```

---

## 🚀 Deploy em Produção (Futuro)

### Raspberry Pi

```bash
# Instalar dependências
sudo apt-get update
sudo apt-get install python3-pip

# Clonar repositório
git clone https://github.com/amadomaker/IA-JOSE.git
cd IA-JOSE

# Instalar dependências
pip3 install -r requirements.txt

# Configurar autostart (systemd)
sudo nano /etc/systemd/system/jose.service
```

**Conteúdo do service:**
```ini
[Unit]
Description=J.O.S.E Robot Assistant
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/IA-JOSE
ExecStart=/home/pi/IA-JOSE/venv/bin/uvicorn src.api.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

**Ativar service:**
```bash
sudo systemctl enable jose.service
sudo systemctl start jose.service
sudo systemctl status jose.service
```

---

## 📝 Checklist de Execução

### Primeira Execução

- [ ] Python 3.8+ instalado
- [ ] Git instalado
- [ ] Repositório clonado
- [ ] Ambiente virtual criado
- [ ] Dependências instaladas
- [ ] Microfone testado


### Execução Diária (Desenvolvimento)

- [ ] Venv ativado
- [ ] Código atualizado (`git pull`)
- [ ] Servidor API rodando
- [ ] Testes passando
- [ ] KB atualizado (se necessário)

---

**Desenvolvido em parceria: Amado Maker × NIED/Unicamp**
