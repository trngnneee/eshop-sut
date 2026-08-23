# TC-CART-SCH-014: GET cart without JWT — response body shape

## Requirement ID
FR-07 / SEC-02

## Module / Test type / Technique
cart / Schema validation / Response & request shape

## Schema aspect
Unauthenticated error body

## Preconditions
- EShop at http://localhost:3000.

## Test data
| (see steps) | |

## Test steps
1. GET /api/cart without Authorization.
2. Record whether body is JSON object/array vs HTML.

## Expected result
Must not return cart array without auth. Error body schema not specified — record parseable JSON keys if any. HTTP status is not specified in api_specification.md — record actual without inventing codes.

## Schema contract reference
SEC-02 + api_spec section 4 auth note.

## Type
Schema validation

## Audit
- **Status:** VALID
- **Reasoning:** Unauthenticated cart access must not return a cart array; error body shape is observe-only.

## Status / Related bugs
Not Run / None
