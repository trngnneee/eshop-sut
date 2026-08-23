# TC-CART-SCH-004: Cart line name is string

## Requirement ID
FR-07

## Module / Test type / Technique
cart / Schema validation / Response & request shape

## Schema aspect
Line item name type

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.
- Item in cart.

## Test data
| (see steps) | |

## Test steps
1. GET /api/cart.
2. Assert each line.name typeof string.

## Expected result
name is string on every cart line object.

## Schema contract reference
api_spec POST example name string.

## Type
Schema validation

## Audit
- **Status:** VALID
- **Reasoning:** name is string in POST example and on stored cart lines.

## Status / Related bugs
Not Run / None
