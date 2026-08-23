# TC-ADMINUSERS-ST-SUP-001: Delete another admin account (not self) — A-ID-10 state transition

## Requirement ID
FR-19

## Module / Test type / Technique
admin-users / Functional / State Transition Testing (human extension)

## State machine
U_ADMIN_OTHER → U_DELETED

## Transition under test
delete other admin

## Preconditions
- EShop at http://localhost:3000.
- Admin JWT.
- Second admin account exists (register+promote or seed) with id=A, caller id=1, A!=1.

## Test data
| (see steps) | |

## Test steps
1. DELETE /api/admin/users/{other_admin_id} with admin JWT (not self).
2. GET /api/admin/users.
3. Confirm caller admin still exists.

## Expected result
FR-19 allows deleting users other than self; whether another admin may be deleted is not specified. Record outcome. Do not invent mandatory 403/200. Password never in list responses.

## States / transitions covered
U_ADMIN→DELETED

## Type
Unspecified

## Why the AI missed this
API characteristic — FR-19 forbids only self-delete; deleting another admin is unspecified. Domain TC-ADMINUSERS-010 exists but no state-transition lifecycle case; ST suite stopped at disposable users.

## Audit (human SUP)
- **Status:** VALID
- **Reasoning:** Delete-other-admin unspecified in FR-19; observe-only oracle.

## Status / Related bugs
Not Run / None
