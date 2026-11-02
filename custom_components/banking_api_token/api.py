"""Bank API clients."""

from __future__ import annotations

import logging
import time
from typing import Any

from aiohttp import ClientError, ClientSession

_LOGGER = logging.getLogger(__name__)
CREDITAS_BASE_URL = "https://api.creditas.cz/oam"


class BankingApiError(Exception):
    """Safe API error without credential material."""


class CreditasClient:
    """Minimal read-only Creditas PremiumAPI client."""

    def __init__(self, session: ClientSession, account_id: str, token: str, debug: bool = False):
        self._session = session
        self._account_id = account_id
        self._token = token
        self._debug = debug

    async def _post(self, path: str, body: dict[str, Any]) -> dict[str, Any]:
        started = time.monotonic()
        url = f"{CREDITAS_BASE_URL}{path}"
        try:
            async with self._session.post(
                url,
                json=body,
                headers={"Authorization": f"Bearer {self._token}", "Accept": "application/json"},
            ) as response:
                if self._debug:
                    _LOGGER.debug("Creditas API POST %s status=%s duration_ms=%.0f", path, response.status, (time.monotonic() - started) * 1000)
                payload = await response.json(content_type=None)
                if response.status != 200:
                    # Deliberately do not include response body: bank errors can contain private data.
                    raise BankingApiError(f"Creditas API returned HTTP {response.status} for {path}")
                if not isinstance(payload, dict):
                    raise BankingApiError(f"Creditas API returned an invalid response for {path}")
                return payload
        except (ClientError, TimeoutError, ValueError) as err:
            if isinstance(err, BankingApiError):
                raise
            raise BankingApiError(f"Creditas API request failed for {path}: {type(err).__name__}") from None

    async def async_get_data(self) -> dict[str, Any]:
        """Fetch balance and a small recent-transaction page."""
        balance = await self._post("/v1/account/balance/get", {"accountId": self._account_id})
        transactions = await self._post(
            "/v1/account/transaction/search",
            {"accountId": self._account_id, "pageItemCount": 10, "pageIndex": 0},
        )
        rows = transactions.get("transactions", [])
        if not isinstance(rows, list):
            rows = []
        return {"balance": balance, "transactions": rows[:10], "transaction_count": transactions.get("itemCount", len(rows))}
