# TC-CART-ST-SUP-005: Race — POST /api/cart concurrent with POST /api/checkout on C_MULTI

## Requirement ID
FR-07 / FR-08

## Module / Test type / Technique
cart / Functional / State Transition Testing (human extension)

## State machine
C_MULTI → checkout ∥ add → ?

## Transition under test
concurrent checkout vs add

## Preconditions
- EShop at http://localhost:3000.
- Login test@eshop.com.
- Cart non-empty.
- Snapshot C_MULTI.

## Test data
| (see steps) | |

## Test steps
1. Fire POST /api/checkout (valid body) and POST /api/cart id=1 qty=1 in parallel
2. GET /api/cart

## Expected result
Outcome not specified. Record final GET /api/cart line count/qty and whether checkout completed. Must not show corrupt duplicate lines for same id. Cross-FR probe (FR-07 + FR-08). HTTP status is not specified — record actual without inventing codes.

## States / transitions covered
C_MULTI→C_EMPTY or C_MULTI+

## Type
Unspecified (concurrency)

## Why the AI missed this
API characteristic — FR-08 clears cart on successful checkout but says nothing about an add in flight; in-memory SUT may drop items or duplicate. AI never combined checkout with parallel POST.

## Audit (human SUP)
- **Status:** INCOMPLETE
- **Reasoning:** Checkout∥POST is cross-FR concurrency; oracle corrected to observe-only without mandating empty cart.

## Status / Related bugs
Not Run / None
