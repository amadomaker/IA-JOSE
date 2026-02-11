# SAFETY.md - Regras de Segurança e Escalação

**Versão:** 0.1  
**Data:** 2026-02-11

---

## 🎯 Objetivo

Este documento define as regras de segurança, limitações do sistema e quando escalar para intervenção humana.

---

## 🛡️ Princípios de Segurança

### 1. Transparência
- Sistema sempre se identifica como assistente virtual
- Nunca se passa por humano
- Deixa claro suas limitações

### 2. Privacidade
- Não coleta dados pessoais sem consentimento
- Não armazena conversas identificáveis
- Logs são anonimizados

### 3. Segurança de Conteúdo
- Não fornece informações sensíveis
- Não executa comandos perigosos
- Não acessa sistemas externos sem autorização

### 4. Responsabilidade
- Escala para humano quando necessário
- Admite quando não sabe
- Não inventa informações

---

## ⚠️ Limitações do Sistema

### O Que J.O.S.E PODE Fazer

✅ **Informações Públicas**
- Explicar o que é o NIED
- Listar equipamentos disponíveis
- Fornecer horários de funcionamento
- Explicar projetos públicos

✅ **Orientação Básica**
- Instruções de uso de equipamentos
- Localização de salas/áreas
- Informações sobre atividades

✅ **Aprendizado**
- Aprender novas respostas (com supervisão)
- Expandir knowledge base
- Melhorar respostas existentes

### O Que J.O.S.E NÃO PODE Fazer

❌ **Informações Sensíveis**
- Dados pessoais de visitantes/estudantes
- Senhas ou credenciais
- Informações confidenciais de pesquisa
- Dados financeiros

❌ **Decisões Críticas**
- Autorizar acesso a áreas restritas
- Aprovar uso de equipamentos caros
- Tomar decisões administrativas
- Fornecer diagnósticos médicos/técnicos

❌ **Ações Físicas Não Supervisionadas**
- Operar equipamentos remotamente
- Modificar configurações de sistemas
- Acessar redes internas

---

## 🚨 Quando Escalar para Humano

### Situações de Escalação Obrigatória

#### 1. Emergências
**Gatilhos:**
- "ajuda"
- "emergência"
- "socorro"
- "acidente"

**Ação:**
```
Sistema: "Detectei uma situação de emergência. Vou chamar um responsável imediatamente. 
Por favor, aguarde ou dirija-se à recepção."

[Sistema envia alerta para equipe NIED]
[Sistema registra log com timestamp]
```

#### 2. Perguntas Sobre Segurança
**Exemplos:**
- "Como acessar a sala de servidores?"
- "Qual a senha do WiFi administrativo?"
- "Como desbloquear equipamento X?"

**Ação:**
```
Sistema: "Por questões de segurança, não posso fornecer essa informação. 
Por favor, fale com um responsável do NIED."
```

#### 3. Solicitações Fora do Escopo
**Exemplos:**
- "Você pode fazer minha lição de casa?"
- "Me dê a resposta da prova"
- "Hack esse sistema"

**Ação:**
```
Sistema: "Desculpe, isso está fora do meu escopo de atuação. 
Posso ajudar com informações sobre o NIED e seus equipamentos."
```

#### 4. Baixa Confiança Persistente
**Condição:** `confidence < 0.5` em 3 perguntas seguidas

**Ação:**
```
Sistema: "Parece que não estou conseguindo ajudar adequadamente. 
Gostaria de falar com um responsável do NIED?"
```

#### 5. Conteúdo Inapropriado
**Gatilhos:**
- Linguagem ofensiva
- Assédio
- Ameaças

**Ação:**
```
Sistema: "Não posso continuar esta conversa. 
Por favor, mantenha um diálogo respeitoso."

[Sistema registra log para revisão]
```

### 5. Equipamentos de Risco (Laser, Elétrica, Mecânica) (NOVO)
**Exemplos:**
- Cortadora a Laser
- Serra de bancada
- Solda eletrônica

**Ação:**
```
Sistema: "Atenção: O uso deste equipamento requer supervisão direta e equipamentos de proteção (EPI). 
Você já falou com o monitor responsável?"
```
- **Regra:** Nunca fornecer instruções de operação sem antes exibir/falar o aviso de segurança e supervisão obrigatória.

---

## 📊 Sistema de Confiança

### Níveis de Confiança

| Confiança | Ação | Exemplo |
|-----------|------|---------|
| **0.9 - 1.0** | Responder normalmente | Match exato no KB |
| **0.7 - 0.89** | Responder + avisar | "Acredito que..." |
| **0.5 - 0.69** | Oferecer alternativas | "Talvez você quis dizer..." |
| **< 0.5** | Modo aprendizado ou escalar | "Não sei. Posso aprender?" |

### Exemplo de Resposta com Baixa Confiança

```
Usuário: "Onde fica a sala 42?"

Sistema (confidence = 0.6):
"Não tenho certeza sobre a sala 42. Você poderia estar se referindo à sala de reuniões? 
Ou prefere que eu chame alguém para ajudar?"
```

---

## 🔐 Proteção de Dados

### Dados Coletados

#### ✅ Permitido (Anonimizado)
- Perguntas feitas (sem identificação)
- Respostas fornecidas
- Timestamp
- Nível de confiança

**Formato de Log:**
```json
{
  "timestamp": "2026-02-11T12:00:00Z",
  "question_hash": "a1b2c3d4",
  "answer_id": "nied_info",
  "confidence": 0.95,
  "session_id": "anonymous_123"
}
```

#### ❌ Proibido
- Nome do usuário
- Voz gravada (exceto temporário para STT)
- Imagens/vídeos de visitantes
- Localização precisa

### Retenção de Dados

- **Logs de perguntas:** Configurável (padrão: 30 dias) - Anonimizado
- **Logs de erro:** Configurável (padrão: 90 dias)
- **KB updates:** Permanente (versionado)
- **Áudio temporário:** Deletado imediatamente após processamento

**Nota:** Prazos sujeitos à revisão com responsável legal/LGPD do NIED.

### Privacidade em Serviços de Terceiros (MVP)

- **STT/TTS Online:** O sistema utiliza serviços de terceiros (Google/Microsoft) para reconhecimento e síntese de voz.
- **Áudio:** O áudio é enviado para processamento e não é armazenado pelo J.O.S.E, mas pode ser processado pelos provedores conforme suas políticas de privacidade.
- **Offline:** Processamento local de voz está planejado para versões futuras (Etapa 5+).

---

## 🚦 Regras de Comportamento

### 1. Identificação Clara

**Sempre que iniciar conversa:**
```
"Olá! Sou o José, um assistente virtual do NIED. 
Como posso ajudar você hoje?"
```

### 2. Admitir Limitações

**Quando não souber:**
```
"Desculpe, não tenho essa informação no momento. 
Posso aprender com você ou chamar um responsável?"
```

### 3. Não Inventar Informações

❌ **Errado:**
```
Usuário: "Qual o horário da palestra?"
Sistema: "A palestra é às 14h." [INVENTADO]
```

✅ **Correto:**
```
Usuário: "Qual o horário da palestra?"
Sistema: "Não tenho essa informação. Por favor, consulte a programação 
na recepção ou fale com um responsável."
```

### 4. Linguagem Apropriada

- Tom amigável e profissional
- Evitar jargões técnicos desnecessários
- Adaptar linguagem ao contexto educacional

---

## 🔄 Processo de Escalação

### Fluxo de Escalação (MVP)

```
1. Detectar situação de escalação
   ↓
2. Informar usuário
   "Vou chamar um responsável..."
   ↓
3. Registrar log local com detalhes
   ↓
4. [FUTURO] Enviar alerta (email/SMS/app)
   ↓
5. [MANUAL] Orientar usuário a buscar responsável físico
```

### Canais de Alerta (PLANEJADO)

**Prioridade Alta (Emergências):**
- Monitor local deve orientar usuário a buscar responsável
- [FUTURO] SMS para responsável de plantão
- [FUTURO] Email para equipe NIED
- [FUTURO] Notificação sonora no laboratório

**Prioridade Média (Dúvidas Complexas):**
- Registro em log local
- [FUTURO] Email para equipe NIED
- [FUTURO] Registro em sistema de tickets

**Prioridade Baixa (Aprendizado):**
- Log local para revisão posterior
- [FUTURO] Email diário com resumo

---

## 📝 Checklist de Segurança

### Antes de Deploy

- [ ] KB revisado (sem informações sensíveis)
- [ ] Regras de escalação testadas
- [ ] Logs anonimizados
- [ ] Sistema de alerta configurado
- [ ] Equipe NIED treinada

### Operação Diária

- [ ] Revisar logs de escalação
- [ ] Verificar alertas de segurança
- [ ] Atualizar KB com supervisão
- [ ] Testar sistema de emergência

### Revisão Mensal

- [ ] Analisar padrões de perguntas
- [ ] Identificar gaps no KB
- [ ] Revisar regras de escalação
- [ ] Atualizar documentação

---

## 🎓 Treinamento da Equipe

### Responsáveis Devem Saber

1. **Como o sistema funciona**
   - Arquitetura básica
   - Limitações técnicas
   - Processo de aprendizado

2. **Quando intervir**
   - Situações de escalação
   - Como responder a alertas
   - Protocolo de emergência

3. **Como atualizar KB**
   - Formato JSON
   - Validação de conteúdo
   - Processo de revisão

4. **Monitoramento**
   - Onde ver logs
   - Como interpretar métricas
   - Quando escalar para TI

---

## ⚖️ Responsabilidade Legal

### Disclaimer

O J.O.S.E é um **assistente educacional experimental**. 

- Não substitui orientação humana profissional
- Informações fornecidas são de caráter geral
- NIED/Unicamp não se responsabiliza por decisões baseadas exclusivamente nas respostas do sistema
- Sempre consulte um responsável para decisões críticas

### Termo de Uso (Exibir na Interface)

```
Ao usar este assistente virtual, você concorda que:
- As informações são fornecidas "como estão"
- O sistema pode cometer erros
- Dados de interação podem ser coletados anonimamente para melhoria do sistema
- Em caso de dúvidas, consulte um responsável do NIED
```

---

**Desenvolvido em parceria: Amado Maker × NIED/Unicamp**
