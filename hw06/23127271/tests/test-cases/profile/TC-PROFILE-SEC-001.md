# TC-PROFILE-SEC-001: SQLi classic OR tautology in name field

## Requirement ID
FR-04

## Module / Test type / Technique
profile / Security / SEC-mapped probe

## Security requirement(s)
SEC-05

## Threat / probe
SQL injection in name

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.
- Snapshot GET /api/users/me.

## Test data
| Field | Value |
|-------|-------|
| name | Nguyen' OR '1'='1 |
| phone | 0912345678 |
| shipping_address | 123 Le Loi, Q1 |

## Test steps
1. PUT /api/users/me with SQLi name payload.
2. GET /api/users/me — email/role unchanged; no SQL error leak.

## Expected result
SEC-05: request must not cause SQL syntax errors, 500 stack traces with query text, or unauthorized data change. Record status and GET/list side effects. email and role unchanged on GET /api/users/me.

## SEC coverage
SEC-05

## Type
Security probe

## Audit
- **Status:** VALID
- **Reasoning:** SEC-05 SQLi in documented name field. Oracle observes injection side effects without inventing HTTP codes.

## Status / Related bugs
Not Run / None
