# Legacy Directory

Este diretório contém o **protótipo original** do J.O.S.E, congelado e inalterado.

## 🔒 Propósito

Garantir que sempre temos uma versão funcional do sistema, mesmo durante a refatoração.

## 📁 Arquivos

- `cerebro_inteligente_aprimorado.py` - Script original (286 linhas)
- `cerebro_nied.json` - Knowledge base original

## 🚀 Como Executar

### Opção 1: Script Automatizado (Recomendado)

```powershell
.\scripts\run_legacy.ps1
```

### Opção 2: Manual

```powershell
cd c:\IA-JOSE\legacy
..\venv\Scripts\Activate.ps1
python cerebro_inteligente_aprimorado.py
```

## ⚠️ IMPORTANTE

**NÃO MODIFIQUE** os arquivos neste diretório. Eles servem como referência e backup.

Para desenvolvimento, use os módulos em `src/`.

## 📝 Versão

- **Data do snapshot**: 2026-02-11
- **Funcionalidades**:
  - ✅ Reconhecimento de voz (Google STT)
  - ✅ Síntese de voz (Microsoft Edge TTS)
  - ✅ Wake word "josé"
  - ✅ Knowledge base JSON
  - ✅ Modo aprendizado interativo
  - ✅ Controle Arduino (COM3)
  - ✅ Formatação inteligente de texto
