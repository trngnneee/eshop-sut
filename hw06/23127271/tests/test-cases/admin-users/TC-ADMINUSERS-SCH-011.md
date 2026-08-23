# TC-ADMINUSERS-SCH-011: Seed users appear as valid objects in list

## Requirement ID
FR-19

## Module / Test type / Technique
admin-users / Schema validation / Response & request shape

## Schema aspect
Non-empty list schema

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=admin@eshop.com password=Admin123!.

## Test data
| (see steps) | |

## Test steps
1. GET /api/admin/users.
2. Find email admin@eshop.com and test@eshop.com entries — schema check each.

## Expected result
List length >= 2. Seed users are objects with string email and string role.

## Schema contract reference
SUT seed data; validates list schema on real records.

## Type
Schema validation

## Audit
- **Status:** VALID
- **Reasoning:** Smoke schema check on seed data validates real list elements without inventing HTTP codes.

## Status / Related bugs
Not Run / None
