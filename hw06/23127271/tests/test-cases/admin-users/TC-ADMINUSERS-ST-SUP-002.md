# TC-ADMINUSERS-ST-SUP-002: Race — two concurrent DELETE on same disposable user id

## Requirement ID
FR-19

## Module / Test type / Technique
admin-users / Functional / State Transition Testing (human extension)

## State machine
U_EXISTS → DELETE ∥ DELETE → U_DELETED

## Transition under test
concurrent delete race

## Preconditions
- EShop at http://localhost:3000.
- Admin JWT.
- Disposable user D registered.

## Test data
| (see steps) | |

## Test steps
1. DELETE /api/admin/users/D twice in parallel
2. GET /api/admin/users

## Expected result
D must end absent from list (U_DELETED). No other user deleted. Second parallel DELETE may return error or success — not specified. List count must reflect exactly one removal of D.

## States / transitions covered
U_EXISTS→U_DELETED

## Type
Unspecified (concurrency)

## Why the AI missed this
Model limitation — checklist section 2 lists concurrency; AI ST output was strictly sequential (ST-005 chain). Parallel DELETE idempotency vs double-error is untested without human case.

## Audit (human SUP)
- **Status:** VALID
- **Reasoning:** Parallel DELETE race; final state U_DELETED without inventing second response.

## Status / Related bugs
Not Run / None
