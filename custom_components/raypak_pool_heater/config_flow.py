"""Config flow for Raypak Pool Heater integration."""

from __future__ import annotations

import logging
from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import RaypakApiClient
from .const import CONF_TOKEN, DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_TOKEN): str,
    }
)


class RaypakPoolHeaterConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Raypak Pool Heater."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Handle the initial step — user enters their Raymote token."""
        errors: dict[str, str] = {}

        if user_input is not None:
            token = user_input[CONF_TOKEN].strip()

            # Prevent duplicate entries for the same token
            await self.async_set_unique_id(token)
            self._abort_if_unique_id_configured()

            # Validate the token against the API
            session = async_get_clientsession(self.hass)
            client = RaypakApiClient(session, token)
            if await client.async_validate_token():
                return self.async_create_entry(
                    title="Raypak Pool Heater",
                    data={CONF_TOKEN: token},
                )
            errors["base"] = "invalid_token"

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )
