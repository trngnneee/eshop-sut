# BUG-FR15-007 — Create product without JWT returns 200 (FR-12)

| Field | Value |
| --- | --- |
| Feature | FR-15 Product CRUD / FR-12 AuthZ |
| Severity | Critical |
| Environment | `POST /api/products` · localhost:3000 |
| Found by | TC-PRODUCT-013 (Chromium) |
| Date | 2026-08-10 |

## Spec

FR-12 / FR-15: product mutations require a valid admin JWT. Unauthenticated `POST` must be rejected (**401–403**).

## Steps

1. Call `POST /api/products` with a valid body and **no** `Authorization` header.
2. Observe HTTP status.

## Expected

Status **401** or **403**; no product created.

## Actual

Status **200**; create succeeds without JWT.

## Evidence

Playwright `apiStatus` failure for TC-PRODUCT-013 under `test-results/fr15-admin-product/<browser>/`. Related: HW02 issue #182 if applicable.

## GitHub Issue

https://github.com/trngnneee/eshop-sut/issues/388
