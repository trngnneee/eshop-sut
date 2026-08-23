# TC-ADMINUSERS-SEC-SUP-005: Path traversal — encoded slash in :id

## Requirement ID
FR-19 / SEC-05

## Module / Test type / Technique
admin-users / Security / Human extension (SEC-SUP)

## Security requirement(s)
SEC-05

## Threat / probe
Path traversal — encoded slash in :id

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=admin@eshop.com password=Admin123!.
- Note seed user id=2 exists.

## Test data
```json
{
  "path": {
    "id": "1%2f2"
  }
}
```

## Test steps
1. DELETE /api/admin/users/1%2f2 with admin JWT.
2. GET /api/admin/users — confirm user id=2 still exists.

## Expected result
DELETE must not remove user 2 via path confusion. GET /api/admin/users — user 2 still present unless id literally matched. HTTP status is not specified — record actual without inventing codes.

## Type
Path manipulation

## Why the AI missed this
API characteristic — AI used SQL metacharacters in path; URL-encoded slash (%2f) routing confusion is an HTTP/framework attack absent from spec text.

## Audit (human SUP)
- **Status:** VALID
- **Reasoning:** Encoded slash path manipulation probe.

## Status / Related bugs
Not Run / None
