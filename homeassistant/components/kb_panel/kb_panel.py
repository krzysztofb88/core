"""Module for KB Panel."""
from enum import Enum
import threading
from typing import Callable, Set, Text

import serial


class LEDColor(Enum):
    """Enum class with led collors."""

    GREEN = 0
    ORANGE = 1
    RED = 2


class LEDMode(Enum):
    """Enum class with led modes."""

    OFF = ord("0")
    ON = ord("1")
    BLINK = ord("2")


class BuzzerMode(Enum):
    """Enum class with buzzer modes."""

    OFF = ord("0")
    ON = ord("1")
    SHORT = ord("2")
    LONG = ord("3")
    CONTINUOS_PULSE = ord("4")


class KBPanel(threading.Thread):
    """Main class of KB Panel."""

    STX = b"\x02"
    ETX = b"\x03"

    def __init__(self, port: Text) -> None:
        """Init KB Panel."""
        threading.Thread.__init__(self, daemon=True)
        self._port = serial.Serial(port, 19200)
        self._status = bytearray(b"0000")
        self._callbacks: Set[Callable[[Text], None]] = set()

        self.start()

    def set_led_mode(self, led: LEDColor, mode: LEDMode) -> None:
        """Set mode for chosen led."""
        msg = bytearray(b"XXXX")
        msg[led.value] = mode.value
        self._status[led.value] = mode.value
        self._change_state(msg)

    def set_buzzer_mode(self, mode: BuzzerMode) -> None:
        """Set mode for buzzer."""
        msg = bytearray(b"XXXX")
        msg[3] = mode.value
        self._status[3] = mode.value
        self._change_state(msg)

    def get_led_mode(self, led: LEDColor) -> LEDMode:
        """Return mode for given led."""
        return LEDMode(self._status[led.value])

    def get_buzzer_mode(self) -> BuzzerMode:
        """Return mode for buzzer."""
        return BuzzerMode(self._status[3])

    def add_callback(self, callback: Callable[[Text], None]) -> None:
        """Add callback to list."""
        self._callbacks.add(callback)

    def run(self) -> None:
        """Serve main loop."""
        self._request_status()
        buffer = b""
        while True:
            buffer += self._port.read()
            stx_pos = buffer.find(self.STX)

            if stx_pos > 0:
                buffer = buffer[stx_pos:]

            etx_pos = buffer.find(self.ETX)

            if etx_pos > 0:
                msg = buffer[: etx_pos + 1]
                buffer = buffer[etx_pos + 1 :]
                self._process_msg(msg)

    def _process_msg(self, msg: bytes) -> None:
        if msg[1] == ord("S") and len(msg) == 7:
            self._status = bytearray(msg[2:6])

        elif msg[1] == ord("C") and len(msg) == 11:
            card_id = msg[2:10].decode()
            for callback in self._callbacks:
                callback(card_id)

    def _change_state(self, cmd: bytearray) -> None:
        msg = b"" + self.STX + cmd + self.ETX
        self._port.write(msg)

    def _request_status(self) -> None:
        msg = b"" + self.STX + b"S" + self.ETX
        self._port.write(msg)


class KBPanelLED:
    """Class for KP Panel LED."""

    def __init__(self, panel: KBPanel, color: LEDColor) -> None:
        """Init KB Panel LED."""
        super().__init__()

        self._color = color
        self._panel = panel

    @property
    def mode(self) -> LEDMode:
        """Property for led mode."""
        return self._panel.get_led_mode(self._color)

    @mode.setter
    def mode(self, mode: LEDMode) -> None:
        """Setter for led mode."""
        self._panel.set_led_mode(self._color, mode)


class KBPanelBuzzer:
    """Class for KB Panel Buzzer."""

    def __init__(self, panel: KBPanel) -> None:
        """Init KB Panel Buzzer."""
        super().__init__()

        self._panel = panel

    @property
    def mode(self) -> BuzzerMode:
        """Property for buzzer mode."""
        return self._panel.get_buzzer_mode()

    @mode.setter
    def mode(self, mode: LEDMode) -> None:
        """Setter for buzzer mode."""
        self._panel.set_buzzer_mode(mode)


class KBPanelReader:
    """Class for KB Panel Reader."""

    def __init__(self, panel: KBPanel) -> None:
        """Init KB Panel Reader."""
        super().__init__()

        self._callbacks: Set[Callable[[Text], None]] = set()
        panel.add_callback(self._new_value)

    def _new_value(self, card_id: Text) -> None:
        for callback in self._callbacks:
            callback(card_id)
