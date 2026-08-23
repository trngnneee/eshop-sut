# TC-ADMINUSERS-ST-SUP-005: Race — DELETE user D concurrent with GET /api/admin/users

## Requirement ID
FR-19

## Module / Test type / Technique
admin-users / Functional / State Transition Testing (human extension)

## State machine
U_EXISTS → DELETE ∥ GET list

## Transition under test
concurrent delete vs list read

## Preconditions
- EShop at http://localhost:3000.
- Admin JWT.
- Disposable D registered and in list.

## Test data
| (see steps) | |

## Test steps
1. Fire DELETE /api/admin/users/D and GET /api/admin/users in parallel
2. GET /api/admin/users after both complete

## Expected result
Final GET must show D absent (U_DELETED). Concurrent GET may or may not include D — not specified. No duplicate or partial delete of other users. Record intermediate vs final list.

## States / transitions covered
LIST(N)→LIST(N-1)?

## Type
Unspecified (concurrency)

## Why the AI missed this
Model limitation — ST-004 tests sequential GET→DELETE→GET; parallel list read during delete may show D present or absent depending on timing — checklist concurrency gap.

## Audit (human SUP)
- **Status:** VALID
- **Reasoning:** DELETE∥GET list race; intermediate state observe-only.

## Status / Related bugs
Not Run / None
