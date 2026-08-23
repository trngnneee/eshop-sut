# TC-CART-SEC-SUP-004: Unicode-escaped XSS bypass in cart name

## Requirement ID
FR-07 / SEC-04

## Module / Test type / Technique
cart / Security / Human extension (SEC-SUP)

## Security requirement(s)
SEC-04

## Threat / probe
Unicode-escaped XSS bypass in cart name

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.

## Test data
```json
{
  "body": {
    "id": 1,
    "name": "\\u003cscript\\u003ealert(1)\\u003c/script\\u003e",
    "price": 30000000,
    "quantity": 1
  }
}
```

## Test steps
1. POST /api/cart with Unicode-escaped script in name.
2. GET /api/cart — inspect JSON literal.

## Expected result
SEC-04: record literal stored/returned text; note for manual UI follow-up. HTTP status is not specified — record actual without inventing codes.

## Type
Encoding / XSS bypass

## Why the AI missed this
Model limitation — TC-CART-SEC-005 used literal <script> tags; Unicode escape and normalization bypasses for SEC-04 are a known gap when prompts say 'XSS' generically.

## Audit (human SUP)
- **Status:** VALID
- **Reasoning:** SEC-04 Unicode-escape XSS bypass probe.

## Status / Related bugs
Not Run / None
