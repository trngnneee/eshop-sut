# TC-PROFILE-018: Omit phone — not specified as required

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
| phone | (omitted) |
| name | Nguyen Van A |
| shipping_address | 123 Le Loi, Q1, TP.HCM |

## Test steps
1. PUT /api/users/me omitting phone.
2. GET /api/users/me.

## Expected result
phone is not specified as required on every PUT. Do not expect rejection. If a phone is stored afterwards, it must still be a FR-04-valid phone when one is present.

## Sub-domains covered
P-PHONE-07, P-NAME-01, P-ADDR-01

## Type
Unspecified

## Audit
- **Status:** INVALID
- **Reasoning:** Omitting phone is not the same as submitting an invalid phone. Partial update is not forbidden. Required-on-PUT was assumed.

## Status / Related bugs
Not Run / None
