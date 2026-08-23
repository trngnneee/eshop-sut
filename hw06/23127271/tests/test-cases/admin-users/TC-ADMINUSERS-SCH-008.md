# TC-ADMINUSERS-SCH-008: List items must not contain password_hash

## Requirement ID
FR-19 / SEC-01

## Module / Test type / Technique
admin-users / Schema validation / Response & request shape

## Schema aspect
Forbidden password_hash field

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=admin@eshop.com password=Admin123!.

## Test data
| (see steps) | |

## Test steps
1. GET /api/admin/users.
2. Assert password_hash absent on all elements.

## Expected result
No password_hash key on any list element.

## Schema contract reference
SEC-01 no plaintext — hash also must not leak in API list.

## Type
Schema validation

## Audit
- **Status:** VALID
- **Reasoning:** SEC-01 extension: password_hash must not appear in list responses.

## Status / Related bugs
Not Run / None
