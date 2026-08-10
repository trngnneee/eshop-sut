# BUG-FR08-004 — Backend trusts client `total_amount`

| Field | Value |
| --- | --- |
| Feature | FR-08 Checkout |
| Severity | Critical |
| Found by | TC-CHECKOUT-008 |
| Date | 2026-08-09 |

## Spec
Backend must recalculate total; must not accept client-supplied `total_amount`.

## Actual
After lowering the UI total to `1`, `POST /api/checkout` stores `total_amount = 1` instead of the cart total (e.g. 30000000).

## Evidence
TC-CHECKOUT-008: Expected cart total, Received `1`.

## GitHub Issue

https://github.com/trngnneee/eshop-sut/issues/380
