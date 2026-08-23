# TC-PROFILE-ST-002: Sequential partial updates — name then phone

## Requirement ID
FR-04

## Module / Test type / Technique
profile / Functional / State Transition Testing

## State machine
P0 → P1a (name) → P1b (name+phone)

## Transition under test
P0 → P1a → P1b

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!
- Snapshot P0 via GET /api/users/me.

## Test data
| (see steps — multi-step sequence) | |

## Test steps
1. PUT /api/users/me body {"name":"Updated Name Only"}.
2. PUT /api/users/me body {"phone":"0987654321"}.
3. GET /api/users/me.

## Expected result
GET shows name=Updated Name Only and phone=0987654321 if both applied. shipping_address after partial PUTs is not specified — record P0 vs cleared vs unchanged. email/role unchanged.

## States / transitions covered
P0→P1a→P1b

## Type
Legal / Unspecified

## Audit
- **Status:** VALID
- **Reasoning:** Sequential partial PUTs test replace-vs-partial semantics which the spec leaves open. Oracle already records observe-only for omitted fields.

## Status / Related bugs
Not Run / None
