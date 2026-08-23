# TC-PROFILE-SEC-004: SQLi OR probe in phone field

## Requirement ID
FR-04

## Module / Test type / Technique
profile / Security / SEC-mapped probe

## Security requirement(s)
SEC-05

## Threat / probe
SQL injection in phone

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.

## Test data
| Field | Value |
|-------|-------|
| phone | 0912345678' OR '1'='1 |

## Test steps
1. PUT /api/users/me with SQLi phone (other fields FR-04-valid).
2. GET /api/users/me.

## Expected result
SEC-05: request must not cause SQL syntax errors, 500 stack traces with query text, or unauthorized data change. Record status and GET/list side effects. Record stored phone; injection string must not silently pass as a valid FR-04 phone.

## SEC coverage
SEC-05

## Type
Security probe

## Audit
- **Status:** VALID
- **Reasoning:** SEC-05 SQLi on phone field. Observing stored phone vs FR-04 format is a reasonable side-effect check.

## Status / Related bugs
Not Run / None
