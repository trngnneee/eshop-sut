# TC-CART-SEC-SUP-003: Race — GET /api/cart concurrent with POST add

## Requirement ID
FR-07 / SEC-02

## Module / Test type / Technique
cart / Security / Human extension (SEC-SUP)

## Security requirement(s)
SEC-02

## Threat / probe
Race — GET /api/cart concurrent with POST add

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.
- Cart empty.

## Test data
```json
{
  "sequence": [
    "Fire POST /api/cart id=1 qty=5 and GET /api/cart in parallel",
    "GET /api/cart after both complete"
  ]
}
```

## Test steps
1. Fire POST /api/cart id=1 qty=5 and GET /api/cart in parallel
2. GET /api/cart after both complete

## Expected result
Final GET must show id=1 qty=5 if POST succeeded. Concurrent GET may show empty or partial — record. Must not leak another user's lines. No duplicate corrupt rows. HTTP status is not specified — record actual without inventing codes.

## Type
Unspecified (concurrency)

## Why the AI missed this
API characteristic — TC-CART-SEC-007 tested sequential cross-user IDOR; same-user GET during POST may expose partial cart state or stale JWT-scoped snapshot under race.

## Audit (human SUP)
- **Status:** VALID
- **Reasoning:** Same-user GET∥POST race; IDOR clause correct.

## Status / Related bugs
Not Run / None
