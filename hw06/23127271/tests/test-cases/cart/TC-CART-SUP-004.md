# TC-CART-SUP-004: Minimal body — id and quantity only (name and price omitted)

## Requirement ID
FR-07

## Module / Test type / Technique
cart / Functional / Domain Testing – Equivalence Partitioning (human extension)

## Preconditions
- EShop backend is running at http://localhost:3000.
- Logged in as test@eshop.com / Test1234!.
- GET /api/cart and snapshot (prefer empty cart).
- Seed product id=1 exists.

## Test data
| Field | Value |
|-------|-------|
| Authorization | Bearer <user_token> |
| id | 1 |
| quantity | 1 |
| name | (omitted) |
| price | (omitted) |

## Test steps
1. POST /api/cart with body `{"id":1,"quantity":1}` only.
2. GET /api/cart.

## Expected result
Minimal body id+quantity only. name/price not required per spec — record line shape; do not expect reject solely for omission.

## Sub-domains covered
C-ID-01, C-QTY-01, C-NAME-03, C-PRICE-04 (human: minimal partial body)

## Type
Valid / Unspecified

## Why the AI missed this
Prompt quality: parallel to profile omit-field audit — Stage 1 treated the four-field cart example as atomic and generated omit-id / omit-price only as **reject** cases. After Stage 2 marked those as unspecified, no **positive minimal-body** representative was added for the cart API.

## Audit (human SUP)
- **Status:** VALID
- **Reasoning:** Minimal body positive case after Stage 2; no mandatory reject for omitted name/price.

## Status / Related bugs
Not Run / None
