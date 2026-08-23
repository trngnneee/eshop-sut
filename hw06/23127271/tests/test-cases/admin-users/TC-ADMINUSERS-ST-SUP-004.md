# TC-ADMINUSERS-ST-SUP-004: Illegal — delete active session user D while D holds valid JWT

## Requirement ID
FR-19

## Module / Test type / Technique
admin-users / Functional / State Transition Testing (human extension)

## State machine
U_EXISTS(session) → DELETE → U_DELETED; D token probe

## Transition under test
delete user with live session

## Preconditions
- EShop at http://localhost:3000.
- Register D.
- D logged in (token T).
- Admin JWT.
- D visible in GET /api/admin/users.

## Test data
| (see steps) | |

## Test steps
1. Admin DELETE /api/admin/users/D while D session conceptually active
2. GET /api/users/me with D token T
3. GET /api/admin/users as admin

## Expected result
D absent from admin list after DELETE (FR-19). GET /api/users/me with victim token T — record status/body; live profile for deleted user must not persist. Admin unchanged. Cascade/session rules not specified.

## States / transitions covered
EXISTS→DELETED

## Type
Legal delete / Unspecified session

## Why the AI missed this
Prompt quality — ST-008 lifecycle is register→list→delete; no case combined active JWT held by victim during admin DELETE (cross-endpoint session state).

## Audit (human SUP)
- **Status:** INCOMPLETE
- **Reasoning:** Removed 'must not succeed' as mandatory status; session invalidation unspecified.

## Status / Related bugs
Not Run / None
