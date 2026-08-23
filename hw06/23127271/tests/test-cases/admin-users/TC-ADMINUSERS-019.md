# TC-ADMINUSERS-019: Self-delete still forbidden when body sends a different id

## Requirement ID
FR-19

## Module / Test type / Technique
admin-users / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- EShop backend is running at http://localhost:3000.
- Seed admin admin@eshop.com / Admin123! exists (role=admin).
- Obtain an admin JWT via POST /api/login with email=admin@eshop.com password=Admin123!.
- Create a disposable user (must survive).
- Resolve admin_self_id.

## Test data
| Field | Value |
|-------|-------|
| path id | <admin_self_id> |
| body | {"id": "<disposable_user_id>"} |

## Test steps
1. DELETE /api/admin/users/{admin_self_id} with JSON body claiming a different id.
2. Confirm admin still exists and disposable user still exists (body must not retarget; self path must not succeed).

## Expected result
Path id is the documented identifier. If that id is the caller, the caller still exists (FR-19). A body field id is not specified and must not be used as the resource id. HTTP status is not specified.

## Sub-domains covered
A-REL-02, A-ID-02, A-AUTH-01

## Type
Invalid

## Audit
- **Status:** INCOMPLETE
- **Reasoning:** Path id is the specified resource; FR-19 forbids self-delete. Generated HTTP 403 is not specified.

## Status / Related bugs
Not Run / None
