# HW04 Feature B prep — FR-08 Checkout

**Student ID:** 23127271  
**Status:** Implemented + verified (2026-08-09) — stage docs `fr08-analysis.md`…`fr08-verify-chromium.md`  
**Rule:** Feature A evidence stays frozen — use `npm run test:matrix:fr08` only for B.

## Requirement ledger

| Feature | Source | Case IDs | Count | Data file | Spec file | Browsers | Reports |
| --- | --- | --- | ---: | --- | --- | --- | --- |
| FR-03 (A) | done | TC-FORGOT-001…014 | 14 | `test-data/fr03-forgot-password.json` | `tests/fr03-forgot-password.spec.js` | 3 | `reports/html/fr03-forgot-password/<browser>/` **FROZEN** |
| FR-08 (B) | README FR-08 + HW02 Feature B | TC-CHECKOUT-001…014 | 14 | `test-data/fr08-checkout.json` | `tests/fr08-checkout.spec.js` | 3 | `reports/html/fr08-checkout/<browser>/` |
| FR-15 (C) | done | TC-PRODUCT-001…014 | 14 | `test-data/fr15-admin-product.json` | `tests/fr15-admin-product.spec.js` | 3 | `reports/html/fr15-admin-product/<browser>/` |

## FR-08 acceptance criteria (README)

1. Only **logged-in** users may checkout.
2. Payment total is computed from the cart and **not user-editable** in the UI.
3. Checkout UI lists all ordered product lines.
4. Backend **recalculates** total; rejects trusting client `total_amount`.
5. After successful checkout, the **cart is cleared**.

Related HW02 defects kept as oracles (do not soften): editable total, backend trusts client total, empty-cart checkout, missing `/checkout` route guard.

## Stage docs (AI-first, one stage per prompt)

| Stage | File |
| --- | --- |
| Analyze | `docs/fr08-analysis.md` |
| Design | `docs/fr08-design.md` |
| Review | `docs/fr08-review.md` |
| Model data | `docs/fr08-model-data.md` |
| Map | `docs/fr08-map-automation.md` |
| Verify | `docs/fr08-verify-chromium.md` |

## Evidence isolation (mandatory)

| Path | Purpose |
| --- | --- |
| `evidence/feature-a-fr03-frozen-2026-08-07/` | Immutable copy of Feature A HTML reports + manifest |
| `reports/html/fr03-forgot-password/*/EVIDENCE-LOCK.json` | Matrix skips these cells unless `FORCE_OVERWRITE=1` |
| `reports/html/fr08-checkout/<browser>/` | Feature B reports only |
| `reports/run-manifest-fr08-checkout.json` | Feature B cell status only |
| `reports/run-manifest.json` | Merged; B runs must not drop A cells |
| `test-results/fr08-checkout/<browser>/` | B failure artifacts only |

### Safe commands

```powershell
cd SoftwareTesting-HW\HW4\23127271
npm run evidence:verify-fr03   # must PASS before/after B work
npm run test:matrix:fr08       # B only — never overwrites locked FR-03 dirs
```
