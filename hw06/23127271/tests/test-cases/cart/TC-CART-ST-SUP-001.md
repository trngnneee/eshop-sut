# TC-CART-ST-SUP-001: C_THREE — merge on line 2 (id=2), lines 1 and 3 unchanged

## Requirement ID
FR-07

## Module / Test type / Technique
cart / Functional / State Transition Testing (human extension)

## State machine
C_THREE → POST id=2 → C_THREE'

## Transition under test
merge non-first line

## Preconditions
- EShop at http://localhost:3000.
- Login test@eshop.com.
- Cart has id=1 qty=1, id=2 qty=1, id=3 qty=1.

## Test data
| (see steps) | |

## Test steps
1. POST id=2 qty=2
2. GET /api/cart

## Expected result
FR-07: id=2 qty=3 (1+2 merged). id=1 and id=3 each qty=1 unchanged. Still three lines. No duplicate row for id=2. Success status/body not specified.

## States / transitions covered
C_THREE→C_THREE'

## Type
Legal

## Why the AI missed this
Prompt quality — merge cases (ST-002, ST-004) always targeted product id=1; multi-line cart + merge on middle line was never combined (1x1 bias toward first seed product).

## Audit (human SUP)
- **Status:** VALID
- **Reasoning:** Merge on middle line of 3-line cart; FR-07 merge arithmetic.

## Status / Related bugs
Not Run / None
