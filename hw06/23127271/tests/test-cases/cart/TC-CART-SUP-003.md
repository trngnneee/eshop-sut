# TC-CART-SUP-003: Merge same id when second add has different price

## Requirement ID
FR-07

## Module / Test type / Technique
cart / Functional / Domain Testing – Equivalence Partitioning (human extension)

## Preconditions
- EShop backend is running at http://localhost:3000.
- Logged in as test@eshop.com / Test1234!.
- Cart has one line: id=1, name=iPhone 15 Pro Max, price=30000000, quantity=1.
- GET /api/cart confirms one line.

## Test data
| Field | Value |
|-------|-------|
| Authorization | Bearer <user_token> |
| id | 1 |
| name | iPhone 15 Pro Max |
| price | 1 |
| quantity | 1 |

## Test steps
1. POST /api/cart with the same id=1 and quantity=1 but price=1 (catalogue is 30000000).
2. GET /api/cart.

## Expected result
FR-07 merge: one line for id=1 if id-keyed. Stored price after merge not specified. Fail if second line for id=1.

## Sub-domains covered
C-STATE-02, C-PRICE-07, C-ID-01 (human: merge + price mismatch interaction)

## Type
Unspecified

## Why the AI missed this
Characteristic of the API: Stage 1 tested price mismatch as a **standalone** invalid field (TC-CART-028) and merge with **identical** bodies (TC-CART-006). It never combined “same id merge” with “different client price” as one interaction partition — the cart line is a composite object in memory, not independent fields.

## Audit (human SUP)
- **Status:** VALID
- **Reasoning:** Price mismatch on merge; stored price unspecified — oracle records only.

## Status / Related bugs
Not Run / None
