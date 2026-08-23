# TC-ADMINUSERS-ST-SUP-003: Terminal — deleted user's old JWT on GET /api/users/me

## Requirement ID
FR-19 / SEC-02

## Module / Test type / Technique
admin-users / Functional / State Transition Testing (human extension)

## State machine
U_DELETED → GET /api/users/me(old token)

## Transition under test
terminal session invalidation

## Preconditions
- EShop at http://localhost:3000.
- Register user D.
- Login as D → save token T.
- Admin deletes D via DELETE /api/admin/users/D.

## Test data
| (see steps) | |

## Test steps
1. GET /api/users/me using token T captured before admin deleted D.

## Expected result
Deleted account must not return a live profile for that user. Must not show another user's data (IDOR). HTTP status is not specified — record actual without inventing codes.

## States / transitions covered
U_DELETED→auth blocked

## Type
Illegal / Unspecified

## Why the AI missed this
API characteristic — ST-011 tests login after delete; it does not probe whether an existing JWT from before DELETE still authorizes GET /api/users/me (session invalidation unspecified).

## Audit (human SUP)
- **Status:** INCOMPLETE
- **Reasoning:** Oracle said '401/403 expected' — HTTP codes not in spec; corrected to observe-only.

## Status / Related bugs
Not Run / None
