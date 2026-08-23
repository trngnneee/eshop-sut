# TC-ADMINUSERS-SCH-004: User list item name is string

## Requirement ID
FR-19

## Module / Test type / Technique
admin-users / Schema validation / Response & request shape

## Schema aspect
Field name type

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=admin@eshop.com password=Admin123!.

## Test data
| (see steps) | |

## Test steps
1. GET /api/admin/users.
2. Assert each user.name typeof string when present.

## Expected result
If name is returned on each user object, typeof must be string. Record if absent — not documented in api_spec.

## Schema contract reference
User entity name from register example.

## Type
Schema validation

## Audit
- **Status:** INCOMPLETE
- **Reasoning:** name field on admin list items is not documented in api_spec or FR-19.

## Status / Related bugs
Not Run / None
