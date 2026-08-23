# TC-ADMINUSERS-SEC-SUP-001: Auth bypass — GET admin list without JWT

## Requirement ID
FR-19 / SEC-02

## Module / Test type / Technique
admin-users / Security / Human extension (SEC-SUP)

## Security requirement(s)
SEC-02

## Threat / probe
Auth bypass — GET admin list without JWT

## Preconditions
- EShop at http://localhost:3000.
- Disposable users exist in system.

## Test data
```json
{
  "headers": {}
}
```

## Test steps
1. GET /api/admin/users without Authorization header.
2. Inspect response for user list and password fields.

## Expected result
SEC-02: unauthenticated GET must not return full user roster or password fields. Record status/body. HTTP status is not specified — record actual without inventing codes.

## Type
Illegal / auth bypass

## Why the AI missed this
Prompt quality — SEC-02 probes targeted DELETE /api/admin/users/:id (SEC-001/010); GET list is part of FR-19 but never tested unauthenticated, leaving list exposure untested.

## Audit (human SUP)
- **Status:** VALID
- **Reasoning:** SEC-02 unauthenticated GET list — FR-19/§6 paired endpoint.

## Status / Related bugs
Not Run / None
