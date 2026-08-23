# TC-PROFILE-ST-003: Second full PUT overwrites first update

## Requirement ID
FR-04

## Module / Test type / Technique
profile / Functional / State Transition Testing

## State machine
P0 → P1 → P2 (full overwrite)

## Transition under test
P1 → P2

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!
- P0 snapshot taken.

## Test data
| (see steps — multi-step sequence) | |

## Test steps
1. PUT /api/users/me set A (name A, phone A, address A). GET → P1.
2. PUT /api/users/me set B (name B, phone B, address B).
3. GET /api/users/me.

## Expected result
After the second full PUT (set B), GET /api/users/me shows set B name, phone, and shipping_address (P2). email/role unchanged. Success status/body not specified.

## States / transitions covered
P0→P1→P2

## Type
Legal

## Audit
- **Status:** VALID
- **Reasoning:** Two full PUTs with documented three-field bodies test profile snapshot overwrite. FR-04 lists all three as updatable; expecting GET to reflect the latest submitted triple is spec-aligned.

## Status / Related bugs
Not Run / None
