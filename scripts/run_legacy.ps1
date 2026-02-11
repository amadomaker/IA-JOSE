# ==================================================================================
# SCRIPT DE EXECUÇÃO DO PROTÓTIPO LEGADO (SEMPRE FUNCIONA)
# ==================================================================================
# Este script garante que você sempre pode rodar a versão original do J.O.S.E
# mesmo durante o processo de refatoração.
#
# USO:
#   .\scripts\run_legacy.ps1
#
# ==================================================================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  J.O.S.E - DEMO LEGADO (PROTÓTIPO)    " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar se estamos no diretório correto
$projectRoot = "c:\IA-JOSE"
if ((Get-Location).Path -ne $projectRoot) {
    Write-Host "Navegando para o diretório do projeto..." -ForegroundColor Yellow
    Set-Location $projectRoot
}

# Verificar se o ambiente virtual existe
$venvPath = Join-Path $projectRoot "venv"
if (-not (Test-Path $venvPath)) {
    Write-Host "ERRO: Ambiente virtual não encontrado em: $venvPath" -ForegroundColor Red
    Write-Host "Por favor, crie o ambiente virtual primeiro:" -ForegroundColor Yellow
    Write-Host "  python -m venv venv" -ForegroundColor Yellow
    exit 1
}

# Verificar se o script legado existe
$legacyScript = Join-Path $projectRoot "legacy\cerebro_inteligente_aprimorado.py"
if (-not (Test-Path $legacyScript)) {
    Write-Host "ERRO: Script legado não encontrado em: $legacyScript" -ForegroundColor Red
    exit 1
}

# Verificar se o KB legado existe
$legacyKB = Join-Path $projectRoot "legacy\cerebro_nied.json"
if (-not (Test-Path $legacyKB)) {
    Write-Host "ERRO: KB legado não encontrado em: $legacyKB" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Ambiente virtual encontrado" -ForegroundColor Green
Write-Host "✓ Script legado encontrado" -ForegroundColor Green
Write-Host "✓ Knowledge base encontrado" -ForegroundColor Green
Write-Host ""

# Ativar ambiente virtual
Write-Host "Ativando ambiente virtual..." -ForegroundColor Yellow
& "$venvPath\Scripts\Activate.ps1"

# Verificar se as dependências estão instaladas
Write-Host "Verificando dependências..." -ForegroundColor Yellow
$pipList = pip list 2>&1
if ($pipList -notmatch "SpeechRecognition") {
    Write-Host "⚠️  Dependências não instaladas. Instalando..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  INICIANDO PROTÓTIPO LEGADO...        " -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "INSTRUÇÕES:" -ForegroundColor Cyan
Write-Host "  1. Diga: 'José, o que é o NIED?'" -ForegroundColor White
Write-Host "  2. Para sair: 'José, tchau'" -ForegroundColor White
Write-Host ""
Write-Host "Pressione Ctrl+C a qualquer momento para encerrar." -ForegroundColor Yellow
Write-Host ""

# Executar o script legado
Set-Location (Join-Path $projectRoot "legacy")
python cerebro_inteligente_aprimorado.py

# Voltar ao diretório raiz
Set-Location $projectRoot

Write-Host ""
Write-Host "Demo encerrada." -ForegroundColor Cyan
