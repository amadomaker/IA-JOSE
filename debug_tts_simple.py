import asyncio
import edge_tts

async def main():
    voice = "pt-BR-AntonioNeural"
    text = "Teste de som do sistema J.O.S.E."
    output = "teste_debug.mp3"
    
    print(f"Tentando gerar áudio com voz: {voice}")
    try:
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output)
        print(f"✅ SUCESSO! Arquivo salvo em {output}")
    except Exception as e:
        print(f"❌ ERRO: {e}")

if __name__ == "__main__":
    asyncio.run(main())
