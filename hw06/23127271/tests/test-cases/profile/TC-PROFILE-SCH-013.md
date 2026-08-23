# TC-PROFILE-SCH-013: id field type if present on GET profile

## Requirement ID
FR-04

## Module / Test type / Technique
profile / Schema validation / Response & request shape

## Schema aspect
Numeric id field

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.

## Test data
| (see steps) | |

## Test steps
1. GET /api/users/me.
2. If id key exists, assert typeof id === 'number' (integer).

## Expected result
If id is returned, it must be JSON number (not string). If absent, record — not documented in api_spec GET.

## Schema contract reference
Login/register responses reference numeric id; profile GET schema silent.

## Type
Schema validation

## Audit
- **Status:** VALID
- **Reasoning:** id type probe is observe-only when field is not documented on GET profile.

## Status / Related bugs
Not Run / None
