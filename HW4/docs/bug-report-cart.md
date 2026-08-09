# Bug Report — FR-07 (Shopping Cart)

**Student ID:** 23127207 · **Reproduced by:** `tests/cart.spec.ts`, `tests/cart-api.spec.ts`  
**Execution evidence:** Chromium, Firefox, and WebKit each ran the full 63-case suite and produced
the identical result **29 passed / 34 failed / 63**. Reports:
`HW4/reports/cart/{chromium,firefox,webkit}/index.html`, each labeled `Run by: 23127207` with an
ISO timestamp.

An earlier run surfaced a test-isolation bug (two edge cases mutated the shared seed product
catalog without restoring it, contaminating a later browser's run with stale data) — fixed by
switching those cases to a disposable, self-cleaning product; see `docs/ai-review-cart.md` §3.

> **GitHub Issues status:** this environment has no `gh` CLI and no `GITHUB_TOKEN`. The existing
> HW02 issue links are preserved in `docs/hw02-reference/tests/issues_list.txt`; the new findings
> below are ready to file manually or with a supplied token.

## A. Previously known bugs reproduced

| # | Bug ID | Reproducing cases | Actual result |
|---:|---|---|---|
| 1 | `BUG-FR07-B-01` | `TC-CART-043`, `044`, `045` | API returns `200` for quantity `0`, `-3`, and `1.5`; invalid items are accepted |
| 2 | `BUG-FR07-B-04` | `TC-CART-023` | No `+/-` quantity controls exist in the cart row |
| 3 | `BUG-FR07-B-05` | `TC-CART-030` | Delete runs without a native confirmation dialog |
| 4 | `BUG-FR07-B-06` | `TC-CART-008` | Total label is “Tổng tạm tính”, not “Tổng cộng” |
| 5 | `BUG-FR07-B-07` | `TC-CART-002` | Empty cart has no icon/image illustration |
| 6 | `BUG-FR07-B-08` | `TC-CART-004` | Breadcrumb is absent |
| 7 | `BUG-FR07-B-10` | `TC-CART-046`, `057`, `058`, `062` | Missing quantity/id/price and tampered name are accepted |
| 8 | `BUG-FR07-B-11` | `TC-CART-038` | No success toast/alert appears after add |
| 9 | `BUG-FR07-B-12` | `TC-CART-060` | No stock information or over-stock warning is shown |
| 10 | `BUG-FR07-B-13` | `TC-CART-059`, `063`, `080`, `088-CHECKOUT-TAMPER` | Client-provided price/checkout total is trusted |
| 11 | `BUG-FR07-B-14` | `TC-CART-061` | Product ID `999999` is accepted and stored |
| 12 | `BUG-FR07-B-15` | `TC-CART-045` | Quantity type is not validated by the API |
| 13 | `BUG-FR07-B-16` | `TC-CART-070` | Extra fields, including `isAdmin`, survive in the stored cart item |
| 14 | `BUG-FR07-B-17` | `TC-CART-076` | Empty checkout submit control is enabled |
| 15 | `BUG-FR07-B-19` | `TC-CART-089` | Successful checkout leaves the cart populated |

## B. New findings isolated by this automation pass

### NEW-BUG-FR07-01 — Product-detail add button ignores the first click

- **Severity:** Medium
- **Cases:** `TC-CART-054`
- **Steps:** Log in, open a product detail page, click `Thêm vào giỏ hàng` once, then inspect the
  cart or the button state.
- **Expected:** One click adds one unit and changes the button state to the success state.
- **Actual:** The first click only sets an internal counter and returns. The item is not added;
  a second click is required.
- **Evidence:** `frontend-web/src/pages/ProductDetail.jsx` contains `if (clickCount === 0) { ...
  return; }`. The report diagnostic for `TC-CART-054` shows the expected `Đã thêm` state was not
  visible after one click.
- **Suggested issue title:** `[BUG][Cart] Product detail ignores the first Add to Cart click`

### NEW-BUG-FR07-02 — React-memory cart disappears after reload or re-login

- **Severity:** Medium
- **Cases:** `TC-CART-072`, `TC-CART-087`
- **Steps:** Add a product, reload the page or log out and back in, then open `/cart`.
- **Expected:** The cart remains available, or the product is restored from a documented persistent
  source and the user is told if restoration is impossible.
- **Actual:** The cart is empty after the `CartProvider` remounts.
- **Evidence:** `frontend-web/src/context/CartContext.jsx` initializes `useState([])` and has no
  localStorage or server synchronization. The Chromium report contains failures for both cases.
- **Suggested issue title:** `[BUG][Cart] Cart contents are lost after page reload and re-login`

### NEW-BUG-FR07-03 — Product-detail quantity has no client-side validation

- **Severity:** High
- **Cases:** `TC-CART-017`, `018`, `019`, `022`
- **Steps:** On a product detail page, enter `0`, `-5`, `1.5`, or an empty value and click add.
- **Expected:** The UI rejects the value, keeps the cart empty, and shows a useful validation
  message.
- **Actual:** `parseInt(quantity)` is passed directly into `addToCart`; the cart can receive an
  invalid, zero, negative, or `NaN` quantity. The Chromium report shows the expected empty-cart
  message was not visible for the invalid numeric inputs.
- **Evidence:** `frontend-web/src/pages/ProductDetail.jsx` performs no finite/integer/positive
  check before calling `addToCart`. The API has the related known validation defect
  `BUG-FR07-B-01`.
- **Suggested issue title:** `[BUG][Cart][Validation] Product-detail quantity accepts zero, negative, fractional, and empty values`

## C. Testability note — not filed as a product bug

`TC-CART-020` and `TC-CART-021` attempt `abc` and `!@#` through an HTML
`input[type=number]`. The browser rejects those characters before the React handler receives them,
so Playwright's `fill()` raises `Cannot type text into input[type=number]`. This is a limitation of
the UI test data/control combination, not evidence that the SUT accepted the invalid strings. The
API case `TC-CART-066` covers string quantity at the server boundary without this limitation.

## D. Filing note

The ready-to-file titles and evidence above are intentionally separate from the known HW02 bug
IDs. No GitHub issue was created automatically because the environment does not provide the
required CLI/token.
