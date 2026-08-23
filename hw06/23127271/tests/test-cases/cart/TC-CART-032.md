# TC-CART-032: Reject add-to-cart with no Authorization header

## Requirement ID
FR-07

## Module / Test type / Technique
cart / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- EShop backend is running at http://localhost:3000.
- Do not send a token.

## Test data
| Field | Value |
|-------|-------|
| Authorization | (omitted) |
| body | {"id": 1, "name": "iPhone 15 Pro Max", "price": 30000000, "quantity": 2} |

## Test steps
1. POST /api/cart with valid body and no Authorization header.

## Expected result
POST /api/cart requires Authorization: Bearer <token> (API spec §4). No cart line is added for this caller. HTTP status is not specified.

## Sub-domains covered
C-AUTH-03

## Type
Invalid

## Audit
- **Status:** INCOMPLETE
- **Reasoning:** Auth is required (API spec §4). HTTP 401 is not specified.

## Status / Related bugs
Not Run / None
