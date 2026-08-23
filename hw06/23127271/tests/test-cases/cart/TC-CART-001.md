# TC-CART-001: Add existing product with typical valid body (on-point)

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
| quantity | 2 |

## Test steps
1. POST /api/cart with the valid body and user JWT.
2. GET /api/cart.

## Expected result
The authenticated user's cart includes a line for product id=1 with quantity 2 (or merged qty if a line already existed — FR-07). Success status/body are not specified.

## Sub-domains covered
C-ID-01, C-QTY-02, C-PRICE-01, C-NAME-01, C-AUTH-01, C-STATE-01, C-BODY-01

## Type
Valid

## Audit
- **Status:** VALID
- **Reasoning:** Documented POST /api/cart body with a typical quantity from the example, under required auth. No extra reject rule claimed.

## Status / Related bugs
Not Run / None
