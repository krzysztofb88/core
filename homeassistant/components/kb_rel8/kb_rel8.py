"""KB Rel8 modules."""
import serial


class KBRel8:
    """KB Rel8 class."""

    def __init__(self, ip_address: str, device_id: int = 1) -> None:
        """Init KB Rel8."""
        self._ip_address = ip_address
        self._device_id = device_id
        self._status = [
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
        ]

    def status(self, port: int) -> bool:
        """Return status of given port."""
        return self._status[port - 1]

    def on(self, port: int) -> None:
        """On given port."""
        self._set_port(port, 1)
        self._status[port - 1] = True

    def off(self, port: int) -> None:
        """Off given port."""
        self._set_port(port, 0)
        self._status[port - 1] = False

    def _set_port(self, port: int, state: int) -> None:
        command = bytearray(b"\x02\x00")
        command.append(port)
        command.append(state)
        self._send_command(command)

    def _send_command(self, command: bytearray) -> bytearray:
        ser = serial.serial_for_url(f"socket://{self._ip_address}:2000", timeout=1)

        new_command = (
            bytearray(b"\x55\xAA") + self._device_id.to_bytes(1, "big") + command
        )
        new_command.append(self._calc_sum(new_command))

        ser.write(new_command)

    @staticmethod
    def _calc_sum(command: bytearray) -> int:
        calculated_sum = 0
        for i in command:
            calculated_sum += i
        return calculated_sum & 0xFF
