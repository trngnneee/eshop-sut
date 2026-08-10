# BUG-FR15-006 — Invalid category_id accepted (HTTP 200)

| Field | Value |
| --- | --- |
| Feature | FR-15 Product CRUD (Admin) |
| Severity | High |
| Environment | `POST /api/products` · localhost:3000 |
| Found by | TC-PRODUCT-012 (Chromium) |
| Date | 2026-08-10 |

## Spec

`category_id` must reference an existing category. Unknown IDs (e.g. `999999`) must be rejected.

## Steps

1. As admin, `POST /api/products` with valid name/price and `category_id: 999999`.
2. Observe HTTP status.

## Expected

Status in **400–499**.

## Actual

Status **200**; invalid category accepted.

## Evidence

Playwright `apiStatus` failure for TC-PRODUCT-012 under `test-results/fr15-admin-product/<browser>/`.

## GitHub Issue

TBD — attach screenshot when filing.
