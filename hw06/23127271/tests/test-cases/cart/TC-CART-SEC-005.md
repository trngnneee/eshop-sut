# TC-CART-SEC-005: XSS payload in cart item name

## Requirement ID
FR-07

## Module / Test type / Technique
cart / Security / SEC-mapped probe

## Security requirement(s)
SEC-04

## Threat / probe
Stored XSS in cart name

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.

## Test data
| (see steps) | |

## Test steps
1. POST with XSS name.
2. GET /api/cart — literal in JSON.

## Expected result
SEC-04: at API layer record whether payload is stored/returned as literal text without server execution; UI escaping is a manual follow-up.

## SEC coverage
SEC-04

## Type
Security probe

## Audit
- **Status:** VALID
- **Reasoning:** SEC-04 XSS in cart name. API literal-storage oracle matches SEC-04 scope.

## Status / Related bugs
Not Run / None
