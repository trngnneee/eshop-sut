# TC-ADMINUSERS-SUP-004: Path id mixed alphanumeric (12abc)

## Requirement ID
FR-19

## Module / Test type / Technique
admin-users / Functional / Domain Testing – Equivalence Partitioning (human extension)

## Preconditions
- EShop backend is running at http://localhost:3000.
- Logged in as admin@eshop.com / Admin123!.
- Snapshot GET /api/admin/users (count and ids).

## Test data
| Field | Value |
|-------|-------|
| Authorization | Bearer <admin_token> |
| id | 12abc |

## Test steps
1. DELETE /api/admin/users/12abc with admin JWT.
2. GET /api/admin/users — same users as before (especially id=1 admin and id=2 test user if present).
3. GET /api/users/me as admin still succeeds.

## Expected result
Mixed alphanumeric path not specified. No unintended user deleted; admin still exists.

## Sub-domains covered
A-ID-06 (human: alphanumeric path, distinct from pure letters)

## Type
Unspecified

## Why the AI missed this
Model limitation: non-numeric path partitions were either pure letters (`abc`) or floats (`1.5`). Mixed digit-letter strings (`12abc`) are a separate URI/path parsing class that the generator collapsed into “non-numeric” without a dedicated representative.

## Audit (human SUP)
- **Status:** VALID
- **Reasoning:** Mixed alphanumeric path partition; no invented 404.

## Status / Related bugs
Not Run / None
