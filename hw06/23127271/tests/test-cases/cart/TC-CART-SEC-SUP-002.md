# TC-CART-SEC-SUP-002: Negative quantity integrity probe

## Requirement ID
FR-07 / SEC-06

## Module / Test type / Technique
cart / Security / Human extension (SEC-SUP)

## Security requirement(s)
SEC-06

## Threat / probe
Negative quantity integrity probe

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
    "quantity": -1
  }
}
```

## Test steps
1. POST /api/cart with quantity=-1.
2. GET /api/cart.

## Expected result
Negative quantity not specified for POST /api/cart. Record whether line is added, qty stored negative, or request rejected. GET must not show corrupt cart state. HTTP status is not specified — record actual without inventing codes.

## Type
Illegal / integrity observe

## Why the AI missed this
Model limitation — AI focused on auth/SQLi/XSS/price tampering; negative qty is an integrity edge (refund/credit exploit) not visible in spec example body.

## Audit (human SUP)
- **Status:** INCOMPLETE
- **Reasoning:** Negative qty not a specified invalid class for POST /api/cart (FR-06 is UI).

## Status / Related bugs
Not Run / None
