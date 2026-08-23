# TC-PROFILE-SCH-011: phone sent as JSON number — observe type handling

## Requirement ID
FR-04

## Module / Test type / Technique
profile / Schema validation / Response & request shape

## Schema aspect
Request field type coercion

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.

## Test data
| (see steps) | |

## Test steps
1. PUT body {"name":"Nguyen Van A","shipping_address":"Addr","phone":912345678} (phone number not string).
2. GET /api/users/me — record typeof phone.

## Expected result
Spec example types phone as string. Record whether server coerces number to string, rejects, or stores number. HTTP status is not specified in api_specification.md — record actual without inventing codes.

## Schema contract reference
api_spec example uses string phone; numeric type is schema deviation probe.

## Type
Schema validation

## Audit
- **Status:** VALID
- **Reasoning:** Spec example types phone as string; observe coercion without mandating reject is spec-aligned.

## Status / Related bugs
Not Run / None
