# BUG-FR08-001 — No auth route guard on `/checkout`

| Field | Value |
| --- | --- |
| Feature | FR-08 Checkout |
| Severity | High |
| Found by | TC-CHECKOUT-002 |
| Date | 2026-08-09 |

## Spec
Only logged-in users may checkout.

## Actual
Guest can open `/checkout` directly; confirm button remains available.

## Evidence
Playwright failure under `test-results/fr08-checkout/<browser>/`.

## GitHub Issue

https://github.com/trngnneee/eshop-sut/issues/377
