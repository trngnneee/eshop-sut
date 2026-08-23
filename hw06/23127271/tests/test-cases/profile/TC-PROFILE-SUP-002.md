# TC-PROFILE-SUP-002: Phone using fullwidth Unicode digits (０９１２３４５６７８)

## Requirement ID
FR-04

## Module / Test type / Technique
profile / Functional / Domain Testing – Equivalence Partitioning (human extension)

## Preconditions
- EShop backend is running at http://localhost:3000.
- Logged in as test@eshop.com / Test1234!.
- Snapshot GET /api/users/me phone.

## Test data
| Field | Value |
|-------|-------|
| Authorization | Bearer <user_token> |
| name | Nguyen Van A |
| shipping_address | 123 Le Loi, Q1, TP.HCM |
| phone | ０９１２３４５６７８ (U+FF10…U+FF18; 10 fullwidth digit characters) |

## Test steps
1. PUT /api/users/me with phone set to the 10 fullwidth digits above (not ASCII 0912345678).
2. GET /api/users/me.

## Expected result
Fullwidth digits (U+FF10…) are not the documented ASCII 0–9 form. GET must not persist as FR-04-valid phone. Normalisation not specified — record only.

## Sub-domains covered
P-PHONE-H01 (human: non-ASCII digit alphabet)

## Type
Invalid

## Why the AI missed this
Model limitation: phone partitions were generated only in ASCII 0–9 (empty, 9/10/11/12 digits, letters, `+84`, separators). The model did not split “chữ số” into Unicode digit scripts even though the SUT is a Vietnamese app that already uses Unicode in other fields.

## Audit (human SUP)
- **Status:** VALID
- **Reasoning:** Fullwidth digits violate FR-04 ASCII phone rule; observe-only invalid partition.

## Status / Related bugs
Not Run / None
