# TC-PROFILE-038: Extra field nickname — handling not specified

## Requirement ID
FR-04

## Module / Test type / Technique
profile / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- EShop backend is running at http://localhost:3000.
- Seed user test@eshop.com / Test1234! exists (role=user).
- Obtain a user JWT via POST /api/login with email=test@eshop.com password=Test1234!.

## Test data
| Field | Value |
|-------|-------|
| nickname | A |
| name | Nguyen Van A |
| phone | 0912345678 |
| shipping_address | 123 Le Loi, Q1, TP.HCM |

## Test steps
1. PUT /api/users/me with documented fields plus nickname=A.
2. GET /api/users/me.

## Expected result
Extra-field handling is not specified. Documented fields may still update. Do not assert how the extra field is stored or rejected. email and role still must not change.

## Sub-domains covered
P-BODY-04, P-NAME-01, P-PHONE-01, P-ADDR-01

## Type
Unspecified

## Audit
- **Status:** INCOMPLETE
- **Reasoning:** Extra-field policy is not specified. The generated case asserted nickname must not persist, which is not written.

## Status / Related bugs
Not Run / None
