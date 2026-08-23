# TC-ADMINUSERS-005: Non-existent user id — not specified as invalid

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
| id | 99999 |

## Test steps
1. DELETE /api/admin/users/99999 with admin JWT.
2. GET /api/admin/users: count unchanged.

## Expected result
The SRS and api_specification.md do not state this input is invalid or required. Do not expect rejection. Record what the SUT does; do not fail it against an invented rule.

## Sub-domains covered
A-ID-05, A-AUTH-01

## Type
Unspecified

## Audit
- **Status:** INVALID
- **Reasoning:** Missing-user / HTTP 404 is not specified.

## Status / Related bugs
Not Run / None
