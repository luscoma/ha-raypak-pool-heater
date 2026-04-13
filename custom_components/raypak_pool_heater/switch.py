"""Switch platform for the Raypak Pool Heater integration."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.switch import SwitchDeviceClass, SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .api import RaypakApiError
from .const import DOMAIN, KEY_HEATER_ON_OFF
from .coordinator import RaypakDataCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Raypak heater switch from a config entry."""
    coordinator: RaypakDataCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([RaypakHeaterSwitch(coordinator, entry)])


class RaypakHeaterSwitch(CoordinatorEntity[RaypakDataCoordinator], SwitchEntity):
    """Switch to turn the Raypak pool heater on or off."""

    _attr_has_entity_name = True
    _attr_name = "Heater"
    _attr_device_class = SwitchDeviceClass.SWITCH
    _attr_icon = "mdi:water-boiler"

    def __init__(
        self,
        coordinator: RaypakDataCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialise the switch."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_heater_switch"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "Raypak Pool Heater",
            "manufacturer": "Raypak",
            "model": "Raymote",
        }

    @property
    def is_on(self) -> bool | None:
        """Return True if the heater is on."""
        if self.coordinator.data is None:
            return None
        val = self.coordinator.data.get(KEY_HEATER_ON_OFF)
        if val is None:
            return None
        try:
            return int(val) == 1
        except (ValueError, TypeError):
            return None

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the heater on."""
        try:
            await self.coordinator.client.async_set_heater(True)
        except RaypakApiError as err:
            _LOGGER.error("Failed to turn on heater: %s", err)
            return
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the heater off."""
        try:
            await self.coordinator.client.async_set_heater(False)
        except RaypakApiError as err:
            _LOGGER.error("Failed to turn off heater: %s", err)
            return
        await self.coordinator.async_request_refresh()
