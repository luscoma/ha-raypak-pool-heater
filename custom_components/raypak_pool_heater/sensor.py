"""Sensor platform for the Raypak Pool Heater integration."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import AVIA_STATUS, DIAGNOSTIC_SENSOR_TYPES, DOMAIN, KEY_AVIA_STATUS, SENSOR_TYPES
from .coordinator import RaypakDataCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Raypak sensors from a config entry."""
    coordinator: RaypakDataCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities: list[RaypakSensor] = []

    for description in SENSOR_TYPES:
        if description.key == KEY_AVIA_STATUS:
            entities.append(RaypakAviaStatusSensor(coordinator, entry, description))
        else:
            entities.append(RaypakSensor(coordinator, entry, description))

    for description in DIAGNOSTIC_SENSOR_TYPES:
        entities.append(
            RaypakSensor(coordinator, entry, description, entity_category=EntityCategory.DIAGNOSTIC)
        )

    async_add_entities(entities)


class RaypakSensor(CoordinatorEntity[RaypakDataCoordinator], SensorEntity):
    """Representation of a single Raypak sensor."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: RaypakDataCoordinator,
        entry: ConfigEntry,
        description: SensorEntityDescription,
        entity_category: EntityCategory | None = None,
    ) -> None:
        """Initialise the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "Raypak Pool Heater",
            "manufacturer": "Raypak",
            "model": "Raymote",
        }
        if entity_category is not None:
            self._attr_entity_category = entity_category

    @property
    def native_value(self):
        """Return the sensor value from the coordinator data."""
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.get(self.entity_description.key)


class RaypakAviaStatusSensor(RaypakSensor):
    """Sensor for AVIA Status (v65) that returns the human-readable state name.

    The raw integer code is preserved as an extra attribute.
    """

    @property
    def native_value(self) -> str | None:
        """Return the AVIA status as a readable string (e.g. 'Heating')."""
        if self.coordinator.data is None:
            return None
        raw = self.coordinator.data.get(KEY_AVIA_STATUS)
        try:
            code = int(raw)
        except (ValueError, TypeError):
            return None
        return AVIA_STATUS.get(code, f"Unknown ({raw})")

    @property
    def extra_state_attributes(self) -> dict:
        """Include the raw integer code as an attribute."""
        if self.coordinator.data is None:
            return {}
        raw = self.coordinator.data.get(KEY_AVIA_STATUS)
        try:
            return {"code": int(raw)}
        except (ValueError, TypeError):
            return {}
