# TC-ADMINUSERS-001: Admin deletes another existing user (on-point)

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

## Test data
| Field | Value |
|-------|-------|
| id | <disposable_user_id> |
| Authorization | Bearer <admin_token> |

## Test steps
1. DELETE /api/admin/users/{disposable_user_id} with admin JWT.
2. GET /api/admin/users and confirm the id is absent.
3. Confirm response JSON does not include a password field.

## Expected result
The disposable user is absent from a subsequent GET /api/admin/users. The caller's own account still exists. GET /api/admin/users must not include passwords (FR-19). Success HTTP status/body are not specified.

## Sub-domains covered
A-ID-01, A-AUTH-01, A-ROLE-01, A-REL-01

## Type
Valid

## Audit
- **Status:** VALID
- **Reasoning:** FR-19: admin may delete users other than the currently logged-in account. FR-12: caller is admin with JWT.

## Status / Related bugs
Not Run / None
