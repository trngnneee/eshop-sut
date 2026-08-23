# TC-ADMINUSERS-SCH-SUP-004: Registered user with normal schema after disposable add

## Requirement ID
FR-19 / SEC-01

## Module / Test type / Technique
admin-users / Schema validation / Human extension (SCH-SUP)

## Schema aspect
Register-then-list schema

## Preconditions
- EShop at http://localhost:3000.
- Admin JWT.
- Register user schema-test@example.com.

## Test data
```json
{
  "sequence": [
    "GET list",
    "find new user by email"
  ]
}
```

## Test steps
1. Register disposable user.
2. GET /api/admin/users.
3. Schema-check new row only.

## Expected result
After register schema-test@example.com, list entry is object with number id and string email. role/name types recorded if present — register response only guarantees id in api_spec. No password fields.

## Why the AI missed this
Prompt quality — SCH-011 checked seed users exist; schema validation immediately after register+list (new row shape) not isolated.

## Audit (human SUP)
- **Status:** INCOMPLETE
- **Reasoning:** Aspect label said 'empty string email' but case registers new user — corrected oracle; name field not guaranteed by register response.

## Status / Related bugs
Not Run / None
