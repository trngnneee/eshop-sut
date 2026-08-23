# TC-CART-002: Add with quantity=1 (typical value; FR-06 is product-detail UI, not this API)

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
| quantity | 1 |

## Test steps
1. POST /api/cart with quantity=1.
2. GET /api/cart.

## Expected result
Quantity 1 is not specified as the API minimum. Treat as a typical add: GET /api/cart includes product 1. Do not use this case to prove an API min=1 rule. Success status/body not specified.

## Sub-domains covered
C-QTY-01, C-ID-01, C-PRICE-01, C-NAME-01, C-AUTH-01

## Type
Valid

## Audit
- **Status:** INCOMPLETE
- **Reasoning:** FR-06's 'quantity ≥ 1' is the product-detail UI box, not a stated POST /api/cart rule. Quantity 1 is still a reasonable typical value from the example domain (example uses 2).

## Status / Related bugs
Not Run / None
