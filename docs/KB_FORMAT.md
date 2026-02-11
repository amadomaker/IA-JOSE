# KB_FORMAT.md - Formato do Knowledge Base

**Versão:** 0.1  
**Data:** 2026-02-11

---

## 📋 Visão Geral

O Knowledge Base (KB) do J.O.S.E é armazenado em formato JSON estruturado, permitindo fácil edição, versionamento e expansão.

**Localização:** `data/kb/nied_kb.json`

---

## 📄 Estrutura do JSON

### Formato Geral

```json
[
  {
    "gatilhos": ["trigger1", "trigger2", "trigger3"],
    "resposta": "Texto da resposta que será falada pelo sistema."
  },
  {
    "gatilhos": ["outro trigger", "variação"],
    "resposta": "Outra resposta."
  }
]
```

### Campos

#### `gatilhos` (obrigatório)
**Tipo:** Array de strings  
**Descrição:** Lista de frases/palavras que ativam esta resposta

**Regras:**
- Mínimo 1 gatilho
- Máximo recomendado: 10 gatilhos
- Case-insensitive (sistema normaliza para lowercase)
- Remover acentos não é necessário (sistema faz automaticamente)
- Incluir variações comuns da pergunta

**Exemplos:**
```json
"gatilhos": [
  "o que é o nied",
  "o que é nied",
  "me fale sobre o nied",
  "explique o nied",
  "nied"
]
```

#### `resposta` (obrigatório)
**Tipo:** String  
**Descrição:** Texto que será convertido em fala e exibido

**Regras:**
- Linguagem natural e clara
- Evitar textos muito longos (máx. 500 caracteres recomendado)
- Usar pontuação adequada para pausas naturais
- Pode incluir números, siglas, etc.

**Exemplos:**
```json
"resposta": "O NIED é o Núcleo de Informática Aplicada à Educação da Unicamp. Fundado em 1983, desenvolve pesquisas em tecnologia educacional e robótica pedagógica."
```

---

## 📝 Exemplo Completo

```json
[
  {
    "gatilhos": [
      "olá",
      "oi",
      "bom dia",
      "boa tarde",
      "boa noite",
      "saudações"
    ],
    "resposta": "Olá! Seja bem-vindo ao NIED. Como posso ajudar você a explorar o nosso Espaço Maker hoje?"
  },
  {
    "gatilhos": [
      "o que é o nied",
      "o que é nied",
      "me fale sobre o nied",
      "explique o nied"
    ],
    "resposta": "O NIED é o Núcleo de Informática Aplicada à Educação da Unicamp. Fundado em 1983, desenvolve pesquisas em tecnologia educacional e robótica pedagógica."
  },
  {
    "gatilhos": [
      "quais equipamentos vocês têm",
      "que equipamentos tem aqui",
      "o que tem no espaço maker"
    ],
    "resposta": "Temos impressoras 3D, cortadora laser, kits de robótica Arduino e LEGO, computadores para programação, e muito mais!"
  },
  {
    "gatilhos": [
      "tchau",
      "até logo",
      "adeus",
      "até mais"
    ],
    "resposta": "Até logo! Foi um prazer ajudar. Volte sempre ao NIED!"
  }
]
```

---

## 🔍 Algoritmo de Matching

### Como o Sistema Busca Respostas

1. **Normalização da Pergunta**
   ```python
   pergunta = "O QUE É O NIED?"
   normalizada = "o que e o nied"  # lowercase, sem acentos
   ```

2. **Comparação com Gatilhos**
   ```python
   for entrada in kb:
       for gatilho in entrada["gatilhos"]:
           similaridade = calcular_similaridade(normalizada, gatilho)
           if similaridade > 0.7:
               return entrada["resposta"]
   ```

3. **Cálculo de Confiança**
   - Similaridade exata: `confidence = 1.0`
   - Similaridade parcial: `confidence = 0.7 - 0.99`
   - Sem match: `confidence < 0.7` → Modo aprendizado

---

## 📊 Versionamento do KB

### Controle de Versão

O KB deve ser versionado no Git junto com o código:

```bash
git add data/kb/nied_kb.json
git commit -m "kb: add entry about 3D printers"
git push origin dev
```

### Histórico de Mudanças

Manter changelog no topo do arquivo (comentário):

```json
[
  {
    "_comment": "Changelog:",
    "_v1.0": "2026-02-11 - KB inicial com 42 entradas",
    "_v1.1": "2026-02-12 - Adicionadas 5 entradas sobre equipamentos",
    "_v1.2": "2026-02-13 - Corrigida resposta sobre horários"
  },
  {
    "gatilhos": ["..."],
    "resposta": "..."
  }
]
```

**Nota:** Campos com `_` são ignorados pelo sistema.

---

## ✅ Boas Práticas

### 1. Gatilhos Variados
❌ **Ruim:**
```json
"gatilhos": ["o que é o nied"]
```

✅ **Bom:**
```json
"gatilhos": [
  "o que é o nied",
  "o que é nied",
  "me fale sobre o nied",
  "explique o nied",
  "nied"
]
```

### 2. Respostas Claras
❌ **Ruim:**
```json
"resposta": "É um núcleo."
```

✅ **Bom:**
```json
"resposta": "O NIED é o Núcleo de Informática Aplicada à Educação da Unicamp, fundado em 1983."
```

### 3. Evitar Duplicação
❌ **Ruim:**
```json
[
  {
    "gatilhos": ["o que é o nied"],
    "resposta": "O NIED é..."
  },
  {
    "gatilhos": ["me fale sobre o nied"],
    "resposta": "O NIED é..."  // Mesma resposta!
  }
]
```

✅ **Bom:**
```json
[
  {
    "gatilhos": ["o que é o nied", "me fale sobre o nied"],
    "resposta": "O NIED é..."
  }
]
```

### 4. Organização por Categoria
```json
[
  // Saudações
  { "gatilhos": ["olá", "oi"], "resposta": "..." },
  
  // Sobre o NIED
  { "gatilhos": ["o que é o nied"], "resposta": "..." },
  
  // Equipamentos
  { "gatilhos": ["quais equipamentos"], "resposta": "..." },
  
  // Despedidas
  { "gatilhos": ["tchau", "até logo"], "resposta": "..." }
]
```

---

## 🔧 Validação do KB

### Validador Automático

O sistema valida o KB ao carregar:

```python
def validate_kb(kb):
    for i, entry in enumerate(kb):
        # Verificar campos obrigatórios
        if "gatilhos" not in entry:
            raise ValueError(f"Entrada {i}: falta campo 'gatilhos'")
        if "resposta" not in entry:
            raise ValueError(f"Entrada {i}: falta campo 'resposta'")
        
        # Verificar tipos
        if not isinstance(entry["gatilhos"], list):
            raise ValueError(f"Entrada {i}: 'gatilhos' deve ser lista")
        if not isinstance(entry["resposta"], str):
            raise ValueError(f"Entrada {i}: 'resposta' deve ser string")
        
        # Verificar conteúdo
        if len(entry["gatilhos"]) == 0:
            raise ValueError(f"Entrada {i}: 'gatilhos' vazio")
        if len(entry["resposta"]) == 0:
            raise ValueError(f"Entrada {i}: 'resposta' vazia")
```

### Testar Manualmente

```powershell
# Validar JSON
python -m json.tool data/kb/nied_kb.json

# Se retornar sem erro, JSON é válido
```

---

## 📈 Expansão do KB

### Modo Aprendizado Interativo

Quando o sistema não sabe responder:

```
Usuário: "José, quem é o coordenador do NIED?"
Sistema: "Eu não sei sobre 'quem é o coordenador do NIED'. O que devo responder?"
Usuário: "O coordenador é o Professor José Armando Valente."
Sistema: "Entendi. A resposta será: 'O coordenador é o Professor José Armando Valente.' Posso salvar?"
Usuário: "Sim"
Sistema: "Perfeito! Informação salva."
```

**Resultado no KB:**
```json
{
  "gatilhos": ["quem é o coordenador do nied"],
  "resposta": "O coordenador é o Professor José Armando Valente."
}
```

### Edição Manual

Editar `data/kb/nied_kb.json` diretamente:

1. Abrir arquivo em editor de texto
2. Adicionar/modificar entrada
3. Validar JSON (`python -m json.tool ...`)
4. Reiniciar sistema para recarregar KB

---

## 🔐 Segurança

### Conteúdo Permitido

✅ **Permitido:**
- Informações públicas sobre NIED
- Instruções de uso de equipamentos
- Horários e contatos públicos
- Informações educacionais

❌ **Proibido:**
- Dados pessoais sensíveis
- Senhas ou credenciais
- Informações confidenciais
- Conteúdo ofensivo

### Revisão de Conteúdo

Antes de commitar KB atualizado:
1. Revisar novas entradas
2. Verificar se informações estão corretas
3. Validar JSON
4. Testar com sistema

---

**Desenvolvido em parceria: Amado Maker × NIED/Unicamp**
