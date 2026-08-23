# TC-CART-SEC-011: IDOR attempt — user_id path not in API; body user_id swap

## Requirement ID
FR-07

## Module / Test type / Technique
cart / Security / SEC-mapped probe

## Security requirement(s)
SEC-02

## Threat / probe
IDOR — POST to another user cart

## Preconditions
- EShop at http://localhost:3000.
- Register user C.
- Login test user.

## Test data
| (see steps) | |

## Test steps
1. POST with user_id set to C's id.
2. Login as C. GET /api/cart.

## Expected result
Line must not appear in user C's cart unless server ignores user_id (record as finding if it does).

## SEC coverage
SEC-02

## Type
Security probe / IDOR

## Audit
- **Status:** VALID
- **Reasoning:** IDOR-style POST with foreign user_id in body. Oracle correctly records cross-user cart binding.

## Status / Related bugs
Not Run / None
