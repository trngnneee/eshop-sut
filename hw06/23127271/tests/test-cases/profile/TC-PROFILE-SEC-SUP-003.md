# TC-PROFILE-SEC-SUP-003: Null-byte encoding in name field

## Requirement ID
FR-04 / SEC-05

## Module / Test type / Technique
profile / Security / Human extension (SEC-SUP)

## Security requirement(s)
SEC-05

## Threat / probe
Null-byte encoding in name field

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.

## Test data
```json
{
  "body": {
    "name": "Nguyen\u0000admin",
    "phone": "0912345678",
    "shipping_address": "123 Le Loi"
  }
}
```

## Test steps
1. PUT /api/users/me with null byte in name field.
2. GET /api/users/me.

## Expected result
SEC-05: null byte must not truncate stored name or cause SQL/500 leak. GET shows literal storage or rejection; email/role unchanged. HTTP status is not specified — record actual without inventing codes.

## Type
Encoding / injection probe

## Why the AI missed this
Model limitation — SQLi/XSS probes used printable ASCII quotes; null-byte and encoding-truncation attacks on SQLite/string handling are absent from LLM default payloads.

## Audit (human SUP)
- **Status:** VALID
- **Reasoning:** SEC-05 null-byte encoding probe; observe storage/leak.

## Status / Related bugs
Not Run / None
