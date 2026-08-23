# TC-PROFILE-ST-005: Profile persists across re-login

## Requirement ID
FR-04

## Module / Test type / Technique
profile / Functional / State Transition Testing

## State machine
P0 → P1 → (new session) → P1

## Transition under test
session boundary

## Preconditions
- EShop at http://localhost:3000.

## Test data
| (see steps — multi-step sequence) | |

## Test steps
1. Login as test@eshop.com. PUT /api/users/me (set V). GET → P1.
2. POST /api/login again (new token). GET /api/users/me.

## Expected result
After re-login with a new token, GET /api/users/me should show P1 if the profile is persisted server-side. If values reset, record actual behaviour — persistence medium is not specified.

## States / transitions covered
P0→P1→P1

## Type
Legal / Unspecified

## Audit
- **Status:** INCOMPLETE
- **Reasoning:** Persistence across re-login is a reasonable probe but the spec does not define storage medium (DB vs session). Generated oracle assumed DB persistence as mandatory.

## Status / Related bugs
Not Run / None
