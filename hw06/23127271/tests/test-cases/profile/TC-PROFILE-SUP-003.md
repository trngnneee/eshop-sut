# TC-PROFILE-SUP-003: Duplicate JSON key `phone` (valid then invalid)

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
| Raw body | `{"name":"Nguyen Van A","shipping_address":"123 Le Loi, Q1, TP.HCM","phone":"0912345678","phone":"1912345678"}` |

## Test steps
1. PUT /api/users/me with the raw JSON above (duplicate `phone` keys; first value FR-04-valid, second starts with 1).
2. GET /api/users/me.

## Expected result
Duplicate JSON keys not specified. Stored phone, if any, must be FR-04-valid — GET must not show 1912345678. email/role unchanged.

## Sub-domains covered
P-BODY-H01 (human: duplicate JSON keys)

## Type
Invalid / Unspecified

## Why the AI missed this
Characteristic of JSON APIs + model limitation: `api_specification.md` never mentions duplicate keys, and LLMs almost always emit unique keys. Last-key-wins vs first-key-wins is a parser property of the Node/Express SUT, not visible from the spec text alone.

## Audit (human SUP)
- **Status:** VALID
- **Reasoning:** Duplicate JSON key probe; oracle does not invent parser winner.

## Status / Related bugs
Not Run / None
