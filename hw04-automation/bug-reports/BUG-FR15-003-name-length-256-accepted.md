# BUG-FR15-003 — Product name length 256 accepted (HTTP 200)

| Field | Value |
| --- | --- |
| Feature | FR-15 Product CRUD (Admin) |
| Severity | Medium |
| Environment | `POST /api/products` · localhost:3000 |
| Found by | TC-PRODUCT-008 (Chromium) |
| Date | 2026-08-10 |

## Spec

Product name max length is **255**. Length 256 must be rejected.

## Steps

1. As admin, `POST /api/products` with `name` of length 256, valid price/category.
2. Observe HTTP status.

## Expected

Status in **400–499**.

## Actual

Status **200**; oversized name accepted.

## Evidence

Playwright `apiStatus` failure for TC-PRODUCT-008 under `test-results/fr15-admin-product/<browser>/`.

## GitHub Issue

https://github.com/trngnneee/eshop-sut/issues/384
