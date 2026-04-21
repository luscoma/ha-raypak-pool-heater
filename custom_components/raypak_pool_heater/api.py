"""API client for the Raypak Raymote cloud API."""

from __future__ import annotations

import logging
from typing import Any

import aiohttp

from .const import API_GET_ALL, API_UPDATE

_LOGGER = logging.getLogger(__name__)


class RaypakApiError(Exception):
    """Raised when an API call fails."""


class RaypakApiClient:
    """Thin async wrapper around the Raymote external API."""

    def __init__(
        self,
        session: aiohttp.ClientSession,
        token: str,
    ) -> None:
        """Initialise the client."""
        self._session = session
        self._token = token

    async def async_get_data(self) -> dict[str, Any]:
        """Fetch all values from the heater."""
        url = f"{API_GET_ALL}?token={self._token}"
        try:
            async with self._session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                resp.raise_for_status()
                data: dict[str, Any] = await resp.json(content_type=None)
                return data
        except (aiohttp.ClientError, TimeoutError) as err:
            raise RaypakApiError(f"Error fetching data: {err}") from err

    async def async_set_heat_mode(self, mode: int) -> None:
        """Set the AVIA heat mode via v53.

        mode: 0=Off, 1=Pool, 2=Spa (see HEAT_MODE in const.py)
        """
        await self._async_update("v53", mode)

    async def async_set_temperature(self, temp: int) -> None:
        """Set the pool target temperature via v41."""
        await self._async_update("v41", temp)

    async def async_set_spa_temperature(self, temp: int) -> None:
        """Set the spa target temperature via v43."""
        await self._async_update("v43", temp)

    async def _async_update(self, key: str, value: int | float) -> None:
        """Send an update command to the Raymote API."""
        url = f"{API_UPDATE}?token={self._token}&{key}={value}"
        try:
            async with self._session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                resp.raise_for_status()
        except (aiohttp.ClientError, TimeoutError) as err:
            raise RaypakApiError(f"Error sending update {key}={value}: {err}") from err

    async def async_validate_token(self) -> bool:
        """Validate the token by making a test API call."""
        try:
            data = await self.async_get_data()
            return "v55" in data
        except RaypakApiError:
            return False
