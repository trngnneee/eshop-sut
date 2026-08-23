# TC-ADMINUSERS-SEC-013: DELETE success body must not echo password

## Requirement ID
FR-19

## Module / Test type / Technique
admin-users / Security / SEC-mapped probe

## Security requirement(s)
SEC-01

## Threat / probe
Data exposure after successful delete

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=admin@eshop.com password=Admin123!.
- Register D.

## Test data
| (see steps) | |

## Test steps
1. DELETE D.
2. Inspect 200/success JSON for password fields.

## Expected result
SEC-01: password must not appear in response bodies (plaintext or hash). Inspect JSON and error text.

## SEC coverage
SEC-01

## Type
Security probe

## Audit
- **Status:** VALID
- **Reasoning:** SEC-01 on successful DELETE response body.

## Status / Related bugs
Not Run / None
