# TC-ADMINUSERS-SUP-001: Path id as percent-encoded decimal digits

## Requirement ID
FR-19

## Module / Test type / Technique
admin-users / Functional / Domain Testing – Equivalence Partitioning (human extension)

## Preconditions
- EShop backend is running at http://localhost:3000.
- Logged in as admin@eshop.com / Admin123!.
- Register a disposable user; note `disposable_user_id` (decimal, not the admin’s own id).
- Let `enc` be that id written as ASCII digits then percent-encoded per digit (e.g. id 12 → `%31%32`).

## Test data
| Field | Value |
|-------|-------|
| Authorization | Bearer <admin_token> |
| path | `/api/admin/users/{enc}` |

## Test steps
1. DELETE /api/admin/users/{enc} with the admin JWT (do not send the raw decimal id).
2. GET /api/admin/users.
3. Confirm the caller’s own account still exists.

## Expected result
Percent-encoded path id not specified. If decoded to disposable id (not self), FR-19 allows delete. If not decoded, record status; no other user deleted.

## Sub-domains covered
A-ID-01, A-REL-01 (human: percent-encoded path id)

## Type
Valid / Unspecified

## Why the AI missed this
Model limitation: path-id partitions stayed on decimal literals (`1`, `0`, `-1`, `abc`, `1.5`, `0001`). Percent-encoded digits are a standard HTTP URI partition and do not appear in `api_specification.md`, so the generator never produced them.

## Audit (human SUP)
- **Status:** VALID
- **Reasoning:** Percent-encoded path observe partition; FR-19 delete-if-not-self.

## Status / Related bugs
Not Run / None
