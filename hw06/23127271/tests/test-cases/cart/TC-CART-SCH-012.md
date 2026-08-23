# TC-CART-SCH-012: POST body JSON array instead of object

## Requirement ID
FR-07

## Module / Test type / Technique
cart / Schema validation / Response & request shape

## Schema aspect
Malformed request root

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.

## Test data
| (see steps) | |

## Test steps
1. POST /api/cart with raw body `[{"id":1}]` Content-Type application/json.
2. Inspect response body type.

## Expected result
Server rejects or ignores malformed root; response JSON or parse error — record shape. Cart unchanged on GET. HTTP status is not specified in api_specification.md — record actual without inventing codes.

## Schema contract reference
Request must be object per example; array root is schema violation.

## Type
Schema validation

## Audit
- **Status:** VALID
- **Reasoning:** Malformed array root is a valid request-shape probe; observe response type without inventing status codes.

## Status / Related bugs
Not Run / None
