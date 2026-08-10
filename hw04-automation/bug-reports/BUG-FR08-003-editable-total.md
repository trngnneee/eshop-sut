# BUG-FR08-003 — Payment total is user-editable

| Field | Value |
| --- | --- |
| Feature | FR-08 Checkout |
| Severity | High |
| Found by | TC-CHECKOUT-007 |
| Date | 2026-08-09 |

## Spec
Total is computed from the cart and must not be directly editable.

## Actual
Checkout renders `<input type="number">` bound to `editableTotal` (red bold), fully editable.

## Evidence
TC-CHECKOUT-007 failure screenshots.

## GitHub Issue

https://github.com/trngnneee/eshop-sut/issues/379
