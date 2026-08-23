# TC-ADMINUSERS-ST-014: Delete seed user id=2 — admin id=1 survives

## Requirement ID
FR-19

## Module / Test type / Technique
admin-users / Functional / State Transition Testing

## State machine
U2→DELETED; U1(admin)→EXISTS

## Transition under test
seed user delete

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=admin@eshop.com password=Admin123!
- Fresh seed DB.

## Test data
| (see steps — multi-step sequence) | |

## Test steps
1. DELETE /api/admin/users/2 (test@eshop.com).
2. GET /api/admin/users.
3. GET /api/users/me as admin.

## Expected result
id=2 absent from list; admin id=1 still exists and can GET /api/users/me.

## States / transitions covered
U2→DEAD; U1→EXISTS

## Type
Legal

## Audit
- **Status:** VALID
- **Reasoning:** FR-19: delete user id=2 (not self). Admin id=1 must remain.

## Status / Related bugs
Not Run / None
