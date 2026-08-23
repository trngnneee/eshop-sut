# TC-CART-ST-007: MERGED qty=5 → add 3 → qty=8

## Requirement ID
FR-07

## Module / Test type / Technique
cart / Functional / State Transition Testing

## State machine
C_MERGED(5) → C_MERGED(8)

## Transition under test
quantity accumulation

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!
- Cart id=1 qty=5.

## Test data
| (see steps — multi-step sequence) | |

## Test steps
1. POST /api/cart id=1 qty=3.
2. GET /api/cart.

## Expected result
One line id=1 qty=8 (5+3). FR-07: adding the same product increases quantity and must not create a new line. Success status/body for POST /api/cart is not specified.

## States / transitions covered
C_MERGED(5)→C_MERGED(8)

## Type
Legal

## Audit
- **Status:** VALID
- **Reasoning:** Quantity accumulation via merge is FR-07.

## Status / Related bugs
Not Run / None
