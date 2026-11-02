# Zadání: Home Assistant Banking API Token

## Cíl

Vytvořit HACS custom integration pro Home Assistant, která umožní připojit více bankovních účtů přes bankovní API a sledovat zůstatek, transakce a později stav plateb. Repo: [`alkaacz/homeassistant-banking-api-token`](https://github.com/alkaacz/homeassistant-banking-api-token).

## Rozsah první verze (MVP)

- Creditas PremiumAPI jako první a ověřovaný adaptér.
- Libovolný počet samostatných HA konfigurací; každá reprezentuje jednu banku a jeden účet. Více účtů stejného klienta lze přidat opakovaným průvodcem.
- Konfigurace Creditas: popisek účtu, `accountId`, read token, pay token. Pay token se bezpečně uloží, ale MVP jej nepoužívá; vytváření/odesílání plateb je mimo rozsah první verze.
- Čtení zůstatku a posledních transakcí přes read token. Aktualizace přes HA DataUpdateCoordinator s konfigurovatelným intervalem a respektováním limitů API.
- Senzory pro aktuální zůstatek a dostupný zůstatek; poslední transakce budou dostupné jako atributy senzoru nebo samostatná entita s omezeným počtem položek. Přesný model se ověří proti reálnému payloadu.
- Odstranění/změna konfigurace v HA a podpora opakovaného přidání účtu.
- Přehledná dokumentace, HACS metadata a návod k ověření na čisté instalaci HA-stage.

## API podklady a ověřené operace

Zdrojem je `creditas-open-api-tests/input-docs/Creditas-PremiumAPI-1.0.1.swagger.json` a `tests/creditas-api.spec.ts`. Base URL je `https://api.creditas.cz/oam`; autentizace je `Authorization: Bearer <token>`; volání používají JSON POST.

- `POST /v1/account/balance/get`, body `{accountId}`; read scope; odpověď obsahuje `currency`, `currentBalance`, `availableBalance`.
- `POST /v1/account/transaction/search`, body `{accountId, pageItemCount, pageIndex}`; read scope; odpověď obsahuje `transactions` a `itemCount`.
- `POST /v1/account/current/get` může doplnit metadata účtu.
- `POST /v2/payment/search` poskytuje čtení plateb; zařadit až po samostatném ověření response schématu a bezpečném návrhu entit.
- Endpointy `.../payment/.../create`, import/cancel a další mutace se v MVP nikdy nevolají.

## Více bank / FIO

Architektura oddělí společný HA lifecycle a entity od bankovních klientů/adaptérů. Creditas bude první implementací. FIO je cílový adaptér druhé fáze; před implementací je nutné ověřit aktuální oficiální API, autentizační model, limity a dostupná data. Konfigurace se nesmí snažit vnutit FIO model dvojice read/pay token, pokud jej FIO nepoužívá. Do MVP se FIO nezobrazuje jako funkční volba.

## Bezpečnost a logování

- Tokeny nesmí být v logách, diagnostice, názvu entity, URL ani exception textu. Authorization a citlivé hlavičky se nikdy nelogují.
- Standardní režim loguje pouze chyby integrace a HA lifecycle.
- Debug režim loguje metodu, relativní endpoint, dobu trvání, HTTP status, počet vrácených položek a bezpečně omezené/redigované chybové detaily. Těla requestů/responses se standardně nevypisují; případné rozšířené payload debugging musí mít explicitní opt-in, sanitizaci a jasné upozornění.
- Nepoužívat pay token pro read endpointy ani read token pro operace vyžadující platební scope.
- Žádné platební operace bez samostatného explicitního návrhu potvrzení, ochrany proti duplicitě a testů.

## Uživatelské rozhraní a entity

- HA konfigurační flow: výběr banky (zatím Creditas), název účtu, accountId, read token, pay token.
- Samostatný config entry pro každý účet; názvy a unique IDs musí být stabilní a nekolidovat při více účtech.
- Počáteční entity: `sensor.<ucet>_current_balance`, `sensor.<ucet>_available_balance`, případně `sensor.<ucet>_transactions` s omezenými atributy a timestampem poslední aktualizace.
- Jednotka měny odpovídá API, stav částek zůstane přesný (decimal/string bezpečně převedený na numerický stav).
- Při chybě API zůstane poslední známá hodnota, HA označí entitu jako nedostupnou a log poskytne bezpečně redigovaný důvod.

## Akceptační kritéria

1. Repo lze nainstalovat přes HACS jako custom integration a HA ji po restartu objeví.
2. Uživatelský config flow uloží Creditas účet a založí odpovídající entity.
3. Lze přidat nejméně dva účty s odlišnými accountId/tokeny; entity a data se nemíchají.
4. Zůstatek a transakce se načítají přes read token a odpovídají API payloadu.
5. Neplatný token, timeout a HTTP/API chyba mají srozumitelný stav bez úniku credentials.
6. Debug log obsahuje užitečnou trasu API volání bez tokenu nebo citlivých hlaviček.
7. Žádný kód MVP nevytváří ani nemění platbu.
8. HACS metadata, README, licence, manifest a minimální automatické kontroly jsou připravené; ověření instalace proběhne na HA-stage.

## Fáze

1. Zadání a repo/HACS kostra (nyní).
2. Creditas read-only klient, config flow, coordinator a senzory.
3. Lokální kontrola kvality a bezpečnostní kontrola logování.
4. Instalace a ověření na HA-stage; tokeny zadává uživatel přímo do HA, nikdy do repa/chatu.
5. Vylepšení podle testu; následně samostatný návrh FIO a čtení/stav plateb.

## Mimo rozsah MVP

Odesílání plateb, jejich rušení či import, FIO implementace, historické backfilly, automatické párování plateb a publikace do HACS default repository.
