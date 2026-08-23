# TC-CART-007: Adding a different product creates a new line

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
- Ensure cart has product 1 only.
- Seed product 2 exists: Samsung Galaxy S24 Ultra, 28000000.

## Test data
| Field | Value |
|-------|-------|
| id | 2 |
| name | Samsung Galaxy S24 Ultra |
| price | 28000000 |
| quantity | 1 |

## Test steps
1. POST /api/cart for product 2.
2. GET /api/cart.

## Expected result
GET /api/cart contains distinct lines for id=1 and id=2. Product 1 quantity is unchanged.

## Sub-domains covered
C-STATE-03, C-ID-01, C-ID-02, C-AUTH-01

## Type
Valid

## Audit
- **Status:** VALID
- **Reasoning:** FR-07 merge applies to the same product; a different id is a different line.

## Status / Related bugs
Not Run / None
