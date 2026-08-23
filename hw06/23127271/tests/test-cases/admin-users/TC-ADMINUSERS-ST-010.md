# TC-ADMINUSERS-ST-010: Self-delete attempt leaves other users untouched

## Requirement ID
FR-19

## Module / Test type / Technique
admin-users / Functional / State Transition Testing

## State machine
U_SELF block; others EXISTS

## Transition under test
illegal self + list stability

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=admin@eshop.com password=Admin123!
- List includes admin + test@eshop.com.

## Test data
| (see steps — multi-step sequence) | |

## Test steps
1. DELETE /api/admin/users/{admin_self_id}.
2. GET /api/admin/users.

## Expected result
User list count and ids unchanged after self-delete attempt. Admin account remains.

## States / transitions covered
U_SELF→U_SELF; others unchanged

## Type
Illegal

## Audit
- **Status:** VALID
- **Reasoning:** Self-delete blocked (FR-19) with list stability — no collateral deletes.

## Status / Related bugs
Not Run / None
