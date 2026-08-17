# Frozen scope — Search-to-buy (23127271)

Do not let AI change this. Used by every gate in [`prompt-plan.md`](./prompt-plan.md).

| Item | Value |
|------|--------|
| Auth-heavy | `POST /api/login` |
| Read-heavy | `GET /api/products?search={q}` → `GET /api/products/{id}` |
| Transactional | `POST /api/cart` → `POST /api/checkout` |
| Out of scope | register, forgot-password, categories, coupon, admin, my-orders |
| Teammate workflows (do not duplicate) | Khoa: list-all browse; Nguyên: categories+search; Thịnh: apply-coupon; Bảo: my-orders |
| CSV | `email,password,search,product_id,quantity,price,total_amount,shipping_address` |
| Plan names | `23127271_Load_20260814.jmx`, `23127271_Stress_20260814.jmx`, `23127271_Spike_20260814.jmx` |
| k6 bonus names | `23127271_Load_20260814.js` (and Stress / Spike / Soak) + matching `logs/*.json` |
| Listeners (one each, no repeat) | Load → View Results Tree · Stress → Summary Report · Spike → Aggregate Report |
| Lockout (implementation, not spec) | each failed login does `login_attempts += 2`; lock when `>= 3` for **180s** (`locked_until`); HTTP **403** while locked |
| Cart | in-memory `userCarts`; `POST /api/cart` pushes `req.body` |
| Search | `LIKE '%{search}%'` (unsanitized — keep CSV keywords clean) |
| Product detail quirk | even `id` returns `price` as string; missing id returns `200` + `{}` |
| Assertions | Login 200 + `$.token`; search 200 + `$[0].id` (reject `[]`); detail 200 + `$.name`/`$.id` (**do not** assert `price` type); cart 200 + `Added to cart`; checkout 200 + `$.orderId`. HTTP timeout 10 s. |

VU sequence (same for Load / Stress / Spike; only load profile changes):

```
1. POST /api/login          → extract token, user.id
2. GET  /api/products?search=${search}
3. GET  /api/products/${product_id}  → extract $.name (and $.price if needed)
4. POST /api/cart           Bearer + product_id,quantity,price (CSV) + name (from detail)
5. POST /api/checkout       Bearer + total_amount, shipping_address

Think-time: one Uniform Random Timer per plan (P01 bands), not per-step P00 bands.
```
