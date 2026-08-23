# TC-CART-036: Send malformed JSON (not the documented JSON body)

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
| body | {id: |

## Test steps
1. POST /api/cart with body `{id:`.

## Expected result
The body is not the documented JSON object. Do not treat this payload as a successful add. HTTP status is not specified.

## Sub-domains covered
C-BODY-03, C-AUTH-01

## Type
Invalid

## Audit
- **Status:** INCOMPLETE
- **Reasoning:** Body is documented as JSON. Malformed text is not JSON. HTTP 400 is not specified.

## Status / Related bugs
Not Run / None
