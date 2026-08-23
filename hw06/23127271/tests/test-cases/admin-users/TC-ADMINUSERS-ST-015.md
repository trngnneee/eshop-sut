# TC-ADMINUSERS-ST-015: Non-existent id — U_NONE stays none, list unchanged

## Requirement ID
FR-19

## Module / Test type / Technique
admin-users / Functional / State Transition Testing

## State machine
U_NONE → DELETE → U_NONE

## Transition under test
delete missing user

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=admin@eshop.com password=Admin123!
- Snapshot user list L0.

## Test data
| (see steps — multi-step sequence) | |

## Test steps
1. DELETE /api/admin/users/99999.
2. GET /api/admin/users → L1.

## Expected result
L1 equals L0 — no user removed. HTTP status for non-existent id is not specified — record actual.

## States / transitions covered
U_NONE→U_NONE

## Type
Unspecified

## Audit
- **Status:** INCOMPLETE
- **Reasoning:** Missing user id is not specified as invalid in FR-19. Expecting 404/4xx was invented (same as domain TC-ADMINUSERS-005 audit).

## Status / Related bugs
Not Run / None
