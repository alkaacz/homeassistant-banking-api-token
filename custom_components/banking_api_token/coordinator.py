"""Data update coordinator."""

from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed, UpdateFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .api import BankingApiError, CreditasClient
from .const import BANK_CREDITAS, CONF_ACCOUNT_ID, CONF_BANK, CONF_READ_TOKEN, DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)


class BankingDataUpdateCoordinator(DataUpdateCoordinator):
    """Coordinate updates for one configured bank account."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self.entry = entry
        self.client = CreditasClient(
            async_get_clientsession(hass),
            entry.data[CONF_ACCOUNT_ID],
            entry.data[CONF_READ_TOKEN],
            entry.options.get("debug_api", False),
        )
        interval = entry.options.get("scan_interval", DEFAULT_SCAN_INTERVAL)
        super().__init__(hass, _LOGGER, name=f"{DOMAIN}_{entry.entry_id}", update_interval=timedelta(seconds=interval))

    async def _async_update_data(self):
        try:
            return await self.client.async_get_data()
        except BankingApiError as err:
            if "HTTP 401" in str(err) or "HTTP 403" in str(err):
                raise ConfigEntryAuthFailed("Creditas rejected the read token") from err
            raise UpdateFailed(str(err)) from err
