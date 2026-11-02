# Home Assistant Banking API Token

Home Assistant custom integration for banking APIs using transferable/API tokens. Initial development targets Creditas PremiumAPI and read-only account monitoring. FIO is planned as a separate adapter after its API/authentication model is verified.

> Early development. Do not use for payment execution. The first release is read-only.

## Planned features

- Multiple bank accounts, each configured as an independent Home Assistant integration entry.
- Creditas account ID and separate read/pay tokens (pay token is stored for future use but not used by the initial read-only implementation).
- Balance and recent-transaction sensors.
- Opt-in API debug logging with credentials redacted.

See [doc/PROJECT-SPEC.md](doc/PROJECT-SPEC.md) for scope, API assumptions, security requirements, and acceptance criteria.

## Development status

The first read-only implementation is in progress and has not yet been tested on HA-stage. HACS installation and live API verification remain pending.

## Local installation for development

Copy `custom_components/banking_api_token` into the Home Assistant configuration's `custom_components` directory, restart Home Assistant, then add **Banking API Token** under **Settings → Devices & services → Add integration**. Do not commit real account IDs or tokens.
