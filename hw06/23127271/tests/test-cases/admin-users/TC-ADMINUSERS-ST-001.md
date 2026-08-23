# TC-ADMINUSERS-ST-001: U_EXISTS → U_DELETED — other user removed from list

## Requirement ID
FR-19

## Module / Test type / Technique
admin-users / Functional / State Transition Testing

## State machine
U_EXISTS → U_DELETED

## Transition under test
U_EXISTS → U_DELETED

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=admin@eshop.com password=Admin123!
- Register disposable user → id D.

## Test data
| (see steps — multi-step sequence) | |

## Test steps
1. GET /api/admin/users → includes D.
2. DELETE /api/admin/users/D.
3. GET /api/admin/users.

## Expected result
D absent from GET /api/admin/users; admin caller remains. Password never in responses. FR-19: admin may delete users other than self. Password must not appear in list responses. Success DELETE status/body is not specified.

## States / transitions covered
U_EXISTS→U_DELETED

## Type
Legal

## Audit
- **Status:** VALID
- **Reasoning:** FR-19 legal EXISTS to DELETED for a non-self user.

## Status / Related bugs
Not Run / None
