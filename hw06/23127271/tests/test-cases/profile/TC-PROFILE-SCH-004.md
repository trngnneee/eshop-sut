# TC-PROFILE-SCH-004: shipping_address field is string

## Requirement ID
FR-04

## Module / Test type / Technique
profile / Schema validation / Response & request shape

## Schema aspect
Field shipping_address type

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.

## Test data
| (see steps) | |

## Test steps
1. GET /api/users/me.
2. Assert typeof shipping_address === 'string' when present.

## Expected result
If shipping_address is returned on GET /api/users/me, typeof must be string. Record if absent — not documented on GET in api_spec.

## Schema contract reference
api_spec PUT example shipping_address string.

## Type
Schema validation

## Audit
- **Status:** INCOMPLETE
- **Reasoning:** shipping_address type is implied by PUT example; GET presence is not guaranteed by api_spec.

## Status / Related bugs
Not Run / None
