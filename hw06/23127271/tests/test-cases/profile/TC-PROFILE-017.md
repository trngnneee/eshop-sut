# TC-PROFILE-017: Reject empty phone

## Requirement ID
FR-04

## Module / Test type / Technique
profile / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- EShop backend is running at http://localhost:3000.
- Seed user test@eshop.com / Test1234! exists (role=user).
- Obtain a user JWT via POST /api/login with email=test@eshop.com password=Test1234!.
- Snapshot GET /api/users/me.

## Test data
| Field | Value |
|-------|-------|
| phone | "" (empty string) |
| name | Nguyen Van A |
| shipping_address | 123 Le Loi, Q1, TP.HCM |

## Test steps
1. PUT /api/users/me with phone="" (empty string) and other fields valid.
2. GET /api/users/me.

## Expected result
The submitted phone is not a valid FR-04 phone (must start with 0 and be 10–11 digits). GET /api/users/me must not persist this value as phone. HTTP status and error body are not specified.

## Sub-domains covered
P-PHONE-06, P-NAME-01, P-ADDR-01, P-AUTH-01

## Type
Invalid

## Audit
- **Status:** INCOMPLETE
- **Reasoning:** Empty string is not 10–11 digits starting with 0, so it fails the stated phone rule (this is format, not an assumed 'required' flag). HTTP 400 is not specified.

## Status / Related bugs
Not Run / None
