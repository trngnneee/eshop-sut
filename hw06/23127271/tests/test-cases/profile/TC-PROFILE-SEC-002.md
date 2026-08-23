# TC-PROFILE-SEC-002: SQLi UNION SELECT probe in name

## Requirement ID
FR-04

## Module / Test type / Technique
profile / Security / SEC-mapped probe

## Security requirement(s)
SEC-05

## Threat / probe
SQL injection UNION in name

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.

## Test data
| Field | Value |
|-------|-------|
| name | x' UNION SELECT null,null,null-- |
| phone | 0912345678 |
| shipping_address | Addr |

## Test steps
1. PUT /api/users/me with UNION payload in name.
2. GET /api/users/me.

## Expected result
SEC-05: request must not cause SQL syntax errors, 500 stack traces with query text, or unauthorized data change. Record status and GET/list side effects.

## SEC coverage
SEC-05

## Type
Security probe

## Audit
- **Status:** VALID
- **Reasoning:** SEC-05 UNION probe on name. Oracle is observe-only for SQL leaks.

## Status / Related bugs
Not Run / None
