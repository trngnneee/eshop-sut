# TC-ADMINUSERS-010: Delete another admin — only self-delete is specified

## Requirement ID
FR-19

## Module / Test type / Technique
admin-users / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- EShop backend is running at http://localhost:3000.
- Seed admin admin@eshop.com / Admin123! exists (role=admin).
- Obtain an admin JWT via POST /api/login with email=admin@eshop.com password=Admin123!.
- ⚠️ Spec forbids only self-delete; deleting another admin is not forbidden in text.
- Create a second admin if the SUT allows it; otherwise skip and mark Blocked with reason.

## Test data
| Field | Value |
|-------|-------|
| id | <other_admin_id> |

## Test steps
1. DELETE /api/admin/users/{other_admin_id} as the seed admin (ids differ).
2. GET /api/admin/users.

## Expected result
Spec forbids only deleting the currently logged-in account. Outcome for another admin is not specified. Do not expect success or failure. Blocked if a second admin cannot be created.

## Sub-domains covered
A-ID-10, A-REL-01, A-AUTH-01

## Type
Unspecified

## Audit
- **Status:** INCOMPLETE
- **Reasoning:** FR-19 forbids only self-delete. Expecting 200 for deleting another admin invents a success rule; expecting reject would also invent a rule.

## Status / Related bugs
Not Run / None
