# TC-CART-SEC-SUP-001: Race — parallel POST same id with price=1 vs catalogue price

## Requirement ID
FR-07 / SEC-06

## Module / Test type / Technique
cart / Security / Human extension (SEC-SUP)

## Security requirement(s)
SEC-06

## Threat / probe
Race — parallel POST same id with price=1 vs catalogue price

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.
- GET /api/cart empty.

## Test data
```json
{
  "sequence": [
    "POST id=1 name=iPhone price=1 qty=1",
    "POST id=1 name=iPhone price=30000000 qty=1 — parallel",
    "GET /api/cart"
  ]
}
```

## Test steps
1. POST id=1 name=iPhone price=1 qty=1
2. POST id=1 name=iPhone price=30000000 qty=1 — parallel
3. GET /api/cart

## Expected result
Parallel POST same id with different client prices. Record stored price and qty on GET (merge may yield qty=2). FR-08 governs checkout totals, not POST /api/cart — do not fail solely because price=1 was stored. HTTP status is not specified — record actual without inventing codes.

## Type
Integrity observe (unspecified)

## Why the AI missed this
Prompt quality — TC-CART-SEC-006 tested price tampering sequentially; parallel client price writes are the realistic attack for in-memory cart without locking.

## Audit (human SUP)
- **Status:** INVALID
- **Reasoning:** Same flaw as audited TC-CART-SEC-006: invented mandatory catalogue price on POST /api/cart.

## Status / Related bugs
Not Run / None
