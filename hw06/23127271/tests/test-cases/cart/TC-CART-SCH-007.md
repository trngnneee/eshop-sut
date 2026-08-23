# TC-CART-SCH-007: POST /api/cart success response is JSON object

## Requirement ID
FR-07

## Module / Test type / Technique
cart / Schema validation / Response & request shape

## Schema aspect
POST success response envelope

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.

## Test data
| (see steps) | |

## Test steps
1. POST /api/cart with documented body.
2. Inspect response JSON root type and keys.

## Expected result
Response body is JSON object. Top-level fields not documented in api_spec — record names/types. HTTP status is not specified in api_specification.md — record actual without inventing codes.

## Schema contract reference
Gap: api_spec 4.2 documents request only, not POST success response.

## Type
Schema validation

## Audit
- **Status:** VALID
- **Reasoning:** POST success body is undocumented; observe-only JSON object check is correct.

## Status / Related bugs
Not Run / None
