# TC-CART-SEC-002: POST /api/cart with malformed JWT

## Requirement ID
FR-07

## Module / Test type / Technique
cart / Security / SEC-mapped probe

## Security requirement(s)
SEC-02

## Threat / probe
Auth bypass — malformed JWT

## Preconditions
- EShop at http://localhost:3000.

## Test data
| (see steps) | |

## Test steps
1. POST /api/cart with Bearer not-a-jwt.
2. GET /api/cart with valid user token.

## Expected result
SEC-02: protected endpoint requires a valid JWT; attack must not apply the intended change. HTTP status and error body are not specified — record actual without inventing codes.

## SEC coverage
SEC-02

## Type
Security probe

## Audit
- **Status:** VALID
- **Reasoning:** SEC-02 malformed JWT on POST /api/cart. Oracle is spec-aligned.

## Status / Related bugs
Not Run / None
