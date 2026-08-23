# TC-PROFILE-012: Numeric name — type not specified

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
| name | 12345 |
| phone | 0912345678 |
| shipping_address | 123 Le Loi, Q1, TP.HCM |

## Test steps
1. PUT /api/users/me with invalid name and other fields valid.
2. GET /api/users/me and confirm no change.

## Expected result
The SRS and api_specification.md do not state this input is invalid or required. Do not expect rejection. Record what the SUT does; do not fail it against an invented rule.

## Sub-domains covered
P-NAME-07, P-PHONE-01, P-ADDR-01, P-AUTH-01

## Type
Unspecified

## Audit
- **Status:** INVALID
- **Reasoning:** JSON type for name is not specified (example is a string, not a type constraint).

## Status / Related bugs
Not Run / None
