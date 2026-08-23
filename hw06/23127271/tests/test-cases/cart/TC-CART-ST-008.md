# TC-CART-ST-008: Idempotent POST from SINGLE — merged not duplicated

## Requirement ID
FR-07

## Module / Test type / Technique
cart / Functional / State Transition Testing

## State machine
C_SINGLE → C_MERGED (repeat identical POST)

## Transition under test
idempotent add

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!
- Cart id=1 qty=2.

## Test data
| (see steps — multi-step sequence) | |

## Test steps
1. POST /api/cart identical body id=1 qty=2.
2. GET /api/cart.

## Expected result
One line id=1 qty=4 (2+2). Never two rows for id=1. FR-07: adding the same product increases quantity and must not create a new line. Success status/body for POST /api/cart is not specified.

## States / transitions covered
C_SINGLE→C_MERGED

## Type
Legal (idempotency)

## Audit
- **Status:** VALID
- **Reasoning:** Repeat POST with same id tests idempotent merge behaviour under FR-07.

## Status / Related bugs
Not Run / None
