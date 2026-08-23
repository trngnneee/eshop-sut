# TC-CART-SUP-001: Second add, same product id, different name (merge identity)

## Requirement ID
FR-07

## Module / Test type / Technique
cart / Functional / Domain Testing – Equivalence Partitioning (human extension)

## Preconditions
- EShop backend is running at http://localhost:3000.
- Logged in as test@eshop.com / Test1234!.
- Cart has exactly one line: id=1, name=iPhone 15 Pro Max, quantity=1 (POST once if needed). GET /api/cart to confirm.

## Test data
| Field | Value |
|-------|-------|
| Authorization | Bearer <user_token> |
| id | 1 |
| name | Completely Different Label |
| price | 30000000 |
| quantity | 1 |

## Test steps
1. POST /api/cart with id=1 and a name that does not match the catalogue / existing line.
2. GET /api/cart.

## Expected result
FR-07 same-product merge does not define identity key (id vs name). Record: one line qty=2 if id-keyed, or two lines if name-keyed. Fail only on crash or lost qty.

## Sub-domains covered
C-STATE-02, C-NAME-04, C-ID-01 (human: merge key)

## Type
Unspecified

## Why the AI missed this
Characteristic of the API: FR-07’s “cùng một sản phẩm” never defines the identity key, while the example body always repeats matching `id`+`name`. Stage 1 tested name-mismatch as a standalone invalid field (assumed catalogue match) and merge only with identical bodies, so the interaction was never a partition of its own.

## Audit (human SUP)
- **Status:** VALID
- **Reasoning:** Merge identity key ambiguity is real FR-07 gap; observe-only oracle.

## Status / Related bugs
Not Run / None
