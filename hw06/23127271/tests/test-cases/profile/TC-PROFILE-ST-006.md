# TC-PROFILE-ST-006: email immutable through profile update transition

## Requirement ID
FR-04

## Module / Test type / Technique
profile / Functional / State Transition Testing

## State machine
P0 → PUT(with email) → P1, email stays P0.email

## Transition under test
immutable email

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!
- P0 email=test@eshop.com.

## Test data
| (see steps — multi-step sequence) | |

## Test steps
1. PUT /api/users/me with valid fields plus "email":"attacker@evil.com".
2. GET /api/users/me.

## Expected result
email remains test@eshop.com. Other fields may update. Request rejected or email ignored — either way email unchanged.

## States / transitions covered
P0→P1 (email locked)

## Type
Legal constraint

## Audit
- **Status:** VALID
- **Reasoning:** FR-04: email must not be changed. Oracle allows reject-or-ignore and requires email unchanged.

## Status / Related bugs
Not Run / None
