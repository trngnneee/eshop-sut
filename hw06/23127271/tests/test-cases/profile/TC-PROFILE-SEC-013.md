# TC-PROFILE-SEC-013: SQLi probe via Authorization Bearer value

## Requirement ID
FR-04

## Module / Test type / Technique
profile / Security / SEC-mapped probe

## Security requirement(s)
SEC-05

## Threat / probe
SQLi in Authorization header

## Preconditions
- EShop at http://localhost:3000.

## Test data
| (see steps) | |

## Test steps
1. PUT /api/users/me with Authorization: Bearer ' OR 1=1-- and valid body.
2. GET /api/users/me with valid token.

## Expected result
SEC-05: request must not cause SQL syntax errors, 500 stack traces with query text, or unauthorized data change. Record status and GET/list side effects. SEC-02: protected endpoint requires a valid JWT; attack must not apply the intended change. HTTP status and error body are not specified — record actual without inventing codes.

## SEC coverage
SEC-05

## Type
Security probe

## Audit
- **Status:** VALID
- **Reasoning:** Combined SEC-05 (Auth header SQLi) and SEC-02 (invalid token) probe. Both requirements are written.

## Status / Related bugs
Not Run / None
