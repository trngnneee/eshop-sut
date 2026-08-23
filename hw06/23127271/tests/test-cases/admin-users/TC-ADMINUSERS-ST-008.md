# TC-ADMINUSERS-ST-008: Register → EXISTS → delete — full lifecycle

## Requirement ID
FR-19

## Module / Test type / Technique
admin-users / Functional / State Transition Testing

## State machine
REGISTER → U_EXISTS → U_DELETED

## Transition under test
lifecycle

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=admin@eshop.com password=Admin123!

## Test data
| (see steps — multi-step sequence) | |

## Test steps
1. POST /api/register new user → id R.
2. GET /api/admin/users includes R.
3. DELETE /api/admin/users/R.
4. GET /api/admin/users excludes R.

## Expected result
R appears in list after register, absent after DELETE. Password never in list responses.

## States / transitions covered
REGISTER→EXISTS→DELETED

## Type
Legal

## Audit
- **Status:** VALID
- **Reasoning:** Register to EXISTS to DELETED lifecycle under FR-19.

## Status / Related bugs
Not Run / None
