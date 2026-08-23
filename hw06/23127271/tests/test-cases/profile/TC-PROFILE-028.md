# TC-PROFILE-028: Address length 500 — no max specified

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
| shipping_address | x × 500 |
| name | Nguyen Van A |
| phone | 0912345678 |

## Test steps
1. PUT /api/users/me with 500-character address.
2. GET /api/users/me.

## Expected result
No maximum length/quantity is specified. Do not expect accept or reject. Record actual behaviour.

## Sub-domains covered
P-ADDR-06, P-NAME-01, P-PHONE-01

## Type
Unspecified

## Audit
- **Status:** INCOMPLETE
- **Reasoning:** No max address length is specified. Generated case expected accept.

## Status / Related bugs
Not Run / None
