# TC-ADMINUSERS-ST-012: Delete user with orders — cascade unspecified

## Requirement ID
FR-19

## Module / Test type / Technique
admin-users / Functional / State Transition Testing

## State machine
U_EXISTS(+orders) → ?

## Transition under test
cascade edge

## Preconditions
- EShop at http://localhost:3000.
- Register user D. Login as D. POST cart + POST checkout to create order.
- POST /api/login email=admin@eshop.com password=Admin123!

## Test data
| (see steps — multi-step sequence) | |

## Test steps
1. DELETE /api/admin/users/D.
2. GET /api/admin/users.
3. GET /api/admin/orders (optional).

## Expected result
Cascade when user has orders is not specified in FR-19. Record whether delete succeeds or is blocked and effect on orders.

## States / transitions covered
U_EXISTS→DELETED or blocked

## Type
Unspecified

## Audit
- **Status:** VALID
- **Reasoning:** Cascade delete with orders is correctly flagged unspecified; no invented requirement.

## Status / Related bugs
Not Run / None
