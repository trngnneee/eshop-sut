# TC-CART-038: Extra field color — handling not specified

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
| color | red |
| id | 1 |
| name | iPhone 15 Pro Max |
| price | 30000000 |
| quantity | 2 |

## Test steps
1. POST /api/cart with documented fields plus color=red.
2. GET /api/cart.

## Expected result
Extra-field handling is not specified. Documented fields may still update. Do not assert how the extra field is stored or rejected.

## Sub-domains covered
C-BODY-05, C-ID-01, C-QTY-02

## Type
Unspecified

## Audit
- **Status:** INCOMPLETE
- **Reasoning:** Extra-field policy is not specified. Asserting color must not affect merge/price invents a rule.

## Status / Related bugs
Not Run / None
