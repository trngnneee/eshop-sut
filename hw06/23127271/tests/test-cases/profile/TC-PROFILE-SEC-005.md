# TC-PROFILE-SEC-005: Stored XSS script tag in name (API literal storage)

## Requirement ID
FR-04

## Module / Test type / Technique
profile / Security / SEC-mapped probe

## Security requirement(s)
SEC-04

## Threat / probe
Stored XSS script in name

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.

## Test data
| Field | Value |
|-------|-------|
| name | <script>alert("SEC04")</script> |

## Test steps
1. PUT /api/users/me with script payload in name.
2. GET /api/users/me — inspect JSON literal.

## Expected result
SEC-04: at API layer record whether payload is stored/returned as literal text without server execution; UI escaping is a manual follow-up. role and email unchanged.

## SEC coverage
SEC-04

## Type
Security probe

## Audit
- **Status:** VALID
- **Reasoning:** SEC-04 stored XSS probe on name. API-layer literal storage oracle matches SEC-04 testing scope.

## Status / Related bugs
Not Run / None
