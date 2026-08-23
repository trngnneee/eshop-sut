# TC-CART-022: Very large quantity — no max specified

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
| quantity | 999999999 |
| id | 1 |
| name | iPhone 15 Pro Max |
| price | 30000000 |

## Test steps
1. POST /api/cart with quantity=999999999.
2. GET /api/cart.

## Expected result
No maximum length/quantity is specified. Do not expect accept or reject. Record actual behaviour.

## Sub-domains covered
C-QTY-10, C-ID-01, C-AUTH-01

## Type
Unspecified

## Audit
- **Status:** INCOMPLETE
- **Reasoning:** No max quantity is specified. 'Must not crash' is not a written requirement.

## Status / Related bugs
Not Run / None
