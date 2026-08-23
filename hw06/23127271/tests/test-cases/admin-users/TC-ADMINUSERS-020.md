# TC-ADMINUSERS-020: Path id 0001 — encoding not specified (FR-19 only if resolved as self)

## Requirement ID
FR-19

## Module / Test type / Technique
admin-users / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- EShop backend is running at http://localhost:3000.
- Seed admin admin@eshop.com / Admin123! exists (role=admin).
- Obtain an admin JWT via POST /api/login with email=admin@eshop.com password=Admin123!.
- Seed admin is id=1 on a fresh DB. Do not delete id=1.

## Test data
| Field | Value |
|-------|-------|
| id | 0001 |

## Test steps
1. DELETE /api/admin/users/0001 with admin JWT.
2. GET /api/users/me as admin still works; GET /api/admin/users still lists id=1.

## Expected result
No path-encoding rule is stated. Do not expect 400/404. If 0001 is treated as the caller's id, FR-19: that account must not be deleted.

## Sub-domains covered
A-ID-06, A-ID-07, A-AUTH-01

## Type
Unspecified

## Audit
- **Status:** INCOMPLETE
- **Reasoning:** Leading-zero encoding is not specified. Generated 400/404 was invented. FR-19 applies only if the path is resolved as the caller.

## Status / Related bugs
Not Run / None
