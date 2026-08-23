# TC-PROFILE-035: Reject email change via PUT /api/users/me

## Requirement ID
FR-04

## Module / Test type / Technique
profile / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- EShop backend is running at http://localhost:3000.
- Seed user test@eshop.com / Test1234! exists (role=user).
- Obtain a user JWT via POST /api/login with email=test@eshop.com password=Test1234!.
- Snapshot email from GET /api/users/me (test@eshop.com).

## Test data
| Field | Value |
|-------|-------|
| email | hijack@example.com |
| name | Nguyen Van A |
| phone | 0912345678 |
| shipping_address | 123 Le Loi, Q1, TP.HCM |

## Test steps
1. PUT /api/users/me with an extra email field.
2. GET /api/users/me.

## Expected result
GET /api/users/me still shows the original email (test@eshop.com). Whether the request is rejected or the extra field is ignored is not specified.

## Sub-domains covered
P-EMAIL-02, P-NAME-01, P-PHONE-01, P-ADDR-01

## Type
Invalid

## Audit
- **Status:** VALID
- **Reasoning:** FR-04: email must not be changed. Reject vs ignore is unspecified; unchanged email is specified.

## Status / Related bugs
Not Run / None
