# TC-PROFILE-SCH-SUP-002: PUT with nested profile object — wrong request schema

## Requirement ID
FR-04

## Module / Test type / Technique
profile / Schema validation / Human extension (SCH-SUP)

## Schema aspect
Nested request envelope

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.
- Snapshot GET.

## Test data
```json
{
  "body": {
    "profile": {
      "name": "Nested Name",
      "phone": "0912345678",
      "shipping_address": "Addr"
    }
  }
}
```

## Test steps
1. PUT nested body.
2. GET /api/users/me — compare to snapshot.

## Expected result
api_spec shows flat body keys. Server must reject or ignore nested envelope; record GET profile. HTTP status is not specified in api_specification.md — record actual without inventing codes.

## Why the AI missed this
Prompt quality — schema generator used flat objects matching api_spec example; nested envelope {profile:{...}} is a common client mistake never probed.

## Audit (human SUP)
- **Status:** VALID
- **Reasoning:** Nested envelope malformed request schema.

## Status / Related bugs
Not Run / None
