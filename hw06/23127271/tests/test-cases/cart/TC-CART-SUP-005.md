# TC-CART-SUP-005: Merge after cart already has two different products

## Requirement ID
FR-07

## Module / Test type / Technique
cart / Functional / Domain Testing – Equivalence Partitioning (human extension)

## Preconditions
- EShop backend is running at http://localhost:3000.
- Logged in as test@eshop.com / Test1234!.
- Cart contains two lines: id=1 qty=1 and id=2 qty=1 (POST both if needed).
- GET /api/cart confirms exactly two lines.

## Test data
| Field | Value |
|-------|-------|
| Authorization | Bearer <user_token> |
| id | 1 |
| name | iPhone 15 Pro Max |
| price | 30000000 |
| quantity | 2 |

## Test steps
1. POST /api/cart again for product id=1 with quantity=2.
2. GET /api/cart.

## Expected result
FR-07: two lines remain; id=1 qty=3 (1+2); id=2 qty=1 unchanged.

## Sub-domains covered
C-STATE-02, C-STATE-03 (human: multi-line cart then merge)

## Type
Valid

## Why the AI missed this
Prompt quality / state coverage: Stage 1 had C-STATE-01 empty, C-STATE-02 same-only, C-STATE-03 add-different. It never merged into a cart that **already held another product**, so merge behaviour in a multi-line cart was an untested state combination.

## Audit (human SUP)
- **Status:** VALID
- **Reasoning:** Multi-line cart merge; FR-07 qty arithmetic spec-backed.

## Status / Related bugs
Not Run / None
