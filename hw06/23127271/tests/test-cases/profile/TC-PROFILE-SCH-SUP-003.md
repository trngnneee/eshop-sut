# TC-PROFILE-SCH-SUP-003: Schema inventory — no password column on GET user object

## Requirement ID
FR-04 / SEC-01

## Module / Test type / Technique
profile / Schema validation / Human extension (SCH-SUP)

## Schema aspect
Full column dump vs minimum schema

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
2. Assert forbidden secret keys absent; log full key list.

## Expected result
List all keys. Must not include password, password_hash, or hash. Document unexpected sensitive-looking keys.

## Why the AI missed this
API characteristic — SELECT * returns full row; AI SCH-007 checked password key but not whether other sensitive columns (e.g. password hash variants) appear under alternate names.

## Audit (human SUP)
- **Status:** VALID
- **Reasoning:** SEC-01 key inventory beyond password key name.

## Status / Related bugs
Not Run / None
