# AI Review & Gap Analysis — FR-07 (Shopping Cart)

**Student ID:** 23127207 · **Feature:** FR-07 — Pool B  
**Spec files:** `tests/cart.spec.ts`, `tests/cart-api.spec.ts`  
**Data files:** `test-data/cart-ui-cases.json` (32), `test-data/cart-edge-cases.json` (5), `test-data/cart-api-cases.json` (26) — **63 test cases total**

## 1. Scope and conversion from HW02

The suite was converted from the FR-07 material selected in HW02 and cross-checked against
`docs/hw02-reference/tests/test-cases/cart/` and `tests/issues_list.txt`. It deliberately covers
three different shapes rather than repeating one happy path:

| Shape | Cases | Main oracle |
|---|---:|---|
| Cart page UI/UX | 32 | Cart rendering, navigation, quantity boundaries, totals, controls, checkout guard |
| Cross-session/data-integrity edge cases | 5 | User switching, reload/re-login, deleted/changed products, checkout tampering |
| Cart API contract/security | 26 | Authentication, validation, product integrity, type safety, mass assignment |

The data files are external JSON arrays. The loaders validate that each file exists, contains an
array, has the required minimum size, and has no duplicate `caseId`. The tests annotate every case
with `Run by: 23127207` and preserve the original bug reference when one exists.

## 2. Important repair made before this review

`CartContext` stores the cart only in React memory. A second `page.goto()` remounts the SPA and
silently clears the cart. The first Cart draft used real navigations between setup steps, which
made otherwise valid cases fail for the wrong reason. The current spec keeps the cart alive by
clicking the EShop link and in-app product/cart links (`gotoHome`, `gotoProductDetail`, and
`gotoCart`). A real reload is used only by the persistence case, where losing the cart is the
behavior under test.

The product-detail page also contains a known first-click defect: `handleAddToCart()` returns
without adding when `clickCount === 0`. Setup helpers therefore use two clicks for cases that are
not testing that defect; `TC-CART-054` tests the single-click behavior directly. This workaround
is intentionally local to test setup and does not change the SUT.

## 3. A second repair found only by running on more than one browser

The first full 3-browser attempt exposed a real test-isolation bug that Chromium alone could not
reveal: `cart-with-price-changed-product` called `PUT /api/products/1` to lower the seed iPhone's
price to `1 ₫` and never restored it, and `cart-with-deleted-product` permanently `DELETE`d seed
product `5`. Because the SUT backend is a single long-lived process shared across all three browser
runs, Chromium's run silently mutated the catalog that Firefox's run then inherited — Firefox
failed `TC-CART-007`, `026`, `029`, and `078` for the wrong reason (`PRODUCT_A_PRICE` no longer
matched reality), not because of anything Firefox itself did differently.

Fix: both cases now create a disposable product via `POST /api/products` (public, no auth check —
itself a minor access-control observation, not filed as a bug since Product Management is FR-15,
outside this feature's scope), operate only on that product, and delete it afterward. A new
`addFromDetailByUrl` helper navigates to the freshly created product by URL instead of clicking its
home-page card, because Home's product grid is fetched once on mount and a same-route client-side
"navigation" does not refetch it — a brand-new product's card would not exist yet to click.

After the fix, Chromium and Firefox produced byte-for-byte identical pass/fail sets (see below),
and the backend was restarted once (clean reseed) before the corrected suite's first run to purge
the earlier mutation.

## 4. What the 3-browser run found

### 4.1 Previously known HW02 bugs reproduced

| Bug | Reproducing cases in the report | Interpretation |
|---|---|---|
| `BUG-FR07-B-01` | `TC-CART-043`, `044`, `045` | API accepts zero, negative, and fractional quantities instead of rejecting them |
| `BUG-FR07-B-04` | `TC-CART-023` | Cart has no quantity increment/decrement or direct quantity control |
| `BUG-FR07-B-05` | `TC-CART-030` | Removing a row does not show a confirmation dialog |
| `BUG-FR07-B-06` | `TC-CART-008` | UI says “Tổng tạm tính” where the specification requires “Tổng cộng” |
| `BUG-FR07-B-07` | `TC-CART-002` | Empty state has no illustrative icon/image |
| `BUG-FR07-B-08` | `TC-CART-004` | Cart page has no breadcrumb navigation |
| `BUG-FR07-B-10` | `TC-CART-046`, `057`, `058`, `062` | Missing or tampered product fields are accepted as supplied by the client |
| `BUG-FR07-B-11` | `TC-CART-038` | Successful add has no toast/alert feedback |
| `BUG-FR07-B-12` | `TC-CART-060` | Stock quantity and over-stock warning are absent |
| `BUG-FR07-B-13` | `TC-CART-059`, `063`, `080`, `088-CHECKOUT-TAMPER` | Client-controlled price/total is trusted; changed catalog prices are not reconciled |
| `BUG-FR07-B-14` | `TC-CART-061` | A nonexistent product ID is accepted by `POST /api/cart` |
| `BUG-FR07-B-15` | `TC-CART-045` | `quantity` type is not validated at the API boundary |
| `BUG-FR07-B-16` | `TC-CART-070` | Extra fields such as `isAdmin` and `discount` are stored through mass assignment |
| `BUG-FR07-B-17` | `TC-CART-076` | Empty checkout is reachable and its submit control is enabled |
| `BUG-FR07-B-19` | `TC-CART-089` | Successful checkout does not clear the in-memory cart |

The duplicate-ID positive case passed at the API level, while the frontend duplicate merge case
also passed because `CartContext` merges by product ID. This distinction is useful: the old
`BUG-FR07-B-02/B-03` behavior was not reproduced by the current selected cases.

### 4.2 New or newly isolated findings

| Finding | Cases | Evidence and impact |
|---|---|---|
| First add click is swallowed | `TC-CART-054` | `ProductDetail.jsx` explicitly returns on the first click. A user must click twice before the product is added. This is a functional defect not represented by a `bugRef` in the selected JSON. |
| Cart persistence is not implemented | `TC-CART-072`, `TC-CART-087` | The cart is held only in `useState`; re-login/reload remounts `CartProvider` and loses the item. This is a cross-session/data-persistence gap, distinct from the post-checkout cleanup bug. |
| Frontend quantity validation is missing | `TC-CART-017`, `018`, `019`, `022` | `ProductDetail.jsx` calls `parseInt(quantity)` without checking integer, positivity, or finite value. Invalid numeric values can still be inserted into `CartContext`, producing a non-empty cart when the expected result is rejection. The API manifestation is the known `BUG-FR07-B-01`. |
| Two nonnumeric UI values were not injectable through the real control | `TC-CART-020`, `021` | Playwright fails before the assertion because HTML `input[type=number]` rejects `abc` and `!@#`. These are automation/data-model limitations, not valid SUT failures. The API type-validation case remains the stronger oracle for this boundary. |

## 5. Assertion-pattern inventory

The suite exercises more than the required three patterns, including `toHaveURL`, `toBeVisible`,
`toContainText`, `toHaveCount`, `toHaveText`, `toBeDisabled`, `toHaveValue`, `toHaveAttribute`,
dialog-event assertions, and direct HTTP status/body assertions. The UI cases also scope locators
to a cart row or total footer so that a matching price elsewhere on the page cannot produce a false
positive.

## 6. Review conclusion

All three browsers now produce the **exact same result: 29 passed / 34 failed / 63 total**,
confirmed after the test-isolation fix in Section 3. Cross-browser identity (rather than
coincidence) is the useful signal here: every failure is a server-side or React-state defect, not
a browser-rendering difference, which is consistent with a Vietnamese e-commerce SPA whose bugs
live in application logic rather than CSS/engine quirks. The suite was not weakened to make any
known defect pass — every failing assertion still encodes the spec-conformant expectation.
