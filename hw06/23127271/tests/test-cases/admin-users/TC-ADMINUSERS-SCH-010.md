# TC-ADMINUSERS-SCH-010: DELETE response message field type if present

## Requirement ID
FR-19

## Module / Test type / Technique
admin-users / Schema validation / Response & request shape

## Schema aspect
DELETE message field

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=admin@eshop.com password=Admin123!.
- Disposable D.

## Test data
| (see steps) | |

## Test steps
1. DELETE D.
2. If message key exists, assert typeof message === 'string'.

## Expected result
If response includes message, it is string. If absent, record — not required by written spec.

## Schema contract reference
Observe-only; compare with register success {message,id} pattern.

## Type
Schema validation

## Audit
- **Status:** VALID
- **Reasoning:** message field on DELETE is optional and observe-only when present.

## Status / Related bugs
Not Run / None
