# J.O.S.E - Jovem Orientador de Soluções Educacionais

![NIED](https://img.shields.io/badge/NIED-Unicamp-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-green)
![License](https://img.shields.io/badge/License-Educational-orange)

**Robô Humanoide Neural desenvolvido no Espaço Maker de Robótica Pedagógica do NIED/Unicamp**

## 🎯 Sobre o Projeto

J.O.S.E é um assistente virtual interativo com capacidades de:
- 🎤 **Reconhecimento de voz** (Google Speech Recognition)
- 🔊 **Síntese de voz natural** (Microsoft Edge TTS - voz Antonio)
- 🧠 **Aprendizado contínuo** via diálogo interativo
- 🤖 **Controle de hardware** (Arduino para sincronização labial)
- 🌐 **API REST + WebSocket** para integração web
- 💻 **Interface web em modo kiosk** para interação

## 🚀 Quick Start

### Pré-requisitos

- Python 3.8 ou superior
- Microfone funcional
- Arduino Uno (opcional - funciona em modo simulação)
- Conexão com internet (para STT e TTS)

### Instalação

```powershell
# 1. Clone ou navegue até o diretório
cd c:\IA-JOSE

# 2. Crie ambiente virtual (recomendado)
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Instale dependências
pip install -r requirements.txt

# 4. Execute o sistema original (modo CLI)
python cerebro_inteligente_aprimorado.py

# OU execute a API (modo web)
uvicorn src.api.main:app --reload
```

## 🎬 Quick Demo (Protótipo Legado - Sempre Funciona)

Para rodar a versão original garantida:

```powershell
.\scripts\run_legacy.ps1
```

Este script:
- ✅ Ativa o ambiente virtual automaticamente
- ✅ Verifica dependências
- ✅ Executa o protótipo original congelado
- ✅ **Sempre funciona**, mesmo durante refatoração

### Primeiro Uso

1. Diga: **"José, o que é o NIED?"**
2. O sistema responderá com informações do knowledge base
3. Para ensinar algo novo: **"José, quem é [nome]?"**
4. Siga as instruções de voz para completar o aprendizado

## 📁 Estrutura do Projeto

```
c:\IA-JOSE\
├── legacy/            # 🔒 Protótipo original (congelado)
│   ├── cerebro_inteligente_aprimorado.py
│   ├── cerebro_nied.json
│   └── README.md
├── scripts/           # Scripts utilitários
│   └── run_legacy.ps1  # Demo sempre funciona
├── src/
│   ├── core/          # Lógica de negócio (brain, NLP, config)
│   ├── kb/            # Knowledge base (loader, matcher, learner)
│   ├── io/            # I/O (voice, audio, serial)
│   ├── api/           # FastAPI backend
│   └── frontend/      # Interface web
├── tests/
│   ├── unit/          # Testes unitários
│   └── integration/   # Testes de integração
├── docs/              # Documentação técnica
├── data/
│   ├── kb/            # Knowledge base (nied_kb.json)
│   └── cerebro_nied.json  # KB original (mantido)
├── logs/              # Logs de telemetria
├── cerebro_inteligente_aprimorado.py  # Script original (raiz)
└── README.md          # Este arquivo
```

## 📚 Documentação

- **[SPEC.md](docs/SPEC.md)** - Especificação técnica completa
- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - Arquitetura do sistema
- **[ROADMAP.md](docs/ROADMAP.md)** - Plano de evolução
- **[KB_FORMAT.md](docs/KB_FORMAT.md)** - Formato do knowledge base
- **[SAFETY.md](docs/SAFETY.md)** - Segurança e boas práticas
- **[RUNBOOK_WINDOWS.md](docs/RUNBOOK_WINDOWS.md)** - Guia de execução Windows

## 🛠️ Desenvolvimento

### Executar Testes

```powershell
# Todos os testes
pytest

# Apenas testes unitários
pytest tests/unit/

# Com cobertura
pytest --cov=src --cov-report=html
```

### Linting e Formatação

```powershell
# Verificar estilo
flake8 src/ tests/

# Formatar código
black src/ tests/
```

## 👥 Desenvolvimento

### Desenvolvedor
<a href="https://github.com/joaodrj">
  <img src="https://github.com/joaodrj.png" width="60px" style="border-radius: 50%;" alt="João Jr"/>
</a>

**[João Jr](https://github.com/joaodrj)** - Arquitetura do sistema, refatoração, implementação de API/Frontend, testes, documentação e evolução contínua do projeto.

**Organização:** [Amado Maker](https://github.com/amadomaker)

---

### Equipe NIED
<a href="https://github.com/gideone-rafael">
  <img src="https://github.com/gideone-rafael.png" width="60px" style="border-radius: 50%;" alt="Gideone Rafael"/>
</a>
<a href="https://github.com/eliton-nied">
  <img src="https://github.com/eliton-nied.png" width="60px" style="border-radius: 50%;" alt="Eliton"/>
</a>

- **Orientação Técnica**: Eliton
- **Gideone Rafael** - Desenvolvedor
- **Bolsistas BAS**: Henrique, Pedro
- **Bolsistas PIBIC**: Thayla, Otávio, Kauã

## 📝 Licença

Projeto educacional desenvolvido no NIED/Unicamp para fins de pesquisa em robótica pedagógica.

## 🔗 Links

- [NIED - Núcleo de Informática Aplicada à Educação](https://www.nied.unicamp.br/)
- [Unicamp](https://www.unicamp.br/)

---

**Desenvolvido em parceria: Amado Maker × NIED/Unicamp**
