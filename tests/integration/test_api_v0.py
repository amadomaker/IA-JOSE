import pytest
from fastapi.testclient import TestClient
from src.api.main import app
import os

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "kb_loaded" in data
    assert "version" in data

def test_ask_question_known():
    # Pergunta que existe no KB
    response = client.post("/ask", json={"question": "o que é o nied?"})
    assert response.status_code == 200
    data = response.json()
    
    assert "answer" in data
    assert "sources" in data
    assert "confidence" in data
    
    sources = data["sources"]
    assert "kb_entry_id" in sources
    assert "matched_triggers" in sources
    assert isinstance(sources["matched_triggers"], list)
    assert len(sources["matched_triggers"]) > 0
    assert data["confidence"] > 0.5

def test_ask_question_unknown():
    # Pergunta que NÃO existe
    response = client.post("/ask", json={"question": "qual a capital de marte?"})
    # O comportamento atual é retornar 200 com resposta padrão e confiança 0.0
    # ou 404 dependendo da implementação. No main.py implementamos retorno com confiança 0.0
    
    assert response.status_code == 200
    data = response.json()
    assert data["confidence"] == 0.0
    assert data["sources"]["kb_entry_id"] is None
