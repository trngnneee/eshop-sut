# TC-ADMINUSERS-ST-007: No token — U_EXISTS unchanged

## Requirement ID
FR-19 / SEC-02

## Module / Test type / Technique
admin-users / Functional / State Transition Testing

## State machine
U_EXISTS → (no auth DELETE) → U_EXISTS

## Transition under test
illegal unauthenticated

## Preconditions
- EShop at http://localhost:3000.
- Disposable D exists.

## Test data
| (see steps — multi-step sequence) | |

## Test steps
1. DELETE /api/admin/users/D without Authorization.
2. GET /api/admin/users as admin.

## Expected result
DELETE /api/admin/users/:id requires valid JWT and role=admin (API spec section 6; FR-12; SEC-02; SEC-03). Target user must still exist afterwards. HTTP status is not specified.

## States / transitions covered
U_EXISTS→U_EXISTS

## Type
Illegal

## Audit
- **Status:** VALID
- **Reasoning:** SEC-02: protected admin API requires JWT. Oracle checks no delete occurred.

## Status / Related bugs
Not Run / None
