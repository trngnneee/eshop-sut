# Automation Expansion Status — HW03 EShop

| Scope | Tests | Runtime status |
|---|---:|---|
| Product Listing `/` | 20 | Verified previously: 13 Pass, 7 Fail |
| Product Detail `/product/1` | 15 | Blocked by managed sandbox `spawn EPERM` |
| Cart `/cart` | 10 | Blocked by managed sandbox `spawn EPERM` |
| Total | 45 | 20 executed, 25 blocked |

The new suite is located at `tests/eshop-product-detail-cart.spec.js`. Run it in a normal local shell, preserve artifacts, update `HW3/GUI/GUI_Checklist_Data.json` and rerun the report/XLSX generators and validator.
