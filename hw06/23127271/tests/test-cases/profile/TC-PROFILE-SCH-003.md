# TC-PROFILE-SCH-003: Profile phone field is string

## Requirement ID
FR-04

## Module / Test type / Technique
profile / Schema validation / Response & request shape

## Schema aspect
Field phone type

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.

## Test data
| (see steps) | |

## Test steps
1. GET /api/users/me.
2. Assert typeof phone === 'string' when present.

## Expected result
If phone is returned on GET /api/users/me, typeof must be string. FR-04 phone format applies to value, not JSON type. Record if absent.

## Schema contract reference
api_spec PUT example phone:'0912345678' (string).

## Type
Schema validation

## Audit
- **Status:** INCOMPLETE
- **Reasoning:** Same as SCH-002: phone type is inferable from PUT example but GET shape is undocumented.

## Status / Related bugs
Not Run / None
