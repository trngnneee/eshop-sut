# TC-ADMINUSERS-ST-002: U_SELF — admin cannot delete own account

## Requirement ID
FR-19

## Module / Test type / Technique
admin-users / Functional / State Transition Testing

## State machine
U_SELF → U_SELF (blocked)

## Transition under test
illegal self-delete

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=admin@eshop.com password=Admin123!
- Note admin_self_id from token/GET.

## Test data
| (see steps — multi-step sequence) | |

## Test steps
1. DELETE /api/admin/users/{admin_self_id}.
2. GET /api/admin/users.
3. GET /api/users/me as admin.

## Expected result
FR-19: admin must not delete the currently logged-in account. HTTP status is not specified; record whether the admin account remains in GET /api/admin/users.

## States / transitions covered
U_SELF→U_SELF

## Type
Illegal

## Audit
- **Status:** INCOMPLETE
- **Reasoning:** FR-19 self-delete prohibition is real. Generated title/oracle already avoids mandating HTTP 403 — audit confirms INCOMPLETE only because status is unspecified.

## Status / Related bugs
Not Run / None
