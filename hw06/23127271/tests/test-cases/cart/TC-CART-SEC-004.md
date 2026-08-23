# TC-CART-SEC-004: SQLi-style string id in JSON body

## Requirement ID
FR-07

## Module / Test type / Technique
cart / Security / SEC-mapped probe

## Security requirement(s)
SEC-05

## Threat / probe
SQL injection numeric id as string

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.

## Test data
| Field | Value |
|-------|-------|
| id | 1 OR 1=1 |

## Test steps
1. POST /api/cart with id="1 OR 1=1" (string).
2. GET /api/cart.

## Expected result
SEC-05: request must not cause SQL syntax errors, 500 stack traces with query text, or unauthorized data change. Record status and GET/list side effects. Record coercion behaviour on GET /api/cart; no DB error leak.

## SEC coverage
SEC-05

## Type
Security probe

## Audit
- **Status:** VALID
- **Reasoning:** SEC-05 string id coercion probe. Observing parse/coerce behaviour without mandating reject is correct.

## Status / Related bugs
Not Run / None
