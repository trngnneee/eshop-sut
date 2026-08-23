# TC-ADMINUSERS-ST-013: Body id must not override path — self-delete guard holds

## Requirement ID
FR-19

## Module / Test type / Technique
admin-users / Functional / State Transition Testing

## State machine
path=self, body=other → U_SELF protected

## Transition under test
path wins over body

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=admin@eshop.com password=Admin123!
- Disposable D exists.

## Test data
| (see steps — multi-step sequence) | |

## Test steps
1. DELETE /api/admin/users/{admin_self_id} with JSON body {"id": D}.
2. GET /api/admin/users.

## Expected result
Path id is the documented resource identifier. Admin must not be deleted when path is self id; D must not be deleted via body alone. HTTP status not specified.

## States / transitions covered
U_SELF→U_SELF; D→EXISTS

## Type
Unspecified / guard

## Audit
- **Status:** INCOMPLETE
- **Reasoning:** DELETE body is not documented. Path :id is the specified identifier (consistent with domain TC-ADMINUSERS-019). Body override rule is inferred, not written.

## Status / Related bugs
Not Run / None
