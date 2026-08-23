# TC-PROFILE-SCH-008: PUT accepts documented three-field JSON body

## Requirement ID
FR-04

## Module / Test type / Technique
profile / Schema validation / Response & request shape

## Schema aspect
PUT request body schema

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.

## Test data
| (see steps) | |

## Test steps
1. PUT /api/users/me body {"name":"Nguyen Van A","shipping_address":"123 Le Loi, Q1, TP.HCM","phone":"0912345678"}.
2. GET /api/users/me — verify name/phone/shipping_address strings updated.

## Expected result
PUT succeeds per spec example shape (three string fields). GET reflects submitted string values. HTTP status is not specified in api_specification.md — record actual without inventing codes.

## Schema contract reference
api_spec section 2.2 PUT body JSON example.

## Type
Schema validation

## Audit
- **Status:** VALID
- **Reasoning:** api_spec section 2.2 documents PUT body with name, shipping_address, phone as strings.

## Status / Related bugs
Not Run / None
