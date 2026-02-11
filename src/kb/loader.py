"""
Módulo Loader - Carregamento e validação do Knowledge Base
"""
import json
from typing import List, Dict, Any, Optional
from pathlib import Path


class KBValidationError(Exception):
    """Exceção para erros de validação do KB."""

    pass


def load_kb(kb_path: Path) -> List[Dict[str, Any]]:
    """
    Carrega o knowledge base de um arquivo JSON.

    Args:
        kb_path: Caminho para o arquivo JSON

    Returns:
        Lista de entradas do KB

    Raises:
        FileNotFoundError: Se o arquivo não existir
        json.JSONDecodeError: Se o JSON for inválido
        KBValidationError: Se a estrutura do KB for inválida
    """
    if not kb_path.exists():
        raise FileNotFoundError(f"KB não encontrado: {kb_path}")

    with open(kb_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Validar estrutura
    validate_kb_schema(data)

    return data


def validate_kb_schema(data: Any) -> bool:
    """
    Valida a estrutura do knowledge base.

    Estrutura esperada:
    [
        {
            "gatilhos": ["pergunta1", "pergunta2", ...],
            "resposta": "resposta correspondente"
        },
        ...
    ]

    Args:
        data: Dados a serem validados

    Returns:
        True se válido

    Raises:
        KBValidationError: Se a estrutura for inválida
    """
    if not isinstance(data, list):
        raise KBValidationError("KB deve ser uma lista")

    for idx, item in enumerate(data):
        if not isinstance(item, dict):
            raise KBValidationError(f"Entrada {idx} deve ser um dicionário")

        # Auto-gerar ID se não existir (para compatibilidade com JSON antigo)
        if "id" not in item:
            item["id"] = idx + 1

        if not isinstance(item["id"], int):
            raise KBValidationError(f"Entrada {idx}: 'id' deve ser um inteiro")

        if "gatilhos" not in item:
            raise KBValidationError(f"Entrada {idx} não possui campo 'gatilhos'")

        if "resposta" not in item:
            raise KBValidationError(f"Entrada {idx} não possui campo 'resposta'")

        if not isinstance(item["gatilhos"], list):
            raise KBValidationError(f"Entrada {idx}: 'gatilhos' deve ser uma lista")

        if not isinstance(item["resposta"], str):
            raise KBValidationError(f"Entrada {idx}: 'resposta' deve ser uma string")

        if len(item["gatilhos"]) == 0:
            raise KBValidationError(f"Entrada {idx}: 'gatilhos' não pode ser vazio")

        # Validar que todos os gatilhos são strings
        for g_idx, gatilho in enumerate(item["gatilhos"]):
            if not isinstance(gatilho, str):
                raise KBValidationError(
                    f"Entrada {idx}, gatilho {g_idx}: deve ser uma string"
                )

    return True


def save_kb(kb_path: Path, data: List[Dict[str, Any]], validate: bool = True) -> bool:
    """
    Salva o knowledge base em um arquivo JSON.

    Args:
        kb_path: Caminho para o arquivo JSON
        data: Dados a serem salvos
        validate: Se deve validar antes de salvar

    Returns:
        True se salvou com sucesso

    Raises:
        KBValidationError: Se validate=True e os dados forem inválidos
    """
    if validate:
        validate_kb_schema(data)

    # Criar diretório pai se não existir
    kb_path.parent.mkdir(parents=True, exist_ok=True)

    with open(kb_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    return True


def merge_kb_entries(
    existing: List[Dict[str, Any]], new_entries: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Mescla novas entradas com as existentes, evitando duplicatas.

    Args:
        existing: Entradas existentes
        new_entries: Novas entradas a serem adicionadas

    Returns:
        Lista mesclada
    """
    merged = existing.copy()

    for new_entry in new_entries:
        # Verificar se já existe uma entrada com os mesmos gatilhos
        is_duplicate = False
        for existing_entry in merged:
            if set(existing_entry["gatilhos"]) == set(new_entry["gatilhos"]):
                is_duplicate = True
                break

        if not is_duplicate:
            merged.append(new_entry)

    return merged
