# TC-PROFILE-005: Phone 0000000000 is format-valid per FR-04

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
| phone | 0000000000 |
| name | Nguyen Van A |
| shipping_address | 123 Le Loi, Q1, TP.HCM |

## Test steps
1. PUT /api/users/me with phone=0000000000.
2. GET /api/users/me.

## Expected result
GET /api/users/me shows phone=0000000000. Success status/body not specified.

## Sub-domains covered
P-PHONE-14, P-NAME-01, P-ADDR-01

## Type
Valid

## Audit
- **Status:** VALID
- **Reasoning:** 0000000000 starts with 0 and has 10 digits, which is the only phone rule FR-04 states. No numbering-plan rule exists.

## Status / Related bugs
Not Run / None
