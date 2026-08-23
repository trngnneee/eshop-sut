# TC-ADMINUSERS-SEC-SUP-002: Role escalation — user JWT on GET admin list

## Requirement ID
FR-19 / SEC-03

## Module / Test type / Technique
admin-users / Security / Human extension (SEC-SUP)

## Security requirement(s)
SEC-03

## Threat / probe
Role escalation — user JWT on GET admin list

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.

## Test data
```json
{
  "headers": {
    "Authorization": "Bearer <user_token>"
  }
}
```

## Test steps
1. GET /api/admin/users with test user JWT (role=user).
2. Inspect response — must not return full admin roster.

## Expected result
SEC-03 / FR-12: user JWT must not retrieve full user list. No password/hash in body if any data returned. HTTP status is not specified — record actual without inventing codes.

## Type
Illegal / privilege

## Why the AI missed this
Model limitation — AI mapped SEC-03 only to DELETE admin routes (SEC-002/003); spec section 6.1 pairs GET list with DELETE under same admin guard — list endpoint SEC-03 gap.

## Audit (human SUP)
- **Status:** VALID
- **Reasoning:** SEC-03 on GET list — spec §6.1 admin guard.

## Status / Related bugs
Not Run / None
