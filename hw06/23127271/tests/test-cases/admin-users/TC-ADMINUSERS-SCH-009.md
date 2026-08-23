# TC-ADMINUSERS-SCH-009: DELETE success body is JSON object

## Requirement ID
FR-19

## Module / Test type / Technique
admin-users / Schema validation / Response & request shape

## Schema aspect
DELETE success response type

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=admin@eshop.com password=Admin123!.
- Register disposable D.

## Test data
| (see steps) | |

## Test steps
1. DELETE /api/admin/users/D.
2. Parse response as JSON object.

## Expected result
Response body is JSON object (not HTML/array). Field schema not in api_spec — record keys/types. HTTP status is not specified in api_specification.md — record actual without inventing codes.

## Schema contract reference
Gap: api_spec 6.1 DELETE response undocumented.

## Type
Schema validation

## Audit
- **Status:** VALID
- **Reasoning:** DELETE success body is undocumented; observe-only JSON object type check is correct.

## Status / Related bugs
Not Run / None
