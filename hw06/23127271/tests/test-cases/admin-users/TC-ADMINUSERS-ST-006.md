# TC-ADMINUSERS-ST-006: Non-admin token — U_EXISTS unchanged

## Requirement ID
FR-19 / SEC-03

## Module / Test type / Technique
admin-users / Functional / State Transition Testing

## State machine
U_EXISTS → (user DELETE) → U_EXISTS

## Transition under test
illegal role

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!
- Target disposable D exists.

## Test data
| (see steps — multi-step sequence) | |

## Test steps
1. DELETE /api/admin/users/D with user JWT.
2. GET /api/admin/users as admin.

## Expected result
DELETE /api/admin/users/:id requires valid JWT and role=admin (API spec section 6; FR-12; SEC-02; SEC-03). Target user must still exist afterwards. HTTP status is not specified.

## States / transitions covered
U_EXISTS→U_EXISTS

## Type
Illegal

## Audit
- **Status:** VALID
- **Reasoning:** FR-12 / SEC-03: non-admin must not use admin delete API. Oracle checks target still exists without inventing HTTP 403.

## Status / Related bugs
Not Run / None
