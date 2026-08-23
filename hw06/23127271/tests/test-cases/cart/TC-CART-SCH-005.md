# TC-CART-SCH-005: Cart line price is number

## Requirement ID
FR-07

## Module / Test type / Technique
cart / Schema validation / Response & request shape

## Schema aspect
Line item price type

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.
- Item in cart.

## Test data
| (see steps) | |

## Test steps
1. GET /api/cart.
2. Assert each line.price typeof number.

## Expected result
price is JSON number on each line (not string).

## Schema contract reference
api_spec POST example price:100000 number.

## Type
Schema validation

## Audit
- **Status:** VALID
- **Reasoning:** price is number in POST example; string price would be a schema deviation.

## Status / Related bugs
Not Run / None
