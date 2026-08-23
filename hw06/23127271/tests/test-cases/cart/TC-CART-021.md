# TC-CART-021: quantity=null — not specified as invalid

## Requirement ID
FR-07

## Module / Test type / Technique
cart / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- EShop backend is running at http://localhost:3000.
- Seed user test@eshop.com / Test1234! exists (role=user).
- Obtain a user JWT via POST /api/login with email=test@eshop.com password=Test1234!.
- GET /api/cart and snapshot line items (prefer empty cart; if not empty, record ids/qty).
- Seed product id=1 exists: iPhone 15 Pro Max, price 30000000.

## Test data
| Field | Value |
|-------|-------|
| quantity | null |
| id | 1 |
| name | iPhone 15 Pro Max |
| price | 30000000 |

## Test steps
1. POST /api/cart with quantity=null and other fields valid.
2. GET /api/cart.

## Expected result
The SRS and api_specification.md do not state this input is invalid or required. Do not expect rejection. Record what the SUT does; do not fail it against an invented rule.

## Sub-domains covered
C-QTY-09, C-ID-01, C-PRICE-01, C-NAME-01, C-AUTH-01

## Type
Unspecified

## Audit
- **Status:** INVALID
- **Reasoning:** quantity=null is not specified as invalid.

## Status / Related bugs
Not Run / None
