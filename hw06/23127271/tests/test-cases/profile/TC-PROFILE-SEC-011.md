# TC-PROFILE-SEC-011: Immutable email — client attempts email change

## Requirement ID
FR-04

## Module / Test type / Technique
profile / Security / SEC-mapped probe

## Security requirement(s)
SEC-06

## Threat / probe
Privilege — email change

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.
- email=test@eshop.com.

## Test data
| (see steps) | |

## Test steps
1. PUT with "email":"attacker@evil.com".
2. GET /api/users/me.

## Expected result
email remains test@eshop.com. Other fields may update. Request rejected or email ignored. HTTP status and error body are not specified — record actual without inventing codes.

## SEC coverage
SEC-06

## Type
Security probe

## Audit
- **Status:** VALID
- **Reasoning:** FR-04: email must not change. Oracle allows reject-or-ignore and requires email unchanged.

## Status / Related bugs
Not Run / None
