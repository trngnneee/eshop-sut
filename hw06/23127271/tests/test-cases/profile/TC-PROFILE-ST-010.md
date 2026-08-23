# TC-PROFILE-ST-010: Invalid phone after valid update — state rollback unspecified

## Requirement ID
FR-04

## Module / Test type / Technique
profile / Functional / State Transition Testing

## State machine
P0 → P1(valid) → PUT(invalid phone) → ?

## Transition under test
invalid transition attempt

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!
- Reach P1 with valid full PUT.

## Test data
| (see steps — multi-step sequence) | |

## Test steps
1. PUT /api/users/me valid full body → P1.
2. PUT /api/users/me {"name":"Still Valid","shipping_address":"Addr","phone":"123"}.
3. GET /api/users/me.

## Expected result
phone=123 is not a valid FR-04 phone. GET must not persist it as the stored phone. Whether other P1 fields remain if the PUT is rejected is not specified — record status and GET snapshot.

## States / transitions covered
P1→P1 or P1→invalid

## Type
Illegal input / Unspecified

## Audit
- **Status:** INCOMPLETE
- **Reasoning:** phone=123 violates FR-04 format rule (real). Whether a rejected invalid PUT leaves P1 unchanged is not specified — generated oracle assumed rollback.

## Status / Related bugs
Not Run / None
