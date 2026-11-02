"""Config flow for Banking API Token."""

from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant, callback

from .const import BANK_CREDITAS, CONF_ACCOUNT_ID, CONF_BANK, CONF_PAY_TOKEN, CONF_READ_TOKEN, DOMAIN


class BankingApiTokenConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Configure one bank account as one config entry."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Collect the first account's credentials."""
        errors = {}
        if user_input is not None:
            await self.async_set_unique_id(f"{user_input[CONF_BANK]}_{user_input[CONF_ACCOUNT_ID]}")
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title=user_input["name"],
                data={key: value for key, value in user_input.items() if key != "name"},
            )

        schema = vol.Schema(
            {
                vol.Required("name"): str,
                vol.Required(CONF_BANK, default=BANK_CREDITAS): vol.In({BANK_CREDITAS: "Creditas"}),
                vol.Required(CONF_ACCOUNT_ID): str,
                vol.Required(CONF_READ_TOKEN): str,
                vol.Required(CONF_PAY_TOKEN): str,
            }
        )
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return BankingApiTokenOptionsFlow(config_entry)


class BankingApiTokenOptionsFlow(config_entries.OptionsFlow):
    """Options flow for polling interval and verbose API diagnostics."""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            updated_data = dict(self.config_entry.data)
            for key in (CONF_READ_TOKEN, CONF_PAY_TOKEN):
                if user_input.get(key):
                    updated_data[key] = user_input[key]
            self.hass.config_entries.async_update_entry(self.config_entry, data=updated_data)
            options = {key: user_input[key] for key in ("scan_interval", "debug_api")}
            return self.async_create_entry(title="", data=options)
        schema = vol.Schema(
            {
                vol.Optional("scan_interval", default=self.config_entry.options.get("scan_interval", 300)): vol.All(
                    vol.Coerce(int), vol.Range(min=60, max=3600)
                ),
                vol.Optional("debug_api", default=self.config_entry.options.get("debug_api", False)): bool,
                vol.Optional(CONF_READ_TOKEN): str,
                vol.Optional(CONF_PAY_TOKEN): str,
            }
        )
        return self.async_show_form(step_id="init", data_schema=schema)
