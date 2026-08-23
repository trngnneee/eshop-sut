# TC-ADMINUSERS-ST-011: Deleted user cannot login (account terminal)

## Requirement ID
FR-19

## Module / Test type / Technique
admin-users / Functional / State Transition Testing

## State machine
U_DELETED → login fails

## Transition under test
cross-endpoint auth state

## Preconditions
- EShop at http://localhost:3000.
- User D deleted by admin.

## Test data
| (see steps — multi-step sequence) | |

## Test steps
1. POST /api/login with D credentials.

## Expected result
POST /api/login with deleted user credentials must not yield a usable session for that account. HTTP status/body not specified — record actual.

## States / transitions covered
U_DELETED→auth blocked

## Type
Legal consequence / Unspecified

## Audit
- **Status:** INCOMPLETE
- **Reasoning:** Deleted account should not authenticate — reasonable consequence but FR-19 does not state login behaviour; HTTP 401/403 not specified.

## Status / Related bugs
Not Run / None
