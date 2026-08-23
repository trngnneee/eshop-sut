# TC-ADMINUSERS-SCH-014: After DELETE, list remains array of valid user objects

## Requirement ID
FR-19

## Module / Test type / Technique
admin-users / Schema validation / Response & request shape

## Schema aspect
List schema after delete

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=admin@eshop.com password=Admin123!.
- Register D.

## Test data
| (see steps) | |

## Test steps
1. DELETE D.
2. GET /api/admin/users.
3. Assert array; no element with id===D; remaining elements pass object schema.

## Expected result
GET still JSON array. Deleted id absent. Remaining items retain id(number), email(string), role(string).

## Schema contract reference
DELETE effect on list collection schema.

## Type
Schema validation

## Audit
- **Status:** VALID
- **Reasoning:** Post-DELETE list must remain a valid user array with consistent element types.

## Status / Related bugs
Not Run / None
