# TC-PROFILE-004: Admin updates own profile with valid fields

## Requirement ID
FR-04

## Module / Test type / Technique
profile / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- EShop backend is running at http://localhost:3000.
- Seed admin admin@eshop.com / Admin123! exists (role=admin).
- Obtain an admin JWT via POST /api/login with email=admin@eshop.com password=Admin123!.
- Snapshot GET /api/users/me as admin.

## Test data
| Field | Value |
|-------|-------|
| Authorization | Bearer <admin_token> |
| name | Admin Updated |
| phone | 0912345678 |
| shipping_address | 1 Admin Street |

## Test steps
1. PUT /api/users/me as admin with valid body.
2. GET /api/users/me as admin; confirm role remains admin.

## Expected result
GET /api/users/me as that admin shows the new name/phone/address and role still admin. Success status/body not specified.

## Sub-domains covered
P-AUTH-02, P-NAME-01, P-PHONE-01, P-ADDR-01

## Type
Valid

## Audit
- **Status:** VALID
- **Reasoning:** FR-04 applies to a logged-in user; an admin token is a logged-in user. Role must remain admin (FR-04 / SEC-06).

## Status / Related bugs
Not Run / None
