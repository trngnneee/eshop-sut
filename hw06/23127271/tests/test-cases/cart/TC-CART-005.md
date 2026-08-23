# TC-CART-005: Admin JWT can add to the admin's own cart

## Requirement ID
FR-07

## Module / Test type / Technique
cart / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- EShop backend is running at http://localhost:3000.
- Seed admin admin@eshop.com / Admin123! exists (role=admin).
- Obtain an admin JWT via POST /api/login with email=admin@eshop.com password=Admin123!.
- GET /api/cart as admin and snapshot.

## Test data
| Field | Value |
|-------|-------|
| Authorization | Bearer <admin_token> |
| id | 1 |
| quantity | 1 |
| name | iPhone 15 Pro Max |
| price | 30000000 |

## Test steps
1. POST /api/cart as admin with valid body.
2. GET /api/cart as admin.

## Expected result
GET /api/cart with the same admin token shows the added line on that user's cart. Success status/body not specified.

## Sub-domains covered
C-AUTH-02, C-ID-01, C-QTY-01

## Type
Valid

## Audit
- **Status:** VALID
- **Reasoning:** Cart API requires a token, not role=user. An admin JWT is a logged-in user.

## Status / Related bugs
Not Run / None
