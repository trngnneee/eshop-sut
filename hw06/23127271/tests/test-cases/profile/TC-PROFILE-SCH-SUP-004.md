# TC-PROFILE-SCH-SUP-004: PUT body JSON array instead of object

## Requirement ID
FR-04

## Module / Test type / Technique
profile / Schema validation / Human extension (SCH-SUP)

## Schema aspect
Array root request body

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.

## Test data
```json
{
  "body_raw": "[{\"name\":\"Hack\"}]",
  "headers": {
    "Content-Type": "application/json"
  }
}
```

## Test steps
1. PUT with raw JSON array body.
2. GET profile unchanged or record actual.

## Expected result
Profile must not update from array body. Response JSON or parse error — record shape. HTTP status is not specified in api_specification.md — record actual without inventing codes.

## Why the AI missed this
Model limitation — SCH generator tested empty object and type coercion; array-root malformed JSON is a distinct parser/schema failure mode.

## Audit (human SUP)
- **Status:** VALID
- **Reasoning:** Array-root PUT malformed schema.

## Status / Related bugs
Not Run / None
