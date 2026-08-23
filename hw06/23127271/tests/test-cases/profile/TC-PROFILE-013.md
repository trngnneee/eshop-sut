# TC-PROFILE-013: Name length 500 — no max specified

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
| name | A × 500 |
| phone | 0912345678 |
| shipping_address | 123 Le Loi, Q1, TP.HCM |

## Test steps
1. PUT /api/users/me with name of 500 'A' characters.
2. GET /api/users/me.

## Expected result
No maximum length/quantity is specified. Do not expect accept or reject. Record actual behaviour.

## Sub-domains covered
P-NAME-09, P-PHONE-01, P-ADDR-01

## Type
Unspecified

## Audit
- **Status:** INCOMPLETE
- **Reasoning:** FR-04 does not define a max name length. The generated case still told the tester to expect accept (200).

## Status / Related bugs
Not Run / None
