# TC-PROFILE-040: Content-Type text/plain — not specified

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
| Content-Type | text/plain |
| body | {"name": "Nguyen Van A", "shipping_address": "123 Le Loi, Q1, TP.HCM", "phone": "0912345678"} |

## Test steps
1. PUT /api/users/me with Content-Type: text/plain and a JSON-looking body.

## Expected result
The SRS and api_specification.md do not state this input is invalid or required. Do not expect rejection. Record what the SUT does; do not fail it against an invented rule.

## Sub-domains covered
P-BODY-06, P-AUTH-01

## Type
Unspecified

## Audit
- **Status:** INVALID
- **Reasoning:** Content-Type is not specified. JSON in the spec describes the body example, not a header rule.

## Status / Related bugs
Not Run / None
