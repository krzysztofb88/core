"""KB Panel Switch."""
from typing import Any, Callable, List, Text

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity

from .const import DOMAIN
from .kb_panel import BuzzerMode, KBPanel, KBPanelBuzzer


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: Callable[[List[Entity], bool], None],
) -> None:
    """Set up KB Panel light devices."""
    panel: KBPanel = hass.data[DOMAIN][entry.entry_id]

    switches: List[Entity] = [
        KbPanelSwitch(panel),
    ]

    async_add_entities(switches, True)


class KbPanelSwitch(KBPanelBuzzer, SwitchEntity):
    """KB Panel Light."""

    @property
    def name(self) -> Text:
        """Return name of entity."""
        return "Buzzer"

    @property
    def icon(self) -> Text:
        """Return icon name."""
        return "mdi:alarm-bell"

    @property
    def is_on(self) -> bool:
        """Return True if light is on."""
        return self.mode != BuzzerMode.OFF

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on the light."""
        self.mode = BuzzerMode.ON

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off the light."""
        self.mode = BuzzerMode.OFF
