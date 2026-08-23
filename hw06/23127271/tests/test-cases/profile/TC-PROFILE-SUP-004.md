# TC-PROFILE-SUP-004: Partial PUT — only name (phone and address omitted)

## Requirement ID
FR-04

## Module / Test type / Technique
profile / Functional / Domain Testing – Equivalence Partitioning (human extension)

## Preconditions
- EShop backend is running at http://localhost:3000.
- Logged in as test@eshop.com / Test1234!.
- Snapshot GET /api/users/me (name, phone, shipping_address, email, role).

## Test data
| Field | Value |
|-------|-------|
| Authorization | Bearer <user_token> |
| name | Updated Name Only |
| phone | (omitted) |
| shipping_address | (omitted) |

## Test steps
1. PUT /api/users/me with body `{"name":"Updated Name Only"}` only.
2. GET /api/users/me.

## Expected result
If name applied, GET shows Updated Name Only. email/role unchanged. Omitted phone/address not specified — record snapshot vs cleared.

## Sub-domains covered
P-NAME-01, P-PHONE-07, P-ADDR-04 (human: name-only partial update)

## Type
Valid / Unspecified

## Why the AI missed this
Prompt quality: Stage 1 always sent the full example object or isolated one invalid omitted field. Human SUP-001 added phone-only partial update; the model never split the other two updatable fields (name, shipping_address) into their own positive partial-update representatives.

## Audit (human SUP)
- **Status:** VALID
- **Reasoning:** Name-only partial mirrors SUP-001 pattern; spec-aligned.

## Status / Related bugs
Not Run / None
