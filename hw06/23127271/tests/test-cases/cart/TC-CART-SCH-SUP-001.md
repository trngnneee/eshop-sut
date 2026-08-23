# TC-CART-SCH-SUP-001: POST {id, quantity} only — partial line schema

## Requirement ID
FR-07

## Module / Test type / Technique
cart / Schema validation / Human extension (SCH-SUP)

## Schema aspect
Minimal partial POST body

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.

## Test data
```json
{
  "body": {
    "id": 1,
    "quantity": 1
  }
}
```

## Test steps
1. POST {id:1, quantity:1}.
2. GET /api/cart — schema-check first line keys.

## Expected result
GET line may lack name/price keys — record keys and types. Spec example shows four fields; partial storage is deviation. HTTP status is not specified in api_specification.md — record actual without inventing codes.

## Why the AI missed this
Prompt quality — domain SUP-004 added minimal body functionally; schema pass required all four example fields and never tested stored line shape after partial POST.

## Audit (human SUP)
- **Status:** VALID
- **Reasoning:** Partial POST body stored shape observe.

## Status / Related bugs
Not Run / None
