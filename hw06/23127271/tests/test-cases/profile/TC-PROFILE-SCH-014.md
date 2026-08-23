# TC-PROFILE-SCH-014: GET without JWT — error body is JSON not HTML

## Requirement ID
FR-04 / SEC-02

## Module / Test type / Technique
profile / Schema validation / Response & request shape

## Schema aspect
Unauthenticated error body

## Preconditions
- EShop at http://localhost:3000.

## Test data
| (see steps) | |

## Test steps
1. GET /api/users/me without Authorization.
2. Inspect body is parseable JSON or empty; must not be HTML stack trace page.

## Expected result
Body must not be HTML error page with stack trace. If JSON error object, record keys (spec does not define auth error schema). HTTP status is not specified in api_specification.md — record actual without inventing codes.

## Schema contract reference
SEC-02 requires auth; error envelope undefined in api_spec.

## Type
Schema validation

## Audit
- **Status:** VALID
- **Reasoning:** Auth error envelope is unspecified; checking JSON-not-HTML and recording keys is a valid schema probe.

## Status / Related bugs
Not Run / None
