# TC-CART-004: Quantity=10 (valid, no documented max)

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
| id | 1 |
| name | iPhone 15 Pro Max |
| price | 30000000 |
| quantity | 10 |

## Test steps
1. POST /api/cart with quantity=10.
2. GET /api/cart.

## Expected result
GET /api/cart includes a line for id=1 reflecting quantity 10 (or merged). Success status/body not specified.

## Sub-domains covered
C-QTY-03, C-ID-01, C-AUTH-01

## Type
Valid

## Audit
- **Status:** VALID
- **Reasoning:** No maximum quantity is stated, so quantity=10 is not specified as invalid. Treated as a typical valid representative, not as a proven max.

## Status / Related bugs
Not Run / None
