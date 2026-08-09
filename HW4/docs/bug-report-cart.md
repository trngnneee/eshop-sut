# Bug Report — FR-07 (Shopping Cart)

**Student ID:** 23127207 · **Reproduced by:** `tests/cart.spec.ts`, `tests/cart-api.spec.ts`  
**Execution evidence:** Chromium, Firefox, and WebKit each ran the full 92-case suite and produced
the identical result **46 passed / 46 failed / 92**. Reports:
`HW4/reports/cart/{chromium,firefox,webkit}/index.html`, each labeled `Run by: 23127207` with an
ISO timestamp.

An earlier run surfaced a test-isolation bug (two edge cases mutated the shared seed product
catalog without restoring it, contaminating a later browser's run with stale data) — fixed by
switching those cases to a disposable, self-cleaning product; see `docs/ai-review-cart.md` §3.

> **GitHub Issues status:** all 7 new findings below have been filed as real GitHub Issues
> (#322–#324, #328, #336–#337, #339) with screenshot evidence attached. The existing HW02 issue
> links for previously-known bugs are in `docs/hw02-reference/tests/issues_list.txt`.

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
- **GitHub Issue:** https://github.com/trngnneee/eshop-sut/issues/322 (screenshot attached)

### NEW-BUG-FR07-02 — React-memory cart disappears after reload or re-login

- **Severity:** Medium
- **Cases:** `TC-CART-072`, `TC-CART-087`
- **Steps:** Add a product, reload the page or log out and back in, then open `/cart`.
- **Expected:** The cart remains available, or the product is restored from a documented persistent
  source and the user is told if restoration is impossible.
- **Actual:** The cart is empty after the `CartProvider` remounts.
- **Evidence:** `frontend-web/src/context/CartContext.jsx` initializes `useState([])` and has no
  localStorage or server synchronization. The Chromium report contains failures for both cases.
- **GitHub Issue:** https://github.com/trngnneee/eshop-sut/issues/323 (screenshot attached)

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
- **GitHub Issue:** https://github.com/trngnneee/eshop-sut/issues/324 (screenshot attached)

### NEW-BUG-FR07-04 — Cart is not synced across browser tabs

- **Severity:** Medium
- **Cases:** `TC-CART-050`
- **Steps:** Log in and add a product in one tab; open the cart page in a second tab of the same
  logged-in session.
- **Expected:** The item added in the first tab is visible in the second tab.
- **Actual:** The second tab shows an empty cart.
- **Evidence:** `frontend-web/src/context/CartContext.jsx` has no `localStorage`,
  `BroadcastChannel`, or server sync — every tab's `CartProvider` is an independent in-memory
  instance. Distinct from `NEW-BUG-FR07-02` (that one is sequential reload/re-login; this one is
  two tabs open concurrently in the same session).
- **GitHub Issue:** https://github.com/trngnneee/eshop-sut/issues/328 (screenshot attached)

### NEW-BUG-FR07-05 — `GET /api/orders/:id` has no authentication or ownership check (IDOR)

- **Severity:** High (broken access control — OWASP A01)
- **Cases:** `TC-CART-095`
- **Steps:** Check out as any user to get a real `orderId`, then `GET /api/orders/:id` with no
  `Authorization` header at all.
- **Expected:** `401`/`403` — viewing an order requires authentication and ownership (or admin).
- **Actual:** `200` with the full order body (`shipping_address`, `total_amount`, `status`,
  `user_id`). Unlike every other `/api/orders*` route, this one has no `authenticateToken`
  middleware and no ownership comparison — any numeric id can be enumerated.
- **GitHub Issue:** https://github.com/trngnneee/eshop-sut/issues/336 (screenshot attached)

### NEW-BUG-FR07-06 — Customer can cancel an order that is already `shipping`

- **Severity:** Medium (broken state guard)
- **Cases:** `TC-CART-096`
- **Steps:** Check out, have an admin advance the order to `shipping`, then call
  `PUT /api/orders/:id/cancel` with the owning customer's own token.
- **Expected:** `400` — only `pending`/`confirmed` orders should be customer-cancelable.
- **Actual:** `200 Order canceled successfully`. The handler only blocks `delivered`/`canceled`;
  its own source comment documents the intended, stricter condition (`!== 'pending' && !==
  'confirmed'`), confirming this is a known-wrong condition left in place.
- **GitHub Issue:** https://github.com/trngnneee/eshop-sut/issues/337 (screenshot attached)

### NEW-BUG-FR07-07 — `POST /api/checkout` performs no validation

- **Severity:** Medium (data integrity)
- **Cases:** `TC-CART-097` (missing `total_amount`), `TC-CART-098` (negative `total_amount`),
  `TC-CART-099` (missing `shipping_address`)
- **Steps:** Call checkout with each field missing/invalid in turn.
- **Expected:** `4xx` validation error for each.
- **Actual:** All three return `200 Checkout successful` and create a real order row with the
  invalid/missing data as-is.
- **Evidence:** The checkout handler inserts `req.body.total_amount`/`shipping_address` directly
  with no validation — a distinct facet of the same trust-the-client family as `BUG-FR07-B-13`,
  but about missing/invalid fields rather than merely attacker-controlled ones.
- **GitHub Issue:** https://github.com/trngnneee/eshop-sut/issues/339 (screenshot attached)

## C. Testability note — not filed as a product bug

`TC-CART-020` and `TC-CART-021` attempt `abc` and `!@#` through an HTML
`input[type=number]`. The browser rejects those characters before the React handler receives them,
so Playwright's `fill()` raises `Cannot type text into input[type=number]`. This is a limitation of
the UI test data/control combination, not evidence that the SUT accepted the invalid strings. The
API case `TC-CART-066` covers string quantity at the server boundary without this limitation.

## D. Filing note

The 7 new findings above are intentionally numbered separately from the known HW02 `BUG-FR07-B-*`
IDs and have been filed as GitHub Issues #322–#324, #328, #336–#337, #339, each with a screenshot
generated from a real failing run attached as evidence. `NEW-BUG-FR07-05`, `-06`, and `-07` were
found by a deliberate source review of the checkout/order endpoints (`ai-review-cart.md` §3d/§3e)
rather than by adding more UI-level coverage — a related coupon-limit-bypass observation was found
the same way but deliberately *not* filed here, since coupons are outside FR-07's scope.
