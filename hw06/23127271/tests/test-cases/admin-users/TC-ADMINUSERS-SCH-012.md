# TC-ADMINUSERS-SCH-012: GET admin users Content-Type is JSON

## Requirement ID
FR-19

## Module / Test type / Technique
admin-users / Schema validation / Response & request shape

## Schema aspect
Content-Type header

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=admin@eshop.com password=Admin123!.

## Test data
| (see steps) | |

## Test steps
1. GET /api/admin/users.
2. Inspect Content-Type.

## Expected result
Response Content-Type header includes application/json (or charset=utf-8 JSON body).

## Schema contract reference
Checklist section 4.

## Type
Schema validation

## Audit
- **Status:** VALID
- **Reasoning:** Content-Type application/json is a standard schema contract check.

## Status / Related bugs
Not Run / None
