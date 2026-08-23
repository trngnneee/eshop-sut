# TC-PROFILE-SEC-003: SQLi stacked DROP probe in shipping_address

## Requirement ID
FR-04

## Module / Test type / Technique
profile / Security / SEC-mapped probe

## Security requirement(s)
SEC-05

## Threat / probe
SQL injection in shipping_address

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.

## Test data
| Field | Value |
|-------|-------|
| name | Nguyen Van A |
| phone | 0912345678 |
| shipping_address | 123 Le Loi'; DROP TABLE users;-- |

## Test steps
1. PUT /api/users/me with SQLi address.
2. GET /api/users/me — profile intact; no SQL error leak.

## Expected result
SEC-05: request must not cause SQL syntax errors, 500 stack traces with query text, or unauthorized data change. Record status and GET/list side effects. User profile must remain intact on GET /api/users/me.

## SEC coverage
SEC-05

## Type
Security probe

## Audit
- **Status:** VALID
- **Reasoning:** SEC-05 stacked DROP probe on shipping_address. Oracle correctly scoped to profile integrity.

## Status / Related bugs
Not Run / None
