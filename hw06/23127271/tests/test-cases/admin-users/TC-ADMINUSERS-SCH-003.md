# TC-ADMINUSERS-SCH-003: User list item id is number

## Requirement ID
FR-19

## Module / Test type / Technique
admin-users / Schema validation / Response & request shape

## Schema aspect
Field id type

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=admin@eshop.com password=Admin123!.

## Test data
| (see steps) | |

## Test steps
1. GET /api/admin/users.
2. Pick first user — typeof id === 'number'.

## Expected result
If id is returned on list items, it must be JSON number. Record if absent — list field schema not in api_spec.

## Schema contract reference
Register response documents numeric id; list items expected consistent.

## Type
Schema validation

## Audit
- **Status:** INCOMPLETE
- **Reasoning:** GET /api/admin/users item schema is not defined in api_spec; id:number is inferred from register response, not list contract.

## Status / Related bugs
Not Run / None
