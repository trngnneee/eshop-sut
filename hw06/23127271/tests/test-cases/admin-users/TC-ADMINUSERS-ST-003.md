# TC-ADMINUSERS-ST-003: U_DELETED → repeat DELETE — terminal state

## Requirement ID
FR-19

## Module / Test type / Technique
admin-users / Functional / State Transition Testing

## State machine
U_DELETED → DELETE → U_DELETED

## Transition under test
terminal / idempotency

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=admin@eshop.com password=Admin123!
- User D already deleted.

## Test data
| (see steps — multi-step sequence) | |

## Test steps
1. DELETE /api/admin/users/D again.
2. GET /api/admin/users.

## Expected result
D remains absent. Second DELETE must not delete a different user or restore D. HTTP status for repeat delete is not specified — record actual.

## States / transitions covered
U_DELETED→U_DELETED

## Type
Illegal repeat / Unspecified

## Audit
- **Status:** INCOMPLETE
- **Reasoning:** Repeat DELETE on a gone user is a valid terminal-state probe. Preferring 404/4xx over silent 200 is not in the spec.

## Status / Related bugs
Not Run / None
