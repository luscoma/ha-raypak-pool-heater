"""Climate platform for the Raypak Pool Heater integration."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityFeature,
    HVACAction,
    HVACMode,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_TEMPERATURE, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .api import RaypakApiError
from .const import DOMAIN, KEY_AVG_INLET, KEY_HEATER_ON_OFF, KEY_SETPOINT
from .coordinator import RaypakDataCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Raypak climate entity from a config entry."""
    coordinator: RaypakDataCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([RaypakClimateEntity(coordinator, entry)])


class RaypakClimateEntity(CoordinatorEntity[RaypakDataCoordinator], ClimateEntity):
    """Climate entity for the Raypak pool heater."""

    _attr_has_entity_name = True
    _attr_name = "Thermostat"
    _attr_temperature_unit = UnitOfTemperature.FAHRENHEIT
    _attr_hvac_modes = [HVACMode.HEAT, HVACMode.OFF]
    _attr_supported_features = ClimateEntityFeature.TARGET_TEMPERATURE
    _attr_min_temp = 50
    _attr_max_temp = 104
    _attr_target_temperature_step = 1
    _attr_icon = "mdi:pool-thermometer"
    _enable_turn_on_off_backwards_compatibility = False

    def __init__(
        self,
        coordinator: RaypakDataCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialise the climate entity."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_climate"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "Raypak Pool Heater",
            "manufacturer": "Raypak",
            "model": "Raymote",
        }

    @property
    def current_temperature(self) -> float | None:
        """Return the average inlet temperature as the current temperature."""
        if self.coordinator.data is None:
            return None
        val = self.coordinator.data.get(KEY_AVG_INLET)
        if val is None:
            return None
        try:
            return float(val)
        except (ValueError, TypeError):
            return None

    @property
    def target_temperature(self) -> float | None:
        """Return the current setpoint."""
        if self.coordinator.data is None:
            return None
        val = self.coordinator.data.get(KEY_SETPOINT)
        if val is None:
            return None
        try:
            return float(val)
        except (ValueError, TypeError):
            return None

    @property
    def hvac_mode(self) -> HVACMode:
        """Return the current HVAC mode."""
        if self.coordinator.data is None:
            return HVACMode.OFF
        val = self.coordinator.data.get(KEY_HEATER_ON_OFF)
        try:
            return HVACMode.HEAT if int(val) == 1 else HVACMode.OFF
        except (ValueError, TypeError):
            return HVACMode.OFF

    @property
    def hvac_action(self) -> HVACAction | None:
        """Return the current HVAC action (heating or idle)."""
        if self.coordinator.data is None:
            return None
        status = self.coordinator.data.get("v55", "")
        if isinstance(status, str) and status.lower() == "heating":
            return HVACAction.HEATING
        val = self.coordinator.data.get(KEY_HEATER_ON_OFF)
        try:
            return HVACAction.IDLE if int(val) == 1 else HVACAction.OFF
        except (ValueError, TypeError):
            return HVACAction.OFF

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set the HVAC mode (heat or off)."""
        try:
            if hvac_mode == HVACMode.HEAT:
                await self.coordinator.client.async_set_heater(True)
            else:
                await self.coordinator.client.async_set_heater(False)
        except RaypakApiError as err:
            _LOGGER.error("Failed to set HVAC mode: %s", err)
            return
        await self.coordinator.async_request_refresh()

    async def async_set_temperature(self, **kwargs: Any) -> None:
        """Set the target temperature."""
        temp = kwargs.get(ATTR_TEMPERATURE)
        if temp is None:
            return
        try:
            await self.coordinator.client.async_set_temperature(int(temp))
        except RaypakApiError as err:
            _LOGGER.error("Failed to set temperature: %s", err)
            return
        await self.coordinator.async_request_refresh()
