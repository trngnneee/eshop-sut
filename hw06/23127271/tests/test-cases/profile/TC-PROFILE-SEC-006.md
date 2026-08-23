# TC-PROFILE-SEC-006: Stored XSS img onerror in shipping_address

## Requirement ID
FR-04

## Module / Test type / Technique
profile / Security / SEC-mapped probe

## Security requirement(s)
SEC-04

## Threat / probe
Stored XSS event handler in address

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.

## Test data
| Field | Value |
|-------|-------|
| shipping_address | "><img src=x onerror=alert(1)> |

## Test steps
1. PUT /api/users/me with XSS address payload.
2. GET /api/users/me.

## Expected result
SEC-04: at API layer record whether payload is stored/returned as literal text without server execution; UI escaping is a manual follow-up.

## SEC coverage
SEC-04

## Type
Security probe

## Audit
- **Status:** VALID
- **Reasoning:** SEC-04 XSS event handler in shipping_address. Oracle is spec-aligned for API storage observe.

## Status / Related bugs
Not Run / None
