# Playwright Automation — HW03 EShop GUI

This suite contains **45 tests** across:

- Product Listing `/`: 20 tests in `eshop-product-list.spec.js`.
- Product Detail `/product/1`: 15 tests in `eshop-product-detail-cart.spec.js`.
- Cart `/cart`: 10 tests in `eshop-product-detail-cart.spec.js`.

API calls are mocked with `page.route()` for deterministic data and abnormal states. The React SUT itself is the real frontend source.

## Run

```powershell
cd "GUI testing/automation"
npm install
npx playwright install chromium
npm test
```

Artifacts are kept only for failed assertions:

- `test-results/<test>/test-failed-1.png`
- `test-results/<test>/video.webm`
- `test-results/<test>/trace.zip`
- `playwright-report/index.html`

## Current verification state

The original Product Listing run was verified as 13 Pass / 7 Fail. The additional 25 Product Detail/Cart tests are syntactically prepared but could not run in the managed sandbox because child browser processes return `spawn EPERM`. They must remain `Blocked` until run outside that sandbox.

A Playwright exit code of 1 can be a valid defect-discovery result when expected UI behavior is absent. Review every failed assertion to rule out locator/test-data defects before logging a SUT bug.
