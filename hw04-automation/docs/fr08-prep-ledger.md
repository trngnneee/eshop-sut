# HW04 Feature B prep — FR-08 Checkout (do not run yet)

**Student ID:** 23127271  
**Status:** Prepared / not implemented  
**Rule:** Feature A evidence is frozen — use `npm run test:matrix:fr08` only when implementing B.

## Requirement ledger (pre-implementation)

| Feature | Source | Case IDs (planned) | Count | Data file | Spec file | Browsers | Reports |
| --- | --- | --- | ---: | --- | --- | --- | --- |
| FR-03 (A) | done | TC-FORGOT-001…014 | 14 | `test-data/fr03-forgot-password.json` | `tests/fr03-forgot-password.spec.js` | 3 | `reports/html/fr03-forgot-password/<browser>/` **FROZEN** |
| FR-08 (B) | README FR-08 + HW02 Feature B | TC-CHECKOUT-001…≥012 | ≥12 | `test-data/fr08-checkout.json` *(TBD)* | `tests/fr08-checkout.spec.js` *(TBD)* | 3 | `reports/html/fr08-checkout/<browser>/` |
| FR-15 (C) | later | — | ≥12 | TBD | TBD | 3 | `reports/html/fr15-admin-product/<browser>/` |

## FR-08 acceptance criteria (README)

1. Only **logged-in** users may checkout.
2. Payment total is computed from the cart and **not user-editable** in the UI.
3. Checkout UI lists all ordered product lines.
4. Backend **recalculates** total; rejects trusting client `total_amount`.
5. After successful checkout, the **cart is cleared**.

Related HW02 defects to keep as oracles (do not soften): editable total, backend trusts client total, empty-cart checkout, missing `/checkout` route guard.

## Planned case themes (≥12)

| Theme | Example IDs | Category |
| --- | --- | --- |
| Auth gate / guest | 001 | negative |
| Empty cart | 002 | negative |
| Happy path logged-in + items | 003 | positive |
| Line items visible | 004–005 | positive / validation |
| Total read-only (not editable) | 006 | validation |
| Client total tamper rejected | 007 | negative / security |
| Cart cleared after success | 008 | state |
| Qty / multi-item boundaries | 009–011 | boundary |
| Unauthenticated API/UI combo | 012 | negative |

Exact IDs/oracles will be finalized in Analyze→Design stages when implementation starts.

## Evidence isolation (mandatory)

| Path | Purpose |
| --- | --- |
| `evidence/feature-a-fr03-frozen-2026-08-07/` | Immutable copy of Feature A HTML reports + manifest |
| `reports/html/fr03-forgot-password/*/EVIDENCE-LOCK.json` | Matrix skips these cells unless `FORCE_OVERWRITE=1` |
| `reports/html/fr08-checkout/<browser>/` | Feature B reports only (created on first B run) |
| `reports/run-manifest-fr08-checkout.json` | Feature B cell status only |
| `reports/run-manifest.json` | Merged; B runs must not drop A cells |
| `test-results/fr08-checkout/<browser>/` | B failure artifacts only |

### Safe commands when starting Feature B

```powershell
cd SoftwareTesting-HW\HW4\23127271
npm run evidence:verify-fr03   # must PASS before/after B work
npm run test:matrix:fr08       # B only — never overwrites locked FR-03 dirs
```

Avoid:

```powershell
npx playwright test   # defaults to reports/html/adhoc — OK, but don't point FEATURE_SLUG at fr03
npm run test:matrix:fr03
$env:FORCE_OVERWRITE=1        # only if intentionally regenerating Feature A
```

## Dependencies / seed notes

- Web: `http://localhost:5173` · API: `http://localhost:3000`
- Need logged-in user (API register/login or seed `test@eshop.com` / `Test1234!` — prefer unique users)
- Cart must be seeded via UI or API before checkout happy paths
- Do not mutate Feature A test data files or FR-03 specs while building B

## AI conversion stages (start when implementing)

1. Analyze → 2. Design (≥12) → 3. Review → 4. Model data → 5. Map automation → 6. Generate → 7. Verify  
Append stages to `docs/ai-conversion-log.md` under a **Feature B** section (do not replace Feature A stages).
