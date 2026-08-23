# TC-PROFILE-ST-001: Seed profile → full update → verified snapshot

## Requirement ID
FR-04

## Module / Test type / Technique
profile / Functional / State Transition Testing

## State machine
P0 (seed) → P1 (updated) via valid full PUT

## Transition under test
P0 → P1

## Preconditions
- EShop backend at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!
- GET /api/users/me → snapshot P0 (name, phone, shipping_address, email, role).

## Test data
| (see steps — multi-step sequence) | |

## Test steps
1. PUT /api/users/me with name, phone, shipping_address (FR-04-valid).
2. GET /api/users/me.

## Expected result
After PUT, GET /api/users/me shows the submitted name, phone, and shipping_address (P1). email and role unchanged from P0 (FR-04 / SEC-06). Success HTTP status/body not specified.

## States / transitions covered
P0→P1

## Type
Legal

## Audit
- **Status:** VALID
- **Reasoning:** FR-04 allows a logged-in user to update name, phone, and shipping_address. Multi-step P0 to P1 is a valid state-transition probe. email/role immutability is spec-backed.

## Status / Related bugs
Not Run / None
