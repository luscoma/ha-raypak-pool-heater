"""Sensor platform for the Raypak Pool Heater integration."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DIAGNOSTIC_SENSOR_TYPES, DOMAIN, SENSOR_TYPES
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
