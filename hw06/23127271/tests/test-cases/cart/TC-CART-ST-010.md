# TC-CART-ST-010: User A cart isolated from User B

## Requirement ID
FR-07

## Module / Test type / Technique
cart / Functional / State Transition Testing

## State machine
CA evolves; CB unchanged

## Transition under test
cross-user isolation

## Preconditions
- EShop at http://localhost:3000.
- test@eshop.com and admin@eshop.com exist.

## Test data
| (see steps — multi-step sequence) | |

## Test steps
1. Login test@eshop.com. POST id=1. GET → CA1.
2. Login admin@eshop.com. GET /api/cart → CB.

## Expected result
Admin GET /api/cart does not contain user A's line. User A cart has the posted line.

## States / transitions covered
CA: C_EMPTY→C_SINGLE; CB: unchanged

## Type
Legal (isolation)

## Audit
- **Status:** VALID
- **Reasoning:** Cart is scoped to the authenticated user (JWT). Another user's cart must not show the line.

## Status / Related bugs
Not Run / None
