# TC-CART-SCH-008: POST body matches example four-field schema

## Requirement ID
FR-07

## Module / Test type / Technique
cart / Schema validation / Response & request shape

## Schema aspect
POST request four-field schema

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.

## Test data
| (see steps) | |

## Test steps
1. POST body {"id":1,"name":"San pham A","price":100000,"quantity":2}.
2. GET /api/cart — line contains id,name,price,quantity keys.

## Expected result
Stored line object includes all four keys from api_spec example with matching JSON types.

## Schema contract reference
api_spec section 4.2 POST JSON example.

## Type
Schema validation

## Audit
- **Status:** VALID
- **Reasoning:** Four-field POST body matches api_spec section 4.2 example exactly.

## Status / Related bugs
Not Run / None
