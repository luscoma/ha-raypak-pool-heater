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
)

DOMAIN = "raypak_pool_heater"

API_BASE_URL = "https://raymote.raypak.com/external/api"
API_GET_ALL = f"{API_BASE_URL}/getAll"
API_UPDATE = f"{API_BASE_URL}/update"

CONF_TOKEN = "token"

DEFAULT_SCAN_INTERVAL = 30  # seconds

# ── AVIA Status enum (v65) ────────────────────────────────────────────────────
# Source: observed values from the Raymote UI
AVIA_STATUS = {
    0: "Initialization",
    1: "No Demand",
    2: "Pre-Purge",
    3: "Spark",
    4: "Heating",
    5: "Post-Purge",
    6: "Waiting Water",
    9: "Check Heater",
}

# ── Heat Mode enum (v53) ──────────────────────────────────────────────────────
HEAT_MODE = {
    0: "Off",
    1: "Pool",
    2: "Spa",
    3: "T Spa", # No idea what this is so I wouldn't use it
}

# ── Primary sensors (enabled by default, included in auto-generated dashboards)
#
# Keep this list focused on the sensors most users will actually want on a
# dashboard. Sensors that are informational, rarely change, or only useful for
# specific setups belong in DIAGNOSTIC_SENSOR_TYPES instead.

SENSOR_TYPES: tuple[SensorEntityDescription, ...] = (

    # ── Temperature ──────────────────────────────────────────────────────
    SensorEntityDescription(
        key="v52",
        name="Inlet Water Temp (Avg)",
        native_unit_of_measurement=UnitOfTemperature.FAHRENHEIT,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:thermometer-water",
    ),
    SensorEntityDescription(
        key="v5",
        name="Outlet Water Temp",
        native_unit_of_measurement=UnitOfTemperature.FAHRENHEIT,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:thermometer-water",
    ),
    SensorEntityDescription(
        key="v41",
        name="Pool Setpoint",
        native_unit_of_measurement=UnitOfTemperature.FAHRENHEIT,
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermostat",
    ),

    # ── Flow ─────────────────────────────────────────────────────────────
    SensorEntityDescription(
        key="v7",
        name="Flow Sensor",
        native_unit_of_measurement="gal",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:waves-arrow-right",
    ),
    SensorEntityDescription(
        key="v112",
        name="Raymote Estimated Flow",
        native_unit_of_measurement="gal",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:water-pump",
    ),

    # ── Status ───────────────────────────────────────────────────────────
    SensorEntityDescription(
        key="v55",
        name="Status Text",
        icon="mdi:fire-circle",
    ),
    SensorEntityDescription(
        key="v65",
        name="AVIA Status",
        # 0=Init, 1=No Demand, 2=Pre-Purge, 3=Spark,
        # 4=Heating, 5=Post-Purge, 6=Waiting Water, 9=Check Heater
        icon="mdi:state-machine",
    ),
    SensorEntityDescription(
        key="v13",
        name="Fault Code",
        icon="mdi:alert-circle-outline",
    ),

    # ── Heating estimates (useful for automations) ────────────────────────
    SensorEntityDescription(
        key="v16",
        name="Est Heat Time Pool",
        # Hours to reach pool setpoint from current temp
        native_unit_of_measurement=UnitOfTime.HOURS,
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:clock-fast",
    ),

    # ── Spa (disabled by default; enable if spa is present) ──────────────
    SensorEntityDescription(
        key="v43",
        name="Spa Setpoint",
        native_unit_of_measurement=UnitOfTemperature.FAHRENHEIT,
        device_class=SensorDeviceClass.TEMPERATURE,
        entity_registry_enabled_default=False,
        icon="mdi:hot-tub",
    ),
    SensorEntityDescription(
        key="v18",
        name="Est Heat Time Spa",
        native_unit_of_measurement=UnitOfTime.HOURS,
        device_class=SensorDeviceClass.DURATION,
        entity_registry_enabled_default=False,
        icon="mdi:clock-fast",
    ),
)

# ── Diagnostic sensors ────────────────────────────────────────────────────────
#
# These carry EntityCategory.DIAGNOSTIC, which prevents them from appearing in
# auto-generated dashboards. Enabled status is preserved — sensors without
# entity_registry_enabled_default=False are still on by default, they just
# won't be picked up by automatic dashboard generation.

DIAGNOSTIC_SENSOR_TYPES: tuple[SensorEntityDescription, ...] = (

    # ── Raw inlet temps (avg v52 is the primary dashboard sensor) ────────
    SensorEntityDescription(
        key="v3",
        name="Inlet Water Temp 1",
        native_unit_of_measurement=UnitOfTemperature.FAHRENHEIT,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:thermometer-water",
    ),
    SensorEntityDescription(
        key="v4",
        name="Inlet Water Temp 2",
        native_unit_of_measurement=UnitOfTemperature.FAHRENHEIT,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:thermometer-water",
    ),
    SensorEntityDescription(
        key="v6",
        name="Vent Flue Temp",
        native_unit_of_measurement=UnitOfTemperature.FAHRENHEIT,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:thermometer-high",
    ),

    # ── Flow ─────────────────────────────────────────────────────────────
    SensorEntityDescription(
        key="v14",
        name="AVIA Estimated HX Flow",
        native_unit_of_measurement="gal",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:water-pump",
    ),

    # ── Electrical / combustion ──────────────────────────────────────────
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
        name="Flame Strength",
        native_unit_of_measurement="uA",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:fire",
    ),

    # ── Lifetime counters ────────────────────────────────────────────────
    SensorEntityDescription(
        key="v25",
        name="Heating Cycles",
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
        name="Lifetime Heating Hours",
        native_unit_of_measurement=UnitOfTime.HOURS,
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:clock-outline",
    ),

    # ── Pool configuration ────────────────────────────────────────────────
    SensorEntityDescription(
        key="v45",
        name="Heater BTUs",
        native_unit_of_measurement="kBTU",
        icon="mdi:fire",
    ),
    SensorEntityDescription(
        key="v15",
        name="AVIA Est Pool Volume",
        # Heater's internally calculated pool volume; compare with v115 (user-configured)
        native_unit_of_measurement="gal",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:pool",
    ),
    SensorEntityDescription(
        key="v115",
        name="Pool Volume",
        # This is user provided, i.e. you configure it in the app
        native_unit_of_measurement="gal",
        icon="mdi:pool",
    ),
    SensorEntityDescription(
        key="v40",
        name="Max Pool Setpoint",
        native_unit_of_measurement=UnitOfTemperature.FAHRENHEIT,
        entity_registry_enabled_default=False,
        icon="mdi:thermometer-chevron-up",
    ),

    # ── Spa configuration (disabled by default; enable if spa is present) ─
    SensorEntityDescription(
        key="v42",
        name="Max Spa Setpoint",
        native_unit_of_measurement=UnitOfTemperature.FAHRENHEIT,
        entity_registry_enabled_default=False,
        icon="mdi:thermometer-chevron-up",
    ),
    SensorEntityDescription(
        key="v116",
        name="Spa Volume",
        # This is user provided (i.e. you configure it in the app)
        native_unit_of_measurement="gal",
        entity_registry_enabled_default=False,
        icon="mdi:hot-tub",
    ),
    SensorEntityDescription(
        key="v17",
        name="AVIA Est Spa Volume",
        native_unit_of_measurement="gal",
        entity_registry_enabled_default=False,
        icon="mdi:hot-tub",
    ),

    # ── Connectivity ─────────────────────────────────────────────────────
    SensorEntityDescription(
        key="v64",
        name="WiFi RSSI",
        native_unit_of_measurement=SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
        device_class=SensorDeviceClass.SIGNAL_STRENGTH,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:wifi",
    ),

    # ── Service / calibration ─────────────────────────────────────────────
    SensorEntityDescription(
        key="v8",
        name="ASME Setting",
        # Pressure vessel calibration offset; range ±2.5; non-zero at rest is normal
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
        icon="mdi:gauge",
    ),
    SensorEntityDescription(
        key="v12",
        name="Safety Bits",
        # Bitmask; non-zero values indicate specific safety systems active during operation
        entity_registry_enabled_default=False,
        icon="mdi:shield-alert-outline",
    ),

    # ── External sensors (enable if hardware present) ─────────────────────
    SensorEntityDescription(
        key="v233",
        name="Outside Air Temp",
        # °C from optional external sensor; reads 0 if sensor not connected
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
        icon="mdi:thermometer",
    ),
)

# ── Keys used by other platforms ─────────────────────────────────────────────

# v53 = AVIA Heat Mode enum: 0=Off, 1=Pool, 2=Spa, 3=T Spa
KEY_HEAT_MODE = "v53"
HEAT_MODE_OFF = 0
HEAT_MODE_POOL = 1
HEAT_MODE_SPA = 2

KEY_HEATER_STATUS_TEXT = "v55"
KEY_AVIA_STATUS = "v65"     # Rich state enum (used for hvac_action in climate.py)

KEY_SETPOINT = "v41"        # Pool setpoint (double)
KEY_SPA_SETPOINT = "v43"    # Spa setpoint (double)
KEY_AVG_INLET = "v52"       # AVIA average inlet temp
