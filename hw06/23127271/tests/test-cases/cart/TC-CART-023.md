# TC-CART-023: price=0 — not specified as invalid for this API

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
| price | 0 |
| id | 1 |
| name | iPhone 15 Pro Max |
| quantity | 2 |

## Test steps
1. POST /api/cart with price=0.
2. GET /api/cart.

## Expected result
The SRS and api_specification.md do not state this input is invalid or required. Do not expect rejection. Record what the SUT does; do not fail it against an invented rule.

## Sub-domains covered
C-PRICE-02, C-ID-01, C-QTY-02, C-AUTH-01

## Type
Unspecified

## Audit
- **Status:** INVALID
- **Reasoning:** FR-15 price > 0 is product CRUD, not POST /api/cart.

## Status / Related bugs
Not Run / None
