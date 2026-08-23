# TC-ADMINUSERS-SCH-013: GET list as user — error response JSON shape

## Requirement ID
FR-19 / FR-12

## Module / Test type / Technique
admin-users / Schema validation / Response & request shape

## Schema aspect
User JWT error body

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.

## Test data
| (see steps) | |

## Test steps
1. GET /api/admin/users with user JWT.
2. Record response body JSON type and keys.

## Expected result
Must not return full admin user array. Error envelope not specified — record JSON vs HTML. HTTP status is not specified in api_specification.md — record actual without inventing codes.

## Schema contract reference
FR-12 admin-only API; error schema gap in api_spec.

## Type
Schema validation

## Audit
- **Status:** VALID
- **Reasoning:** Non-admin JWT must not receive full user array; error envelope is observe-only.

## Status / Related bugs
Not Run / None
