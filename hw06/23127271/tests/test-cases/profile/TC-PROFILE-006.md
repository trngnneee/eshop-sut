# TC-PROFILE-006: HTML in name — no format rule specified

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
| name | Nguyen <b>A</b> |
| phone | 0912345678 |
| shipping_address | 123 Le Loi, Q1, TP.HCM |

## Test steps
1. PUT /api/users/me with HTML in name.
2. GET /api/users/me and assert name stored as the submitted string.

## Expected result
Name charset/HTML handling is not specified. Do not expect accept or reject. If a name is stored, email and role still must not change (FR-04 / SEC-06).

## Sub-domains covered
P-NAME-08, P-PHONE-01, P-ADDR-01

## Type
Unspecified

## Audit
- **Status:** INCOMPLETE
- **Reasoning:** No name-format or HTML rule is stated. The generated case asserted HTTP 200 and literal persistence, which is not in the spec.

## Status / Related bugs
Not Run / None
