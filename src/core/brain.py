"""
Módulo Brain - Gerenciamento de memória e knowledge base
Funções para carregar, buscar e salvar conhecimento
"""
import json
import os
from typing import Optional, List, Dict, Any
from pathlib import Path
from datetime import datetime

from src.core.config import KnowledgeBaseConfig


class Brain:
    """
    Classe principal para gerenciamento do knowledge base (cérebro do robô).
    """

    def __init__(self, kb_path: Optional[Path] = None):
        """
        Inicializa o Brain.

        Args:
            kb_path: Caminho para o arquivo JSON do KB (opcional)
        """
        self.kb_path = kb_path or KnowledgeBaseConfig.KB_PATH
        self.memoria: List[Dict[str, Any]] = []
        self.carregar_memoria()

    def carregar_memoria(self) -> List[Dict[str, Any]]:
        """
        Carrega o knowledge base do arquivo JSON.
        Se o arquivo não existir, cria um novo com FAQ inicial.

        Returns:
            Lista de entradas do KB
        """
        if not os.path.exists(self.kb_path):
            print(f"⚠️  KB não encontrado. Criando novo em: {self.kb_path}")
            self._criar_kb_inicial()
            return KnowledgeBaseConfig.FAQ_INICIAL

        try:
            with open(self.kb_path, "r", encoding="utf-8") as f:
                self.memoria = json.load(f)
            print(f"✓ KB carregado: {len(self.memoria)} entradas")
            return self.memoria
        except json.JSONDecodeError as e:
            print(f"❌ Erro ao ler KB: {e}")
            return KnowledgeBaseConfig.FAQ_INICIAL
        except Exception as e:
            print(f"❌ Erro inesperado ao carregar KB: {e}")
            return KnowledgeBaseConfig.FAQ_INICIAL

    def _criar_kb_inicial(self):
        """Cria um arquivo KB inicial vazio."""
        self.kb_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.kb_path, "w", encoding="utf-8") as f:
            json.dump(KnowledgeBaseConfig.FAQ_INICIAL, f, ensure_ascii=False, indent=4)
        self.memoria = KnowledgeBaseConfig.FAQ_INICIAL

    def buscar_resposta(self, pergunta: str) -> Optional[str]:
        """
        Busca uma resposta no knowledge base baseado em gatilhos.

        Args:
            pergunta: Pergunta do usuário (já normalizada)

        Returns:
            Resposta encontrada ou None se não houver match
        """
        pergunta_lower = pergunta.lower().strip()

        for item in self.memoria:
            # Verifica se algum gatilho está contido na pergunta
            if any(gatilho in pergunta_lower for gatilho in item["gatilhos"]):
                return item["resposta"]

        return None

    def salvar_aprendizado(self, nova_pergunta: str, nova_resposta: str) -> bool:
        """
        Salva um novo aprendizado no knowledge base.

        Args:
            nova_pergunta: Pergunta/gatilho a ser adicionado
            nova_resposta: Resposta correspondente

        Returns:
            True se salvou com sucesso, False caso contrário
        """
        try:
            # Criar backup se habilitado
            if KnowledgeBaseConfig.BACKUP_ENABLED:
                self._criar_backup()

            # Criar nova entrada
            nova_entrada = {"gatilhos": [nova_pergunta], "resposta": nova_resposta}

            # Adicionar à memória
            self.memoria.append(nova_entrada)

            # Salvar no arquivo
            with open(self.kb_path, "w", encoding="utf-8") as f:
                json.dump(self.memoria, f, ensure_ascii=False, indent=4)

            print(f"✓ Aprendido: '{nova_pergunta}' -> '{nova_resposta}'")
            return True

        except Exception as e:
            print(f"❌ Erro ao salvar aprendizado: {e}")
            return False

    def _criar_backup(self):
        """Cria um backup do KB atual."""
        if os.path.exists(self.kb_path):
            backup_path = str(self.kb_path) + KnowledgeBaseConfig.BACKUP_SUFFIX
            try:
                with open(self.kb_path, "r", encoding="utf-8") as f:
                    conteudo = f.read()
                with open(backup_path, "w", encoding="utf-8") as f:
                    f.write(conteudo)
            except Exception as e:
                print(f"⚠️  Erro ao criar backup: {e}")

    def obter_estatisticas(self) -> Dict[str, Any]:
        """
        Retorna estatísticas do knowledge base.

        Returns:
            Dicionário com estatísticas
        """
        total_entradas = len(self.memoria)
        total_gatilhos = sum(len(item["gatilhos"]) for item in self.memoria)

        return {
            "total_entradas": total_entradas,
            "total_gatilhos": total_gatilhos,
            "media_gatilhos_por_entrada": (
                round(total_gatilhos / total_entradas, 2) if total_entradas > 0 else 0
            ),
            "kb_path": str(self.kb_path),
            "kb_existe": os.path.exists(self.kb_path),
        }

    def listar_todas_entradas(self) -> List[Dict[str, Any]]:
        """
        Retorna todas as entradas do KB.

        Returns:
            Lista completa de entradas
        """
        return self.memoria.copy()

    def buscar_por_gatilho(self, gatilho: str) -> List[Dict[str, Any]]:
        """
        Busca entradas que contenham um gatilho específico.

        Args:
            gatilho: Gatilho a ser buscado

        Returns:
            Lista de entradas que contêm o gatilho
        """
        gatilho_lower = gatilho.lower()
        resultados = []

        for item in self.memoria:
            if any(gatilho_lower in g.lower() for g in item["gatilhos"]):
                resultados.append(item)

        return resultados


# Instância global (singleton pattern)
_brain_instance: Optional[Brain] = None


def get_brain() -> Brain:
    """
    Retorna a instância global do Brain (singleton).

    Returns:
        Instância do Brain
    """
    global _brain_instance
    if _brain_instance is None:
        _brain_instance = Brain()
    return _brain_instance
