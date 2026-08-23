# TC-PROFILE-SEC-012: Mass assignment — login_attempts and locked_until in body

## Requirement ID
FR-04

## Module / Test type / Technique
profile / Security / SEC-mapped probe

## Security requirement(s)
SEC-06

## Threat / probe
Mass assignment login_attempts / locked_until

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.

## Test data
| (see steps) | |

## Test steps
1. PUT with "login_attempts":0,"locked_until":null plus valid fields.
2. GET /api/users/me.

## Expected result
Undocumented fields login_attempts/locked_until must not change role or email. Record whether they appear in GET /api/users/me. HTTP status and error body are not specified — record actual without inventing codes.

## SEC coverage
SEC-06

## Type
Security probe / mass assignment

## Audit
- **Status:** INCOMPLETE
- **Reasoning:** Undocumented fields are worth probing, but 'account-lockout bypass' is not a written SRS/SEC rule.

## Status / Related bugs
Not Run / None
