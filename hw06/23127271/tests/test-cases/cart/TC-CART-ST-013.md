# TC-CART-ST-013: POST add-only — not a specified illegal transition

## Requirement ID
FR-07

## Module / Test type / Technique
cart / Functional / State Transition Testing

## State machine
C_SINGLE(qty=5) → POST cannot reduce

## Transition under test
illegal qty decrease via POST-only

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!
- Cart id=1 qty=5.

## Test data
| (see steps — multi-step sequence) | |

## Test steps
1. POST /api/cart id=1 qty=1 (add-only semantics).
2. GET /api/cart.

## Expected result
POST /api/cart only adds quantity per FR-07 merge semantics. GET qty should not decrease below 5 unless a remove API exists (none in spec). Record resulting qty.

## States / transitions covered
C_SINGLE(5)→C_SINGLE(6)

## Type
Unspecified (monotonic add)

## Audit
- **Status:** INCOMPLETE
- **Reasoning:** Mislabelled as illegal transition. Spec has no cart qty-decrease API; POST only adds/merges. Case is an observe-only monotonic-add probe, not a specified illegal transition.

## Status / Related bugs
Not Run / None
