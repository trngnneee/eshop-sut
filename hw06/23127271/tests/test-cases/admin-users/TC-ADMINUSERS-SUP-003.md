# TC-ADMINUSERS-SUP-003: Admin deletes seed test user (id=2 on fresh DB)

## Requirement ID
FR-19

## Module / Test type / Technique
admin-users / Functional / Domain Testing – Equivalence Partitioning (human extension)

## Preconditions
- EShop backend is running at http://localhost:3000 with default seed (admin id=1, test user id=2 at test@eshop.com).
- Logged in as admin@eshop.com / Admin123!.
- Do **not** use the admin’s own id (1).

## Test data
| Field | Value |
|-------|-------|
| Authorization | Bearer <admin_token> |
| id | 2 |

## Test steps
1. DELETE /api/admin/users/2 with admin JWT.
2. GET /api/admin/users — id=2 absent; id=1 (admin) still present.
3. Confirm response bodies never include a password field (FR-19).

## Expected result
FR-19: delete user id=2 (not admin self) allowed if id=2 exists. Record id=2 absent and admin id=1 present after test. Restore seed DB if test environment requires test@eshop.com. No password in list (SEC-01).

## Sub-domains covered
A-ID-01, A-REL-01, A-AUTH-01 (human: known seed target user)

## Type
Valid / Unspecified

## Why the AI missed this
Prompt quality: Stage 1 preconditions always said “register a disposable user” for the happy path, so the **fixed seed id=2** partition was never a representative. The model preferred dynamic registration over using documented seed data as a stable domain value.

## Audit (human SUP)
- **Status:** INCOMPLETE
- **Reasoning:** Destructive seed-user delete is acceptable probe but oracle assumed id=2 always exists — precondition should note DB restore.

## Status / Related bugs
Not Run / None
