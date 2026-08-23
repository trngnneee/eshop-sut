# TC-PROFILE-026: Omit shipping_address — not specified as required

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
| shipping_address | (omitted) |
| name | Nguyen Van A |
| phone | 0912345678 |

## Test steps
1. PUT /api/users/me omitting shipping_address.
2. GET /api/users/me.

## Expected result
shipping_address is not specified as required. Do not expect rejection. Record what happens to the stored address.

## Sub-domains covered
P-ADDR-04, P-NAME-01, P-PHONE-01

## Type
Unspecified

## Audit
- **Status:** INVALID
- **Reasoning:** shipping_address is listed as updatable, not as mandatory on every PUT.

## Status / Related bugs
Not Run / None
