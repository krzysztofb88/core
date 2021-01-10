"""KB Rel8 Switch."""
from typing import Any, Callable, List, Text

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity

from .const import DOMAIN
from .kb_rel8 import KBRel8


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: Callable[[List[Entity], bool], None],
) -> None:
    """Set up KB Rel8 switch devices."""
    kb_rel8: KBRel8 = hass.data[DOMAIN][entry.entry_id]

    switches: List[Entity] = [
        KbRel8Switch(kb_rel8, 1),
        KbRel8Switch(kb_rel8, 2),
        KbRel8Switch(kb_rel8, 3),
        KbRel8Switch(kb_rel8, 4),
        KbRel8Switch(kb_rel8, 5),
        KbRel8Switch(kb_rel8, 6),
        KbRel8Switch(kb_rel8, 7),
        KbRel8Switch(kb_rel8, 8),
    ]

    async_add_entities(switches, True)


class KbRel8Switch(SwitchEntity):
    """KB Rel8 switch."""

    def __init__(self, kb_rel8: KBRel8, port: int) -> None:
        """Init KB Rel8."""
        self._kb_rel8 = kb_rel8
        self._port = port

    @property
    def name(self) -> Text:
        """Return name of entity."""
        return f"Relay {self._port}"

    @property
    def is_on(self) -> bool:
        """Return True if switch is on."""
        return self._kb_rel8.status(self._port)

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on the switch."""
        self._kb_rel8.on(self._port)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off the switch."""
        self._kb_rel8.off(self._port)
