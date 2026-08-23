# TC-PROFILE-ST-SUP-005: Partial chain — address-only then name-only (missing 2-of-3 path)

## Requirement ID
FR-04

## Module / Test type / Technique
profile / Functional / State Transition Testing (human extension)

## State machine
P0 → P(addr) → P(addr+name)

## Transition under test
address-first partial chain

## Preconditions
- EShop at http://localhost:3000.
- Login test@eshop.com.
- GET P0.

## Test data
| (see steps) | |

## Test steps
1. PUT {"shipping_address":"77 Nguyen Hue, Q1"} only
2. PUT {"name":"Address First Name"} only
3. GET /api/users/me

## Expected result
If partial PUTs apply, GET shows Address First Name and 77 Nguyen Hue. phone may stay P0 or clear — not specified. email/role unchanged. Record partial-vs-replace semantics.

## States / transitions covered
P0→Pa→Pan

## Type
Legal / Unspecified

## Why the AI missed this
Prompt quality — ST-002 covered name→phone; ST-009 used name→phone→address order; address-only as the first partial transition was never a dedicated state path.

## Audit (human SUP)
- **Status:** VALID
- **Reasoning:** Address-first partial chain; partial semantics observe-only.

## Status / Related bugs
Not Run / None
