"""DataUpdateCoordinator for the Raypak Pool Heater integration."""

from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import RaypakApiClient, RaypakApiError
from .const import DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)


class RaypakDataCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator that polls the Raymote API for all heater data."""

    def __init__(self, hass: HomeAssistant, client: RaypakApiClient) -> None:
        """Initialise the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )
        self.client = client

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from the API."""
        try:
            return await self.client.async_get_data()
        except RaypakApiError as err:
            raise UpdateFailed(f"Error communicating with Raypak API: {err}") from err
