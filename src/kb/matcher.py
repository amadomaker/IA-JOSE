"""
Módulo Matcher - Matching de perguntas com gatilhos do KB
"""
from typing import Optional, Dict, Any, List, Tuple


def find_match(pergunta: str, kb: List[Dict[str, Any]]) -> Optional[str]:
    """
    Busca uma resposta no KB baseado em matching de gatilhos.

    Algoritmo:
    - Normaliza a pergunta (lowercase, strip)
    - Para cada entrada do KB, verifica se algum gatilho está contido na pergunta
    - Retorna a primeira resposta encontrada

    Args:
        pergunta: Pergunta do usuário
        kb: Knowledge base (lista de entradas)

    Returns:
        Resposta encontrada ou None
    """
    pergunta_lower = pergunta.lower().strip()

    for item in kb:
        if any(gatilho in pergunta_lower for gatilho in item["gatilhos"]):
            return item["resposta"]

    return None


def find_all_matches(pergunta: str, kb: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Busca TODAS as respostas que fazem match com a pergunta.

    Args:
        pergunta: Pergunta do usuário
        kb: Knowledge base

    Returns:
        Lista de entradas que fazem match
    """
    pergunta_lower = pergunta.lower().strip()
    matches = []

    for item in kb:
        if any(gatilho in pergunta_lower for gatilho in item["gatilhos"]):
            matches.append(item)

    return matches


def calculate_similarity(pergunta: str, gatilho: str) -> float:
    """
    Calcula similaridade entre pergunta e gatilho (0.0 a 1.0).

    Implementação simples baseada em substring matching.
    Futuro: implementar fuzzy matching (Levenshtein, etc.)

    Args:
        pergunta: Pergunta do usuário
        gatilho: Gatilho do KB

    Returns:
        Score de similaridade (0.0 a 1.0)
    """
    pergunta_lower = pergunta.lower().strip()
    gatilho_lower = gatilho.lower().strip()

    # Match exato
    if pergunta_lower == gatilho_lower:
        return 1.0

    # Substring match
    if gatilho_lower in pergunta_lower:
        return 0.8

    # Palavras em comum
    palavras_pergunta = set(pergunta_lower.split())
    palavras_gatilho = set(gatilho_lower.split())

    if not palavras_gatilho:
        return 0.0

    palavras_comuns = palavras_pergunta.intersection(palavras_gatilho)
    similarity = len(palavras_comuns) / len(palavras_gatilho)

    return similarity


def find_best_match(
    pergunta: str, kb: List[Dict[str, Any]], threshold: float = 0.5
) -> Optional[Tuple[str, float]]:
    """
    Busca a melhor resposta baseado em score de similaridade.

    Args:
        pergunta: Pergunta do usuário
        kb: Knowledge base
        threshold: Score mínimo para considerar um match

    Returns:
        Tupla (resposta, score) ou None se não houver match acima do threshold
    """
    best_score = 0.0
    best_response = None

    for item in kb:
        for gatilho in item["gatilhos"]:
            score = calculate_similarity(pergunta, gatilho)

            if score > best_score:
                best_score = score
                best_response = item["resposta"]

    if best_score >= threshold:
        return (best_response, best_score)

    return None


def suggest_similar_questions(
    pergunta: str, kb: List[Dict[str, Any]], top_n: int = 3
) -> List[Tuple[str, float]]:
    """
    Sugere perguntas similares do KB.

    Args:
        pergunta: Pergunta do usuário
        kb: Knowledge base
        top_n: Número de sugestões a retornar

    Returns:
        Lista de tuplas (gatilho, score) ordenadas por score
    """
    scores = []

    for item in kb:
        for gatilho in item["gatilhos"]:
            score = calculate_similarity(pergunta, gatilho)
            if score > 0:
                scores.append((gatilho, score))

    # Ordenar por score (decrescente)
    scores.sort(key=lambda x: x[1], reverse=True)

    return scores[:top_n]
