# TC-PROFILE-029: Reject update with no Authorization header

## Requirement ID
FR-04

## Module / Test type / Technique
profile / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- EShop backend is running at http://localhost:3000.
- Do not send a token.

## Test data
| Field | Value |
|-------|-------|
| Authorization | (omitted) |
| body | {"name": "Nguyen Van A", "shipping_address": "123 Le Loi, Q1, TP.HCM", "phone": "0912345678"} |

## Test steps
1. PUT /api/users/me with valid JSON body and no Authorization header.

## Expected result
The endpoint requires a valid JWT (API spec Authorization note; SEC-02; FR-04 requires a logged-in user). The profile / cart / user-list must not change. HTTP status (401 vs 403 vs other) is not specified.

## Sub-domains covered
P-AUTH-03

## Type
Invalid

## Audit
- **Status:** INCOMPLETE
- **Reasoning:** Token is required (API spec Users section; SEC-02). Generated HTTP 401 is not specified.

## Status / Related bugs
Not Run / None
