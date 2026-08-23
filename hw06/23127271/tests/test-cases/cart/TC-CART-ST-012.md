# TC-CART-ST-012: After checkout EMPTY → fresh SINGLE (no stale lines)

## Requirement ID
FR-07 / FR-08

## Module / Test type / Technique
cart / Functional / State Transition Testing

## State machine
C_EMPTY(post-checkout) → C_SINGLE

## Transition under test
post-checkout fresh add

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!
- Cart empty after prior checkout.

## Test data
| (see steps — multi-step sequence) | |

## Test steps
1. POST /api/cart id=1 qty=1.
2. GET /api/cart.

## Expected result
GET shows exactly one new line id=1 qty=1. No lines from any prior non-empty cart state.

## States / transitions covered
C_EMPTY→C_SINGLE

## Type
Legal

## Audit
- **Status:** VALID
- **Reasoning:** After cart is empty (post-checkout per FR-08), a new POST starts a fresh SINGLE line.

## Status / Related bugs
Not Run / None
