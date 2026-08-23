# TC-PROFILE-SUP-001: Partial PUT — only a FR-04-valid phone (name and address omitted)

## Requirement ID
FR-04

## Module / Test type / Technique
profile / Functional / Domain Testing – Equivalence Partitioning (human extension)

## Preconditions
- EShop backend is running at http://localhost:3000.
- Seed user test@eshop.com / Test1234! exists (role=user).
- Obtain a user JWT via POST /api/login.
- Snapshot GET /api/users/me (name, phone, shipping_address, email, role).
- Choose a new phone that is FR-04-valid and different from the snapshot, e.g. 0987654321.

## Test data
| Field | Value |
|-------|-------|
| Authorization | Bearer <user_token> |
| phone | 0987654321 |
| name | (omitted) |
| shipping_address | (omitted) |

## Test steps
1. PUT /api/users/me with body `{"phone":"0987654321"}` only.
2. GET /api/users/me with the same token.

## Expected result
If phone is applied, GET shows phone=0987654321 (FR-04-valid). email/role unchanged. Omitted name/address semantics not specified — record whether snapshot fields stay or change. Do not reject solely because body is not the three-field example.

## Sub-domains covered
P-PHONE-01, P-NAME-05, P-ADDR-04, P-AUTH-01 (human: partial-update on-point)

## Type
Valid / Unspecified

## Why the AI missed this
Prompt quality: Stage 1 was driven off the API example object `{name, shipping_address, phone}`, so the model treated that triple as the only valid shape and generated omit-name only as a negative (assumed required). After Stage 2 dropped that assumption, there was still no positive “phone-only update” representative.

## Audit (human SUP)
- **Status:** VALID
- **Reasoning:** Positive phone-only partial after Stage 2 dropped mandatory triple-body; oracle observe-only for omitted fields.

## Status / Related bugs
Not Run / None
