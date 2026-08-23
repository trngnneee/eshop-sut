# TC-PROFILE-ST-SUP-001: Race — two PUTs with different names before any GET

## Requirement ID
FR-04

## Module / Test type / Technique
profile / Functional / State Transition Testing (human extension)

## State machine
P0 → PUT(A) ∥ PUT(B) → P?

## Transition under test
concurrent PUT race

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login test@eshop.com.
- Snapshot P0 via GET /api/users/me.

## Test data
| (see steps) | |

## Test steps
1. PUT name=Race Name A (other fields FR-04-valid)
2. PUT name=Race Name B (immediately, no GET between)
3. GET /api/users/me

## Expected result
Ordering of back-to-back PUTs is not specified. GET must show exactly one consistent profile: either Race Name A or Race Name B for name, not a mixed/corrupt row. email/role unchanged. Record which PUT wins. HTTP status is not specified — record actual without inventing codes.

## States / transitions covered
P0→P?(last-write-wins)

## Type
Unspecified (concurrency)

## Why the AI missed this
Prompt quality — Stage 1 ST generator used strictly sequential PUT→GET chains; checklist section 2 calls for concurrency/race edges but the prompt never asked for parallel transitions.

## Audit (human SUP)
- **Status:** VALID
- **Reasoning:** Concurrency race on PUT; oracle allows either winner without inventing order.

## Status / Related bugs
Not Run / None
