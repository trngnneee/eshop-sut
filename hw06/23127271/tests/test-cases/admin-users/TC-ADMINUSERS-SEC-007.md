# TC-ADMINUSERS-SEC-007: SEC-01 — error response on DELETE must not leak password

## Requirement ID
FR-19

## Module / Test type / Technique
admin-users / Security / SEC-mapped probe

## Security requirement(s)
SEC-01

## Threat / probe
Password in DELETE error response

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=admin@eshop.com password=Admin123!.

## Test data
| (see steps) | |

## Test steps
1. DELETE /api/admin/users/99999 (missing user).
2. Inspect response body for password/hash substrings.

## Expected result
SEC-01: password must not appear in response bodies (plaintext or hash). Inspect JSON and error text. HTTP status and error body are not specified — record actual without inventing codes.

## SEC coverage
SEC-01

## Type
Security probe

## Audit
- **Status:** VALID
- **Reasoning:** SEC-01 on DELETE error response for missing user. Missing-user behaviour is unspecified but password leak check is valid.

## Status / Related bugs
Not Run / None
