# BUG-FR15-001 — Edit updates sibling product rows in Admin UI

| Field | Value |
| --- | --- |
| Feature | FR-15 Product CRUD (Admin) |
| Severity | High |
| Environment | frontend-admin Products · localhost:5174 · API `:3000` |
| Found by | TC-PRODUCT-004 (Chromium) |
| Date | 2026-08-10 |

## Spec

Editing one product must change only that product. Sibling products keep their names in the list (UI and API).

## Steps

1. Login as admin; open Products.
2. Ensure two distinct products exist (target + sibling).
3. Edit the target product name via UI; save.
4. Observe the sibling row in the product table.

## Expected

Only the target row shows the new name. Sibling row still shows the original sibling name.

## Actual

After edit, sibling name is no longer found in the UI table (mass-rename / shared list mutation — `fakeMassUpdatedProducts` behavior). API sibling persistence may still be correct; UI isolation fails.

## Evidence

Playwright failure screenshot for TC-PRODUCT-004 under `test-results/fr15-admin-product/<browser>/`.

## GitHub Issue

https://github.com/trngnneee/eshop-sut/issues/382
