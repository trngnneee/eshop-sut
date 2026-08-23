# TC-ADMINUSERS-SEC-004: SQLi OR tautology in path :id

## Requirement ID
FR-19

## Module / Test type / Technique
admin-users / Security / SEC-mapped probe

## Security requirement(s)
SEC-05

## Threat / probe
SQL injection in path id

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=admin@eshop.com password=Admin123!.

## Test data
| (see steps) | |

## Test steps
1. DELETE /api/admin/users/1 OR 1=1.
2. GET /api/admin/users — no mass delete of all users.

## Expected result
SEC-05: request must not cause SQL syntax errors, 500 stack traces with query text, or unauthorized data change. Record status and GET/list side effects. Must not delete all users or return SQL error with query text.

## SEC coverage
SEC-05

## Type
Security probe

## Audit
- **Status:** VALID
- **Reasoning:** SEC-05 path SQLi OR tautology. Preventing mass delete via injection is a valid SEC-05 oracle.

## Status / Related bugs
Not Run / None
