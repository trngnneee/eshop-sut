# TC-CART-ST-SUP-004: C_THREE — merge on line 3 (id=3), lines 1 and 2 unchanged

## Requirement ID
FR-07

## Module / Test type / Technique
cart / Functional / State Transition Testing (human extension)

## State machine
C_THREE → POST id=3 → C_THREE'

## Transition under test
merge last line

## Preconditions
- EShop at http://localhost:3000.
- Login test@eshop.com.
- Cart has id=1 qty=1, id=2 qty=1, id=3 qty=1.

## Test data
| (see steps) | |

## Test steps
1. POST id=3 qty=4
2. GET /api/cart

## Expected result
FR-07: id=3 qty=5 (1+4 merged). id=1 and id=2 each qty=1 unchanged. Three lines total. No duplicate row for id=3.

## States / transitions covered
C_THREE→C_THREE'

## Type
Legal

## Why the AI missed this
Prompt quality — SUP-001 fixed merge on line 2; AI never enumerated merge on line 3 in a three-line cart (complete the N-line merge matrix).

## Audit (human SUP)
- **Status:** VALID
- **Reasoning:** Merge on line 3 completes matrix; FR-07 merge.

## Status / Related bugs
Not Run / None
