# TC-PROFILE-034: Reject or ignore role=user when sent by client

## Requirement ID
FR-04

## Module / Test type / Technique
profile / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- EShop backend is running at http://localhost:3000.
- Seed user test@eshop.com / Test1234! exists (role=user).
- Obtain a user JWT via POST /api/login with email=test@eshop.com password=Test1234!.
- Snapshot role from GET /api/users/me.

## Test data
| Field | Value |
|-------|-------|
| role | user |
| name | Nguyen Van A |
| phone | 0912345678 |
| shipping_address | 123 Le Loi, Q1, TP.HCM |

## Test steps
1. PUT /api/users/me including role=user.
2. GET /api/users/me.

## Expected result
GET /api/users/me still shows the same role as before. The API must not treat role as a client-writable field.

## Sub-domains covered
P-ROLE-03, P-AUTH-01

## Type
Invalid

## Audit
- **Status:** VALID
- **Reasoning:** Role is not a documented writable field (FR-04 / SEC-06), even when the value equals the current role.

## Status / Related bugs
Not Run / None
