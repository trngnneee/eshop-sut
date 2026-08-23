# TC-ADMINUSERS-SUP-002: DELETE with trailing slash on path id

## Requirement ID
FR-19

## Module / Test type / Technique
admin-users / Functional / Domain Testing – Equivalence Partitioning (human extension)

## Preconditions
- EShop backend is running at http://localhost:3000.
- Logged in as admin@eshop.com / Admin123!.
- Register a disposable user; note `disposable_user_id` (not the admin’s own id).

## Test data
| Field | Value |
|-------|-------|
| Authorization | Bearer <admin_token> |
| path | `/api/admin/users/{disposable_user_id}/` (note trailing slash) |

## Test steps
1. DELETE `/api/admin/users/{disposable_user_id}/` with admin JWT.
2. GET /api/admin/users.
3. GET /api/users/me as admin still succeeds.

## Expected result
Trailing slash not specified. Record routing outcome; if delete succeeds, target is disposable user only.

## Sub-domains covered
A-ID-01, A-REL-01 (human: trailing-slash path variant)

## Type
Unspecified

## Why the AI missed this
Model limitation: path partitions used literal `/api/admin/users/{id}` forms. HTTP servers often treat `/users/3` and `/users/3/` differently; that URI normalisation domain is not in `api_specification.md`, so the generator never emitted it.

## Audit (human SUP)
- **Status:** VALID
- **Reasoning:** Trailing slash routing unspecified; observe-only.

## Status / Related bugs
Not Run / None
