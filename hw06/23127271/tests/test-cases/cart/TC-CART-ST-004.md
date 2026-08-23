# TC-CART-ST-004: TWO_LINES → merge on line 1, line 2 unchanged

## Requirement ID
FR-07

## Module / Test type / Technique
cart / Functional / State Transition Testing

## State machine
C_TWO → C_TWO(merged L1)

## Transition under test
C_TWO → C_TWO'

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!
- Cart: id=1 qty=1, id=2 qty=1.

## Test data
| (see steps — multi-step sequence) | |

## Test steps
1. POST /api/cart id=1 qty=2.
2. GET /api/cart.

## Expected result
id=1 qty=3 (1+2 merged), id=2 qty=1 unchanged, two lines total. FR-07: adding the same product increases quantity and must not create a new line. Success status/body for POST /api/cart is not specified.

## States / transitions covered
C_TWO→C_TWO'

## Type
Legal

## Audit
- **Status:** VALID
- **Reasoning:** Merge on an existing line while another line stays unchanged — FR-07 in multi-line cart.

## Status / Related bugs
Not Run / None
