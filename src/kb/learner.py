"""
Módulo Learner - Modo aprendizado interativo
Gerencia o processo de ensinar novas respostas ao robô
"""
from typing import Optional, Callable
from enum import Enum

from src.core.nlp import formatar_texto_inteligente


class LearningState(Enum):
    """Estados do processo de aprendizado."""

    WAITING_ANSWER = "waiting_answer"
    WAITING_CONFIRMATION = "waiting_confirmation"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class LearningSession:
    """
    Classe para gerenciar uma sessão de aprendizado.

    Fluxo:
    1. Usuário faz pergunta desconhecida
    2. Sistema pede a resposta
    3. Usuário fornece resposta
    4. Sistema formata e pede confirmação
    5. Usuário confirma ou cancela
    6. Sistema salva (se confirmado)
    """

    def __init__(self, pergunta_desconhecida: str):
        """
        Inicializa uma sessão de aprendizado.

        Args:
            pergunta_desconhecida: Pergunta que não foi encontrada no KB
        """
        self.pergunta = pergunta_desconhecida
        self.resposta_bruta: Optional[str] = None
        self.resposta_formatada: Optional[str] = None
        self.state = LearningState.WAITING_ANSWER

    def processar_resposta(self, resposta: str) -> tuple[str, LearningState]:
        """
        Processa a resposta fornecida pelo usuário.

        Args:
            resposta: Resposta fornecida

        Returns:
            Tupla (mensagem_para_usuario, novo_estado)
        """
        # Verificar cancelamento
        if any(x in resposta.lower() for x in ["cancelar", "esquece", "sair"]):
            self.state = LearningState.CANCELLED
            return ("Operação cancelada.", LearningState.CANCELLED)

        # Validar tamanho mínimo
        if len(resposta.strip()) < 3:
            return (
                "Resposta muito curta. Por favor, forneça uma resposta mais completa.",
                self.state,
            )

        # Formatar resposta
        self.resposta_bruta = resposta
        self.resposta_formatada = formatar_texto_inteligente(resposta)

        # Pedir confirmação
        self.state = LearningState.WAITING_CONFIRMATION
        mensagem = (
            f"Entendi. A resposta será: '{self.resposta_formatada}'. Posso salvar?"
        )

        return (mensagem, self.state)

    def processar_confirmacao(self, confirmacao: str) -> tuple[str, LearningState]:
        """
        Processa a confirmação do usuário.

        Args:
            confirmacao: Confirmação fornecida

        Returns:
            Tupla (mensagem_para_usuario, novo_estado)
        """
        confirmacao_lower = confirmacao.lower()

        # Cancelamento
        if any(x in confirmacao_lower for x in ["cancelar", "esquece"]):
            self.state = LearningState.CANCELLED
            return ("Entendido. Cancelei.", LearningState.CANCELLED)

        # Negação (voltar para esperar resposta)
        if "não" in confirmacao_lower and "cancelar" not in confirmacao_lower:
            self.state = LearningState.WAITING_ANSWER
            return ("Ok, diga a resposta correta novamente.", LearningState.WAITING_ANSWER)

        # Confirmação
        if any(x in confirmacao_lower for x in ["sim", "pode", "ok", "claro", "isso"]):
            self.state = LearningState.COMPLETED
            return ("Perfeito! Informação salva.", LearningState.COMPLETED)

        # Resposta ambígua
        return (
            "Diga 'sim' para gravar ou 'cancelar' para desistir.",
            self.state,
        )

    def get_learning_data(self) -> Optional[tuple[str, str]]:
        """
        Retorna os dados de aprendizado se a sessão foi completada.

        Returns:
            Tupla (pergunta, resposta) ou None se não completado
        """
        if self.state == LearningState.COMPLETED and self.resposta_formatada:
            return (self.pergunta, self.resposta_formatada)
        return None


def modo_aprendizado_sync(
    pergunta_desconhecida: str,
    falar_func: Callable[[str], None],
    ouvir_func: Callable[[], Optional[str]],
    salvar_func: Callable[[str, str], bool],
) -> bool:
    """
    Executa o modo aprendizado de forma síncrona (para CLI).

    Args:
        pergunta_desconhecida: Pergunta que não foi encontrada
        falar_func: Função para falar (TTS)
        ouvir_func: Função para ouvir (STT)
        salvar_func: Função para salvar no KB

    Returns:
        True se aprendizado foi concluído, False se cancelado
    """
    session = LearningSession(pergunta_desconhecida)

    # Mensagem inicial
    falar_func(
        f"Eu não sei sobre '{pergunta_desconhecida}'. "
        "O que devo responder? (Diga 'cancelar' para sair)"
    )

    while True:
        if session.state == LearningState.WAITING_ANSWER:
            resposta_ensino = ouvir_func()

            if not resposta_ensino:
                falar_func("Não ouvi a resposta. Repita ou diga 'cancelar'.")
                continue

            mensagem, novo_estado = session.processar_resposta(resposta_ensino)
            falar_func(mensagem)

            if novo_estado == LearningState.CANCELLED:
                return False

        elif session.state == LearningState.WAITING_CONFIRMATION:
            confirmacao = ouvir_func()

            if not confirmacao:
                falar_func("Não ouvi. Diga 'sim' ou 'cancelar'.")
                continue

            mensagem, novo_estado = session.processar_confirmacao(confirmacao)
            falar_func(mensagem)

            if novo_estado == LearningState.COMPLETED:
                # Salvar aprendizado
                dados = session.get_learning_data()
                if dados:
                    pergunta, resposta = dados
                    return salvar_func(pergunta, resposta)
                return False

            elif novo_estado == LearningState.CANCELLED:
                return False

        else:
            break

    return False
