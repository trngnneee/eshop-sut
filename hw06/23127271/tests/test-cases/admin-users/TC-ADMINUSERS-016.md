# TC-ADMINUSERS-016: DELETE with unexpected JSON body — body not specified

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
| body | {"force":true} |

## Test steps
1. DELETE /api/admin/users/{disposable_user_id} with admin JWT and a JSON body {"force": true}.
2. GET /api/admin/users.

## Expected result
No request body is specified. The path id is the documented identifier. Do not expect the body to be required, forbidden, or honoured. If a user is deleted, it must be the path id, and not the caller if path id is self (FR-19).

## Sub-domains covered
A-ID-01, A-AUTH-01

## Type
Unspecified

## Audit
- **Status:** INCOMPLETE
- **Reasoning:** No body is documented for DELETE. Assuming the delete still succeeds with {force:true} invents a body-ignored rule.

## Status / Related bugs
Not Run / None
