"""KB Panel Lights."""
from typing import Any, Callable, List, Text

from homeassistant.components.light import ATTR_EFFECT, SUPPORT_EFFECT, LightEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity

from .const import DOMAIN
from .kb_panel import KBPanel, KBPanelLED, LEDColor, LEDMode


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: Callable[[List[Entity], bool], None],
) -> None:
    """Set up KB Panel light devices."""
    panel: KBPanel = hass.data[DOMAIN][entry.entry_id]

    lights: List[Entity] = [
        KBPanelLight(panel, LEDColor.GREEN),
        KBPanelLight(panel, LEDColor.ORANGE),
        KBPanelLight(panel, LEDColor.RED),
    ]

    async_add_entities(lights, True)


class KBPanelLight(KBPanelLED, LightEntity):
    """KB Panel Light."""

    def __init__(self, panel, color):
        """Init KB Panel Light."""
        super().__init__(panel, color)

        self._efects_list = [name for name, _ in LEDMode.__members__.items()]

    @property
    def name(self) -> Text:
        """Return name of entity."""
        return f"{self._color.name.capitalize()} LED"

    @property
    def supported_features(self) -> int:
        """Flag supported features."""
        return SUPPORT_EFFECT

    @property
    def effect_list(self):
        """Return the list of supported effects."""
        return self._efects_list

    @property
    def effect(self):
        """Return current effect."""
        return self.mode.name

    @property
    def is_on(self) -> bool:
        """Return True if light is on."""
        return self.mode != LEDMode.OFF

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on the light."""
        effect = kwargs.get(ATTR_EFFECT)

        if effect:
            self.mode = LEDMode[effect]
        else:
            self.mode = LEDMode.ON

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off the light."""
        self.mode = LEDMode.OFF
