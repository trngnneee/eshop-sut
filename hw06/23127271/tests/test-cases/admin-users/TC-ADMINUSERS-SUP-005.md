# TC-ADMINUSERS-SUP-005: Double percent-encoding of path id digits

## Requirement ID
FR-19

## Module / Test type / Technique
admin-users / Functional / Domain Testing – Equivalence Partitioning (human extension)

## Preconditions
- EShop backend is running at http://localhost:3000.
- Logged in as admin@eshop.com / Admin123!.
- Register a disposable user; note decimal `disposable_user_id` (e.g. 12).
- Build **double-encoded** path: encode `%31%32` again so `%` becomes `%25` (e.g. `%2531%2532` for id 12).

## Test data
| Field | Value |
|-------|-------|
| Authorization | Bearer <admin_token> |
| path | `/api/admin/users/%2531%2532` (example when id=12) |

## Test steps
1. DELETE the double-encoded path with admin JWT (not the single-encoded or raw decimal path).
2. GET /api/admin/users.
3. Confirm admin still exists.

## Expected result
Double-encoding decode depth not specified. Record outcome; FR-19: admin must not delete self.

## Sub-domains covered
A-ID-01 (human: double percent-encoding)

## Type
Unspecified

## Why the AI missed this
Characteristic of HTTP APIs + model limitation: SUP-001 added single percent-encoding. Decoding depth (once vs twice) is a real server behaviour edge; the spec only names `:id`, not encoding layers. Models rarely chain encoding variants without a human tester thinking about proxy/gateway paths.

## Audit (human SUP)
- **Status:** VALID
- **Reasoning:** Double-encoding depth observe; FR-19 self-delete guard retained.

## Status / Related bugs
Not Run / None
