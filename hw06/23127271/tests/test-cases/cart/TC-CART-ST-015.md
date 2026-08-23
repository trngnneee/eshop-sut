# TC-CART-ST-015: Cart survives re-login (persistence boundary)

## Requirement ID
FR-07

## Module / Test type / Technique
cart / Functional / State Transition Testing

## State machine
C_SINGLE → (new token) → C_SINGLE

## Transition under test
session boundary

## Preconditions
- EShop at http://localhost:3000.

## Test data
| (see steps — multi-step sequence) | |

## Test steps
1. Login test@eshop.com. POST id=1 qty=1. GET → C_SINGLE.
2. Login again (new token). GET /api/cart.

## Expected result
After re-login, GET /api/cart still shows id=1 if cart is server-persisted per user. If in-memory only, record actual — persistence medium not specified.

## States / transitions covered
C_SINGLE→C_SINGLE

## Type
Legal / Unspecified

## Audit
- **Status:** VALID
- **Reasoning:** Session-boundary probe; oracle already flags persistence medium as unspecified.

## Status / Related bugs
Not Run / None
