# TC-ADMINUSERS-SEC-003: FR-19 — admin cannot delete self via DELETE

## Requirement ID
FR-19

## Module / Test type / Technique
admin-users / Security / SEC-mapped probe

## Security requirement(s)
SEC-03

## Threat / probe
Admin self-delete bypass FR-19

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=admin@eshop.com password=Admin123!.
- admin_self_id from GET.

## Test data
| (see steps) | |

## Test steps
1. DELETE /api/admin/users/{admin_self_id}.
2. GET /api/admin/users — admin account still present.

## Expected result
FR-19: logged-in admin must not be deleted. GET /api/admin/users shows admin account still present. HTTP status and error body are not specified — record actual without inventing codes.

## SEC coverage
SEC-03

## Type
FR-19 constraint

## Audit
- **Status:** INCOMPLETE
- **Reasoning:** Self-delete rule is FR-19, not SEC-03 (caller already has admin role). Mis-tagged SEC requirement.

## Status / Related bugs
Not Run / None
