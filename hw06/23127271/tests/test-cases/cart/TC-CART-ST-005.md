# TC-CART-ST-005: TWO_LINES → THREE_LINES — third distinct product

## Requirement ID
FR-07

## Module / Test type / Technique
cart / Functional / State Transition Testing

## State machine
C_TWO → C_THREE

## Transition under test
C_TWO → C_THREE

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!
- Cart: id=1 and id=2 each qty=1.

## Test data
| (see steps — multi-step sequence) | |

## Test steps
1. POST /api/cart id=3 qty=1 (seed product 3).
2. GET /api/cart.

## Expected result
GET shows three distinct lines; prior lines unchanged except new id=3 line. Success status/body not specified.

## States / transitions covered
C_TWO→C_THREE

## Type
Legal

## Audit
- **Status:** VALID
- **Reasoning:** Adding a third distinct product extends MULTI state by one line.

## Status / Related bugs
Not Run / None
