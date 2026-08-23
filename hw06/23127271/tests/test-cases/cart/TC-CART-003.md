# TC-CART-003: Add last seed product id=5 with matching unicode name

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
- Seed product id=5 exists: Bàn phím cơ Keychron Q1, price 4000000.

## Test data
| Field | Value |
|-------|-------|
| id | 5 |
| name | Bàn phím cơ Keychron Q1 |
| price | 4000000 |
| quantity | 2 |

## Test steps
1. POST /api/cart for product 5.
2. GET /api/cart.

## Expected result
GET /api/cart as the same user includes a line for id=5. Success status/body not specified.

## Sub-domains covered
C-ID-02, C-NAME-05, C-QTY-02, C-AUTH-01

## Type
Valid

## Audit
- **Status:** VALID
- **Reasoning:** Another seed product with a typical body. No charset restriction. Does not invent catalogue-match rules.

## Status / Related bugs
Not Run / None
