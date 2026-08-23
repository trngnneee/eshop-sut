# TC-CART-025: Omit price — not specified as required

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
| price | (omitted) |
| id | 1 |
| name | iPhone 15 Pro Max |
| quantity | 2 |

## Test steps
1. POST /api/cart omitting price.
2. GET /api/cart.

## Expected result
price is not specified as required on POST /api/cart. Do not expect rejection. Observe whether a cart line is added and what price (if any) is stored. Do not apply FR-15 (product CRUD price > 0) to this endpoint.

## Sub-domains covered
C-PRICE-04, C-ID-01, C-QTY-02

## Type
Unspecified

## Audit
- **Status:** INVALID
- **Reasoning:** C-PRICE-04: the API example includes price. Neither FR-07 nor api_specification.md says price is mandatory on every POST /api/cart. Required-on-body was assumed.

## Status / Related bugs
Not Run / None
