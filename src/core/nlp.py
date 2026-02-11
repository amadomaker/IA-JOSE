"""
Módulo de Processamento de Linguagem Natural (NLP)
Funções para formatação e processamento de texto
"""
from src.core.config import NLPConfig, WakeWordConfig


def formatar_texto_inteligente(texto: str) -> str:
    """
    Formata texto com capitalização inteligente e correção de termos técnicos.

    Transformações:
    - Primeira letra maiúscula
    - Termos técnicos corrigidos (NIED, Unicamp, Arduino, etc.)
    - Adiciona ponto final se não houver pontuação

    Exemplo:
        >>> formatar_texto_inteligente("o nied é legal")
        "O NIED é legal."

    Args:
        texto: Texto a ser formatado

    Returns:
        Texto formatado
    """
    if not texto:
        return ""

    # 1. Primeira letra maiúscula
    texto = texto.strip().capitalize()

    # 2. Correção de Termos Técnicos
    palavras = texto.split()
    novas_palavras = []

    for palavra in palavras:
        # Remove pontuação temporária para checar a palavra
        palavra_limpa = palavra.lower().strip(".,?!")

        if palavra_limpa in NLPConfig.TERM_REPLACEMENTS:
            # Reconstrói a palavra com a grafia correta
            novas_palavras.append(NLPConfig.TERM_REPLACEMENTS[palavra_limpa])
        else:
            novas_palavras.append(palavra)

    texto = " ".join(novas_palavras)

    # 3. Adiciona Ponto Final se não tiver pontuação no fim
    if texto and texto[-1] not in [".", "!", "?", ":"]:
        texto += "."

    return texto


def limpar_wake_word(texto: str, variantes: list = None) -> str:
    """
    Remove a wake word e suas variantes do texto.

    Args:
        texto: Texto contendo a wake word
        variantes: Lista de variantes da wake word (opcional)

    Returns:
        Texto sem a wake word

    Exemplo:
        >>> limpar_wake_word("josé o que é o nied")
        "o que é o nied"
    """
    if variantes is None:
        variantes = WakeWordConfig.VARIANTES_NOME

    texto_limpo = texto.lower()

    # Remove todas as variações do nome
    for variante in variantes:
        texto_limpo = texto_limpo.replace(variante, "")

    return texto_limpo.strip()


def detectar_wake_word(texto: str, variantes: list = None) -> bool:
    """
    Detecta se a wake word está presente no texto.

    Args:
        texto: Texto a ser verificado
        variantes: Lista de variantes da wake word (opcional)

    Returns:
        True se a wake word foi detectada, False caso contrário

    Exemplo:
        >>> detectar_wake_word("josé o que é o nied")
        True
        >>> detectar_wake_word("o que é o nied")
        False
    """
    if variantes is None:
        variantes = WakeWordConfig.VARIANTES_NOME

    texto_lower = texto.lower()
    return any(variante in texto_lower for variante in variantes)


def extrair_pergunta(texto: str) -> str:
    """
    Extrai a pergunta do texto, removendo a wake word e formatando.

    Args:
        texto: Texto completo com wake word

    Returns:
        Pergunta limpa e formatada

    Exemplo:
        >>> extrair_pergunta("josé o que é o nied")
        "o que é o nied"
    """
    pergunta = limpar_wake_word(texto)

    # Remove espaços extras
    pergunta = " ".join(pergunta.split())

    return pergunta.strip()


def normalizar_texto(texto: str) -> str:
    """
    Normaliza texto para comparação (lowercase, sem pontuação extra).

    Args:
        texto: Texto a ser normalizado

    Returns:
        Texto normalizado

    Exemplo:
        >>> normalizar_texto("O que é o NIED?")
        "o que é o nied"
    """
    # Lowercase
    texto = texto.lower()

    # Remove pontuação no final
    texto = texto.strip(".,?!:;")

    # Remove espaços extras
    texto = " ".join(texto.split())

    return texto
