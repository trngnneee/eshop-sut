# TC-ADMINUSERS-SCH-001: GET /api/admin/users returns JSON array

## Requirement ID
FR-19

## Module / Test type / Technique
admin-users / Schema validation / Response & request shape

## Schema aspect
GET list root type

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=admin@eshop.com password=Admin123!.

## Test data
| (see steps) | |

## Test steps
1. GET /api/admin/users.
2. Assert Array.isArray(body).

## Expected result
Root is JSON array of users. Response Content-Type header includes application/json (or charset=utf-8 JSON body).

## Schema contract reference
api_spec section 6.1 user list.

## Type
Schema validation

## Audit
- **Status:** VALID
- **Reasoning:** Admin user list is a collection; JSON array root + Content-Type is valid.

## Status / Related bugs
Not Run / None
