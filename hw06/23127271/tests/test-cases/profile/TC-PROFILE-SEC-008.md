# TC-PROFILE-SEC-008: Mass assignment — password in profile PUT body

## Requirement ID
FR-04

## Module / Test type / Technique
profile / Security / SEC-mapped probe

## Security requirement(s)
SEC-06

## Threat / probe
Mass assignment password field

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.

## Test data
| (see steps) | |

## Test steps
1. PUT body includes "password":"Hacked123!" with valid profile fields.
2. POST /api/login with original password Test1234!.

## Expected result
SEC-01 / FR-04: PUT documents only name, phone, shipping_address. Password must not be overwritten (observe via POST /api/login with original password; GET /api/users/me must not expose password). HTTP status and error body are not specified — record actual without inventing codes.

## SEC coverage
SEC-06

## Type
Security probe / mass assignment

## Audit
- **Status:** INCOMPLETE
- **Reasoning:** Probe is valid mass-assignment, but tagged SEC-06 (role-only per README). Password rule comes from FR-04 field list + SEC-01, not SEC-06.

## Status / Related bugs
Not Run / None
