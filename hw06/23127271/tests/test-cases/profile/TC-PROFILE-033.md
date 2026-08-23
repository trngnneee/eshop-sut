# TC-PROFILE-033: Reject or ignore role=admin in profile body (SEC-06)

## Requirement ID
FR-04

## Module / Test type / Technique
profile / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- EShop backend is running at http://localhost:3000.
- Seed user test@eshop.com / Test1234! exists (role=user).
- Obtain a user JWT via POST /api/login with email=test@eshop.com password=Test1234!.
- Confirm GET /api/users/me shows role=user.

## Test data
| Field | Value |
|-------|-------|
| name | Nguyen Van A |
| phone | 0912345678 |
| shipping_address | 123 Le Loi, Q1, TP.HCM |
| role | admin |

## Test steps
1. PUT /api/users/me with valid profile fields plus role=admin.
2. GET /api/users/me and assert role is still user.

## Expected result
role remains the pre-request value (user). Documented profile fields may or may not update; that is unspecified. A silent role change to admin fails FR-04 / SEC-06.

## Sub-domains covered
P-ROLE-02, P-NAME-01, P-PHONE-01, P-ADDR-01, P-AUTH-01

## Type
Invalid

## Audit
- **Status:** VALID
- **Reasoning:** FR-04 and SEC-06 forbid changing role from the client. The oracle allows reject or ignore, so it does not invent a status code.

## Status / Related bugs
Not Run / None
