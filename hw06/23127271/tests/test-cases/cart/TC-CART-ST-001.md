# TC-CART-ST-001: EMPTY → SINGLE — first add creates one line

## Requirement ID
FR-07

## Module / Test type / Technique
cart / Functional / State Transition Testing

## State machine
C_EMPTY → C_SINGLE

## Transition under test
C_EMPTY → C_SINGLE

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!
- GET /api/cart → [] (empty).

## Test data
| (see steps — multi-step sequence) | |

## Test steps
1. POST /api/cart id=1 qty=1.
2. GET /api/cart.

## Expected result
GET /api/cart shows exactly one line id=1 qty=1 (C_SINGLE). FR-07: adding the same product increases quantity and must not create a new line.

## States / transitions covered
C_EMPTY→C_SINGLE

## Type
Legal

## Audit
- **Status:** VALID
- **Reasoning:** EMPTY to one line is the base cart state transition under authenticated POST /api/cart.

## Status / Related bugs
Not Run / None
