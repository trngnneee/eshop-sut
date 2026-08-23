# TC-PROFILE-037: Send malformed JSON (not the documented JSON body)

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
| body | {name: |

## Test steps
1. PUT /api/users/me with body `{name:` (invalid JSON).

## Expected result
The body is not the documented JSON object. Profile fields must not be updated from this payload. HTTP status is not specified.

## Sub-domains covered
P-BODY-03, P-AUTH-01

## Type
Invalid

## Audit
- **Status:** INCOMPLETE
- **Reasoning:** The API documents Body (JSON). Malformed text is not JSON. Generated HTTP 400 is not specified.

## Status / Related bugs
Not Run / None
