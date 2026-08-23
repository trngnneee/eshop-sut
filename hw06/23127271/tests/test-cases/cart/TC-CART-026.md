# TC-CART-026: price as JSON string — coercion not specified

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
| price | "30000000" |
| id | 1 |
| name | iPhone 15 Pro Max |
| quantity | 2 |

## Test steps
1. POST /api/cart with price as JSON string "30000000".
2. GET /api/cart.

## Expected result
No type-coercion rule is specified. Do not expect accept, reject, or a particular coerced value. Record actual behaviour.

## Sub-domains covered
C-PRICE-05, C-ID-01, C-QTY-02

## Type
Unspecified

## Audit
- **Status:** INCOMPLETE
- **Reasoning:** Price type coercion is not specified.

## Status / Related bugs
Not Run / None
