# TC-ADMINUSERS-SCH-007: List items must not contain password

## Requirement ID
FR-19 / SEC-01

## Module / Test type / Technique
admin-users / Schema validation / Response & request shape

## Schema aspect
Forbidden password field

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=admin@eshop.com password=Admin123!.

## Test data
| (see steps) | |

## Test steps
1. GET /api/admin/users.
2. For each object assert password key absent.

## Expected result
No password key on any list element (FR-19 / SEC-01).

## Schema contract reference
FR-19: list must not expose password.

## Type
Schema validation

## Audit
- **Status:** VALID
- **Reasoning:** FR-19 / SEC-01: admin list must not expose password.

## Status / Related bugs
Not Run / None
