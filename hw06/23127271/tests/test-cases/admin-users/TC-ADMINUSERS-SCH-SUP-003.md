# TC-ADMINUSERS-SCH-SUP-003: DELETE path id=abc — error JSON shape

## Requirement ID
FR-19

## Module / Test type / Technique
admin-users / Schema validation / Human extension (SCH-SUP)

## Schema aspect
DELETE non-numeric path schema

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=admin@eshop.com password=Admin123!.

## Test data
```json
{
  "path": {
    "id": "abc"
  }
}
```

## Test steps
1. DELETE /api/admin/users/abc.
2. Record response Content-Type and JSON root type.

## Expected result
Response body type is JSON object or parseable JSON — not HTML. Record keys if object. HTTP status is not specified in api_specification.md — record actual without inventing codes.

## Why the AI missed this
Model limitation — schema DELETE cases assumed valid numeric delete; malformed path error envelope type (object vs string vs HTML) not catalogued.

## Audit (human SUP)
- **Status:** VALID
- **Reasoning:** Non-numeric DELETE path error envelope type observe.

## Status / Related bugs
Not Run / None
