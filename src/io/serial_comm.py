"""
Módulo Serial Communication - Comunicação com Arduino
Controle de atuadores via porta serial
"""
import serial
import time
from typing import Optional

from src.core.config import SerialConfig


class ArduinoController:
    """Controlador de comunicação serial com Arduino."""

    def __init__(self, port: str = None, baud_rate: int = None):
        """
        Inicializa o controlador.

        Args:
            port: Porta serial (padrão: SerialConfig.PORT)
            baud_rate: Taxa de transmissão (padrão: SerialConfig.BAUD_RATE)
        """
        self.port = port or SerialConfig.PORT
        self.baud_rate = baud_rate or SerialConfig.BAUD_RATE
        self.connection: Optional[serial.Serial] = None
        self._is_connected = False

    def connect(self) -> bool:
        """
        Conecta ao Arduino.

        Returns:
            True se conectou com sucesso
        """
        try:
            self.connection = serial.Serial(
                self.port, self.baud_rate, timeout=SerialConfig.TIMEOUT
            )
            time.sleep(SerialConfig.CONNECT_DELAY)
            self._is_connected = True
            print(f"✓ Sistema Nervoso (Arduino) Online na porta {self.port}.")
            return True
        except Exception as e:
            print(f"! Modo Simulação: Atuadores de boca offline. ({e})")
            self._is_connected = False
            return False

    def disconnect(self):
        """Desconecta do Arduino."""
        if self.connection:
            try:
                self.connection.close()
            except:
                pass
            self._is_connected = False

    def mouth_open(self) -> bool:
        """
        Envia comando para abrir a boca.

        Returns:
            True se enviou com sucesso
        """
        return self._send_command(SerialConfig.CMD_MOUTH_OPEN)

    def mouth_close(self) -> bool:
        """
        Envia comando para fechar a boca.

        Returns:
            True se enviou com sucesso
        """
        return self._send_command(SerialConfig.CMD_MOUTH_CLOSE)

    def _send_command(self, command: bytes) -> bool:
        """
        Envia um comando via serial.

        Args:
            command: Comando em bytes

        Returns:
            True se enviou com sucesso
        """
        if not self._is_connected or not self.connection:
            return False

        try:
            self.connection.write(command)
            return True
        except Exception as e:
            print(f"⚠️  Erro ao enviar comando serial: {e}")
            return False

    @property
    def is_connected(self) -> bool:
        """Retorna se está conectado ao Arduino."""
        return self._is_connected

    def __enter__(self):
        """Context manager: conecta ao entrar."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager: desconecta ao sair."""
        self.disconnect()


# Instância global
_arduino_controller: Optional[ArduinoController] = None


def get_arduino_controller() -> ArduinoController:
    """
    Retorna a instância global do ArduinoController (singleton).

    Returns:
        Instância do ArduinoController
    """
    global _arduino_controller
    if _arduino_controller is None:
        _arduino_controller = ArduinoController()
        _arduino_controller.connect()
    return _arduino_controller
