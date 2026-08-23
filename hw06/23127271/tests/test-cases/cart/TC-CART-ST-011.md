# TC-CART-ST-011: MULTI → checkout → EMPTY (FR-08 clears cart)

## Requirement ID
FR-07 / FR-08

## Module / Test type / Technique
cart / Functional / State Transition Testing

## State machine
C_MULTI → C_EMPTY after successful checkout

## Transition under test
C_MULTI → C_EMPTY

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!
- Cart has at least one line.

## Test data
| (see steps — multi-step sequence) | |

## Test steps
1. POST /api/cart until cart non-empty. GET snapshot C_MULTI.
2. POST /api/checkout with shipping_address (total per cart).
3. GET /api/cart.

## Expected result
FR-08: after successful checkout the cart is cleared. Checkout success status/body and order shape are not specified.

## States / transitions covered
C_MULTI→C_EMPTY

## Type
Legal (cross-endpoint FR-08)

## Audit
- **Status:** INCOMPLETE
- **Reasoning:** FR-08 cart-clear after successful checkout is spec-backed. Generated oracle also asserted order status pending (FR-10) and assumed checkout success shape — not required for this cart transition test.

## Status / Related bugs
Not Run / None
