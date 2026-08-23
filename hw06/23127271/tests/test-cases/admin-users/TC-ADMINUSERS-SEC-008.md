# TC-ADMINUSERS-SEC-008: SQLi in unexpected DELETE JSON body

## Requirement ID
FR-19

## Module / Test type / Technique
admin-users / Security / SEC-mapped probe

## Security requirement(s)
SEC-05

## Threat / probe
SQLi in JSON DELETE body

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=admin@eshop.com password=Admin123!.
- Disposable D.

## Test data
| (see steps) | |

## Test steps
1. DELETE /api/admin/users/D with body {"id":"' OR 1=1--"}.
2. GET /api/admin/users.

## Expected result
SEC-05: request must not cause SQL syntax errors, 500 stack traces with query text, or unauthorized data change. Record status and GET/list side effects. Path id D is authoritative; body must not widen delete scope.

## SEC coverage
SEC-05

## Type
Security probe

## Audit
- **Status:** VALID
- **Reasoning:** DELETE body is undocumented; probing unexpected JSON is a valid SEC-05 observe test. Path id authoritative oracle is reasonable.

## Status / Related bugs
Not Run / None
