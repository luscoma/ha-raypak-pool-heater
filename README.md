# Raypak Pool Heater

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

A Home Assistant custom integration for **Raypak pool heaters** equipped with the **Raymote** Wi-Fi module. Monitor temperatures, control your heater, and adjust the setpoint directly from Home Assistant.

## Credits

This integration is based on the original YAML configuration by **u/duclaws** on Reddit.

- [Original Reddit post](https://www.reddit.com/r/homeassistant/comments/1kpk6et/raymote_raypak_pool_heat_integration/)
- [Original YAML files (Google Drive)](https://drive.google.com/drive/folders/1Mlw1KKNlMsJ5ypbVEvIbX2FmPkkQsSP9)

## Features

- **Climate entity** -- control the heater mode (heat/off) and adjust the target temperature
- **Heater switch** -- quick on/off toggle
- **20+ sensors** including:
  - Inlet temps (1, 2, and average), outlet temp, vent temp, outside air temp
  - Power supply voltage, flame current
  - Estimated HX flow, flow meter
  - Heater status, error code
  - Heat cycles, power cycles, lifetime heat hours
  - Capacity (kBTU), pool size, VS pump status, RSSI
- **Diagnostic sensors** (disabled by default) for unknown API values -- enable them to help the community map more fields

## Requirements

- A Raypak pool heater with the **Raymote** Wi-Fi module
- A Raymote device token (found at [raymote.raypak.com](https://raymote.raypak.com))

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Click the three dots in the top right and select **Custom repositories**
3. Add this repository URL and select **Integration** as the category
4. Click **Download**
5. Restart Home Assistant

### Manual

1. Copy the `custom_components/raypak_pool_heater` folder into your Home Assistant `config/custom_components/` directory
2. Restart Home Assistant

## Configuration

1. Go to **Settings > Devices & Services > Add Integration**
2. Search for **Raypak Pool Heater**
3. Enter your Raymote device token
4. The integration validates the token and creates all entities

All entities are grouped under a single **Raypak Pool Heater** device. You can assign it to an area (e.g., "Pool") in the device settings.

## Finding Your Token

1. Log in to [raymote.raypak.com](https://raymote.raypak.com)
2. Navigate to your device
3. Your token is in the URL or available in the device/API settings

## API Value Map

These values have been confirmed by comparing the Raymote dashboard to the raw API responses:

| API Key | Sensor | Unit |
|---------|--------|------|
| v3 | Inlet Temp 1 | F |
| v4 | Inlet Temp 2 | F |
| v5 | Outlet Temp | F |
| v6 | Vent Temp | F |
| v10 | Power Supply Voltage | V |
| v11 | Flame Current | uA |
| v25 | Heat Cycles | # |
| v27 | Lifetime Heat Hours | hr |
| v29 | Power Cycles | # |
| v41 | Setpoint | F |
| v43 | Outside Air Temp | F |
| v45 | Capacity | kBTU |
| v46 | VS Pump Running | bool |
| v52 | Average Inlet Temp | F |
| v53 | Heater On/Off (command) | bool |
| v55 | Heater Status | text |
| v64 | RSSI | dBm |
| v106 | Error Code | # |
| v112 | Estimated HX Flow | gal |
| v114 | Flow Meter | gal |
| v115 | Pool Size | gal |

Several additional API keys are exposed as disabled diagnostic sensors. If you identify what they represent, please open an issue or PR.

## Contributing

Contributions are welcome. If you have a Raypak heater and can help identify unknown API values, please open an issue with your findings.
