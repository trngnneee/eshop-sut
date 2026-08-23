# TC-CART-SEC-003: SQLi in cart line name field

## Requirement ID
FR-07

## Module / Test type / Technique
cart / Security / SEC-mapped probe

## Security requirement(s)
SEC-05

## Threat / probe
SQL injection in name

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.

## Test data
| Field | Value |
|-------|-------|
| name | Nguyen' OR '1'='1 |

## Test steps
1. POST /api/cart with SQLi name.
2. GET /api/cart — line stored or rejected; no SQL error leak.

## Expected result
SEC-05: request must not cause SQL syntax errors, 500 stack traces with query text, or unauthorized data change. Record status and GET/list side effects. Cart data must not corrupt or leak SQL errors on GET /api/cart.

## SEC coverage
SEC-05

## Type
Security probe

## Audit
- **Status:** VALID
- **Reasoning:** SEC-05 SQLi in cart line name. Oracle scoped to cart POST/GET side effects.

## Status / Related bugs
Not Run / None
