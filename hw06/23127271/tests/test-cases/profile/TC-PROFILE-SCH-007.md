# TC-PROFILE-SCH-007: GET profile must not expose password

## Requirement ID
FR-04 / SEC-01

## Module / Test type / Technique
profile / Schema validation / Response & request shape

## Schema aspect
Forbidden field password

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.

## Test data
| (see steps) | |

## Test steps
1. GET /api/users/me.
2. Assert no password or password_hash key in JSON object.

## Expected result
Response object must not contain password or password_hash (SEC-01). Other fields may exist — record keys.

## Schema contract reference
SEC-01 README; api_spec does not document password on profile GET.

## Type
Schema validation

## Audit
- **Status:** VALID
- **Reasoning:** SEC-01: password and password_hash must not appear in API responses.

## Status / Related bugs
Not Run / None
