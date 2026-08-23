# TC-PROFILE-ST-004: Idempotent — identical PUT twice leaves stable P1

## Requirement ID
FR-04

## Module / Test type / Technique
profile / Functional / State Transition Testing

## State machine
P0 → P1 → P1 (idempotent)

## Transition under test
P1 → P1

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!

## Test data
| (see steps — multi-step sequence) | |

## Test steps
1. PUT /api/users/me with valid full body (set V).
2. PUT /api/users/me with identical body (set V) again.
3. GET /api/users/me twice.

## Expected result
Both GET calls after identical PUTs show the same profile values (P1). No drift between reads. Success status/body not specified.

## States / transitions covered
P0→P1→P1

## Type
Legal (idempotency)

## Audit
- **Status:** VALID
- **Reasoning:** Idempotent repeat of the same valid PUT is a standard state-transition edge. Oracle checks stable reads only.

## Status / Related bugs
Not Run / None
