# Home Assistant Banking API Token

Home Assistant custom integration for banking APIs using transferable/API tokens. Initial development targets Creditas PremiumAPI and read-only account monitoring. FIO is planned as a separate adapter after its API/authentication model is verified.

> Early development. Do not use for payment execution. The first release is read-only.

## Planned features

- Multiple bank accounts, each configured as an independent Home Assistant integration entry.
- Creditas account ID and separate read/pay tokens (pay token is stored for future use but not used by the initial read-only implementation).
- Balance and recent-transaction sensors.
- Opt-in API debug logging with credentials redacted.

See [doc/PROJECT-SPEC.md](doc/PROJECT-SPEC.md) for scope, API assumptions, security requirements, and acceptance criteria.

## Install on HA-stage

1. In Home Assistant open **HACS → Integrations → ⋮ → Custom repositories**.
2. Add `https://github.com/alkaacz/homeassistant-banking-api-token` with category **Integration**.
3. Find **Home Assistant Banking API Token**, download it, and restart Home Assistant.
4. Open **Settings → Devices & services → Add integration**, search for **Banking API Token**, and enter one Creditas account's display name, `accountId`, read token, and pay token.
5. The integration performs read-only balance and transaction requests using the read token. The pay token is stored for future use only; this version never submits payments.

You can add another account as another integration entry. Keep the tokens in the HA form; never put them in GitHub, this repository, issue reports, or chat. For API diagnostics, enable the integration's `debug_api` option and set the integration logger to debug in **Settings → System → Logs**. Logs include endpoint/status/timing metadata, not request/response bodies or credentials.

## Current status

The installable HACS custom integration and Creditas read-only setup flow are present. Local Python/JSON syntax checks pass. Installation on HA-stage and a live request with the first account have **not** yet been performed. After setup, confirm the two balance sensors and recent-transactions sensor appear under the new device; if setup fails, share the redacted HA error/log excerpt (never tokens).

## Local installation for development

Copy `custom_components/banking_api_token` into the Home Assistant configuration's `custom_components` directory, restart Home Assistant, then add **Banking API Token** under **Settings → Devices & services → Add integration**. Do not commit real account IDs or tokens.
