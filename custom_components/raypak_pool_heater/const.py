"""Constants for the Raypak Pool Heater integration."""

from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
    UnitOfElectricPotential,
    UnitOfTemperature,
    UnitOfTime,
    UnitOfVolumeFlowRate,
)

DOMAIN = "raypak_pool_heater"

API_BASE_URL = "https://raymote.raypak.com/external/api"
API_GET_ALL = f"{API_BASE_URL}/getAll"
API_UPDATE = f"{API_BASE_URL}/update"

CONF_TOKEN = "token"

DEFAULT_SCAN_INTERVAL = 30  # seconds

# ── Sensor definitions ──────────────────────────────────────────────────────
# Each tuple: (api_key, name, unit, device_class, state_class, icon, enabled_by_default, entity_category)

SENSOR_TYPES: tuple[SensorEntityDescription, ...] = (
    # ── Temperature sensors ──────────────────────────────────────────────
    SensorEntityDescription(
        key="v3",
        name="Inlet Temp 1",
        native_unit_of_measurement=UnitOfTemperature.FAHRENHEIT,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:thermometer-water",
    ),
    SensorEntityDescription(
        key="v4",
        name="Inlet Temp 2",
        native_unit_of_measurement=UnitOfTemperature.FAHRENHEIT,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:thermometer-water",
    ),
    SensorEntityDescription(
        key="v52",
        name="Average Inlet Temp",
        native_unit_of_measurement=UnitOfTemperature.FAHRENHEIT,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:thermometer-water",
    ),
    SensorEntityDescription(
        key="v5",
        name="Outlet Temp",
        native_unit_of_measurement=UnitOfTemperature.FAHRENHEIT,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:thermometer-water",
    ),
    SensorEntityDescription(
        key="v6",
        name="Vent Temp",
        native_unit_of_measurement=UnitOfTemperature.FAHRENHEIT,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:thermometer-high",
    ),
    SensorEntityDescription(
        key="v43",
        name="Outside Air Temp",
        native_unit_of_measurement=UnitOfTemperature.FAHRENHEIT,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:thermometer",
    ),
    SensorEntityDescription(
        key="v41",
        name="Setpoint",
        native_unit_of_measurement=UnitOfTemperature.FAHRENHEIT,
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermostat",
    ),
    # ── Electrical sensors ───────────────────────────────────────────────
    SensorEntityDescription(
        key="v10",
        name="Power Supply Voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:flash",
    ),
    SensorEntityDescription(
        key="v11",
        name="Flame Current",
        native_unit_of_measurement="uA",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:fire",
    ),
    # ── Flow sensors ─────────────────────────────────────────────────────
    SensorEntityDescription(
        key="v112",
        name="Estimated HX Flow",
        native_unit_of_measurement="gal",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:water-pump",
    ),
    SensorEntityDescription(
        key="v114",
        name="Flow Meter",
        native_unit_of_measurement="gal",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:water-pump",
    ),
    # ── Status sensors ───────────────────────────────────────────────────
    SensorEntityDescription(
        key="v55",
        name="Heater Status",
        icon="mdi:fire-circle",
    ),
    SensorEntityDescription(
        key="v106",
        name="Error Code",
        icon="mdi:alert-circle-outline",
    ),
    # ── Lifetime / counter sensors ───────────────────────────────────────
    SensorEntityDescription(
        key="v25",
        name="Heat Cycles",
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:counter",
    ),
    SensorEntityDescription(
        key="v29",
        name="Power Cycles",
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:counter",
    ),
    SensorEntityDescription(
        key="v27",
        name="Lifetime Heat Hours",
        native_unit_of_measurement=UnitOfTime.HOURS,
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:clock-outline",
    ),
    # ── Equipment info ───────────────────────────────────────────────────
    SensorEntityDescription(
        key="v45",
        name="Capacity",
        native_unit_of_measurement="kBTU",
        icon="mdi:fire",
    ),
    SensorEntityDescription(
        key="v115",
        name="Pool Size",
        native_unit_of_measurement="gal",
        icon="mdi:pool",
    ),
    SensorEntityDescription(
        key="v46",
        name="VS Pump Running",
        icon="mdi:pump",
    ),
    # ── Connectivity ─────────────────────────────────────────────────────
    SensorEntityDescription(
        key="v64",
        name="RSSI",
        native_unit_of_measurement=SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
        device_class=SensorDeviceClass.SIGNAL_STRENGTH,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
        icon="mdi:wifi",
    ),
)

# ── Diagnostic sensors (disabled by default, for investigation) ──────────
DIAGNOSTIC_SENSOR_TYPES: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="v2",
        name="Mode ID",
        icon="mdi:information-outline",
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="v8",
        name="Unknown v8",
        icon="mdi:help-circle-outline",
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="v12",
        name="Unknown v12",
        icon="mdi:help-circle-outline",
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="v14",
        name="Unknown v14",
        icon="mdi:help-circle-outline",
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="v15",
        name="Heat Time Estimate",
        icon="mdi:clock-outline",
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="v16",
        name="Unknown v16",
        icon="mdi:help-circle-outline",
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="v40",
        name="Max Temp Setting",
        native_unit_of_measurement=UnitOfTemperature.FAHRENHEIT,
        icon="mdi:thermometer-chevron-up",
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="v42",
        name="High Limit",
        native_unit_of_measurement=UnitOfTemperature.FAHRENHEIT,
        icon="mdi:thermometer-alert",
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="v44",
        name="Unknown v44",
        icon="mdi:help-circle-outline",
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="v50",
        name="Unknown v50",
        icon="mdi:help-circle-outline",
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="v75",
        name="Unknown v75",
        icon="mdi:help-circle-outline",
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="v145",
        name="Unknown v145",
        icon="mdi:help-circle-outline",
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="v159",
        name="Unknown v159",
        icon="mdi:help-circle-outline",
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="v167",
        name="Unknown v167",
        icon="mdi:help-circle-outline",
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="v168",
        name="Unknown v168",
        icon="mdi:help-circle-outline",
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="v190",
        name="Unknown v190",
        icon="mdi:help-circle-outline",
        entity_registry_enabled_default=False,
    ),
)

# Keys used for the heater switch
KEY_HEATER_ON_OFF = "v53"
KEY_HEATER_STATUS = "v55"

# Keys used for the climate entity
KEY_SETPOINT = "v41"
KEY_AVG_INLET = "v52"
