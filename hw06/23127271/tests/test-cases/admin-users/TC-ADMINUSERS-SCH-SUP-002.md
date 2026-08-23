# TC-ADMINUSERS-SCH-SUP-002: All list users share identical key set

## Requirement ID
FR-19

## Module / Test type / Technique
admin-users / Schema validation / Human extension (SCH-SUP)

## Schema aspect
Homogeneous list element schema

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
1. GET list.
2. Compare Object.keys() for admin@eshop.com vs test@eshop.com entries.

## Expected result
Every user object in array has the same keys (order may differ). Report any row missing email or role compared to others.

## Why the AI missed this
Prompt quality — SCH-002 checked each element is object; key-set equality across seed admin vs test user rows not asserted.

## Audit (human SUP)
- **Status:** VALID
- **Reasoning:** Homogeneous key set across list elements — reasonable schema consistency check.

## Status / Related bugs
Not Run / None
