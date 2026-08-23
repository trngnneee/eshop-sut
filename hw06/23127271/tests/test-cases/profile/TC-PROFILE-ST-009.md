# TC-PROFILE-ST-009: Three single-field transitions accumulate (or last-wins per field)

## Requirement ID
FR-04

## Module / Test type / Technique
profile / Functional / State Transition Testing

## State machine
P0 → P(name) → P(phone) → P(address)

## Transition under test
multi partial chain

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!

## Test data
| (see steps — multi-step sequence) | |

## Test steps
1. PUT {"name":"Step Name"}.
2. PUT {"phone":"0909090909"}.
3. PUT {"shipping_address":"99 Pasteur, Q3"}.
4. GET /api/users/me.

## Expected result
GET shows Step Name, 0909090909, and 99 Pasteur if each partial update applies. If omitted fields revert, record partial-vs-replace semantics. email/role unchanged.

## States / transitions covered
P0→P(n)→P(np)→P(npa)

## Type
Legal / Unspecified

## Audit
- **Status:** VALID
- **Reasoning:** Three sequential single-field PUTs probe partial-update chaining; oracle correctly flags unspecified semantics.

## Status / Related bugs
Not Run / None
