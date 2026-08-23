# TC-CART-SUP-002: Merge same product with unequal quantities (2 then +3)

## Requirement ID
FR-07

## Module / Test type / Technique
cart / Functional / Domain Testing – Equivalence Partitioning (human extension)

## Preconditions
- EShop backend is running at http://localhost:3000.
- Logged in as test@eshop.com / Test1234!.
- POST /api/cart with id=1, name=iPhone 15 Pro Max, price=30000000, quantity=2.
- GET /api/cart: one line, id=1, quantity=2.

## Test data
| Field | Value |
|-------|-------|
| Authorization | Bearer <user_token> |
| id | 1 |
| name | iPhone 15 Pro Max |
| price | 30000000 |
| quantity | 3 |

## Test steps
1. POST /api/cart again with the same product id=1 and quantity=3.
2. GET /api/cart.

## Expected result
FR-07: one line id=1 with quantity 5 (2+3). No second row.

## Sub-domains covered
C-STATE-02, C-QTY-02, C-QTY-03 (human: unequal merge operands)

## Type
Valid

## Why the AI missed this
Prompt quality / 1×1 combination: Stage 1 covered merge once (`TC-CART-006`, 1+1=2) and then moved to other variables. The model did not treat “existing qty × added qty” as its own domain, so unequal operands (2+3) never appeared.

## Audit (human SUP)
- **Status:** VALID
- **Reasoning:** Unequal merge operands 2+3; FR-07 merge rule stated without inventing HTTP.

## Status / Related bugs
Not Run / None
