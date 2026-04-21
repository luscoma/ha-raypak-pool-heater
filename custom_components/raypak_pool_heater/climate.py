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
from .const import (
    AVIA_STATUS,
    DOMAIN,
    HEAT_MODE_OFF,
    HEAT_MODE_POOL,
    HEAT_MODE_SPA,
    KEY_AVIA_STATUS,
    KEY_AVG_INLET,
    KEY_HEAT_MODE,
    KEY_SETPOINT,
    KEY_SPA_SETPOINT,
)
from .coordinator import RaypakDataCoordinator

_LOGGER = logging.getLogger(__name__)

# AVIA Status codes that map to specific HVAC actions
_AVIA_HEATING_STATES = {4}          # Heating
_AVIA_PREHEATING_STATES = {2, 3}    # Pre-Purge, Spark
_AVIA_COOLDOWN_STATES = {5}         # Post-Purge
_AVIA_FAULT_STATES = {9}            # Check Heater


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Raypak climate entities from a config entry."""
    coordinator: RaypakDataCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        RaypakClimateEntity(coordinator, entry),
        RaypakSpaClimateEntity(coordinator, entry),
    ])


class RaypakClimateEntity(CoordinatorEntity[RaypakDataCoordinator], ClimateEntity):
    """Climate entity for the Raypak pool heater."""

    _attr_has_entity_name = True
    _attr_name = "Pool Thermostat"
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
        """Return the AVIA average inlet temperature as the current pool temperature."""
        if self.coordinator.data is None:
            return None
        val = self.coordinator.data.get(KEY_AVG_INLET)
        try:
            return float(val)
        except (ValueError, TypeError):
            return None

    @property
    def target_temperature(self) -> float | None:
        """Return the current pool setpoint."""
        if self.coordinator.data is None:
            return None
        val = self.coordinator.data.get(KEY_SETPOINT)
        try:
            return float(val)
        except (ValueError, TypeError):
            return None

    @property
    def hvac_mode(self) -> HVACMode:
        """Return HEAT if pool mode is active, OFF otherwise."""
        if self.coordinator.data is None:
            return HVACMode.OFF
        val = self.coordinator.data.get(KEY_HEAT_MODE)
        try:
            return HVACMode.HEAT if int(val) == HEAT_MODE_POOL else HVACMode.OFF
        except (ValueError, TypeError):
            return HVACMode.OFF

    @property
    def hvac_action(self) -> HVACAction | None:
        """Return the granular HVAC action using the AVIA Status enum (v65).

        AVIA Status codes:
          0 = Initialization
          1 = No Demand   → OFF
          2 = Pre-Purge   → PREHEATING
          3 = Spark       → PREHEATING
          4 = Heating     → HEATING
          5 = Post-Purge  → IDLE (cooldown)
          6 = Waiting Water → IDLE
          9 = Check Heater  → (treat as IDLE; fault visible on Fault Code sensor)
        """
        if self.coordinator.data is None:
            return None

        avia_status = self.coordinator.data.get(KEY_AVIA_STATUS)
        try:
            code = int(avia_status)
        except (ValueError, TypeError):
            return None

        if code in _AVIA_HEATING_STATES:
            return HVACAction.HEATING
        if code in _AVIA_PREHEATING_STATES:
            return HVACAction.PREHEATING
        if code in _AVIA_COOLDOWN_STATES or code == 6:
            return HVACAction.IDLE
        # No Demand (1) or Initialization (0) or Check Heater (9)
        return HVACAction.OFF

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Expose the AVIA status name as an extra attribute."""
        attrs: dict[str, Any] = {}
        if self.coordinator.data:
            code = self.coordinator.data.get(KEY_AVIA_STATUS)
            try:
                attrs["avia_status"] = AVIA_STATUS.get(int(code), f"Unknown ({code})")
            except (ValueError, TypeError):
                pass
        return attrs

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set heat mode: HEAT → Pool (v53=1), OFF → Off (v53=0)."""
        try:
            if hvac_mode == HVACMode.HEAT:
                await self.coordinator.client.async_set_heat_mode(HEAT_MODE_POOL)
            else:
                await self.coordinator.client.async_set_heat_mode(HEAT_MODE_OFF)
        except RaypakApiError as err:
            _LOGGER.error("Failed to set HVAC mode: %s", err)
            return
        await self.coordinator.async_request_refresh()

    async def async_set_temperature(self, **kwargs: Any) -> None:
        """Set the pool target temperature."""
        temp = kwargs.get(ATTR_TEMPERATURE)
        if temp is None:
            return
        try:
            await self.coordinator.client.async_set_temperature(int(temp))
        except RaypakApiError as err:
            _LOGGER.error("Failed to set temperature: %s", err)
            return
        await self.coordinator.async_request_refresh()


class RaypakSpaClimateEntity(CoordinatorEntity[RaypakDataCoordinator], ClimateEntity):
    """Climate entity for the Raypak spa mode.

    Disabled by default. Enable this entity (along with the spa sensors) if
    your heater is connected to a spa. When active it drives v53=2 (Spa mode)
    and writes the target temperature to v43 (Spa Setpoint).
    """

    _attr_has_entity_name = True
    _attr_name = "Spa Thermostat"
    _attr_temperature_unit = UnitOfTemperature.FAHRENHEIT
    _attr_hvac_modes = [HVACMode.HEAT, HVACMode.OFF]
    _attr_supported_features = ClimateEntityFeature.TARGET_TEMPERATURE
    _attr_min_temp = 50
    _attr_max_temp = 104
    _attr_target_temperature_step = 1
    _attr_icon = "mdi:hot-tub"
    _attr_entity_registry_enabled_default = False
    _enable_turn_on_off_backwards_compatibility = False

    def __init__(
        self,
        coordinator: RaypakDataCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialise the spa climate entity."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_climate_spa"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "Raypak Pool Heater",
            "manufacturer": "Raypak",
            "model": "Raymote",
        }

    @property
    def current_temperature(self) -> float | None:
        """Return the AVIA average inlet temperature as the current water temperature."""
        if self.coordinator.data is None:
            return None
        val = self.coordinator.data.get(KEY_AVG_INLET)
        try:
            return float(val)
        except (ValueError, TypeError):
            return None

    @property
    def target_temperature(self) -> float | None:
        """Return the current spa setpoint (v43)."""
        if self.coordinator.data is None:
            return None
        val = self.coordinator.data.get(KEY_SPA_SETPOINT)
        try:
            return float(val)
        except (ValueError, TypeError):
            return None

    @property
    def hvac_mode(self) -> HVACMode:
        """Return HEAT if spa mode is active (v53=2), OFF otherwise."""
        if self.coordinator.data is None:
            return HVACMode.OFF
        val = self.coordinator.data.get(KEY_HEAT_MODE)
        try:
            return HVACMode.HEAT if int(val) == HEAT_MODE_SPA else HVACMode.OFF
        except (ValueError, TypeError):
            return HVACMode.OFF

    @property
    def hvac_action(self) -> HVACAction | None:
        """Return the granular HVAC action using the AVIA Status enum (v65)."""
        if self.coordinator.data is None:
            return None

        avia_status = self.coordinator.data.get(KEY_AVIA_STATUS)
        try:
            code = int(avia_status)
        except (ValueError, TypeError):
            return None

        if code in _AVIA_HEATING_STATES:
            return HVACAction.HEATING
        if code in _AVIA_PREHEATING_STATES:
            return HVACAction.PREHEATING
        if code in _AVIA_COOLDOWN_STATES or code == 6:
            return HVACAction.IDLE
        return HVACAction.OFF

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Expose the AVIA status name as an extra attribute."""
        attrs: dict[str, Any] = {}
        if self.coordinator.data:
            code = self.coordinator.data.get(KEY_AVIA_STATUS)
            try:
                attrs["avia_status"] = AVIA_STATUS.get(int(code), f"Unknown ({code})")
            except (ValueError, TypeError):
                pass
        return attrs

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set heat mode: HEAT → Spa (v53=2), OFF → Off (v53=0)."""
        try:
            if hvac_mode == HVACMode.HEAT:
                await self.coordinator.client.async_set_heat_mode(HEAT_MODE_SPA)
            else:
                await self.coordinator.client.async_set_heat_mode(HEAT_MODE_OFF)
        except RaypakApiError as err:
            _LOGGER.error("Failed to set spa HVAC mode: %s", err)
            return
        await self.coordinator.async_request_refresh()

    async def async_set_temperature(self, **kwargs: Any) -> None:
        """Set the spa target temperature (v43)."""
        temp = kwargs.get(ATTR_TEMPERATURE)
        if temp is None:
            return
        try:
            await self.coordinator.client.async_set_spa_temperature(int(temp))
        except RaypakApiError as err:
            _LOGGER.error("Failed to set spa temperature: %s", err)
            return
        await self.coordinator.async_request_refresh()
