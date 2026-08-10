# BUG-FR15-005 — Negative price accepted (HTTP 200)

| Field | Value |
| --- | --- |
| Feature | FR-15 Product CRUD (Admin) |
| Severity | High |
| Environment | `POST /api/products` · localhost:3000 |
| Found by | TC-PRODUCT-010 (Chromium) |
| Date | 2026-08-10 |

## Spec

Product price must be positive. `price: -1` must be rejected.

## Steps

1. As admin, `POST /api/products` with valid name, `price: -1`, valid category.
2. Observe HTTP status.

## Expected

Status in **400–499**.

## Actual

Status **200**; negative price accepted.

## Evidence

Playwright `apiStatus` failure for TC-PRODUCT-010 under `test-results/fr15-admin-product/<browser>/`.

## GitHub Issue

https://github.com/trngnneee/eshop-sut/issues/386
