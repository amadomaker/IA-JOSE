"""
Configurações centralizadas do sistema J.O.S.E
Mantém todas as constantes e configurações em um único lugar
"""
import os
from pathlib import Path

# Diretório raiz do projeto
ROOT_DIR = Path(__file__).parent.parent.parent
DATA_DIR = ROOT_DIR / "data"
LOGS_DIR = ROOT_DIR / "logs"
AUDIO_DIR = DATA_DIR / "audio"


class VoiceConfig:
    """Configurações de voz (TTS e STT)"""

    # Text-to-Speech (Microsoft Edge TTS)
    VOZ_MASCULINA = "pt-BR-AntonioNeural"
    VOZ_RATE = "+0%"  # Velocidade da fala (0% = normal, +15% = mais rápido)

    # Speech-to-Text (Google)
    LANGUAGE = "pt-BR"
    PAUSE_THRESHOLD = 1.0  # Segundos de silêncio para considerar fim de frase
    ENERGY_THRESHOLD = 300  # Sensibilidade do microfone
    DYNAMIC_ENERGY = True  # Ajuste automático de sensibilidade
    PHRASE_TIME_LIMIT = 8  # Tempo máximo de frase em segundos

    # Arquivos temporários
    TEMP_AUDIO_FILE = AUDIO_DIR / "resposta.mp3"


class WakeWordConfig:
    """Configurações de wake word (palavra de ativação)"""

    PALAVRA_CHAVE = "josé"
    VARIANTES_NOME = ["josé", "jose", "j.o.s.e", "j o s e"]


class SerialConfig:
    """Configurações de comunicação serial com Arduino"""

    PORT = "COM3"  # Porta serial do Arduino
    BAUD_RATE = 9600  # Taxa de transmissão
    TIMEOUT = 0.1  # Timeout de leitura em segundos
    CONNECT_DELAY = 2  # Delay após conexão (segundos)

    # Comandos
    CMD_MOUTH_OPEN = b"1"
    CMD_MOUTH_CLOSE = b"0"


class KnowledgeBaseConfig:
    """Configurações do Knowledge Base (KB)"""

    KB_PATH = DATA_DIR / "cerebro_nied.json"
    BACKUP_ENABLED = True
    BACKUP_SUFFIX = ".bak"

    # FAQ inicial (usado se o arquivo não existir)
    FAQ_INICIAL = []


class NLPConfig:
    """Configurações de processamento de linguagem natural"""

    # Substituições para formatação inteligente de texto
    TERM_REPLACEMENTS = {
        "nied": "NIED",
        "unicamp": "Unicamp",
        "arduino": "Arduino",
        "maker": "Maker",
        "fe": "FE",
        "pibic": "PIBIC",
        "bas": "BAS",
        "creality": "Creality",
        "gideone": "Gideone",
        "gideoni": "Gideone",  # Correção de pronúncia comum
    }


class LoggingConfig:
    """Configurações de logging"""

    LOG_DIR = LOGS_DIR
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Arquivos de log
    APP_LOG = LOG_DIR / "app.log"
    API_LOG = LOG_DIR / "api.log"
    LEARNING_LOG = LOG_DIR / "learning.log"
    ERROR_LOG = LOG_DIR / "errors.log"


class APIConfig:
    """Configurações da API FastAPI"""

    HOST = "0.0.0.0"
    PORT = 8000
    RELOAD = True  # Auto-reload em desenvolvimento
    CORS_ORIGINS = ["*"]  # Permitir todas as origens (ajustar em produção)

    # Metadata
    TITLE = "J.O.S.E API"
    DESCRIPTION = "API do Jovem Orientador de Soluções Educacionais (NIED Robô Humanoide)"
    VERSION = "1.0.0"


# Criar diretórios se não existirem
DATA_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)
AUDIO_DIR.mkdir(parents=True, exist_ok=True)
