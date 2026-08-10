# BUG-FR08-002 — Empty cart checkout succeeds

| Field | Value |
| --- | --- |
| Feature | FR-08 Checkout |
| Severity | High |
| Found by | TC-CHECKOUT-003 |
| Date | 2026-08-09 |

## Spec
Checkout requires cart line items; empty cart must not complete payment.

## Actual
Logged-in user on `/checkout` with empty cart can confirm and sees “Thanh toán thành công!”.

## Evidence
`test-results/fr08-checkout/<browser>/` for TC-CHECKOUT-003.

## GitHub Issue

https://github.com/trngnneee/eshop-sut/issues/378
