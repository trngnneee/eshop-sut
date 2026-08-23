# TC-PROFILE-ST-SUP-004: Illegal — malformed JWT PUT after valid P1 established

## Requirement ID
FR-04 / SEC-02

## Module / Test type / Technique
profile / Functional / State Transition Testing (human extension)

## State machine
P0 → P1(valid) → PUT(malformed JWT) → P1

## Transition under test
illegal mid-flow auth

## Preconditions
- EShop at http://localhost:3000.
- Login test@eshop.com.
- PUT valid body → GET confirms P1.

## Test data
| (see steps) | |

## Test steps
1. PUT /api/users/me valid body with valid token → P1
2. PUT /api/users/me different valid body with Authorization: Bearer not-a-jwt
3. GET /api/users/me with original valid token

## Expected result
Second PUT with malformed JWT must not change profile state (SEC-02). GET with valid token still shows P1 from first PUT, not the second body. HTTP status is not specified — record actual without inventing codes.

## States / transitions covered
P1→P1

## Type
Illegal

## Why the AI missed this
Model limitation — domain TC-PROFILE-031 tests malformed JWT as a one-shot off-point; no state-transition case guards that P1 already reached must not advance when a later PUT uses Bearer not-a-jwt.

## Audit (human SUP)
- **Status:** VALID
- **Reasoning:** Malformed JWT after P1; SEC-02 mid-flow guard.

## Status / Related bugs
Not Run / None
