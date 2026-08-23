# TC-CART-ST-009: Interleaved POST/GET — state stable between reads

## Requirement ID
FR-07

## Module / Test type / Technique
cart / Functional / State Transition Testing

## State machine
C_EMPTY → POST → GET → POST → GET

## Transition under test
observable consistency

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!
- Empty cart.

## Test data
| (see steps — multi-step sequence) | |

## Test steps
1. POST id=1 qty=1. GET (expect qty=1).
2. POST id=2 qty=1. GET (expect two lines).

## Expected result
Each GET reflects all prior POSTs for this user. No undocumented reset between steps.

## States / transitions covered
C_EMPTY→C_SINGLE→C_TWO

## Type
Legal

## Audit
- **Status:** VALID
- **Reasoning:** Interleaved POST/GET checks observable cart consistency — no invented HTTP codes.

## Status / Related bugs
Not Run / None
