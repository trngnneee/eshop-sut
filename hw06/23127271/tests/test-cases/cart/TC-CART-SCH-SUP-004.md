# TC-CART-SCH-SUP-004: POST with name:null — nullable string schema

## Requirement ID
FR-07

## Module / Test type / Technique
cart / Schema validation / Human extension (SCH-SUP)

## Schema aspect
Null field values

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.

## Test data
```json
{
  "body": {
    "id": 1,
    "name": null,
    "price": 100000,
    "quantity": 1
  }
}
```

## Test steps
1. POST with name:null.
2. GET /api/cart.

## Expected result
Record whether GET stores null, omits name, or rejects. typeof name on GET if present. HTTP status is not specified in api_specification.md — record actual without inventing codes.

## Why the AI missed this
Prompt quality — schema tests used valid strings; null literal for optional-looking name field (not stated required in spec) never tested.

## Audit (human SUP)
- **Status:** VALID
- **Reasoning:** name:null nullable probe observe-only.

## Status / Related bugs
Not Run / None
