# TC-ADMINUSERS-SCH-005: User list item email is string

## Requirement ID
FR-19

## Module / Test type / Technique
admin-users / Schema validation / Response & request shape

## Schema aspect
Field email type

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=admin@eshop.com password=Admin123!.

## Test data
| (see steps) | |

## Test steps
1. GET /api/admin/users.
2. Assert each user.email typeof string.

## Expected result
email is string on each user object.

## Schema contract reference
Login/register email string; admin list exposes users.

## Type
Schema validation

## Audit
- **Status:** VALID
- **Reasoning:** FR-19 admin user list implies identifiable users; email as string is a reasonable schema contract.

## Status / Related bugs
Not Run / None
