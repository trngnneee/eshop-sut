# TC-ADMINUSERS-ST-004: List count N → delete one → N−1

## Requirement ID
FR-19

## Module / Test type / Technique
admin-users / Functional / State Transition Testing

## State machine
LIST(N) → LIST(N-1)

## Transition under test
list state

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=admin@eshop.com password=Admin123!
- Count users N before delete.

## Test data
| (see steps — multi-step sequence) | |

## Test steps
1. GET /api/admin/users → count N.
2. DELETE disposable user D.
3. GET /api/admin/users → count N-1.

## Expected result
GET count drops by exactly one; only target D removed.

## States / transitions covered
LIST(N)→LIST(N-1)

## Type
Legal

## Audit
- **Status:** VALID
- **Reasoning:** List cardinality N to N-1 follows from a successful FR-19 delete of one other user.

## Status / Related bugs
Not Run / None
