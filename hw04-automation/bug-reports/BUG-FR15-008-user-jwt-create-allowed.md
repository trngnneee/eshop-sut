# BUG-FR15-008 — Non-admin JWT can create products (FR-12)

| Field | Value |
| --- | --- |
| Feature | FR-15 Product CRUD / FR-12 AuthZ |
| Severity | Critical |
| Environment | `POST /api/products` · localhost:3000 |
| Found by | TC-PRODUCT-014 (Chromium) |
| Date | 2026-08-10 |

## Spec

Only `role=admin` may create/update/delete products. A normal user JWT must receive **401–403**.

## Steps

1. Login as a non-admin user; obtain JWT.
2. `POST /api/products` with that JWT and a valid body.
3. Observe HTTP status.

## Expected

Status **401** or **403**.

## Actual

Status **200**; user JWT can create products.

## Evidence

Playwright `apiStatus` failure for TC-PRODUCT-014 under `test-results/fr15-admin-product/<browser>/`.

## GitHub Issue

https://github.com/trngnneee/eshop-sut/issues/389
