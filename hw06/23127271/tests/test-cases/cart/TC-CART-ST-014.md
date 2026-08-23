# TC-CART-ST-014: Unequal merge operands 2+3 from EMPTY sequence

## Requirement ID
FR-07

## Module / Test type / Technique
cart / Functional / State Transition Testing

## State machine
C_EMPTY → C_MERGED qty=5

## Transition under test
C_EMPTY → C_MERGED(5)

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!
- Empty cart.

## Test data
| (see steps — multi-step sequence) | |

## Test steps
1. POST id=1 qty=2.
2. POST id=1 qty=3.
3. GET /api/cart.

## Expected result
One line id=1 qty=5. FR-07: adding the same product increases quantity and must not create a new line. Success status/body for POST /api/cart is not specified.

## States / transitions covered
C_EMPTY→C_MERGED(5)

## Type
Legal

## Audit
- **Status:** VALID
- **Reasoning:** Unequal merge operands 2+3 from empty — FR-07.

## Status / Related bugs
Not Run / None
