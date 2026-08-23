# TC-ADMINUSERS-014: Non-admin user cannot delete a user (FR-12 / SEC-03)

## Requirement ID
FR-19

## Module / Test type / Technique
admin-users / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- EShop backend is running at http://localhost:3000.
- Seed user test@eshop.com / Test1234! exists (role=user).
- Obtain a user JWT via POST /api/login with email=test@eshop.com password=Test1234!.
- Create a disposable victim via register (or pick a user id that is not the caller).
- Do not use the caller's own id for this case (that would mix self-delete with role).

## Test data
| Field | Value |
|-------|-------|
| Authorization | Bearer <user_token> |
| id | <other_user_id> |

## Test steps
1. DELETE /api/admin/users/{other_user_id} with the regular user JWT.
2. Login as admin and GET /api/admin/users: victim still exists.

## Expected result
A non-admin caller must not delete the target. The target still exists afterwards. HTTP status is not specified.

## Sub-domains covered
A-AUTH-05, A-ROLE-02

## Type
Invalid

## Audit
- **Status:** INCOMPLETE
- **Reasoning:** FR-12 / SEC-03: admin APIs require role=admin, not merely a token. Generated HTTP 403 is not specified.

## Status / Related bugs
Not Run / None
