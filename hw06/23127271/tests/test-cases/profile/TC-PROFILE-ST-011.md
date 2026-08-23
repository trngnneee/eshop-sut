# TC-PROFILE-ST-011: User A update does not change User B profile (isolation)

## Requirement ID
FR-04

## Module / Test type / Technique
profile / Functional / State Transition Testing

## State machine
PA0→PA1 while PB0 unchanged

## Transition under test
cross-user isolation

## Preconditions
- EShop at http://localhost:3000.
- Users test@eshop.com and admin@eshop.com exist.
- Snapshot PB0 for admin via admin login GET /api/users/me.

## Test data
| (see steps — multi-step sequence) | |

## Test steps
1. Login test@eshop.com. PUT /api/users/me (set V user). GET → PA1.
2. Login admin@eshop.com. GET /api/users/me → PB1.

## Expected result
User A PUT updates A's profile only. Admin GET /api/users/me unchanged from PB0. email/role unchanged on both accounts.

## States / transitions covered
PA0→PA1, PB0→PB0

## Type
Legal (isolation)

## Audit
- **Status:** VALID
- **Reasoning:** FR-04: user may update only their own profile. Cross-user isolation is spec-backed.

## Status / Related bugs
Not Run / None
