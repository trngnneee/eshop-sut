# TC-PROFILE-SCH-SUP-001: GET profile exposes login_attempts / locked_until schema

## Requirement ID
FR-04

## Module / Test type / Technique
profile / Schema validation / Human extension (SCH-SUP)

## Schema aspect
Undocumented DB columns on GET

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.

## Test data
```json
{
  "headers": {}
}
```

## Test steps
1. GET /api/users/me.
2. Inventory every key; note login_attempts and locked_until types if present.

## Expected result
Record all top-level keys on GET /api/users/me. login_attempts/locked_until may appear — not in api_spec. Flag as schema over-exposure if present. HTTP status is not specified in api_specification.md — record actual without inventing codes.

## Why the AI missed this
Model limitation — AI checked documented FR-04 fields only; SUT uses SELECT * and may return lockout columns not listed in api_spec GET schema.

## Audit (human SUP)
- **Status:** VALID
- **Reasoning:** Undocumented column exposure observe; schema inventory.

## Status / Related bugs
Not Run / None
