# TC-ADMINUSERS-015: User JWT cannot delete self via admin route

## Requirement ID
FR-19

## Module / Test type / Technique
admin-users / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- EShop backend is running at http://localhost:3000.
- Seed user test@eshop.com / Test1234! exists (role=user).
- Obtain a user JWT via POST /api/login with email=test@eshop.com password=Test1234!.
- Resolve user_self_id from GET /api/users/me.

## Test data
| Field | Value |
|-------|-------|
| Authorization | Bearer <user_token> |
| id | <user_self_id> |

## Test steps
1. DELETE /api/admin/users/{user_self_id} with that user JWT.
2. GET /api/users/me still succeeds.

## Expected result
A non-admin token must not delete this account (FR-12 / SEC-03). The user still exists. HTTP status is not specified.

## Sub-domains covered
A-AUTH-05, A-REL-02, A-ROLE-02

## Type
Invalid

## Audit
- **Status:** INCOMPLETE
- **Reasoning:** Same FR-12 rule; plus FR-19 is irrelevant if the caller is not allowed to use the admin API at all. HTTP 403 is not specified.

## Status / Related bugs
Not Run / None
