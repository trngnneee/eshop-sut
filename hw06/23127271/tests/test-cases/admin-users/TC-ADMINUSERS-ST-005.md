# TC-ADMINUSERS-ST-005: Sequential delete A then B — both terminal

## Requirement ID
FR-19

## Module / Test type / Technique
admin-users / Functional / State Transition Testing

## State machine
UA_EXISTS→DELETED; UB_EXISTS→DELETED

## Transition under test
multi-delete chain

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=admin@eshop.com password=Admin123!
- Register users A and B.

## Test data
| (see steps — multi-step sequence) | |

## Test steps
1. DELETE /api/admin/users/A.
2. DELETE /api/admin/users/B.
3. GET /api/admin/users.

## Expected result
Neither A nor B in GET /api/admin/users. Other seed users unchanged.

## States / transitions covered
UA→DEAD, UB→DEAD

## Type
Legal

## Audit
- **Status:** VALID
- **Reasoning:** Sequential delete of two disposable users — both reach DELETED terminal state.

## Status / Related bugs
Not Run / None
