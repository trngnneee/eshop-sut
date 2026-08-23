# TC-ADMINUSERS-SEC-005: SQLi stacked DELETE in path :id

## Requirement ID
FR-19

## Module / Test type / Technique
admin-users / Security / SEC-mapped probe

## Security requirement(s)
SEC-05

## Threat / probe
SQL injection stacked in path

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=admin@eshop.com password=Admin123!.

## Test data
| (see steps) | |

## Test steps
1. DELETE /api/admin/users/1; DELETE FROM users WHERE '1'='1.
2. GET /api/admin/users.

## Expected result
SEC-05: request must not cause SQL syntax errors, 500 stack traces with query text, or unauthorized data change. Record status and GET/list side effects. Seed users admin and test still exist unless path parsed as single id safely.

## SEC coverage
SEC-05

## Type
Security probe

## Audit
- **Status:** VALID
- **Reasoning:** SEC-05 stacked DELETE in path id. Oracle observes parameterized parsing.

## Status / Related bugs
Not Run / None
