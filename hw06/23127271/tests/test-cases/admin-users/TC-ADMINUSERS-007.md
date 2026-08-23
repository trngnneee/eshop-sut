# TC-ADMINUSERS-007: id=1.5 — format not specified (FR-19 only if resolved as self)

## Requirement ID
FR-19

## Module / Test type / Technique
admin-users / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- EShop backend is running at http://localhost:3000.
- Seed admin admin@eshop.com / Admin123! exists (role=admin).
- Obtain an admin JWT via POST /api/login with email=admin@eshop.com password=Admin123!.

## Test data
| Field | Value |
|-------|-------|
| id | 1.5 |

## Test steps
1. DELETE /api/admin/users/1.5 with admin JWT.
2. Confirm seed user id=1 was not deleted (no truncation to 1).

## Expected result
No id-format rule is stated. Do not expect 400/404. If this path is treated as the caller's own id, FR-19: that account must not be deleted.

## Sub-domains covered
A-ID-07, A-AUTH-01

## Type
Unspecified

## Audit
- **Status:** INVALID
- **Reasoning:** Non-integer path id is not specified. 'Must not coerce to 1' was invented. If the SUT resolves this path to the caller's id, FR-19 then applies.

## Status / Related bugs
Not Run / None
