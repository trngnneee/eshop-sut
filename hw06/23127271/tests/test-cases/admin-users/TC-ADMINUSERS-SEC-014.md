# TC-ADMINUSERS-SEC-014: SQLi Bearer token on admin DELETE

## Requirement ID
FR-19

## Module / Test type / Technique
admin-users / Security / SEC-mapped probe

## Security requirement(s)
SEC-05

## Threat / probe
SQLi in Authorization on DELETE

## Preconditions
- EShop at http://localhost:3000.
- Disposable D.

## Test data
| (see steps) | |

## Test steps
1. DELETE D with Authorization Bearer ' OR 1=1--.
2. GET list as admin.

## Expected result
SEC-05: request must not cause SQL syntax errors, 500 stack traces with query text, or unauthorized data change. Record status and GET/list side effects. SEC-02: protected endpoint requires a valid JWT; attack must not apply the intended change. HTTP status and error body are not specified — record actual without inventing codes.

## SEC coverage
SEC-05

## Type
Security probe

## Audit
- **Status:** VALID
- **Reasoning:** SEC-05 SQLi Bearer + SEC-02 on admin DELETE.

## Status / Related bugs
Not Run / None
