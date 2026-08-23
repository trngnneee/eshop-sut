# TC-CART-006: Adding the same product again merges quantity (FR-07)

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
- POST /api/cart once with id=1 quantity=1 (or ensure cart already has product 1 qty=1).
- GET /api/cart: exactly one line for id=1 with qty=1.

## Test data
| Field | Value |
|-------|-------|
| id | 1 |
| name | iPhone 15 Pro Max |
| price | 30000000 |
| quantity | 1 |

## Test steps
1. POST /api/cart again with the same product id=1 and quantity=1.
2. GET /api/cart.

## Expected result
GET /api/cart shows exactly one line for product 1 with quantity 2 (1+1). A second row for the same product fails FR-07. Success status/body not specified.

## Sub-domains covered
C-STATE-02, C-ID-01, C-QTY-01, C-AUTH-01

## Type
Valid

## Audit
- **Status:** VALID
- **Reasoning:** FR-07: adding the same product increases quantity and must not create a new line.

## Status / Related bugs
Not Run / None
