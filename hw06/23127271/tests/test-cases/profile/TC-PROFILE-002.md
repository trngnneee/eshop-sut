# TC-PROFILE-002: Phone at 11-digit valid maximum

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
| name | Nguyen Van A |
| phone | 09123456789 |
| shipping_address | 123 Le Loi, Q1, TP.HCM |

## Test steps
1. PUT /api/users/me with phone=09123456789 and other fields valid.
2. GET /api/users/me and assert phone persisted.

## Expected result
GET /api/users/me shows phone=09123456789 together with the submitted name and shipping_address. email and role unchanged. Success status/body not specified.

## Sub-domains covered
P-PHONE-02, P-NAME-01, P-ADDR-01, P-AUTH-01

## Type
Valid

## Audit
- **Status:** VALID
- **Reasoning:** FR-04 states a valid phone is 10–11 digits starting with 0. 11 digits is the documented maximum.

## Status / Related bugs
Not Run / None
