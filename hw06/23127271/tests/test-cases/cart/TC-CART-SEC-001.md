# TC-CART-SEC-001: POST /api/cart without Authorization

## Requirement ID
FR-07

## Module / Test type / Technique
cart / Security / SEC-mapped probe

## Security requirement(s)
SEC-02

## Threat / probe
Auth bypass — no JWT

## Preconditions
- EShop at http://localhost:3000.

## Test data
| (see steps) | |

## Test steps
1. POST /api/cart valid body, no Authorization.
2. GET /api/cart as test user — cart unchanged.

## Expected result
SEC-02: protected endpoint requires a valid JWT; attack must not apply the intended change. HTTP status and error body are not specified — record actual without inventing codes. GET /api/cart as authenticated user shows cart unchanged (no new line).

## SEC coverage
SEC-02

## Type
Security probe

## Audit
- **Status:** VALID
- **Reasoning:** SEC-02: cart APIs require JWT (api_spec section 4). Expect no line added when unauthenticated.

## Status / Related bugs
Not Run / None
