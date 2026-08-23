# TC-PROFILE-SCH-005: email field present as string

## Requirement ID
FR-04

## Module / Test type / Technique
profile / Schema validation / Response & request shape

## Schema aspect
Field email type

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.
- email=test@eshop.com.

## Test data
| (see steps) | |

## Test steps
1. GET /api/users/me.
2. Assert email key exists and typeof string.

## Expected result
email is string equal to test@eshop.com (FR-04: email immutable).

## Schema contract reference
FR-04: email must not change — implies email exposed on profile read.

## Type
Schema validation

## Audit
- **Status:** VALID
- **Reasoning:** FR-04: email is readable on profile and must match the logged-in account.

## Status / Related bugs
Not Run / None
