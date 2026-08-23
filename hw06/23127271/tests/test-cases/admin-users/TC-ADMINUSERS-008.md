# TC-ADMINUSERS-008: Empty path — routing not specified

## Requirement ID
FR-19

## Module / Test type / Technique
admin-users / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- EShop backend is running at http://localhost:3000.
- Seed admin admin@eshop.com / Admin123! exists (role=admin).
- Obtain an admin JWT via POST /api/login with email=admin@eshop.com password=Admin123!.

## Test data
| Field | Value |
|-------|-------|
| id | (empty) |

## Test steps
1. DELETE /api/admin/users/ (trailing slash, no id) with admin JWT.

## Expected result
Empty path is not specified for this operation. Do not expect a particular status. User list must not lose an arbitrary user as a side effect of this call.

## Sub-domains covered
A-ID-08, A-AUTH-01

## Type
Unspecified

## Audit
- **Status:** INCOMPLETE
- **Reasoning:** DELETE /api/admin/users/ may be a different route than /:id. Generated 'not a successful delete' assumed routing. No id-empty rule is written.

## Status / Related bugs
Not Run / None
