# TC-PROFILE-SCH-009: PUT success response is JSON object

## Requirement ID
FR-04

## Module / Test type / Technique
profile / Schema validation / Response & request shape

## Schema aspect
PUT success response envelope

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.

## Test data
| (see steps) | |

## Test steps
1. PUT /api/users/me with valid documented body.
2. Inspect response body JSON type and top-level keys.

## Expected result
Response body is JSON object (not array/HTML). Field names/types not documented in api_spec — record actual. HTTP status is not specified in api_specification.md — record actual without inventing codes.

## Schema contract reference
Gap: api_spec section 2.2 does not document PUT success response envelope.

## Type
Schema validation

## Audit
- **Status:** VALID
- **Reasoning:** PUT success response envelope is not defined in api_spec; observe-only JSON type check is correct.

## Status / Related bugs
Not Run / None
