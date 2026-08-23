# TC-PROFILE-SCH-SUP-005: PUT with Content-Type application/json; charset=utf-8

## Requirement ID
FR-04

## Module / Test type / Technique
profile / Schema validation / Human extension (SCH-SUP)

## Schema aspect
Charset Content-Type variant

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.

## Test data
```json
{
  "headers": {
    "Content-Type": "application/json; charset=utf-8"
  },
  "body": {
    "name": "Charset Name",
    "phone": "0912345678",
    "shipping_address": "Addr"
  }
}
```

## Test steps
1. PUT with charset Content-Type and valid body.
2. GET /api/users/me.

## Expected result
Record whether PUT with Content-Type application/json; charset=utf-8 parses and updates profile. Do not require Charset Name unless observed. HTTP status is not specified in api_specification.md — record actual without inventing codes.

## Why the AI missed this
Prompt quality — SCH-010 checked response Content-Type on GET only; request charset variant on PUT not tested (RFC 7231 interoperability).

## Audit (human SUP)
- **Status:** INCOMPLETE
- **Reasoning:** Oracle assumed charset suffix always parses — corrected to observe-only.

## Status / Related bugs
Not Run / None
