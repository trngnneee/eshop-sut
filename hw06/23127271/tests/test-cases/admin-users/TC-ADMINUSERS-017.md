# TC-ADMINUSERS-017: Query string does not change which user is deleted

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
- Know a second existing user id that must survive (e.g. seed test user).

## Test data
| Field | Value |
|-------|-------|
| id | <disposable_user_id> |
| query | id=<other_existing_id> |

## Test steps
1. DELETE /api/admin/users/{disposable_user_id}?id={other_existing_id} with admin JWT.
2. GET /api/admin/users: disposable gone; other_existing_id still present.

## Expected result
Only the path id is the documented user identifier. A query parameter named id is not specified and must not be treated as the resource id. If a delete occurs, it is the path-id user (and not self — FR-19).

## Sub-domains covered
A-ID-01, A-AUTH-01

## Type
Valid

## Audit
- **Status:** VALID
- **Reasoning:** The specified identifier is the path parameter :id. A query string is not a documented id.

## Status / Related bugs
Not Run / None
