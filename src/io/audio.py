"""
Módulo Audio - Gerenciamento de reprodução de áudio
Wrapper para pygame.mixer com funcionalidades específicas do projeto
"""
import pygame
import time
import os
from pathlib import Path
from typing import Optional


class AudioPlayer:
    """Gerenciador de reprodução de áudio."""

    def __init__(self):
        """Inicializa o mixer do pygame."""
        pygame.mixer.init()
        self._is_playing = False

    def play(self, file_path: str | Path) -> bool:
        """
        Reproduz um arquivo de áudio.

        Args:
            file_path: Caminho para o arquivo de áudio

        Returns:
            True se reproduziu com sucesso
        """
        try:
            pygame.mixer.music.load(str(file_path))
            pygame.mixer.music.play()
            self._is_playing = True
            return True
        except Exception as e:
            print(f"❌ Erro ao reproduzir áudio: {e}")
            return False

    def wait_until_done(self, check_interval: float = 0.05):
        """
        Aguarda até o áudio terminar de tocar.

        Args:
            check_interval: Intervalo de verificação em segundos
        """
        while pygame.mixer.music.get_busy():
            time.sleep(check_interval)
        self._is_playing = False

    def stop(self):
        """Para a reprodução do áudio."""
        pygame.mixer.music.stop()
        self._is_playing = False

    def unload(self):
        """Descarrega o áudio da memória."""
        try:
            pygame.mixer.music.unload()
        except:
            pass

    def cleanup(self, file_path: str | Path):
        """
        Remove arquivo de áudio temporário.

        Args:
            file_path: Caminho para o arquivo a ser removido
        """
        self.unload()
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"⚠️  Erro ao remover arquivo temporário: {e}")

    @property
    def is_playing(self) -> bool:
        """Retorna se está tocando áudio."""
        return self._is_playing


# Instância global
_audio_player: Optional[AudioPlayer] = None


def get_audio_player() -> AudioPlayer:
    """
    Retorna a instância global do AudioPlayer (singleton).

    Returns:
        Instância do AudioPlayer
    """
    global _audio_player
    if _audio_player is None:
        _audio_player = AudioPlayer()
    return _audio_player
