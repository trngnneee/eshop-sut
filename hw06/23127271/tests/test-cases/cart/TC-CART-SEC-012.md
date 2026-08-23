# TC-CART-SEC-012: SQLi in Authorization header on POST /api/cart

## Requirement ID
FR-07

## Module / Test type / Technique
cart / Security / SEC-mapped probe

## Security requirement(s)
SEC-05

## Threat / probe
SQLi in Authorization header

## Preconditions
- EShop at http://localhost:3000.

## Test data
| (see steps) | |

## Test steps
1. POST /api/cart with Bearer SQLi token.
2. GET /api/cart with valid token.

## Expected result
SEC-05: request must not cause SQL syntax errors, 500 stack traces with query text, or unauthorized data change. Record status and GET/list side effects. SEC-02: protected endpoint requires a valid JWT; attack must not apply the intended change. HTTP status and error body are not specified — record actual without inventing codes.

## SEC coverage
SEC-05

## Type
Security probe

## Audit
- **Status:** VALID
- **Reasoning:** SEC-05 SQLi + SEC-02 invalid Bearer on POST /api/cart. Combined probe is valid.

## Status / Related bugs
Not Run / None
