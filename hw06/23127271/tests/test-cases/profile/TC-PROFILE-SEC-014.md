# TC-PROFILE-SEC-014: Polyglot payload ${7*7} in name

## Requirement ID
FR-04

## Module / Test type / Technique
profile / Security / SEC-mapped probe

## Security requirement(s)
SEC-04

## Threat / probe
Template/polyglot injection in name

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.

## Test data
| Field | Value |
|-------|-------|
| name | ${7*7} {{constructor.constructor('return 1')()}} |

## Test steps
1. PUT with template/polyglot name.
2. GET /api/users/me — value stored literally or rejected.

## Expected result
SEC-04: at API layer record whether payload is stored/returned as literal text without server execution; UI escaping is a manual follow-up. No server-side template evaluation in API JSON.

## SEC coverage
SEC-04

## Type
Security probe

## Audit
- **Status:** VALID
- **Reasoning:** SEC-04 polyglot/template literal probe. Oracle observes no server-side evaluation in JSON API.

## Status / Related bugs
Not Run / None
