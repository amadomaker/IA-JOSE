from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from src.kb.loader import load_kb
from src.kb.matcher import find_best_match, find_match
from src.core.config import KnowledgeBaseConfig
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.staticfiles import StaticFiles
from src.io.voice import get_tts
from src.core.config import AUDIO_DIR
from src.kb.matcher import find_best_match, find_match
import logging
import uuid

# Configuração de logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api")

app = FastAPI(
    title="J.O.S.E. API",
    description="API do Robô Humanoide J.O.S.E (NIED/Unicamp)",
    version="0.1.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar frontend estático
# O diretório 'src/frontend' deve existir
frontend_path = Path(__file__).parent.parent / "frontend"
frontend_path.mkdir(parents=True, exist_ok=True)
app.mount("/app", StaticFiles(directory=frontend_path, html=True), name="frontend")

# Montar diretório de áudio temporário
AUDIO_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/audio", StaticFiles(directory=AUDIO_DIR), name="audio")

# Montar diretório de áudio temporário
AUDIO_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/audio", StaticFiles(directory=AUDIO_DIR), name="audio")

# Modelo de entrada para /ask
class QuestionRequest(BaseModel):
    question: str

# Modelo de entrada para /tts
class TTSRequest(BaseModel):
    text: str



# Modelo de saída para /ask
class AskResponse(BaseModel):
    answer: str
    sources: Dict[str, Any]
    confidence: float

# Carregar KB na inicialização
kb_data = []

@app.on_event("startup")
async def startup_event():
    global kb_data
    try:
        kb_data = load_kb(KnowledgeBaseConfig.KB_PATH)
        logger.info(f"KB carregado com {len(kb_data)} entradas.")
    except Exception as e:
        logger.error(f"Erro ao carregar KB: {e}")
        kb_data = []

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "kb_loaded": len(kb_data) > 0,
        "kb_entries": len(kb_data),
        "version": "0.1.0"
    }

@app.post("/ask", response_model=AskResponse)
async def ask_question(request: QuestionRequest):
    if not kb_data:
        raise HTTPException(status_code=503, detail="Knowledge Base not loaded")
    
    # 1. Tentar match exato/substring (mais rápido e confiável para comandos)
    match = find_match(request.question, kb_data)
    
    # 2. Se não encontrar, tentar best match (similaridade)
    if not match:
        match = find_best_match(request.question, kb_data, threshold=0.5)
    
    if match:
        return match
    
    # 3. Se não encontrar nada, retornar resposta padrão de "não sei"
    # Por enquanto, retornamos 404 ou uma resposta genérica com confiança 0
    return {
        "answer": "Desculpe, não sei responder a isso ainda. Pode reformular?",
        "sources": {
            "kb_entry_id": None,
            "matched_triggers": []
        },
        "confidence": 0.0
    }

@app.post("/tts")
async def text_to_speech(request: TTSRequest):
    """
    Gera áudio a partir de texto usando Edge TTS (Backend).
    Retorna URL para o arquivo de áudio gerado.
    """
    try:
        # Gerar nome de arquivo único para evitar colisão/cache
        filename = f"tts_{uuid.uuid4().hex}.mp3"
        output_path = AUDIO_DIR / filename
        
        # Gerar áudio
        tts = get_tts()
        success = await tts.generate_audio(request.text, output_path)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to generate audio")
            
        return {"audio_url": f"/audio/{filename}"}

    except Exception as e:
        logger.error(f"Erro no TTS endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tts")
async def text_to_speech(request: TTSRequest):
    """
    Gera áudio a partir de texto usando Edge TTS (Backend).
    Retorna URL para o arquivo de áudio gerado.
    """
    try:
        # Gerar nome de arquivo único para evitar colisão/cache
        filename = f"tts_{uuid.uuid4().hex}.mp3"
        output_path = AUDIO_DIR / filename
        
        # Gerar áudio
        tts = get_tts()
        success = await tts.generate_audio(request.text, output_path)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to generate audio")
            
        return {"audio_url": f"/audio/{filename}"}

    except Exception as e:
        logger.error(f"Erro no TTS endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


