# FR-13 Playwright requirement ledger

**Student ID:** `23127207`  
**Feature:** FR-13 — EShop Admin Dashboard  
**Source priority:** the existing HW02 FR-13 test-case pool and bug reports under `docs/hw02-reference/`, cross-checked against `frontend-admin/src/App.jsx` and `backend/server.js`.

## Contract

FR-13 covers the admin dashboard UI and the admin endpoints that supply or mutate its data:

| Requirement area | Observable acceptance criteria | Automated cases | Data / spec |
|---|---|---|---|
| Dashboard access | Guests and regular users cannot use the admin dashboard; an admin can reach the dashboard | `TC-DASHBOARD-LOGIN-001`, `TC-DASHBOARD-ACL-001`–`006`, `008` | `dashboard-data-cases.json` / `dashboard-api-cases.json`; `dashboard.spec.ts` / `dashboard-api.spec.ts` |
| Metrics | Order count includes every order; revenue includes delivered orders exactly once and excludes other states | `TC-DASHBOARD-DT-*`, `TC-DASHBOARD-BVA-*`, `TC-DASHBOARD-STATE-*` in the UI data file | `dashboard-data-cases.json`; `dashboard.spec.ts` |
| Data robustness | Null, negative, decimal, zero, large, mixed, empty and network-failure inputs have an explicit oracle | `TC-DASHBOARD-BVA-*`, `TC-DASHBOARD-DT-*`, `TC-DASHBOARD-RESIL-001` | `dashboard-data-cases.json`; `dashboard.spec.ts` |
| User/order administration | Admin API returns safe user data, validates IDs, preserves ordering/data integrity, and does not leak passwords | `TC-DASHBOARD-USR-*`, `TC-DASHBOARD-ACL-*`, `TC-DASHBOARD-ORD-*` | `dashboard-api-cases.json`; `dashboard-api.spec.ts` |
| Order state machine | Valid transitions succeed; skipped, reverse and terminal-state transitions are rejected and state remains observable | `TC-DASHBOARD-ORD-001`–`019`, `TC-DASHBOARD-STATE-001`–`002` | `dashboard-api-cases.json` / `dashboard-data-cases.json` |

## Requirement ledger

| Feature | Source | Case IDs / count | Data file | Spec file | Browsers | Reports |
|---|---|---:|---|---|---|---|
| FR-13 Admin Dashboard | HW02 FR-13 cases, `backend/server.js`, `frontend-admin/src/App.jsx` | UI/data: 32; API: 36; **68 logical cases** | `test-data/dashboard-data-cases.json`; `test-data/dashboard-api-cases.json` | `tests/dashboard.spec.ts`; `tests/dashboard-api.spec.ts` | Chromium, Firefox, WebKit | `reports/fr13-validation/dashboard/<browser>/` |

The 68 cases are logical cases. Browser repetitions are not counted as additional cases. Every case ID is loaded from JSON at runtime, appears in its generated Playwright title, and is checked for uniqueness and required fields before test discovery completes.

## Automation oracles

The suite intentionally asserts the FR-13 requirement rather than the current defect:

- `toBeVisible` / `toContain` verify the admin login guard, dialog and dashboard shell.
- `expect.poll(...).toBe(...)` verifies the rendered order-count and revenue metrics after UI data has loaded.
- `toBe` / `not.toBe` on HTTP status verifies authentication, authorization, input validation and transition contracts.
- `toBeTruthy`, `toHaveURL`-style navigation assertions where applicable, and typed response comparisons verify data integrity and state reflection.

The primary known product failures are preserved as failures: revenue is doubled by the current admin UI, admin endpoints do not consistently enforce role/ID/self-delete rules, canceled orders can be resurrected, and a failed dashboard sub-request has no user-facing error state.

## Reproduction commands

From `HW4/`, after starting the backend on `http://localhost:3000`, the storefront on `http://localhost:5173`, and the admin app on `http://localhost:5174`:

```powershell
$env:FEATURE = 'dashboard'
$env:REPORT_ROOT = 'reports/fr13-validation'
npx playwright test --list --project=chromium
node scripts/run-matrix.js --feature=dashboard
```

The matrix runner is sequential, preserves reports for failed cells, writes `run-manifest.json` beneath the selected report root, and injects the visible `Run by: 23127207` label with the actual run timestamp into every generated HTML report.
