# TC-ADMINUSERS-SEC-010: DELETE with empty Bearer token

## Requirement ID
FR-19

## Module / Test type / Technique
admin-users / Security / SEC-mapped probe

## Security requirement(s)
SEC-02

## Threat / probe
Empty Bearer token

## Preconditions
- EShop at http://localhost:3000.
- Disposable D.

## Test data
| (see steps) | |

## Test steps
1. DELETE with Authorization: Bearer (empty).
2. GET /api/admin/users as admin.

## Expected result
SEC-02: protected endpoint requires a valid JWT; attack must not apply the intended change. HTTP status and error body are not specified — record actual without inventing codes.

## SEC coverage
SEC-02

## Type
Security probe

## Audit
- **Status:** VALID
- **Reasoning:** SEC-02 empty Bearer token on DELETE.

## Status / Related bugs
Not Run / None
