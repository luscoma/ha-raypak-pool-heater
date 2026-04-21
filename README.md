# Raypak Pool Heater

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![GitHub Release](https://img.shields.io/github/v/release/luscoma/ha-raypak-pool-heater?style=flat)](https://github.com/luscoma/ha-raypak-pool-heater/releases)
[![GitHub Last Commit](https://img.shields.io/github/last-commit/luscoma/ha-raypak-pool-heater?style=flat)](https://github.com/luscoma/ha-raypak-pool-heater/commits/main)
[![License](https://img.shields.io/github/license/luscoma/ha-raypak-pool-heater?style=flat)](LICENSE)

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=luscoma&repository=ha-raypak-pool-heater&category=integration)

A Home Assistant custom integration for **Raypak AVIA pool heaters** equipped with the **Raymote** Wi-Fi module. Monitor temperatures, control your heater, and adjust the setpoint directly from Home Assistant.

## Credits

This integration is based on the original YAML configuration by **u/duclaws** on Reddit.

- [Original Reddit post](https://www.reddit.com/r/homeassistant/comments/1kpk6et/raymote_raypak_pool_heat_integration/)
- [Original YAML files (Google Drive)](https://drive.google.com/drive/folders/1Mlw1KKNlMsJ5ypbVEvIbX2FmPkkQsSP9)

Parameter names and definitions are based on the known virtual pins used by the Raymote API, sourced from the Raypak AVIA UI.

## Features

- **Climate entity** — control pool heating mode (heat/off) and adjust the target temperature; displays granular HVAC action using the full AVIA state machine (pre-purge, spark, heating, post-purge, fault)
- **Heater switch** — quick Pool mode on/off toggle
- **20+ sensors** including temperatures, flow, voltage, flame strength, status, counters
- **Diagnostic sensors** (disabled by default) for configuration values, bitmasks, pump speed presets, and optional WChem / external temp sensors

## Requirements

- A Raypak AVIA pool heater with the **Raymote** Wi-Fi module
- A Raymote device token (found at [raymote.raypak.com](https://raymote.raypak.com))

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Click the three dots → **Custom repositories**
3. Add this repository URL and select **Integration**
4. Click **Download**
5. Restart Home Assistant

### Manual

1. Copy `custom_components/raypak_pool_heater/` into your `config/custom_components/` directory
2. Restart Home Assistant

## Configuration

1. Go to **Settings → Devices & Services → Add Integration**
2. Search for **Raypak Pool Heater**
3. Enter your Raymote device token
4. Assign the device to an area (e.g., "Pool") in the device settings

## Finding Your Token

Your token is in the URL when viewing your device at [raymote.raypak.com](https://raymote.raypak.com):
`raymote.raypak.com/dashboard/.../devices/<ID>/dashboard`

It can also be found via your device's API settings or export.

---

## API Parameter Map

The virtual pins below are based on observed values from the Raymote UI and may change across firmware versions.

Each sensor's status in the integration is noted in the table:
- **enabled** — on by default
- **enabled, diagnostic** — on by default but marked as a diagnostic entity (won't appear in auto-generated dashboards)
- **disabled** — off by default, must be manually enabled
- **disabled, diagnostic** — off by default and marked as a diagnostic entity

### Pool Sensors

| API Key | Parameter Name | Unit | Status | Notes |
|---------|---------------|------|--------|-------|
| v5 | Outlet Water Temp | °F | enabled | |
| v7 | Flow Sensor | gal | enabled | |
| v13 | Fault Code | — | enabled | 0 = no fault |
| v14 | AVIA Estimated HX Flow | gal | enabled, diagnostic | Heater-side estimate |
| v16 | Est Heat Time Pool | hr | enabled | Hours to reach pool setpoint |
| v41 | Pool Setpoint | °F | enabled | Write target |
| v52 | Inlet Water Temp (Avg) | °F | enabled | Computed as (v3+v4)/2 |
| v55 | Status Text | string | enabled | "Heating", "No Demand", etc. |
| v65 | AVIA Status | enum | enabled | See state machine below |
| v112 | Raymote Estimated Flow | gal | enabled | Raymote-side estimate |
| v3 | Inlet Water Temp 1 | °F | enabled, diagnostic | Raw sensor 1; v52 is the dashboard-friendly average |
| v4 | Inlet Water Temp 2 | °F | enabled, diagnostic | Raw sensor 2 |
| v6 | Vent Flue Temp | °F | enabled, diagnostic | |
| v10 | Power Supply Voltage | V | enabled, diagnostic | |
| v11 | Flame Strength | uA | enabled, diagnostic | 0 when burner off |
| v15 | AVIA Est Pool Volume | gal | enabled, diagnostic | Heater's internal estimate; compare with v115 |
| v25 | Heating Cycles | — | enabled, diagnostic | |
| v27 | Lifetime Heating Hours | hr | enabled, diagnostic | |
| v29 | Power Cycles | — | enabled, diagnostic | |
| v45 | Heater BTUs | kBTU | enabled, diagnostic | |
| v115 | Pool Volume | gal | enabled, diagnostic | User-configured in app |
| v40 | Max Pool Setpoint | °F | disabled, diagnostic | Config ceiling |
| v53 | Heat Mode | enum | — | Write-only; 0=Off, 1=Pool, 2=Spa |

### Spa Sensors

| API Key | Parameter Name | Unit | Status | Notes |
|---------|---------------|------|--------|-------|
| v43 | Spa Setpoint | °F | disabled | Write target |
| v18 | Est Heat Time Spa | hr | disabled | Hours to reach spa setpoint |
| v17 | AVIA Est Spa Volume | gal | disabled, diagnostic | Heater's internal estimate |
| v42 | Max Spa Setpoint | °F | disabled, diagnostic | Config ceiling |
| v116 | Spa Volume | gal | disabled, diagnostic | User-configured in app |

### Connectivity & Service

| API Key | Parameter Name | Unit | Status | Notes |
|---------|---------------|------|--------|-------|
| v64 | WiFi RSSI | dBm | enabled, diagnostic | |
| v8 | ASME Setting | — | disabled, diagnostic | Pressure vessel calibration offset, range ±2.5 |
| v12 | Safety Bits | — | disabled, diagnostic | Bitmask; non-zero = safety systems active |
| v233 | Outside Air Temp | °C | disabled, diagnostic | 0 if external sensor not connected |

### AVIA Status State Machine (v65)

| Code | State | HVAC Action |
|------|-------|-------------|
| 0 | Initialization | Off |
| 1 | No Demand | Off |
| 2 | Pre-Purge | Preheating |
| 3 | Spark | Preheating |
| 4 | Heating | Heating |
| 5 | Post-Purge | Idle |
| 6 | Waiting Water | Idle |
| 9 | Check Heater | Idle (see Fault Code) |

## Pool vs Spa

By default this integration is set up for pool-only use. A second **Spa Thermostat** climate and switch entity are registered but disabled.  You can enable these to turn the heater on in "SPA mode".
The pool and spa modes are mutually exclusive.  The heater can only be in one mode of operation or the other, enabling and using both may lead to wierd outcomes.  I've never tested spa mode.

**To use spa mode:**

1. In Home Assistant go to **Settings → Devices & Services → Raypak Pool Heater → Entities**
2. Enable the **Spa Thermostat** climate entity and the **Spa Heater** switch if desired
3. Enable the spa sensors you care about: Spa Setpoint (v43) and Est Heat Time Spa (v18) are in the main sensor list; Max Spa Setpoint (v42), Spa Volume (v116), and AVIA Est Spa Volume (v17) are in the diagnostic section

When the Spa Thermostat is set to Heat it sends `v53=2` (Spa mode) to the heater and targets the spa setpoint (`v43`). When turned off it sends `v53=0`. The Pool Thermostat uses `v53=1` (Pool mode) and targets the pool setpoint (`v41`).

Note that the heater can only be in one mode at a time — switching one thermostat on will implicitly take the other offline from the heater's perspective. The integrations `hvac_mode` properties reflect this: whichever entity does not match the active heat mode will report `off`.

If you only have a pool and no spa, you can safely ignore the Spa Thermostat entity entirely.

## Contributing

Contributions welcome as I mostly threw this together with claude and a prayer.
