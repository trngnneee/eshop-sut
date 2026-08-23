# TC-ADMINUSERS-SCH-002: Each list element is JSON object

## Requirement ID
FR-19

## Module / Test type / Technique
admin-users / Schema validation / Response & request shape

## Schema aspect
List element type

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=admin@eshop.com password=Admin123!.

## Test data
| (see steps) | |

## Test steps
1. GET /api/admin/users.
2. For each element assert typeof object and not array.

## Expected result
Every array element is plain JSON object (user record).

## Schema contract reference
List of user objects implied by FR-19 admin user management.

## Type
Schema validation

## Audit
- **Status:** VALID
- **Reasoning:** Each list element must be a user object, not a scalar or nested array.

## Status / Related bugs
Not Run / None
