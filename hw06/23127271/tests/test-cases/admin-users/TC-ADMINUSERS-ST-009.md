# TC-ADMINUSERS-ST-009: Delete user 3 — users 1 and 2 remain

## Requirement ID
FR-19

## Module / Test type / Technique
admin-users / Functional / State Transition Testing

## State machine
selective delete

## Transition under test
U3→DELETED, U1/U2→EXISTS

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=admin@eshop.com password=Admin123!
- Seed users id=1 admin, id=2 test exist.

## Test data
| (see steps — multi-step sequence) | |

## Test steps
1. Register disposable id=3 (or use existing id=3 if present).
2. DELETE /api/admin/users/3.
3. GET /api/admin/users.

## Expected result
id=1 and id=2 still listed; id=3 gone after DELETE.

## States / transitions covered
U3→DEAD; U1/U2 stable

## Type
Legal

## Audit
- **Status:** VALID
- **Reasoning:** Selective delete: other seed users remain while target id=3 is removed.

## Status / Related bugs
Not Run / None
