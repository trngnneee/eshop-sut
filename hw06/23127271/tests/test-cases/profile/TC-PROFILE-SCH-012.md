# TC-PROFILE-SCH-012: PUT with empty JSON object — observe response schema

## Requirement ID
FR-04

## Module / Test type / Technique
profile / Schema validation / Response & request shape

## Schema aspect
Empty PUT body

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.
- Snapshot GET profile.

## Test data
| (see steps) | |

## Test steps
1. PUT /api/users/me with body {}.
2. Inspect response JSON; GET profile.

## Expected result
Response is JSON (object or documented error shape). Partial update semantics not specified — record GET field values. HTTP status is not specified in api_specification.md — record actual without inventing codes.

## Schema contract reference
Required fields on PUT not stated in api_spec — observe-only.

## Type
Schema validation

## Audit
- **Status:** VALID
- **Reasoning:** Partial/empty PUT body semantics are unspecified; observe response and GET field values without inventing rules.

## Status / Related bugs
Not Run / None
