# TC-PROFILE-032: Reject JWT with invalid signature

## Requirement ID
FR-04

## Module / Test type / Technique
profile / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- EShop backend is running at http://localhost:3000.
- Seed user test@eshop.com / Test1234! exists (role=user).
- Obtain a user JWT via POST /api/login with email=test@eshop.com password=Test1234!.
- Create a tampered token by altering the last character of a valid JWT.

## Test data
| Field | Value |
|-------|-------|
| Authorization | Bearer <tampered_jwt> |
| body | {"name": "Nguyen Van A", "shipping_address": "123 Le Loi, Q1, TP.HCM", "phone": "0912345678"} |

## Test steps
1. PUT /api/users/me with the tampered JWT and valid body.

## Expected result
The endpoint requires a valid JWT (API spec Authorization note; SEC-02; FR-04 requires a logged-in user). The profile / cart / user-list must not change. HTTP status (401 vs 403 vs other) is not specified.

## Sub-domains covered
P-AUTH-06

## Type
Invalid

## Audit
- **Status:** INCOMPLETE
- **Reasoning:** A tampered signature is not a valid JWT (SEC-02). HTTP 403 is not specified.

## Status / Related bugs
Not Run / None
