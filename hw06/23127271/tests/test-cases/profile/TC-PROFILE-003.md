# TC-PROFILE-003: Unicode name and unicode address (valid combination at language edge)

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
| name | Nguyễn Văn Á |
| phone | 09123456789 |
| shipping_address | 12 Nguyễn Huệ, Quận 1, TP.HCM |

## Test steps
1. PUT /api/users/me with Unicode name, 11-digit phone, and Unicode address (two/three valid edges together).
2. GET /api/users/me and assert exact strings persisted (no mojibake).

## Expected result
GET /api/users/me persists the Unicode name, Unicode address, and 11-digit phone exactly. email and role unchanged. Success status/body not specified.

## Sub-domains covered
P-NAME-02, P-ADDR-02, P-PHONE-02, P-AUTH-01

## Type
Valid

## Audit
- **Status:** VALID
- **Reasoning:** No charset restriction is stated for name or address. 11-digit phone is in the FR-04 valid set. Combining valid representatives is allowed.

## Status / Related bugs
Not Run / None
