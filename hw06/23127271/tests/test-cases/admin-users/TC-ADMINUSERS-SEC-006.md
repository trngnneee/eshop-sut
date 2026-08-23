# TC-ADMINUSERS-SEC-006: SEC-01 — GET /api/admin/users never exposes password

## Requirement ID
FR-19

## Module / Test type / Technique
admin-users / Security / SEC-mapped probe

## Security requirement(s)
SEC-01

## Threat / probe
Password exposure in list response

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=admin@eshop.com password=Admin123!.

## Test data
| (see steps) | |

## Test steps
1. GET /api/admin/users.
2. Inspect every object for password/password_hash fields.

## Expected result
SEC-01: password must not appear in response bodies (plaintext or hash). Inspect JSON and error text.

## SEC coverage
SEC-01

## Type
Security probe

## Audit
- **Status:** VALID
- **Reasoning:** SEC-01 / FR-19: admin list must not expose passwords. GET /api/admin/users is in FR-19 scope.

## Status / Related bugs
Not Run / None
