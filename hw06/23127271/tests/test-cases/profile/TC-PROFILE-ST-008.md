# TC-PROFILE-ST-008: Admin profile update — role stays admin

## Requirement ID
FR-04

## Module / Test type / Technique
profile / Functional / State Transition Testing

## State machine
P0(admin) → P1 → role=admin

## Transition under test
admin P0→P1

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=admin@eshop.com password=Admin123!
- GET P0 role=admin.

## Test data
| (see steps — multi-step sequence) | |

## Test steps
1. PUT /api/users/me {"name":"Admin Updated","phone":"0911111111","shipping_address":"Admin HQ"}.
2. GET /api/users/me.

## Expected result
GET shows updated profile fields and role still admin. Success status/body not specified.

## States / transitions covered
P0(admin)→P1(admin)

## Type
Legal

## Audit
- **Status:** VALID
- **Reasoning:** FR-04 applies to any logged-in user; admin is a logged-in user. role must remain admin.

## Status / Related bugs
Not Run / None
