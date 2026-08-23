# TC-ADMINUSERS-013: Reject malformed JWT

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
| Authorization | Bearer not-a-jwt |
| id | <disposable_user_id> |

## Test steps
1. DELETE /api/admin/users/{disposable_user_id} with Authorization: Bearer not-a-jwt.

## Expected result
DELETE /api/admin/users/:id requires a valid JWT and role=admin (API spec §6; FR-12; SEC-02; SEC-03). The target user must still exist afterwards. HTTP status is not specified.

## Sub-domains covered
A-AUTH-04

## Type
Invalid

## Audit
- **Status:** INCOMPLETE
- **Reasoning:** Malformed token is not a valid JWT. HTTP 403/401 is not specified.

## Status / Related bugs
Not Run / None
