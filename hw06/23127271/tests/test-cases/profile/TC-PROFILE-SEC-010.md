# TC-PROFILE-SEC-010: JWT tampering — invalid signature on PUT

## Requirement ID
FR-04

## Module / Test type / Technique
profile / Security / SEC-mapped probe

## Security requirement(s)
SEC-02

## Threat / probe
Auth bypass — invalid signature JWT

## Preconditions
- EShop at http://localhost:3000.
- Valid user token available.

## Test data
| (see steps) | |

## Test steps
1. PUT /api/users/me with Authorization Bearer <token_with_bad_signature>.
2. GET with valid token.

## Expected result
SEC-02: protected endpoint requires a valid JWT; attack must not apply the intended change. HTTP status and error body are not specified — record actual without inventing codes.

## SEC coverage
SEC-02

## Type
Security probe

## Audit
- **Status:** VALID
- **Reasoning:** SEC-02 tampered JWT probe. Oracle requires no profile change without inventing status codes.

## Status / Related bugs
Not Run / None
