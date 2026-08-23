# TC-CART-SCH-001: GET /api/cart returns JSON array

## Requirement ID
FR-07

## Module / Test type / Technique
cart / Schema validation / Response & request shape

## Schema aspect
GET response root type

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.

## Test data
| (see steps) | |

## Test steps
1. GET /api/cart.
2. Assert Array.isArray(body) === true.

## Expected result
Root body is JSON array (cart lines list). Response Content-Type header includes application/json (or charset=utf-8 JSON body).

## Schema contract reference
api_spec section 4.1 cart list — implied collection.

## Type
Schema validation

## Audit
- **Status:** VALID
- **Reasoning:** Cart is modeled as a list of line objects; JSON array root + Content-Type is a valid schema check.

## Status / Related bugs
Not Run / None
