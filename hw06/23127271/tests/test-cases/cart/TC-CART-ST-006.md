# TC-CART-ST-006: EMPTY → two POST same id → one merged line (not two rows)

## Requirement ID
FR-07

## Module / Test type / Technique
cart / Functional / State Transition Testing

## State machine
C_EMPTY → C_MERGED via double POST

## Transition under test
C_EMPTY → C_MERGED

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!
- Empty cart.

## Test data
| (see steps — multi-step sequence) | |

## Test steps
1. POST /api/cart id=1 qty=1.
2. POST /api/cart id=1 qty=1.
3. GET /api/cart.

## Expected result
Exactly one line id=1 qty=2 after both POSTs. FR-07: adding the same product increases quantity and must not create a new line. Success status/body for POST /api/cart is not specified.

## States / transitions covered
C_EMPTY→C_MERGED

## Type
Legal

## Audit
- **Status:** VALID
- **Reasoning:** Two POSTs of same id from empty must merge per FR-07, not create two rows.

## Status / Related bugs
Not Run / None
