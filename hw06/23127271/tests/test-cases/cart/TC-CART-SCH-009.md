# TC-CART-SCH-009: Two POST same id — array length and qty schema

## Requirement ID
FR-07

## Module / Test type / Technique
cart / Schema validation / Response & request shape

## Schema aspect
Array length after merge

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.
- Empty cart.

## Test data
| (see steps) | |

## Test steps
1. POST id=1 qty=1 twice (merge).
2. GET /api/cart — array length 1; quantity number >=2.

## Expected result
Array has one object element; quantity is number reflecting merge (FR-07). id still number.

## Schema contract reference
FR-07 merge rule + line object shape from POST example.

## Type
Schema validation

## Audit
- **Status:** VALID
- **Reasoning:** FR-07 merge implies one array element; checking length and numeric quantity type is schema-consistent.

## Status / Related bugs
Not Run / None
