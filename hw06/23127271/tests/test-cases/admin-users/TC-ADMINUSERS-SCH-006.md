# TC-ADMINUSERS-SCH-006: User list item role is string

## Requirement ID
FR-19

## Module / Test type / Technique
admin-users / Schema validation / Response & request shape

## Schema aspect
Field role type

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=admin@eshop.com password=Admin123!.

## Test data
| (see steps) | |

## Test steps
1. GET /api/admin/users.
2. Assert each user.role typeof string in {user,admin}.

## Expected result
role is string (user or admin per FR-12).

## Schema contract reference
FR-12 role=admin for admin APIs implies role field on user records.

## Type
Schema validation

## Audit
- **Status:** VALID
- **Reasoning:** FR-12 defines user and admin roles; role as string on list items is spec-aligned.

## Status / Related bugs
Not Run / None
