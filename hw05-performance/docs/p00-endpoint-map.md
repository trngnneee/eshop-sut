# P00 — Search-to-buy endpoint map (23127271)

**Gate:** P00 only (no thread counts, CSV rows, listeners, or JMeter XML).  
**Student:** 23127271 · **Workflow:** Search-to-buy  
**Base URL:** `http://localhost:3000`  
**Confirmed against:** `backend/server.js` (lines cited below)  
**Out of scope:** register, forgot-password, `GET /api/categories`, `POST /api/apply-coupon`, `GET /api/orders/my-orders`, admin.

---

## 1. Request sequence table

Same VU path for Load, Stress, and Spike. Think-time bands below are **Load pacing** from frozen scope; Stress/Spike will shorten them in P01 — not designed here.

| Step | Method | Path | Headers | Body fields | JSON extractors | Think-time band | Assertions (status **and** JSON field) |
|------|--------|------|---------|-------------|-----------------|-----------------|----------------------------------------|
| 1. Login | `POST` | `/api/login` | `Content-Type: application/json` | `email`, `password` (from CSV) | `$.token` → `token`; `$.user.id` → `user_id` | 1–2 s after response | **200** and JSON `token` present (string). Fail on **401** `{error}` (bad creds) or **403** `{error}` (locked). Do not treat 403 as “system down.” |
| 2. Search | `GET` | `/api/products?search=${search}` | none (public; JWT not required) | — | Optional sanity: `$[0].id` → `search_hit_id`. **Do not** replace CSV `product_id` with this unless the hit’s `id` matches the CSV row. | 1–3 s | **200** and body is a **JSON array**. Array may be empty if `search` does not substring-match `products.name` (see SUT facts). Do not assert a non-empty array until CSV keywords are verified against seed **names**. |
| 3. Detail | `GET` | `/api/products/${product_id}` | none (public) | — | Optional: `$.name` → `product_name`; `$.price` → `product_price` (type may be number **or** string) | 1–2 s | **200** **and** JSON `name` present (and `id`). **Fail if body is `{}`** — missing id still returns HTTP 200 with empty object (`server.js` L159–164). Do **not** treat empty `{}` as a found product. Do **not** assert `price` is a number: even `id` values stringify `price`. |
| 4. Add to cart | `POST` | `/api/cart` | `Content-Type: application/json`; `Authorization: Bearer ${token}` | CSV: `product_id`, `quantity`, `name` (or extracted `product_name`), `price` — handler `push`es entire `req.body` | none | ~1 s | **200** and JSON `message` equals `Added to cart`. Fail on **401** (missing Bearer) or **403** (bad JWT). |
| 5. Checkout | `POST` | `/api/checkout` | `Content-Type: application/json`; `Authorization: Bearer ${token}` | `total_amount`, `shipping_address` | Optional: `$.orderId` → `order_id` (not reused; my-orders is out of scope) | none after last step (or 0–1 s before loop) | **200** and JSON `orderId` present. Do **not** pass on 200 + `{message}` without `orderId`. |

**Auth header after step 1:** `Authorization: Bearer ${token}` (`authenticateToken` splits on space and takes the second token — `server.js` L100–109). Cookie manager is not required.

**JWT is required only on steps 4–5.** Steps 2–3 are unauthenticated reads; login still runs first so every VU exercises the auth-heavy endpoint and carries a token into the transactional steps.

---

## 2. Coverage sentences (three groups)

**Auth-heavy** is step 1, `POST /api/login` (`server.js` L32–66): it issues a JWT, resets or increments `login_attempts`, and can return 401/403. That is the only auth-cost and lockout surface in this workflow.

**Read-heavy** is steps 2–3: `GET /api/products?search={q}` runs a SQLite `LIKE` on every search (`server.js` L141–151), then `GET /api/products/{id}` is a keyed lookup (`server.js` L159–165). Together they are the catalog-read load; search is the distinguishing read, not a full table dump.

**Transactional** is steps 4–5: `POST /api/cart` mutates the in-memory `userCarts` map (`server.js` L290–295) and `POST /api/checkout` `INSERT`s into SQLite `orders` (`server.js` L297–308). This is not Khoa’s browse-to-buy: Khoa’s read step is `GET /api/products` with **no** `search` query (full list). This workflow always sends `?search=${search}` and never calls categories, coupon, or my-orders.

---

## 3. SUT facts that will break a naive load test

1. **Lockout is `+= 2` and 180 s, not FR-02’s “3 fails / 30 s.”** A failed password does `login_attempts + 2` (`server.js` L54–57). After **two** failures (`2` then `4 >= 3`) the account sets `locked_until` to now+**180000 ms** and later logins return **403** until that timestamp. Shared seed `test@eshop.com`, recycled wrong passwords, or Stress designed as “hammer failed logins” will lock the pool and measure lockout, not checkout capacity. Successful login resets attempts to 0 (`server.js` L47–50).

2. **Cart is process memory, not SQLite.** `userCarts` is a module-level object (`server.js` L14, L290–295). `POST /api/cart` does not validate that `product_id` exists; it appends `req.body`. Restarting Node empties every cart. Checkout does **not** read or clear the cart — it only inserts `total_amount` + `shipping_address`. A soak that keeps adding line items will grow heap in the Node process even if order rows look healthy.

3. **Search is unsanitized `LIKE` interpolation on `name` only.** Query is `` SELECT * FROM products WHERE name LIKE '%${searchQuery}%' `` (`server.js` L144). CSV keywords must be substrings of seed **product names**, not category labels. Seed names are `iPhone 15 Pro Max`, `Samsung Galaxy S24 Ultra`, `MacBook Pro M3`, `Tai nghe AirPods Pro 2`, `Bàn phím cơ Keychron Q1` (`database.js` L98–102). The word **`Laptop` is a category name, not a product name** — `?search=Laptop` returns `[]`. SQL metacharacters in `search` can 500 with an HTML error page (`server.js` L146–149), which a JSON assertion will fail.

4. **Missing product id returns `200` + `{}`.** `GET /api/products/:id` does `if (!row) return res.status(200).json({})` (`server.js` L161). A status-only assertion marks a wrong `product_id` as success. Even existing ids with `id % 2 === 0` coerce `price` to a **string** (`server.js` L162) — assert `name` (and reject `{}`), not a numeric `price` type.

---

## Confirmed path list (this workflow only)

| In | Path | `server.js` |
|----|------|-------------|
| yes | `POST /api/login` | L32 |
| yes | `GET /api/products?search=` | L141–151 (`searchQuery` branch) |
| yes | `GET /api/products/:id` | L159 |
| yes | `POST /api/cart` | L290 |
| yes | `POST /api/checkout` | L297 |
| **no** | `GET /api/products` (no query) | Khoa only |
| **no** | `GET /api/categories` | Nguyên |
| **no** | `POST /api/apply-coupon` | Thịnh |
| **no** | `GET /api/orders/my-orders` | Bảo |

**Stop condition met:** endpoint table + 3 coverage sentences. Next gate is P01 (parameters only), after human verdict on this file.
