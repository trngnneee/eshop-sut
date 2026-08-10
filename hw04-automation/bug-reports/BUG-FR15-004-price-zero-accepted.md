# BUG-FR15-004 — Price 0 accepted (HTTP 200)

| Field | Value |
| --- | --- |
| Feature | FR-15 Product CRUD (Admin) |
| Severity | High |
| Environment | `POST /api/products` · localhost:3000 |
| Found by | TC-PRODUCT-009 (Chromium) |
| Date | 2026-08-10 |

## Spec

Product price (`Giá`) must be a positive value. `price: 0` must be rejected.

## Steps

1. As admin, `POST /api/products` with valid name, `price: 0`, valid category.
2. Observe HTTP status.

## Expected

Status in **400–499**.

## Actual

Status **200**; zero price accepted.

## Evidence

Playwright `apiStatus` failure for TC-PRODUCT-009 under `test-results/fr15-admin-product/<browser>/`.

## GitHub Issue

TBD — attach screenshot when filing.
