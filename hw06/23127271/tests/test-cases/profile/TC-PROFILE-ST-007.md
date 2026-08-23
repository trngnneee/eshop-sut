# TC-PROFILE-ST-007: role immutable through profile update chain

## Requirement ID
FR-04 / SEC-06

## Module / Test type / Technique
profile / Functional / State Transition Testing

## State machine
P0(user) → PUT(+role=admin) → P1, role stays user

## Transition under test
immutable role

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!
- P0 role=user.

## Test data
| (see steps — multi-step sequence) | |

## Test steps
1. PUT /api/users/me valid fields plus "role":"admin".
2. GET /api/users/me.

## Expected result
role remains user. Documented profile fields may still update. Success status/body not specified.

## States / transitions covered
P0→P1 (role locked)

## Type
Legal constraint

## Audit
- **Status:** VALID
- **Reasoning:** FR-04 / SEC-06: clients must not change role via profile update. Oracle is spec-aligned.

## Status / Related bugs
Not Run / None
