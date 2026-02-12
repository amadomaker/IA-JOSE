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

## 📁 Estrutura do Projeto

```
c:\IA-JOSE\
├── scripts/           # Scripts utilitários
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

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/joaodrj">
        <img src="https://github.com/joaodrj.png" width="90px" style="border-radius: 50%;" alt="João Jr"/><br/>
        <b>João Jr</b>
      </a><br/>
      Desenvolvedor
    </td>
    <td align="center">
      <a href="https://github.com/vinicius3516">
        <img src="https://github.com/vinicius3516.png" width="90px" style="border-radius: 50%;" alt="Vinicius Costa"/><br/>
        <b>Vinicius Costa</b>
      </a><br/>
      DevOps Engineer
    </td>
  </tr>
</table>

**[João Jr](https://github.com/joaodrj)**  
Arquitetura do sistema, refatoração, implementação de API e Frontend, testes automatizados, documentação técnica e evolução contínua do projeto.

**[Vinicius Costa](https://github.com/vinicius3516)**  
Cultura DevOps, padronização de infraestrutura, pipelines CI/CD, observabilidade e segurança. Responsável também pela **concepção, construção e evolução do agente de IA principal do projeto J.O.S.E**, incluindo arquitetura cognitiva, integração com LLMs, ferramentas (tools), orquestração de fluxos inteligentes e boas práticas de IA aplicada.

**Organização:** [Amado Maker](https://github.com/amadomaker)


---

### Equipe NIED

<table>
  <tr>
    <td align="center">
      <a href="https://www.nied.unicamp.br/equipe/eliton-meires-de-moura/">
        <img src="https://www.nied.unicamp.br/wp-content/uploads/2024/08/Eliton-equipe-nied-v2025-300x289.jpg" width="90px" style="border-radius: 50%;" alt="Eliton"/><br/>
        <b>Eliton</b>
      </a><br/>
      Liderança técnica
    </td>
    <td align="center">
      <a href="https://github.com/gideonesantos-tech">
        <img src="https://github.com/gideonesantos-tech.png" width="90px" style="border-radius: 50%;" alt="Gideone Rafael"/><br/>
        <b>Gideone Rafael</b>
      </a><br/>
      Desenvolvedor
    </td>
    <td align="center">
      <a href="https://github.com/RafaelLevi8708">
        <img src="https://github.com/RafaelLevi8708.png" width="90px" style="border-radius: 50%;" alt="Rafael Levi"/><br/>
        <b>Rafael Levi</b>
      </a><br/>
      Desenvolvedor
    </td>
  </tr>
</table>

- **Bolsistas BAS**: Henrique, Pedro
- **Bolsistas PIBIC**: Thayla, Otávio, Kauã

## 📝 Licença

Projeto educacional desenvolvido no NIED/Unicamp para fins de pesquisa em robótica pedagógica.

## 🔗 Links

- [NIED - Núcleo de Informática Aplicada à Educação](https://www.nied.unicamp.br/)
- [Unicamp](https://www.unicamp.br/)

---

**Desenvolvido em parceria: Amado Maker × NIED/Unicamp**
