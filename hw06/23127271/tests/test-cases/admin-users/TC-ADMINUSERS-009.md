# TC-ADMINUSERS-009: Repeat DELETE of a missing id — not specified

## Requirement ID
FR-19

## Module / Test type / Technique
admin-users / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- EShop backend is running at http://localhost:3000.
- Seed admin admin@eshop.com / Admin123! exists (role=admin).
- Obtain an admin JWT via POST /api/login with email=admin@eshop.com password=Admin123!.
- Create a disposable user to delete: POST /api/register with a unique email (e.g. del.<timestamp>@example.com), password Password123!, name Disposable User.
- Note disposable_user_id from the register response (or GET /api/admin/users).
- Do not use seed test@eshop.com as the success-path victim if later tests still need that account.
- DELETE /api/admin/users/{disposable_user_id} once (must succeed).
- GET /api/admin/users confirms the user is gone.

## Test data
| Field | Value |
|-------|-------|
| id | <deleted_id> |

## Test steps
1. DELETE /api/admin/users/{deleted_id} a second time with admin JWT.

## Expected result
The SRS and api_specification.md do not state this input is invalid or required. Do not expect rejection. Record what the SUT does; do not fail it against an invented rule.

## Sub-domains covered
A-ID-09, A-AUTH-01

## Type
Unspecified

## Audit
- **Status:** INVALID
- **Reasoning:** Repeat delete / 404 is not specified.

## Status / Related bugs
Not Run / None
