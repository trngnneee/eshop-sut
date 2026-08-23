# TC-CART-SCH-011: GET cart Content-Type is JSON

## Requirement ID
FR-07

## Module / Test type / Technique
cart / Schema validation / Response & request shape

## Schema aspect
Content-Type header

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.

## Test data
| (see steps) | |

## Test steps
1. GET /api/cart.
2. Inspect Content-Type header.

## Expected result
Response Content-Type header includes application/json (or charset=utf-8 JSON body).

## Schema contract reference
Checklist section 4 Content-Type.

## Type
Schema validation

## Audit
- **Status:** VALID
- **Reasoning:** Content-Type application/json is a standard schema contract check.

## Status / Related bugs
Not Run / None
