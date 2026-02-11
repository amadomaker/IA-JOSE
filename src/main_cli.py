"""
J.O.S.E - Jovem Orientador de Soluções Educacionais
Versão CLI refatorada usando módulos

Este é o script principal que mantém a funcionalidade original,
mas agora usa os módulos refatorados.
"""
from src.core.brain import get_brain
from src.core.nlp import detectar_wake_word, extrair_pergunta
from src.io.voice import falar, ouvir
from src.kb.learner import modo_aprendizado_sync


def main():
    """Loop principal do sistema."""

    # Inicializar componentes
    brain = get_brain()

    # Mensagem de boas-vindas
    falar(
        "Olá! Sou o José, Jovem Orientador de Soluções Educacionais. "
        "Estou pronto para ajudar!"
    )

    # Loop principal
    while True:
        # Ouvir entrada do usuário
        entrada_usuario = ouvir()

        if not entrada_usuario:
            continue

        # Verificar wake word
        if not detectar_wake_word(entrada_usuario):
            continue

        # Extrair pergunta (sem wake word)
        pergunta_limpa = extrair_pergunta(entrada_usuario)

        # Verificar se é comando de saída
        if any(
            x in entrada_usuario
            for x in [
                "sair",
                "tchau",
                "desligar",
                "até logo",
                "falo josé",
                "falou josé",
                "encerrar josé",
            ]
        ):
            falar("Até logo! Foi um prazer ajudar!")
            break

        # Verificar se pergunta é muito curta
        if len(pergunta_limpa) < 2:
            falar("Estou ouvindo.")
            continue

        # Buscar resposta no KB
        resposta = brain.buscar_resposta(pergunta_limpa)

        if resposta:
            # Resposta encontrada
            falar(resposta)
        else:
            # Modo aprendizado
            modo_aprendizado_sync(
                pergunta_desconhecida=pergunta_limpa,
                falar_func=falar,
                ouvir_func=ouvir,
                salvar_func=brain.salvar_aprendizado,
            )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Encerrando J.O.S.E...")
        falar("Até logo!")
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")
        import traceback

        traceback.print_exc()
