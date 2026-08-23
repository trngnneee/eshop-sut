# TC-CART-SEC-008: Mass assignment — user_id in POST body

## Requirement ID
FR-07

## Module / Test type / Technique
cart / Security / SEC-mapped probe

## Security requirement(s)
SEC-06

## Threat / probe
Mass assignment user_id

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.
- Note admin user id=1.

## Test data
| (see steps) | |

## Test steps
1. POST /api/cart with "user_id":1 in body as test user.
2. GET /api/cart as test user — line belongs to JWT subject, not body user_id.

## Expected result
Line must attach to JWT subject (test user), not admin via body user_id. GET /api/cart as test user — record actual.

## SEC coverage
SEC-06

## Type
Security probe / integrity

## Audit
- **Status:** INCOMPLETE
- **Reasoning:** user_id mass assignment is a valid integrity probe, but SEC-06 applies only to profile role field per README.

## Status / Related bugs
Not Run / None
