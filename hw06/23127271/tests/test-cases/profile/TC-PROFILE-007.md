# TC-PROFILE-007: HTML in shipping_address — no format rule specified

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
| shipping_address | 123 <script>alert(1)</script> |
| name | Nguyen Van A |
| phone | 0912345678 |

## Test steps
1. PUT /api/users/me with HTML address.
2. GET /api/users/me.

## Expected result
Address charset/HTML handling is not specified. Do not expect accept or reject. email and role must not change if any update occurs.

## Sub-domains covered
P-ADDR-07, P-NAME-01, P-PHONE-01

## Type
Unspecified

## Audit
- **Status:** INCOMPLETE
- **Reasoning:** No shipping_address format/HTML rule is stated. Generated oracle assumed accept-and-persist.

## Status / Related bugs
Not Run / None
