# TC-CART-SCH-006: Cart line quantity is number

## Requirement ID
FR-07

## Module / Test type / Technique
cart / Schema validation / Response & request shape

## Schema aspect
Line item quantity type

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.
- Item in cart.

## Test data
| (see steps) | |

## Test steps
1. GET /api/cart.
2. Assert each line.quantity typeof number.

## Expected result
quantity is JSON number on each line.

## Schema contract reference
api_spec POST example quantity:2 number.

## Type
Schema validation

## Audit
- **Status:** VALID
- **Reasoning:** quantity is number in POST example.

## Status / Related bugs
Not Run / None
