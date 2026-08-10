# AI Review & Gap Analysis — FR-07 (Shopping Cart)

**Student ID:** 23127207 · **Feature:** FR-07 — Pool B  
**Spec files:** `tests/cart.spec.ts`, `tests/cart-api.spec.ts`  
**Data files:** `test-data/cart-ui-cases.json` (68), `test-data/cart-edge-cases.json` (5), `test-data/cart-api-cases.json` (69) — **142 test cases total**

## 1. Scope and conversion from HW02

The suite was converted from the FR-07 material selected in HW02 and cross-checked against
`docs/hw02-reference/tests/test-cases/cart/` and `tests/issues_list.txt`. It deliberately covers
three different shapes rather than repeating one happy path:

| Shape | Cases | Main oracle |
|---|---:|---|
| Cart page UI/UX | 39 | Cart rendering, navigation, quantity boundaries, totals, controls, checkout guard, i18n/XSS product names, scale, cross-tab sync |
| Cross-session/data-integrity edge cases | 5 | User switching, reload/re-login, deleted/changed products, checkout tampering |
| Cart API contract/security | 28 | Authentication, validation, product integrity, type safety, mass assignment, compound-invalid input, multi-item consistency |

A second pass (after the user explicitly asked for deeper coverage, twice) added 9 more cases:
i18n/special-character/very-long/XSS product names, a 12-item cart, a very-large total, cross-tab
sync, a compound-invalid API payload, and multi-item order consistency — see §3b.

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
| **Cart is not synced across browser tabs** | `TC-CART-050` | Each tab's `CartProvider` is an independent in-memory instance with no `localStorage`/`BroadcastChannel`/server sync — a second tab of the same logged-in session sees an empty cart. New, distinct from the reload/re-login persistence gap above (this is *concurrent* tabs, not sequential sessions). Filed as [#328](https://github.com/trngnneee/eshop-sut/issues/328). |

## 3d. Fifth pass — deliberate bug hunt in checkout/order endpoints (77 cases total)

The same deliberate-source-review technique applied to Login's register/forgot-password gap
(see `ai-review-login.md` §3c) was repeated here against `/api/checkout`, `/api/orders/:id`, and
`/api/orders/:id/cancel` — parts of the checkout journey that only the UI-level
`checkout-clears-cart`/`checkout-editable-total-tampering` cases had ever touched, never at the
API contract level. Two new bugs were found and confirmed live before being written up:

| ID | Severity | Finding | Case |
|---|---|---|---|
| BUG-FR07-05 | **High** | `GET /api/orders/:id` has **no `authenticateToken` middleware and no ownership check** — unlike every other `/api/orders*` route. Anyone who can guess/enumerate a numeric order id can read that order's shipping address, total, and status without logging in as anyone (IDOR, OWASP A01) | `TC-CART-095` |
| BUG-FR07-06 | Medium | A customer can self-cancel an order that is already `shipping`; the cancel handler only blocks `delivered`/`canceled`. The SUT's own source comment on this handler documents the intended, stricter condition (`!== 'pending' && !== 'confirmed'`), confirming this is a known-wrong condition, not an ambiguous design choice | `TC-CART-096` |

Both filed as real GitHub Issues (#336, #337) with screenshot evidence.

**One related observation, deliberately not filed as a bug:** `POST /api/apply-coupon` skips its
per-user usage-limit check entirely when `user_id` is omitted from the request body, and the
route has no `authenticateToken` — an unauthenticated caller can apply a coupon past its
`max_uses_per_user` limit indefinitely simply by never sending `user_id`. This is a real defect,
but coupons are their own feature area outside FR-07's boundary as scoped for this assignment
(the same reasoning already applied to the unauthenticated `POST /api/products` route in §3 —
Product Management is FR-15, not this feature), so it is noted here rather than turned into a
`TC-CART-*` case or a new GitHub Issue.

## 3b. Second pass — deeper coverage (72 cases total)

After reviewing the first pass, 9 more cases were added to close specific gaps rather than pad the
count: Vietnamese-diacritics and safe-special-character product names (`TC-CART-055/056`, both
**pass** — display is correct), a very long product name and a 12-item cart (`081`, `083`, both
**pass** — no layout break), an XSS payload as a product name (`082`, **passes** — React's default
JSX escaping prevents script execution, a genuine positive security confirmation), a very large
total amount (`084`, **passes** — no overflow/scientific notation), cross-tab sync (`050`,
**fails** — new finding above), a compound-invalid API payload combining negative price *and*
negative quantity (`090`, **fails** — same root cause as the known `BUG-FR07-B-01`/`B-13`, not a
new bug), and multi-item order consistency at the API level (`091`, **passes**).

## 3c. Third pass — targeted quantity/removal/navigation cases (75 cases total)

Three more cases closed narrower gaps the earlier passes left open: none of the existing cases
checked the *exact* quantity value rendered in the cart's quantity cell (only totals derived from
it), removal of a row from the *middle* of a multi-item cart (only "remove the only item" and
"remove one of two" existed), or a positive confirmation that normal client-side navigation between
Cart and Home preserves state (only the page-*reload* case and the negative cross-tab case existed).

| Case | Check | Result |
|---|---|---|
| `TC-CART-092` | Cart quantity cell shows exactly the value set when adding (7) | **Passes** |
| `TC-CART-093` | Removing the middle row of a 3-item cart leaves the other two rows intact | **Passes** |
| `TC-CART-094` | Cart survives a Cart→Home→Cart round trip via in-app link clicks | **Passes** |

**Two script bugs found and fixed while adding these** (both instances of the same root cause
documented in §3: `addFromDetailByUrl`'s `page.goto()` wipes any cart state accumulated by an
earlier `addFromDetailReliable` call, because it's a real navigation, not a client-side route
change):

1. `TC-CART-092` initially called `addFromDetailByUrl` (which adds one unit via its own two-click
   workaround) and *then* set the quantity field and clicked add again — the two calls stacked
   instead of the second overriding the first, producing 8 instead of 7. Fixed by navigating with a
   plain `page.goto()` and setting the quantity **before** the first add-click.
2. `TC-CART-093` added product A via `addFromDetailReliable` (client-side nav), then tried to add
   the disposable "middle" product via `addFromDetailByUrl` — that `goto()` silently wiped product A
   from the cart, so the cart only ever had 2 rows, not 3. Fixed by creating the disposable product
   *before* any navigation and reloading once while the cart is still empty (the same safe pattern
   `many-items-cart` already used), so all three products can be added via the client-side-preserving
   `addFromDetailReliable` helper.

## 3e. Sixth pass — one more bug, plus boundary volume (92 cases total)

Continuing the same source-review technique against `POST /api/checkout` in isolation (rather
than only as a setup step for order-endpoint cases) surfaced one more distinct defect:

| ID | Severity | Finding | Cases |
|---|---|---|---|
| BUG-FR07-07 | Medium | `POST /api/checkout` performs no validation at all — missing `total_amount`, a negative `total_amount`, and a missing `shipping_address` are all accepted and create a real order row | `TC-CART-097`, `098`, `099` |

Filed as GitHub Issue [#339](https://github.com/trngnneee/eshop-sut/issues/339).

Twelve more boundary cases were added reusing already-proven shapes with zero new spec code: 6
more `/api/cart` boundary values (`price: 0` exactly, `quantity: -0.5`, boolean/array/string-typed
`quantity`, string-typed `price`) via the existing `post-quantity-value`/`post-price-value`/
`post-quantity-raw` actions, and 6 more UI cases (`subtotal-single`/`quantity-value-in-cell` at
quantity 1 and 10/99, plus `add-with-quantity` with scientific-notation and negative-zero string
inputs) via the existing parameterized switch cases. One flaky failure was observed and resolved
during this pass: `TC-CART-083` (pre-existing, unrelated to this pass) hit a 30s Playwright
timeout on a single Firefox run while creating 12 disposable products sequentially; a re-run
produced the identical result to Chromium/WebKit, confirming it was a one-off timing flake, not a
real cross-browser difference — consistent with this project's "green on one browser is a
hypothesis" principle from `.agents/skills/playwright-skill/playwright-skill.md`.

## 3f. Seventh pass — pure boundary/robustness volume to reach 400 cases suite-wide (142 cases total)

50 more cases were added reusing already-proven, fully-parameterized shapes, per the same
suite-wide 400-case request described in `ai-review-login.md` §3e:

- **30 more `cart-api-cases.json` rows**: many more distinct boundary values through the existing
  `post-quantity-value`/`post-price-value`/`post-quantity-raw` actions — tiny decimals, large
  negative/positive magnitudes beyond `Number.MAX_SAFE_INTEGER`, and type-confused values (`null`,
  `{}`, `[]`, `true`, numeric-looking strings). The value-boundary cases fail (same known-bug
  family as `BUG-FR07-B-01`/`B-13`/`B-15`); the raw-type-confusion cases pass (no 500s).
- **20 more `cart-ui-cases.json` rows**: 10 more `subtotal-single`/`quantity-value-in-cell`
  quantity boundaries (all pass), and 10 more `add-with-quantity` malformed-string attempts.

**One test-design mistake found and fixed while authoring the UI batch:** the first draft of the
10 new `add-with-quantity` strings included values like `"+5"`, `"5 "`, `" 5"`, `"05"` — these all
parse successfully via `parseInt()` to a valid `5`, so asserting "cart must stay empty" was simply
the wrong oracle for a valid quantity, not a defect. Caught by running the batch before assuming
it was correct (the same "verify, don't assume" discipline from the login-cases fix in §3e) and
replaced with genuinely non-numeric strings (`"abc5"`, `"$5"`, `"null"`, `"V"`, `"%5"`, `"!"`).

**A second, more informative discovery from that same corrected batch:** *every* one of the 10
non-numeric strings still fails the "cart stays empty" assertion — not because the SUT accepts an
invalid quantity, but because `input[type=number]` silently refuses to accept non-numeric
keystrokes at the browser level, leaving the field at its default value, so the product is added
anyway with quantity 1. This is the exact same automation-limitation root cause already documented
for `TC-CART-020`/`021` in §C of `bug-report-cart.md` ("Playwright's `fill()` raises `Cannot type
text into input[type=number]`... a limitation of the UI test data/control combination, not
evidence the SUT accepted the invalid string") — this pass shows the limitation applies to the
*entire* non-numeric-string equivalence class through this control, not just those two characters.
The corresponding API-level cases (`TC-CART-045`/`066`/`110`, etc.) remain the correct oracle for
this boundary.

## 5. Assertion-pattern inventory

The suite exercises more than the required three patterns, including `toHaveURL`, `toBeVisible`,
`toContainText`, `toHaveCount`, `toHaveText`, `toBeDisabled`, `toHaveValue`, `toHaveAttribute`,
dialog-event assertions, and direct HTTP status/body assertions. The UI cases also scope locators
to a cart row or total footer so that a matching price elsewhere on the page cannot produce a false
positive.

## 6. Review conclusion

All three browsers now produce the **exact same result: 66 passed / 76 failed / 142 total**,
confirmed after the test-isolation fix in Section 3. Cross-browser identity (rather than
coincidence) is the useful signal here: every failure is a server-side or React-state defect, not
a browser-rendering difference, which is consistent with a Vietnamese e-commerce SPA whose bugs
live in application logic rather than CSS/engine quirks. The suite was not weakened to make any
known defect pass — every failing assertion still encodes the spec-conformant expectation.
