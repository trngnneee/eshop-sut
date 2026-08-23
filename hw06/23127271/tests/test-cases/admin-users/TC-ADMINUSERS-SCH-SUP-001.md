# TC-ADMINUSERS-SCH-SUP-001: Admin list exposes shipping_address / login_attempts

## Requirement ID
FR-19

## Module / Test type / Technique
admin-users / Schema validation / Human extension (SCH-SUP)

## Schema aspect
Undocumented list columns

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=admin@eshop.com password=Admin123!.

## Test data
```json
{
  "headers": {}
}
```

## Test steps
1. GET /api/admin/users.
2. Inventory keys on first user object.

## Expected result
Record presence/types of shipping_address, login_attempts, locked_until. FR-19 forbids password only.

## Why the AI missed this
API characteristic — SUT SELECT lists extra columns; AI FR-19 schema assumed id/name/email/role only.

## Audit (human SUP)
- **Status:** VALID
- **Reasoning:** Extra list columns from SUT SELECT — schema over-exposure observe.

## Status / Related bugs
Not Run / None
