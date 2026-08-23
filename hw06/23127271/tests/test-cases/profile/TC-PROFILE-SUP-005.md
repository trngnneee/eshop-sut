# TC-PROFILE-SUP-005: Partial PUT — name + phone only (shipping_address omitted)

## Requirement ID
FR-04

## Module / Test type / Technique
profile / Functional / Domain Testing – Equivalence Partitioning (human extension)

## Preconditions
- EShop backend is running at http://localhost:3000.
- Logged in as test@eshop.com / Test1234!.
- Snapshot GET /api/users/me.

## Test data
| Field | Value |
|-------|-------|
| Authorization | Bearer <user_token> |
| name | Nguyen Van B |
| phone | 0909090909 |
| shipping_address | (omitted) |

## Test steps
1. PUT /api/users/me with body `{"name":"Nguyen Van B","phone":"0909090909"}` (no shipping_address).
2. GET /api/users/me.

## Expected result
Two-field subset: name + FR-04-valid phone may update; shipping_address behaviour unspecified. email/role unchanged.

## Sub-domains covered
P-NAME-01, P-PHONE-01, P-ADDR-04 (human: two-field partial combination)

## Type
Valid / Unspecified

## Why the AI missed this
Prompt quality / combination rule gap: domain testing used on-point (all fields valid) and off-point (one invalid field). The generator did not enumerate **valid subsets** of the example body (2-of-3 combinations). Only after audit did single-field partials appear (SUP-001); pairwise omission was still missing.

## Audit (human SUP)
- **Status:** VALID
- **Reasoning:** Two-of-three field subset; oracle correctly flags address unspecified.

## Status / Related bugs
Not Run / None
