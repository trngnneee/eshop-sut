# TC-ADMINUSERS-SEC-001: DELETE without Authorization

## Requirement ID
FR-19

## Module / Test type / Technique
admin-users / Security / SEC-mapped probe

## Security requirement(s)
SEC-02

## Threat / probe
Auth bypass — no JWT

## Preconditions
- EShop at http://localhost:3000.
- Disposable user D registered.

## Test data
| (see steps) | |

## Test steps
1. DELETE /api/admin/users/D without Authorization.
2. GET /api/admin/users as admin.

## Expected result
SEC-02: protected endpoint requires a valid JWT; attack must not apply the intended change. HTTP status and error body are not specified — record actual without inventing codes. D still present in GET /api/admin/users as admin.

## SEC coverage
SEC-02

## Type
Security probe

## Audit
- **Status:** VALID
- **Reasoning:** SEC-02 unauthenticated DELETE. Target user must remain (D still in list).

## Status / Related bugs
Not Run / None
