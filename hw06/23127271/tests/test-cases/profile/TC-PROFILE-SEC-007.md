# TC-PROFILE-SEC-007: Mass assignment — role=admin in profile body

## Requirement ID
FR-04

## Module / Test type / Technique
profile / Security / SEC-mapped probe

## Security requirement(s)
SEC-06

## Threat / probe
Role escalation role=admin

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.
- GET role=user.

## Test data
| (see steps) | |

## Test steps
1. PUT /api/users/me with "role":"admin" plus valid profile fields.
2. GET /api/users/me.

## Expected result
SEC-06 / FR-04: role must remain user on GET /api/users/me. Documented fields may update. HTTP status and error body are not specified — record actual without inventing codes.

## SEC coverage
SEC-06

## Type
Security probe

## Audit
- **Status:** VALID
- **Reasoning:** SEC-06 explicitly forbids client role change; FR-04 repeats the same rule.

## Status / Related bugs
Not Run / None
