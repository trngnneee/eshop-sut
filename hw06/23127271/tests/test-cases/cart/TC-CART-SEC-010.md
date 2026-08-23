# TC-CART-SEC-010: NoSQL-style $gt operator string in name

## Requirement ID
FR-07

## Module / Test type / Technique
cart / Security / SEC-mapped probe

## Security requirement(s)
SEC-05

## Threat / probe
NoSQL-style operator in name

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.

## Test data
| Field | Value |
|-------|-------|
| name | {"$gt":""} |

## Test steps
1. POST with NoSQL-style name string.
2. GET /api/cart.

## Expected result
SEC-05: request must not cause SQL syntax errors, 500 stack traces with query text, or unauthorized data change. Record status and GET/list side effects. Record literal storage vs parse error on GET /api/cart.

## SEC coverage
SEC-05

## Type
Security probe

## Audit
- **Status:** INCOMPLETE
- **Reasoning:** NoSQL-style string probe is valid SEC-05 observe, but oracle assumed SQLite backend which is not in the spec.

## Status / Related bugs
Not Run / None
