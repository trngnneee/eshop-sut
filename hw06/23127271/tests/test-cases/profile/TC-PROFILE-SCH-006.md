# TC-PROFILE-SCH-006: role field is string

## Requirement ID
FR-04

## Module / Test type / Technique
profile / Schema validation / Response & request shape

## Schema aspect
Field role type

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.

## Test data
| (see steps) | |

## Test steps
1. GET /api/users/me.
2. Assert typeof role === 'string'.

## Expected result
role is string with value user (FR-04 / SEC-06 immutability context).

## Schema contract reference
FR-04 forbids client role change — role must be readable.

## Type
Schema validation

## Audit
- **Status:** VALID
- **Reasoning:** FR-04 / SEC-06: role is readable and must remain user for the seed account.

## Status / Related bugs
Not Run / None
