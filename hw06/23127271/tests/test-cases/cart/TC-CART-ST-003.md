# TC-CART-ST-003: SINGLE → TWO_LINES — different product adds new row

## Requirement ID
FR-07

## Module / Test type / Technique
cart / Functional / State Transition Testing

## State machine
C_SINGLE → C_MULTI(2)

## Transition under test
C_SINGLE → C_TWO

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!
- Cart has id=1 qty=1.

## Test data
| (see steps — multi-step sequence) | |

## Test steps
1. POST /api/cart id=2 qty=1.
2. GET /api/cart.

## Expected result
GET shows two lines: id=1 qty=1 unchanged, id=2 qty=1 added (C_TWO). Success status/body not specified.

## States / transitions covered
C_SINGLE→C_TWO

## Type
Legal

## Audit
- **Status:** VALID
- **Reasoning:** FR-07 merge applies to the same product; a different id is a separate line.

## Status / Related bugs
Not Run / None
