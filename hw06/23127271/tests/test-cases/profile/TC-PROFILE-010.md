# TC-PROFILE-010: Omit name — not specified as required

## Requirement ID
FR-04

## Module / Test type / Technique
profile / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- EShop backend is running at http://localhost:3000.
- Seed user test@eshop.com / Test1234! exists (role=user).
- Obtain a user JWT via POST /api/login with email=test@eshop.com password=Test1234!.
- Snapshot GET /api/users/me.

## Test data
| Field | Value |
|-------|-------|
| name | (omitted) |
| phone | 0912345678 |
| shipping_address | 123 Le Loi, Q1, TP.HCM |

## Test steps
1. PUT /api/users/me with body containing only phone and shipping_address.
2. GET /api/users/me.

## Expected result
name is not specified as required on PUT /api/users/me. Do not expect rejection. Observe whether the stored name is unchanged, cleared, or otherwise updated. email and role must not change.

## Sub-domains covered
P-NAME-05, P-PHONE-01, P-ADDR-01

## Type
Unspecified

## Audit
- **Status:** INVALID
- **Reasoning:** P-NAME-05: FR-04 lists Họ Tên as updatable and the API example includes name. Neither document says name is mandatory on every PUT. Omitting it is not a specified invalid class.

## Status / Related bugs
Not Run / None
