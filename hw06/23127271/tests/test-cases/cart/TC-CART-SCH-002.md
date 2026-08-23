# TC-CART-SCH-002: Empty cart is empty array []

## Requirement ID
FR-07

## Module / Test type / Technique
cart / Schema validation / Response & request shape

## Schema aspect
Empty cart shape

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.
- Cart cleared or fresh user.

## Test data
| (see steps) | |

## Test steps
1. GET /api/cart on empty cart.

## Expected result
Body equals JSON empty array [] (length 0), not null or {}.

## Schema contract reference
FR-07 empty-cart UI implies no lines — array envelope.

## Type
Schema validation

## Audit
- **Status:** VALID
- **Reasoning:** Empty cart as [] follows list semantics; null or {} would violate array contract.

## Status / Related bugs
Not Run / None
