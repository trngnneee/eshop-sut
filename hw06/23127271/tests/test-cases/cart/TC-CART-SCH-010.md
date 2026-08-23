# TC-CART-SCH-010: price sent as string — observe stored type

## Requirement ID
FR-07

## Module / Test type / Technique
cart / Schema validation / Response & request shape

## Schema aspect
Request price string type

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.

## Test data
| (see steps) | |

## Test steps
1. POST {"id":1,"name":"A","price":"100000","quantity":1}.
2. GET /api/cart — record typeof price.

## Expected result
Spec types price as number. Record coercion to number vs string storage. HTTP status is not specified in api_specification.md — record actual without inventing codes.

## Schema contract reference
Type deviation probe on documented price field.

## Type
Schema validation

## Audit
- **Status:** VALID
- **Reasoning:** Spec types price as number; observe coercion without mandating reject.

## Status / Related bugs
Not Run / None
