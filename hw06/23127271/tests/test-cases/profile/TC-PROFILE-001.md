# TC-PROFILE-001: Update profile with all typical valid values (on-point)

## Requirement ID
FR-04

## Module / Test type / Technique
profile / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- EShop backend is running at http://localhost:3000.
- Seed user test@eshop.com / Test1234! exists (role=user).
- Obtain a user JWT via POST /api/login with email=test@eshop.com password=Test1234!.
- Snapshot GET /api/users/me (email, role, current profile) before the PUT.

## Test data
| Field | Value |
|-------|-------|
| Authorization | Bearer <user_token> |
| name | Nguyen Van A |
| phone | 0912345678 |
| shipping_address | 123 Le Loi, Q1, TP.HCM |

## Test steps
1. PUT /api/users/me with the test data and Content-Type application/json.
2. Record status code and body.
3. GET /api/users/me with the same token and compare fields.

## Expected result
The authenticated user's name, phone, and shipping_address match the submitted values on a follow-up GET /api/users/me. email and role are unchanged. Success HTTP status and response body are not specified.

## Sub-domains covered
P-NAME-01, P-PHONE-01, P-ADDR-01, P-AUTH-01, P-ROLE-01, P-EMAIL-01, P-BODY-01

## Type
Valid

## Audit
- **Status:** VALID
- **Reasoning:** FR-04 allows updating name, phone, and default shipping address for the logged-in user; email and role must stay unchanged (FR-04 / SEC-06). Input is the documented example shape.

## Status / Related bugs
Not Run / None
