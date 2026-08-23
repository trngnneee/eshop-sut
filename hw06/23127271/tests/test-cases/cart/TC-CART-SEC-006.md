# TC-CART-SEC-006: Client price tampering — price=1 for expensive product

## Requirement ID
FR-07

## Module / Test type / Technique
cart / Security / SEC-mapped probe

## Security requirement(s)
SEC-06

## Threat / probe
Price tampering / integrity

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.

## Test data
| Field | Value |
|-------|-------|
| id | 1 |
| price | 1 |
| quantity | 1 |

## Test steps
1. POST /api/cart id=1 price=1.
2. GET /api/cart — record stored price and quantity.

## Expected result
POST /api/cart example includes client price. Spec does not require cart POST to validate price against catalogue (FR-08 applies at checkout). Record stored price on GET /api/cart. HTTP status and error body are not specified — record actual without inventing codes.

## SEC coverage
SEC-06

## Type
Integrity observe (unspecified at cart POST)

## Audit
- **Status:** INVALID
- **Reasoning:** Oracle claimed FR-07/SEC-06 requires cart POST to reject client price tampering. FR-08 mandates server-side checkout total; FR-07/example body does not forbid storing client price on add. SEC-06 is role-only on profile.

## Status / Related bugs
Not Run / None
