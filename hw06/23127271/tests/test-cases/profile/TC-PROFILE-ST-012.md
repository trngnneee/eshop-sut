# TC-PROFILE-ST-012: Empty body PUT — profile state unchanged

## Requirement ID
FR-04

## Module / Test type / Technique
profile / Functional / State Transition Testing

## State machine
P0 → PUT({}) → P0

## Transition under test
no-op / reject

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!
- Snapshot P0.

## Test data
| (see steps — multi-step sequence) | |

## Test steps
1. PUT /api/users/me with empty JSON object {}.
2. GET /api/users/me.

## Expected result
GET matches P0 (no unintended wipe). Request may be rejected; if so, profile state unchanged.

## States / transitions covered
P0→P0

## Type
Unspecified / no-op

## Audit
- **Status:** VALID
- **Reasoning:** Empty JSON body is not documented. Oracle observes state unchanged or rejection without inventing mandatory 400.

## Status / Related bugs
Not Run / None
