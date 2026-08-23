# TC-CART-SEC-SUP-005: Extreme quantity integer overflow probe

## Requirement ID
FR-07 / SEC-06

## Module / Test type / Technique
cart / Security / Human extension (SEC-SUP)

## Security requirement(s)
SEC-06

## Threat / probe
Extreme quantity integer overflow probe

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.

## Test data
```json
{
  "body": {
    "id": 1,
    "name": "iPhone",
    "price": 30000000,
    "quantity": 999999999
  }
}
```

## Test steps
1. POST /api/cart id=1 quantity=999999999.
2. GET /api/cart.

## Expected result
Extreme quantity not specified. Record stored qty on GET; note any integer wrap or overflow. Do not require reject/clamp unless observed. HTTP status is not specified — record actual without inventing codes.

## Type
Boundary / integrity observe

## Why the AI missed this
Prompt quality — domain partitions covered qty boundaries for FR-07 functionally; security pass did not reuse INT_MAX-scale qty as integrity/DoS probe against cart total.

## Audit (human SUP)
- **Status:** INCOMPLETE
- **Reasoning:** Oracle required reject/clamp; extreme qty not specified in spec.

## Status / Related bugs
Not Run / None
