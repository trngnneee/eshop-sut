# TC-PROFILE-SEC-009: Auth bypass — PUT without Authorization header

## Requirement ID
FR-04

## Module / Test type / Technique
profile / Security / SEC-mapped probe

## Security requirement(s)
SEC-02

## Threat / probe
Auth bypass — no JWT

## Preconditions
- EShop at http://localhost:3000.
- Snapshot GET /api/users/me as test user.

## Test data
| (see steps) | |

## Test steps
1. PUT /api/users/me valid body with no Authorization header.
2. GET /api/users/me with valid token.

## Expected result
SEC-02: protected endpoint requires a valid JWT; attack must not apply the intended change. HTTP status and error body are not specified — record actual without inventing codes. GET /api/users/me with valid token shows snapshot profile unchanged.

## SEC coverage
SEC-02

## Type
Security probe

## Audit
- **Status:** VALID
- **Reasoning:** SEC-02: API spec section 2 requires JWT on PUT /api/users/me. Snapshot unchanged is the correct oracle.

## Status / Related bugs
Not Run / None
