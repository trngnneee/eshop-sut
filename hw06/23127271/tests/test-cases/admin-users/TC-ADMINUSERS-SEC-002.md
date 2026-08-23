# TC-ADMINUSERS-SEC-002: User JWT on admin DELETE

## Requirement ID
FR-19

## Module / Test type / Technique
admin-users / Security / SEC-mapped probe

## Security requirement(s)
SEC-03

## Threat / probe
Role escalation — user JWT

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.
- Disposable D exists.

## Test data
| (see steps) | |

## Test steps
1. DELETE /api/admin/users/D with user token.
2. GET /api/admin/users as admin.

## Expected result
SEC-03 / FR-12: user JWT must not delete target. D still exists in GET /api/admin/users. HTTP status and error body are not specified — record actual without inventing codes.

## SEC coverage
SEC-03

## Type
Security probe

## Audit
- **Status:** VALID
- **Reasoning:** SEC-03 / FR-12: admin DELETE requires role=admin, not merely a valid JWT.

## Status / Related bugs
Not Run / None
