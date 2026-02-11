"""
Módulo Voice - Sistema de voz (TTS e STT)
Text-to-Speech (Microsoft Edge TTS) e Speech-to-Text (Google)
"""
import asyncio
import edge_tts
import speech_recognition as sr
from pathlib import Path
from typing import Optional

from src.core.config import VoiceConfig
from src.io.audio import get_audio_player
from src.io.serial_comm import get_arduino_controller


class TextToSpeech:
    """Classe para síntese de voz (TTS) usando Microsoft Edge TTS."""

    def __init__(self, voice: str = None, rate: str = None):
        """
        Inicializa o TTS.

        Args:
            voice: Voz a ser usada (padrão: VoiceConfig.VOZ_MASCULINA)
            rate: Taxa de velocidade (padrão: VoiceConfig.VOZ_RATE)
        """
        self.voice = voice or VoiceConfig.VOZ_MASCULINA
        self.rate = rate or VoiceConfig.VOZ_RATE

    async def generate_audio(self, texto: str, output_file: str | Path) -> bool:
        """
        Gera arquivo de áudio a partir de texto.

        Args:
            texto: Texto a ser sintetizado
            output_file: Caminho para salvar o arquivo MP3

        Returns:
            True se gerou com sucesso
        """
        try:
            comunicador = edge_tts.Communicate(texto, self.voice, rate=self.rate)
            await comunicador.save(str(output_file))
            return True
        except Exception as e:
            print(f"❌ Erro no TTS: {e}")
            return False

    def speak(self, texto: str, sync_mouth: bool = True) -> bool:
        """
        Fala um texto (gera áudio + reproduz + sincroniza boca).

        Args:
            texto: Texto a ser falado
            sync_mouth: Se deve sincronizar movimento da boca

        Returns:
            True se falou com sucesso
        """
        print(f"\n[J.O.S.E]: {texto}")

        # Gerar áudio
        audio_file = VoiceConfig.TEMP_AUDIO_FILE
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        success = loop.run_until_complete(self.generate_audio(texto, audio_file))
        loop.close()

        if not success:
            return False

        # Obter controladores
        player = get_audio_player()
        arduino = get_arduino_controller() if sync_mouth else None

        # Abrir boca
        if arduino and arduino.is_connected:
            arduino.mouth_open()

        # Reproduzir áudio
        player.play(audio_file)
        player.wait_until_done()

        # Fechar boca
        if arduino and arduino.is_connected:
            arduino.mouth_close()

        # Limpar arquivo temporário
        player.cleanup(audio_file)

        return True


class SpeechToText:
    """Classe para reconhecimento de voz (STT) usando Google."""

    def __init__(self):
        """Inicializa o reconhecedor."""
        self.recognizer = sr.Recognizer()
        self.recognizer.pause_threshold = VoiceConfig.PAUSE_THRESHOLD
        self.recognizer.energy_threshold = VoiceConfig.ENERGY_THRESHOLD
        self.recognizer.dynamic_energy_threshold = VoiceConfig.DYNAMIC_ENERGY

    def listen(self, timeout: Optional[float] = None) -> Optional[str]:
        """
        Escuta e transcreve áudio do microfone.

        Args:
            timeout: Tempo máximo de espera (None = sem limite)

        Returns:
            Texto transcrito ou None se falhou
        """
        with sr.Microphone() as fonte:
            print("\n[Ouvindo...]")

            # Ajustar para ruído ambiente
            self.recognizer.adjust_for_ambient_noise(fonte, duration=0.5)

            try:
                # Capturar áudio
                audio = self.recognizer.listen(
                    fonte, timeout=timeout, phrase_time_limit=VoiceConfig.PHRASE_TIME_LIMIT
                )

                # Transcrever
                texto = self.recognizer.recognize_google(audio, language=VoiceConfig.LANGUAGE)
                texto_lower = texto.lower()
                print(f"-> Você: {texto}")
                return texto_lower

            except sr.WaitTimeoutError:
                print("⏱️  Timeout: nenhum áudio detectado")
                return None
            except sr.UnknownValueError:
                print("❓ Não entendi o que foi dito")
                return None
            except sr.RequestError as e:
                print(f"❌ Erro no serviço de reconhecimento: {e}")
                return None
            except Exception as e:
                print(f"❌ Erro inesperado no STT: {e}")
                return None


# Instâncias globais
_tts: Optional[TextToSpeech] = None
_stt: Optional[SpeechToText] = None


def get_tts() -> TextToSpeech:
    """
    Retorna a instância global do TTS (singleton).

    Returns:
        Instância do TextToSpeech
    """
    global _tts
    if _tts is None:
        _tts = TextToSpeech()
    return _tts


def get_stt() -> SpeechToText:
    """
    Retorna a instância global do STT (singleton).

    Returns:
        Instância do SpeechToText
    """
    global _stt
    if _stt is None:
        _stt = SpeechToText()
    return _stt


# Funções de conveniência
def falar(texto: str, sync_mouth: bool = True) -> bool:
    """
    Atalho para falar texto.

    Args:
        texto: Texto a ser falado
        sync_mouth: Se deve sincronizar boca

    Returns:
        True se falou com sucesso
    """
    return get_tts().speak(texto, sync_mouth)


def ouvir(timeout: Optional[float] = None) -> Optional[str]:
    """
    Atalho para ouvir e transcrever.

    Args:
        timeout: Tempo máximo de espera

    Returns:
        Texto transcrito ou None
    """
    return get_stt().listen(timeout)
