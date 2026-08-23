# TC-PROFILE-SCH-001: GET /api/users/me returns JSON object

## Requirement ID
FR-04

## Module / Test type / Technique
profile / Schema validation / Response & request shape

## Schema aspect
GET response root type

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.

## Test data
| (see steps) | |

## Test steps
1. GET /api/users/me with valid JWT.
2. Parse body as JSON; assert root is object (not array/null).

## Expected result
Body is a JSON object. Response Content-Type header includes application/json (or charset=utf-8 JSON body). HTTP status is not specified in api_specification.md — record actual without inventing codes.

## Schema contract reference
api_spec section 2.1 documents GET profile; root envelope type not explicit — object inferred from single-user resource.

## Type
Schema validation

## Audit
- **Status:** VALID
- **Reasoning:** GET profile returns JSON object per REST convention; Content-Type check is standard schema probe.

## Status / Related bugs
Not Run / None
