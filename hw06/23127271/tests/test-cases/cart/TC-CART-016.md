# TC-CART-016: quantity=0 — not specified as invalid for this API

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
| quantity | 0 |
| id | 1 |
| name | iPhone 15 Pro Max |
| price | 30000000 |

## Test steps
1. POST /api/cart with quantity=0 and other fields valid.
2. GET /api/cart.

## Expected result
The SRS and api_specification.md do not state this input is invalid or required. Do not expect rejection. Record what the SUT does; do not fail it against an invented rule.

## Sub-domains covered
C-QTY-04, C-ID-01, C-PRICE-01, C-NAME-01, C-AUTH-01

## Type
Unspecified

## Audit
- **Status:** INVALID
- **Reasoning:** FR-06 quantity ≥ 1 is the product-detail UI control, not a POST /api/cart rule. Applying it here was an assumption.

## Status / Related bugs
Not Run / None
