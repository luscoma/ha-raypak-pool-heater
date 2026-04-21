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
from .const import DOMAIN, HEAT_MODE_OFF, HEAT_MODE_POOL, HEAT_MODE_SPA, KEY_HEAT_MODE
from .coordinator import RaypakDataCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Raypak heater switches from a config entry."""
    coordinator: RaypakDataCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        RaypakHeaterSwitch(coordinator, entry),
        RaypakSpaSwitch(coordinator, entry),
    ])


class RaypakHeaterSwitch(CoordinatorEntity[RaypakDataCoordinator], SwitchEntity):
    """Switch to turn the Raypak pool heater on (Pool mode) or off.

    Uses v53 AVIA Heat Mode enum: 0=Off, 1=Pool, 2=Spa, 3=T Spa.
    Turning on sets Pool mode (v53=1); turning off sets Off (v53=0).
    """

    _attr_has_entity_name = True
    _attr_name = "Pool Heater"
    _attr_device_class = SwitchDeviceClass.SWITCH
    _attr_icon = "mdi:water-boiler"

    def __init__(
        self,
        coordinator: RaypakDataCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialise the switch."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_pool_heater_switch"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "Raypak Pool Heater",
            "manufacturer": "Raypak",
            "model": "Raymote",
        }

    @property
    def is_on(self) -> bool | None:
        """Return True if pool heat mode is active (v53 == 1)."""
        if self.coordinator.data is None:
            return None
        val = self.coordinator.data.get(KEY_HEAT_MODE)
        try:
            return int(val) == HEAT_MODE_POOL
        except (ValueError, TypeError):
            return None

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Set heat mode to Pool (v53=1)."""
        try:
            await self.coordinator.client.async_set_heat_mode(HEAT_MODE_POOL)
        except RaypakApiError as err:
            _LOGGER.error("Failed to turn on pool heater: %s", err)
            return
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Set heat mode to Off (v53=0)."""
        try:
            await self.coordinator.client.async_set_heat_mode(HEAT_MODE_OFF)
        except RaypakApiError as err:
            _LOGGER.error("Failed to turn off pool heater: %s", err)
            return
        await self.coordinator.async_request_refresh()


class RaypakSpaSwitch(CoordinatorEntity[RaypakDataCoordinator], SwitchEntity):
    """Switch to turn the Raypak heater on in Spa mode or off.

    Uses v53 AVIA Heat Mode enum: 0=Off, 1=Pool, 2=Spa.
    Turning on sets Spa mode (v53=2); turning off sets Off (v53=0).
    Disabled by default — enable if a spa is connected.
    """

    _attr_has_entity_name = True
    _attr_name = "Spa Heater"
    _attr_device_class = SwitchDeviceClass.SWITCH
    _attr_icon = "mdi:hot-tub"
    _attr_entity_registry_enabled_default = False

    def __init__(
        self,
        coordinator: RaypakDataCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialise the spa switch."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_spa_heater_switch"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "Raypak Pool Heater",
            "manufacturer": "Raypak",
            "model": "Raymote",
        }

    @property
    def is_on(self) -> bool | None:
        """Return True if spa heat mode is active (v53 == 2)."""
        if self.coordinator.data is None:
            return None
        val = self.coordinator.data.get(KEY_HEAT_MODE)
        try:
            return int(val) == HEAT_MODE_SPA
        except (ValueError, TypeError):
            return None

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Set heat mode to Spa (v53=2)."""
        try:
            await self.coordinator.client.async_set_heat_mode(HEAT_MODE_SPA)
        except RaypakApiError as err:
            _LOGGER.error("Failed to turn on spa heater: %s", err)
            return
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Set heat mode to Off (v53=0)."""
        try:
            await self.coordinator.client.async_set_heat_mode(HEAT_MODE_OFF)
        except RaypakApiError as err:
            _LOGGER.error("Failed to turn off spa heater: %s", err)
            return
        await self.coordinator.async_request_refresh()
