# TC-PROFILE-030: Reject empty Bearer token

## Requirement ID
FR-04

## Module / Test type / Technique
profile / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- EShop backend is running at http://localhost:3000.
- Seed user test@eshop.com / Test1234! exists (role=user).
- Obtain a user JWT via POST /api/login with email=test@eshop.com password=Test1234!.

## Test data
| Field | Value |
|-------|-------|
| Authorization | Bearer  |
| body | {"name": "Nguyen Van A", "shipping_address": "123 Le Loi, Q1, TP.HCM", "phone": "0912345678"} |

## Test steps
1. PUT /api/users/me with Authorization: Bearer <empty> and valid body.

## Expected result
The endpoint requires a valid JWT (API spec Authorization note; SEC-02; FR-04 requires a logged-in user). The profile / cart / user-list must not change. HTTP status (401 vs 403 vs other) is not specified.

## Sub-domains covered
P-AUTH-04

## Type
Invalid

## Audit
- **Status:** INCOMPLETE
- **Reasoning:** Empty Bearer is not a valid JWT (SEC-02). HTTP 401 is not specified.

## Status / Related bugs
Not Run / None
