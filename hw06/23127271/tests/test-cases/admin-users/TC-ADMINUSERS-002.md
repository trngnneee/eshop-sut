# TC-ADMINUSERS-002: Admin cannot delete their own account (FR-19)

## Requirement ID
FR-19

## Module / Test type / Technique
admin-users / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- EShop backend is running at http://localhost:3000.
- Seed admin admin@eshop.com / Admin123! exists (role=admin).
- Obtain an admin JWT via POST /api/login with email=admin@eshop.com password=Admin123!.
- Resolve admin_self_id from GET /api/users/me (seed admin is id=1 on a fresh DB).

## Test data
| Field | Value |
|-------|-------|
| id | <admin_self_id> |
| Authorization | Bearer <admin_token> |

## Test steps
1. DELETE /api/admin/users/{admin_self_id} with that same admin JWT.
2. GET /api/users/me and GET /api/admin/users: admin still exists.

## Expected result
The admin's own account still exists (GET /api/users/me and GET /api/admin/users). HTTP status is not specified.

## Sub-domains covered
A-ID-02, A-REL-02, A-AUTH-01, A-ROLE-01

## Type
Invalid

## Audit
- **Status:** INCOMPLETE
- **Reasoning:** FR-19 forbids deleting the currently logged-in account. Generated HTTP 403/400 is not specified.

## Status / Related bugs
Not Run / None
