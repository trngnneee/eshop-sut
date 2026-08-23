# TC-PROFILE-SCH-002: Profile name field is string

## Requirement ID
FR-04

## Module / Test type / Technique
profile / Schema validation / Response & request shape

## Schema aspect
Field name type

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.

## Test data
| (see steps) | |

## Test steps
1. GET /api/users/me.
2. Assert typeof name === 'string' when present.

## Expected result
If name is returned on GET /api/users/me, typeof must be string (FR-04 profile field). Record if absent — GET field list not in api_spec.

## Schema contract reference
api_spec PUT example includes name string; FR-04 lists name as updatable profile field.

## Type
Schema validation

## Audit
- **Status:** INCOMPLETE
- **Reasoning:** GET /api/users/me response fields are not listed in api_spec; oracle hedges with observe-if-absent but still opens with mandatory presence.

## Status / Related bugs
Not Run / None
