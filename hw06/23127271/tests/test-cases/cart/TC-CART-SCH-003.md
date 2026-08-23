# TC-CART-SCH-003: Cart line id is number

## Requirement ID
FR-07

## Module / Test type / Technique
cart / Schema validation / Response & request shape

## Schema aspect
Line item id type

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.
- One item in cart.

## Test data
| (see steps) | |

## Test steps
1. POST one item per api_spec example.
2. GET /api/cart — first element typeof id === 'number'.

## Expected result
Each line has id as JSON number per POST example (id:1).

## Schema contract reference
api_spec section 4.2 POST body id numeric.

## Type
Schema validation

## Audit
- **Status:** VALID
- **Reasoning:** api_spec section 4.2 POST example types id as number.

## Status / Related bugs
Not Run / None
