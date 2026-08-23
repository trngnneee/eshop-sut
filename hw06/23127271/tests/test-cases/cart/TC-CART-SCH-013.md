# TC-CART-SCH-013: quantity sent as string — observe stored type

## Requirement ID
FR-07

## Module / Test type / Technique
cart / Schema validation / Response & request shape

## Schema aspect
quantity string type

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.

## Test data
| (see steps) | |

## Test steps
1. POST {"id":1,"name":"A","price":100000,"quantity":"2"}.
2. GET — record typeof quantity.

## Expected result
Spec types quantity as number. Record coercion behaviour. HTTP status is not specified in api_specification.md — record actual without inventing codes.

## Schema contract reference
Type deviation on documented quantity field.

## Type
Schema validation

## Audit
- **Status:** VALID
- **Reasoning:** Spec types quantity as number; observe coercion behaviour.

## Status / Related bugs
Not Run / None
