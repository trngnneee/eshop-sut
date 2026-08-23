# TC-CART-015: id as JSON string — coercion not specified

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
| id | "1" |
| name | iPhone 15 Pro Max |
| price | 30000000 |
| quantity | 2 |

## Test steps
1. POST /api/cart with id as JSON string "1".
2. GET /api/cart.

## Expected result
No type-coercion rule is specified. Do not expect accept, reject, or a particular coerced value. Record actual behaviour.

## Sub-domains covered
C-ID-07, C-QTY-02, C-AUTH-01

## Type
Unspecified

## Audit
- **Status:** INCOMPLETE
- **Reasoning:** Example id is a number; coercion of string '1' is not specified. Generated case still preferred reject/coerce.

## Status / Related bugs
Not Run / None
