# TC-CART-ST-002: SINGLE → MERGED — same product increases quantity

## Requirement ID
FR-07

## Module / Test type / Technique
cart / Functional / State Transition Testing

## State machine
C_SINGLE → C_MERGED (FR-07 merge rule)

## Transition under test
C_SINGLE → C_MERGED

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!
- Cart has id=1 qty=1.

## Test data
| (see steps — multi-step sequence) | |

## Test steps
1. POST /api/cart id=1 qty=1 again.
2. GET /api/cart.

## Expected result
GET /api/cart shows one line id=1 qty=2. No second row. FR-07: adding the same product increases quantity and must not create a new line. Success status/body for POST /api/cart is not specified.

## States / transitions covered
C_SINGLE→C_MERGED

## Type
Legal

## Audit
- **Status:** VALID
- **Reasoning:** FR-07 merge when same product added again — core legal transition.

## Status / Related bugs
Not Run / None
