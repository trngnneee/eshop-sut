# TC-CART-SEC-007: IDOR — user B cannot read user A cart via GET

## Requirement ID
FR-07

## Module / Test type / Technique
cart / Security / SEC-mapped probe

## Security requirement(s)
SEC-02

## Threat / probe
IDOR — cross-user cart read

## Preconditions
- EShop at http://localhost:3000.
- User A and B exist.

## Test data
| (see steps) | |

## Test steps
1. Login A. POST item to cart. Login B. GET /api/cart as B.
2. Confirm B cart does not show A line.

## Expected result
User B's GET /api/cart must not return User A's cart lines.

## SEC coverage
SEC-02

## Type
Security probe / IDOR

## Audit
- **Status:** VALID
- **Reasoning:** Cross-user cart isolation is implied by per-user JWT-scoped cart. IDOR read probe is valid SEC-02 test.

## Status / Related bugs
Not Run / None
