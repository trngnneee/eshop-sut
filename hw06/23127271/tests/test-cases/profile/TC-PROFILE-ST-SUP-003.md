# TC-PROFILE-ST-SUP-003: Race — concurrent PUT changes name vs phone (different fields)

## Requirement ID
FR-04

## Module / Test type / Technique
profile / Functional / State Transition Testing (human extension)

## State machine
P0 → PUT(name) ∥ PUT(phone) → P?

## Transition under test
concurrent multi-field PUT race

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login test@eshop.com.
- GET P0 snapshot.

## Test data
| (see steps) | |

## Test steps
1. PUT name=Race Name X (phone/address FR-04-valid from example)
2. PUT phone=0888888888 (name/address from example) — fire immediately parallel to step 1
3. GET /api/users/me

## Expected result
Parallel updates to different fields are not specified. GET must show one coherent profile row. email/role unchanged. Record field-level vs request-level winner. HTTP status is not specified — record actual without inventing codes.

## States / transitions covered
P0→P?(mixed?)

## Type
Unspecified (concurrency)

## Why the AI missed this
Model limitation — SUP-001 raced the same field (name vs name); cross-field parallel PUTs can yield torn snapshots (name from A, phone from B) — checklist concurrency item not extended to multi-attribute races.

## Audit (human SUP)
- **Status:** VALID
- **Reasoning:** Cross-field parallel PUT race; torn read documented as unspecified.

## Status / Related bugs
Not Run / None
