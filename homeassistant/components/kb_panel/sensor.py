"""KB Panel RFID reader."""
from typing import Callable, List, Text

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity

from .const import DOMAIN
from .kb_panel import KBPanel, KBPanelReader


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: Callable[[List[Entity], bool], None],
) -> None:
    """Set up KB Panel RFID reader devices."""
    panel: KBPanel = hass.data[DOMAIN][entry.entry_id]

    async_add_entities([KBPanelReaderEntity(panel)], True)


class KBPanelReaderEntity(KBPanelReader, Entity):
    """Class for KB Panel Reader Entity."""

    def __init__(self, panel: KBPanel) -> None:
        """Init KB Panel Reader."""
        super().__init__(panel)
        self._callbacks.add(self._new_card)

    @property
    def name(self) -> Text:
        """Return the name of the entity."""
        return "RFID reader"

    @property
    def state(self) -> Text:
        """Return the state of the entity."""
        return "ready"

    def _new_card(self, card_id: Text) -> None:
        self.hass.bus.fire("kb_panel_reader", {"card_id": card_id})
