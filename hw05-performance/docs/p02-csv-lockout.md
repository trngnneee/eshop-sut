# P02 — CSV + lockout (23127271)

> **Before any JMeter run:** the **100** CSV accounts are **not** in the seed. Start SUT on `:3000`, then `node generate-tram-users.js --register` (once per seed). Skipping this → all logins **401**. Do not use `test@eshop.com`. See [`../test-plans/BEFORE-RUN.md`](../test-plans/BEFORE-RUN.md).

**Gate:** P02 only (no `.jmx`).  
**Tied to:** P01 max threads = **100** (Stress) → **100 unique emails**.  
**Files:**
- [`../test-plans/BEFORE-RUN.md`](../test-plans/BEFORE-RUN.md)
- [`../test-plans/23127271_users.csv`](../test-plans/23127271_users.csv)
- [`../test-plans/generate-tram-users.js`](../test-plans/generate-tram-users.js)
- [`../test-plans/reset-lockout.sql`](../test-plans/reset-lockout.sql)

---

## 1. CSV header and rows

Header (exact):

```text
email,password,search,product_id,quantity,price,total_amount,shipping_address
```

- **100** data rows: `tram01@eshop.com` … `tram100@eshop.com`.
- Password for every row: `Test1234!` (valid only — matches seed-user style, **not** `test@eshop.com`).
- `quantity` = 1; `total_amount` = `price * quantity`.
- `shipping_address` is quoted because it contains commas (JMeter **Allow quoted data = true**).

Regenerate:

```bash
cd SoftwareTesting-HW/HW5/23127271/test-plans
node generate-tram-users.js
```

---

## 2. Search / product_id / price vs seed

`GET /api/products?search=` matches **`products.name` only** (`server.js` L144). **Do not use `Laptop`** — that is a **category** name; `?search=Laptop` returns `[]` (P00). No `%`, `_`, `'`, `"`, `;` in `search`.

| `search` | Expected `product_id` | Seed `name` | Seed `price` = `total_amount` |
|----------|----------------------|-------------|-------------------------------|
| `iPhone` | 1 | iPhone 15 Pro Max | 30000000 |
| `Samsung` | 2 | Samsung Galaxy S24 Ultra | 28000000 |
| `MacBook` | 3 | MacBook Pro M3 | 45000000 |
| `AirPods` | 4 | Tai nghe AirPods Pro 2 | 6000000 |
| `Keychron` | 5 | Bàn phím cơ Keychron Q1 | 4000000 |

Rows cycle this table (`tram01` iPhone … `tram05` Keychron … `tram100` Keychron).

**Verify after every seed** (ids are AUTOINCREMENT; a dirty DB can shift them):

```sql
SELECT id, name, price FROM products;
```

If `id`/`price` disagree with the CSV, edit the CSV or re-run `generate-tram-users.js` after fixing `PRODUCTS` in the script. Wrong `product_id` → detail **200 `{}`** (assertion fail), not a 404.

---

## 3. JMeter CSV Data Set Config

Use the **same file** for Load, Stress, Spike, and soak. Put it next to the `.jmx` files (`test-plans/`).

| Setting | Value | Why |
|---------|--------|-----|
| Filename | `23127271_users.csv` | P05 name. |
| File encoding | `UTF-8` | Safe default. |
| Variable names | *(leave empty)* **or** the eight header names | If names are filled in, set **Ignore first line = true** so the header is not used as a user. |
| Ignore first line | **true** | Header row. |
| Delimiter | `,` | |
| Allow quoted data? | **true** | `"123 Nguyen Hue, Q1"` must stay one field. |
| Recycle on EOF? | **true** | Load 8 min and Stress 5 min need more iterations than 100 rows. |
| Stop thread on EOF? | **false** | Stop + 100 rows + All threads ≈ one iteration then halt — too short. |
| Sharing mode | **All threads** | Distributes `tram01`…`tram100` across VUs. **Current thread** would give every VU `tram01` first → 100 parallel logins on one account and one in-memory cart. |
| Identify? | false | Not required. |

**Recycle vs uniqueness:** 100 distinct emails ≥ 100 Stress threads, so the **first wave** is 1:1. Recycle reuses those 100 accounts on later iterations (required for duration). Two threads can share one `user.id` if they get out of lockstep — cart is `userCarts[userId]` and checkout does not read the cart, so shared cart is ugly but does not fake checkout. **Never** collapse the file to one `test@eshop.com` row.

Do **not** set Recycle=false / Stop=true for Load: 20 threads would exhaust 100 rows in a few seconds of CSV reads per thread-iteration and then die.

---

## 4. Lockout policy

Implementation (`server.js` L46–64), **not** FR-02 “3 fails / 30 s”:

- Wrong password → `login_attempts += 2`.
- When `login_attempts >= 3` → `locked_until` = now + **180000 ms**.
- **Two** failed logins lock the account.
- While locked, login returns **403** (Vietnamese message).
- Successful login resets `login_attempts = 0`, `locked_until = NULL`.

| Scenario | Passwords in CSV | Failed-login sampler? |
|----------|------------------|------------------------|
| Load | Valid `Test1234!` only | **No** |
| Stress | Valid only | **No** — Stress is checkout capacity, not lockout. |
| Spike | Valid only | **No** — Spike recover is 90 s; lockout is 180 s; 403s would fake a recover curve. |
| Soak | Valid only | **No** |

If 401/403 appear on login with this CSV, treat them as **setup/lockout contamination**, not as the SUT hitting Search-to-buy capacity.

---

## 5. Reset steps (fill timestamps when you actually run)

Do this **between Stress and Spike** (required). Also after any run that showed login 401/403, and before soak if needed.

Preferred path is **B** (SQL). **C** (re-seed) drops `tramNN` users because `database.js` `DROP TABLE`s on init.

### After Stress, before Spike

1. Stop the Stress JMeter process; confirm `23127271_Stress_20260814.jtl` is flushed.  
   **Time stopped:** `________`
2. Optional check (403 count in the `.jtl` / View Results): any login **403**? yes / no: `________`
3. **Choose one reset:**
   - **A — wait:** if any account was locked, wait **≥ 180 s** from that 403 (wall clock). **Wait until:** `________`
   - **B — SQL (preferred):** SUT may stay up; if “database is locked”, stop Node first.

     ```bash
     sqlite3 Repo/eshop-sut/backend/database.sqlite < SoftwareTesting-HW/HW5/23127271/test-plans/reset-lockout.sql
     ```

     **SQL time:** `________`  
     Confirm `login_attempts=0` and `locked_until` NULL for all `tram%@eshop.com`.
   - **C — re-seed (last resort):** restart SUT so `initDatabase()` runs → **users table wiped**. Then step 7 register. **Re-seed time:** `________`
4. Do **not** start Spike until step 3 is done. **Spike start:** `________`

### After Spike, before soak (same checklist)

5. Stop Spike; `.jtl` flushed. **Time:** `________`
6. Repeat step 3 (A/B/C). **Reset time:** `________`
7. Soak start: `________`

### After Load, before Stress (recommended, usually a no-op)

8. If Load had **zero** 401/403, SQL reset is still cheap insurance. **Time:** `________`

---

## 6. Register `tramNN` before the first run

Seed only creates `admin@eshop.com` and `test@eshop.com`. **`email` is not UNIQUE** in `users` (`database.js` L53) — `POST /api/register` can insert duplicates; login then `SELECT * WHERE email = ?` and may bind the wrong row. Register **once** per seed.

1. Start SUT: `http://localhost:3000` (fresh seed or existing DB).
2. From `test-plans/`:

   ```bash
   node generate-tram-users.js --register
   ```

   Expect 100× HTTP 200 `{ message, id }` (or SKIP if already registered). **Register time:** `________`  **OK count:** `________`
3. Spot-check:

   ```http
   POST /api/login
   { "email": "tram01@eshop.com", "password": "Test1234!" }
   ```

   Expect 200 + `token`. Do **not** use `test@eshop.com` in JMeter.
4. If you later use reset **C**, repeat step 2 before the next scenario.

Windows note: if `sqlite3` is not on PATH, use DB Browser for SQLite and paste `reset-lockout.sql`, or `npx` is not required — the register script only needs Node 18+ (`fetch`).

**Stop condition met:** CSV + recycle/lockout/register. Next gate is P03 (listeners only).
