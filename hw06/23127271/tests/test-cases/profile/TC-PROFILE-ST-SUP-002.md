# TC-PROFILE-ST-SUP-002: Illegal transition — PUT without token after P0 snapshot

## Requirement ID
FR-04 / SEC-02

## Module / Test type / Technique
profile / Functional / State Transition Testing (human extension)

## State machine
P0 → PUT(no auth) → P0

## Transition under test
illegal unauthenticated update

## Preconditions
- EShop at http://localhost:3000.
- Login test@eshop.com.
- GET P0 snapshot.

## Test data
| (see steps) | |

## Test steps
1. PUT /api/users/me with valid body and Bearer token
2. PUT /api/users/me with same body but Authorization header omitted
3. GET with valid token

## Expected result
Second PUT without JWT must not apply a new profile state (SEC-02; API spec section 2 requires token). GET with valid token shows P1 from first PUT only, or P0 if first failed — not a third value. HTTP status is not specified — record actual without inventing codes.

## States / transitions covered
P0→P0

## Type
Illegal

## Why the AI missed this
Model limitation — AI ST cases tested immutables and partial chains but bundled auth failures in domain partition TC-PROFILE-029..032; no dedicated state-transition case that authenticated snapshot P0 must not advance when JWT is removed mid-flow.

## Audit (human SUP)
- **Status:** VALID
- **Reasoning:** Mid-flow auth removal; SEC-02 + spec token requirement.

## Status / Related bugs
Not Run / None
