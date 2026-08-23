# TC-PROFILE-027: shipping_address=null — not specified as invalid

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
| shipping_address | null |
| name | Nguyen Van A |
| phone | 0912345678 |

## Test steps
1. PUT /api/users/me with shipping_address JSON null.
2. GET /api/users/me.

## Expected result
The SRS and api_specification.md do not state this input is invalid or required. Do not expect rejection. Record what the SUT does; do not fail it against an invented rule.

## Sub-domains covered
P-ADDR-05, P-NAME-01, P-PHONE-01

## Type
Unspecified

## Audit
- **Status:** INVALID
- **Reasoning:** Null handling for shipping_address is not specified.

## Status / Related bugs
Not Run / None
