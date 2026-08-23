# TC-CART-ST-SUP-003: Failed checkout — cart stays C_MULTI (illegal empty transition)

## Requirement ID
FR-07 / FR-08

## Module / Test type / Technique
cart / Functional / State Transition Testing (human extension)

## State machine
C_MULTI → failed checkout → C_MULTI

## Transition under test
illegal / failed checkout

## Preconditions
- EShop at http://localhost:3000.
- Login test@eshop.com.
- Cart non-empty.
- Snapshot C_MULTI.

## Test data
| (see steps) | |

## Test steps
1. POST /api/checkout with invalid body (e.g. missing shipping_address or total_amount=0)
2. GET /api/cart

## Expected result
FR-08 clears cart only after successful checkout. On failed checkout, GET /api/cart should still show C_MULTI lines — failure mode not specified. Record checkout status and cart snapshot. Cross-FR probe (FR-07 cart state via FR-08). HTTP status is not specified — record actual without inventing codes.

## States / transitions covered
C_MULTI→C_MULTI

## Type
Illegal / Unspecified (FR-07/FR-08)

## Why the AI missed this
Prompt quality — ST-011 only covered successful checkout→EMPTY (FR-08 happy path); failed checkout leaving cart intact is the negative counterpart and was omitted.

## Audit (human SUP)
- **Status:** INCOMPLETE
- **Reasoning:** Valid FR-08 negative cart transition but primary action is POST /api/checkout (cross-FR); relabelled observe-only.

## Status / Related bugs
Not Run / None
