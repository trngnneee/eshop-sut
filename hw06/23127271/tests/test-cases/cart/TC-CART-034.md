# TC-CART-034: Reject malformed JWT

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
| Authorization | Bearer not-a-jwt |

## Test steps
1. POST /api/cart with Authorization: Bearer not-a-jwt and valid body.

## Expected result
POST /api/cart requires Authorization: Bearer <token> (API spec §4). No cart line is added for this caller. HTTP status is not specified.

## Sub-domains covered
C-AUTH-05

## Type
Invalid

## Audit
- **Status:** INCOMPLETE
- **Reasoning:** Malformed token is not a valid JWT. HTTP 403/401 is not specified.

## Status / Related bugs
Not Run / None
