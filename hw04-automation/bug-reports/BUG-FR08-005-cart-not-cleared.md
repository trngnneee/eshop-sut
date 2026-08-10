# BUG-FR08-005 — Cart not cleared after successful checkout

| Field | Value |
| --- | --- |
| Feature | FR-08 Checkout |
| Severity | High |
| Found by | TC-CHECKOUT-009 |
| Date | 2026-08-09 |

## Spec
After successful payment, the cart must be cleared.

## Actual
`Checkout.jsx` sets success UI but never calls `clearCart()`; cart items remain.

## Evidence
TC-CHECKOUT-009: empty-cart message not visible after success.

## GitHub Issue

https://github.com/trngnneee/eshop-sut/issues/381
