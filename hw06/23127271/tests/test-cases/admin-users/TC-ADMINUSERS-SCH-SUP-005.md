# TC-ADMINUSERS-SCH-SUP-005: DELETE success body minimal schema — no full user object leak

## Requirement ID
FR-19

## Module / Test type / Technique
admin-users / Schema validation / Human extension (SCH-SUP)

## Schema aspect
DELETE response must not echo full user row

## Preconditions
- EShop at http://localhost:3000.
- Admin JWT.
- Register disposable D.

## Test data
```json
{
  "path": {
    "id": "<D>"
  }
}
```

## Test steps
1. DELETE disposable D.
2. Inspect response keys — no email/password echo of deleted user.

## Expected result
DELETE response must not contain full user object with email/password. If only {message:string} — pass. Record actual keys. SEC-01 applies.

## Why the AI missed this
API characteristic — SCH-009/010 checked JSON object and message string; did not forbid echoing deleted user record with PII in DELETE body.

## Audit (human SUP)
- **Status:** VALID
- **Reasoning:** DELETE body must not echo deleted user PII.

## Status / Related bugs
Not Run / None
