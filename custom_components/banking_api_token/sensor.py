"""Sensors for bank account data."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation
from typing import Any

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


def _decimal(value: Any):
    try:
        return Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        return None


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([BalanceSensor(coordinator, entry, "currentBalance"), BalanceSensor(coordinator, entry, "availableBalance"), TransactionsSensor(coordinator, entry)])


class BankingSensor(CoordinatorEntity, SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._entry = entry
        self._attr_device_info = DeviceInfo(identifiers={(DOMAIN, entry.entry_id)}, name=entry.title, manufacturer=entry.data.get("bank", "Bank").title())


class BalanceSensor(BankingSensor):
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator, entry: ConfigEntry, key: str) -> None:
        super().__init__(coordinator, entry)
        self._key = key
        self._attr_name = "Current balance" if key == "currentBalance" else "Available balance"
        self._attr_unique_id = f"{entry.entry_id}_{key}"

    @property
    def native_value(self):
        value = _decimal(self.coordinator.data.get("balance", {}).get(self._key))
        return float(value) if value is not None else None

    @property
    def native_unit_of_measurement(self):
        return self.coordinator.data.get("balance", {}).get("currency")


class TransactionsSensor(BankingSensor):
    """Latest transaction list as bounded attributes; state is item count."""

    def __init__(self, coordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator, entry)
        self._attr_name = "Recent transactions"
        self._attr_unique_id = f"{entry.entry_id}_recent_transactions"

    @property
    def native_value(self):
        return len(self.coordinator.data.get("transactions", []))

    @property
    def extra_state_attributes(self):
        return {
            "transactions": self.coordinator.data.get("transactions", [])[:10],
            "item_count": self.coordinator.data.get("transaction_count"),
        }
