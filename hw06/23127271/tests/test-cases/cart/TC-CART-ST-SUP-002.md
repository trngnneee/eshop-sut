# TC-CART-ST-SUP-002: Race — two POST /api/cart same id=1 fired back-to-back from C_EMPTY

## Requirement ID
FR-07

## Module / Test type / Technique
cart / Functional / State Transition Testing (human extension)

## State machine
C_EMPTY → POST ∥ POST → C_MERGED or corrupt

## Transition under test
concurrent merge race

## Preconditions
- EShop at http://localhost:3000.
- Login test@eshop.com.
- GET cart empty.

## Test data
| (see steps) | |

## Test steps
1. Fire two POST /api/cart id=1 qty=1 as close together as possible (script/Postman parallel)
2. GET /api/cart

## Expected result
FR-07 requires at most one line for id=1 with qty=2 after both adds succeed. If two separate lines for id=1 appear, that violates merge. Record line count and qty. HTTP status is not specified — record actual without inventing codes.

## States / transitions covered
C_EMPTY→C_MERGED?

## Type
Unspecified (concurrency)

## Why the AI missed this
API characteristic + checklist gap — FR-07 merge is synchronous in spec text but in-memory cart without locking may create two lines under race; AI never generated parallel POST probes.

## Audit (human SUP)
- **Status:** VALID
- **Reasoning:** Parallel POST race; merge violation if duplicate lines is FR-07-backed.

## Status / Related bugs
Not Run / None
