# TC-PROFILE-036: Empty HTTP body — not specified as invalid

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
| body | (empty) |

## Test steps
1. PUT /api/users/me with Authorization and Content-Type application/json but empty body.

## Expected result
The SRS and api_specification.md do not state this input is invalid or required. Do not expect rejection. Record what the SUT does; do not fail it against an invented rule.

## Sub-domains covered
P-BODY-02, P-AUTH-01

## Type
Unspecified

## Audit
- **Status:** INVALID
- **Reasoning:** An empty HTTP body is not stated as invalid. Fields were assumed required as a group.

## Status / Related bugs
Not Run / None
