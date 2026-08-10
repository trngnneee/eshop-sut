# BUG-FR15-002 — Empty product name accepted (HTTP 200)

| Field | Value |
| --- | --- |
| Feature | FR-15 Product CRUD (Admin) |
| Severity | High |
| Environment | `POST /api/products` · localhost:3000 |
| Found by | TC-PRODUCT-006 (Chromium) |
| Date | 2026-08-10 |

## Spec

Product name (`Tên`) is required. Empty name must be rejected (client and/or server validation).

## Steps

1. As admin, `POST /api/products` with empty `name`, valid price, valid `category_id`.
2. Observe HTTP status.

## Expected

Status in **400–499**; product not created.

## Actual

Status **200**; create succeeds with empty name.

## Evidence

Playwright `apiStatus` failure for TC-PRODUCT-006 under `test-results/fr15-admin-product/<browser>/`.

## GitHub Issue

TBD — attach screenshot when filing.
