# P12 — Feasible vs hallucinated optimizations (23127271)

**Gate:** P12 only.  
**P10 fact:** [`p10-analysis.md`](./p10-analysis.md) **did not** recommend Redis/Nginx/Postgres/WAL/K8s. It left observations: checkout + login dominate Stress `elapsed`; cart is cheapest; search `LIKE` on five seed rows is not the limiter; Spike recovered at 5 VU.  
**This table** turns those observations (and the usual generic “AI scale-up” list) into recommendations and judges them against **this** repo + **these** `.jtl` files.

**Stack (verified):** Express `server.js`; `sqlite3` **not** `better-sqlite3` (`backend/package.json`); JWT `jsonwebtoken`; `userCarts = {}` (`server.js` L14); no Redis, no pooler, no Nginx in-repo. Search: string-interpolated `LIKE` (`server.js` L144). Cart: `push(req.body)` (`L290–295`). Orders: `INSERT` (`L297–308`).

**Human check (2026-08-16):** line numbers re-read in `Repo/eshop-sut/backend/server.js` + `database.js` + `package.json`. One classification changed: login `db.run` without callback is a **correctness** smell, not a Stress p95 fix (waiting would add latency). All other Hallucinated rows stand.

P11 MATCH kept: Stress checkout p95 **534 ms** vs Load **22 ms**; login p95 **506 ms**; cart p95 **217 ms**; search p95 **447 ms**; error% **0**; no 401/403/5xx; soak checkout p95 **20 → 24 ms**.

---

## Recommendation | class | reasoning

| Recommendation | Feasible / Hallucinated | Reasoning |
|----------------|-------------------------|-----------|
| Treat **SQLite `INSERT` on `/api/checkout`** as the Stress hot path (keep the handler small; do not add coupon/my-orders onto this VU) | **Feasible** | Logs: checkout p95 **534 ms** (slowest label) vs Load **22 ms**. Code: `db.run("INSERT INTO orders …")` `server.js` **L297–308**. One Node process + one `sqlite3` connection serializes writers. No product rewrite — it is already the write. |
| Make the login success **`UPDATE login_attempts=0` wait** before `jwt.sign` / `res.json` (today `db.run` is fire-and-forget) | **Hallucinated as a performance fix** | Code smell is real: `server.js` **L47–51** `db.run(UPDATE…)` has **no callback**, then `jwt.sign` + `res.json`. That is durability/ordering, not the Stress knee. Logs: login p95 **506 ms** from the **same sqlite queue** as checkout (0 errors, max 1009 ms). Waiting on `UPDATE` before the response would **add** latency. Same pattern as the LIKE bind: real defect, wrong reason. |
| **Clear `userCarts[userId]` after a successful checkout** (or cap array length) | **Feasible** as leak hygiene; **not** the Stress p95 fix | Code: `POST /api/cart` only `push` (`L290–295`); checkout **never reads or clears** the cart (`L297–308`). Soak was the place to see heap/`elapsed` climb: checkout p95 **20 → 24 ms** over ~12 min — **not** a cliff. Do this so soak/restart semantics are sane; do **not** claim it explains Stress **534 ms**. |
| Parameterize search: `LIKE ?` with `'%' + q + '%'` instead of `` `%${searchQuery}%` `` | **Hallucinated as a performance fix** | Code defect is real (`server.js` **L144**). Logs do **not** show it: search p95 **447 ms** under Stress with **five** seed names, **0** HTML-500 `Database Error` rows. Binding the LIKE is a security/correctness patch, not what moved checkout to 534 ms. |
| `CREATE INDEX` on `products.name` (or full-text) for search | **Hallucinated** | Five-row `LIKE '%q%'` cannot be the 321 rps limiter. Stress search p95 **447** < checkout **534**. Leading-wildcard `LIKE` would not use a normal B-tree anyway. |
| `CREATE INDEX` / `UNIQUE` on `users.email` to speed login | **Hallucinated** as latency | Login is `SELECT … WHERE email = ?` (`L35`). Table size ≈ 100 `tramNN` rows. Index does not explain p95 **506 ms**. `UNIQUE` would still be a **schema** fix for duplicate register (`database.js` L53 has no UNIQUE) — not the Stress bottleneck. |
| Index `orders.user_id` for faster checkout | **Hallucinated** | Checkout is **INSERT**, not `SELECT` by user (`L301–303`). This workflow never calls `GET /api/orders/my-orders`. Extra indexes **slow** inserts. |
| Enable **SQLite WAL** (`PRAGMA journal_mode=WAL`) | **Hallucinated** | Assignment example: WAL only if logs show write-lock waits. Graded `.jtl`: **0** `5xx`, **0** `SQLITE_BUSY` / connection codes, max elapsed **1009 ms** (under the 10 s timeout). Latency is queueing on one connection, not a captured busy error. |
| Add a **connection pool** in front of SQLite | **Hallucinated** | `sqlite3` here is one `Database` (`database.js` L5). Multiple writers on a file DB typically **worsen** lock contention. No pooler in `package.json`. |
| **Redis** (or other) cache for `GET /api/products?search=` | **Hallucinated** | No Redis in `package.json`. Search is not the Stress limiter (five rows). Would add a component the SUT does not have. |
| Move catalog/orders to **Postgres** and “add indexes” | **Hallucinated** | Would rewrite storage. Logs show a **laptop Node+sqlite3** queue, not missing PG planner stats. |
| **Nginx** / reverse-proxy tuning | **Hallucinated** | JMeter hit `http://localhost:3000` directly. No Nginx in this repo. |
| **Kubernetes HPA** / more replicas | **Hallucinated** | No k8s manifests. `userCarts` is **process memory** (`L14`) — extra replicas split carts and do not share the sqlite file cleanly. |
| Node **cluster / PM2** workers | **Hallucinated** for this cart | Same in-memory cart + one sqlite file. Multi-process without a shared cart store **rewrites** the product. |
| “Checkout already needs prepared statements” | **Hallucinated** | Checkout **already** binds parameters (`L301–303`). Search is the interpolated query, not checkout. |
| Tune lockout (3×30 s vs `+=2` / 180 s) to improve Stress p95 | **Hallucinated** | P10/P11: login **401/403 = 0**. Stress used valid passwords. Lockout did not appear in the graded logs. |
| Add **better-sqlite3** synchronous API for speed | **Hallucinated** as a drop-in | Repo is `sqlite3` async (`package.json`). Switching libraries is a rewrite of every `db.get`/`db.run`. Logs do not prove the async API is the 534 ms cause vs single-file serialization. |

---

## What the logs actually support

| Observation (P10/P11) | Matches code | Allowed conclusion |
|-----------------------|--------------|--------------------|
| Checkout slowest under 100 VU | `INSERT` `L297–308` | One-file SQLite write + event loop is the knee. |
| Login almost as slow | `SELECT` L35 + fire-and-forget `UPDATE` L47–51 + `jwt.sign` L51 | Same sqlite queue. Do **not** “fix p95” by waiting on the UPDATE. |
| Cart fastest | in-memory `push` `L293` | Caching the cart would not move Stress p95. |
| Search not the limiter | `LIKE` on 5 rows `L144` | Do not “optimize search” for this run. |
| Spike recovered | hold checkout p95 464 → recover 24 | No stuck lock/WAL story. |
| Soak p95 almost flat | cart unbounded but 12 min @ 15 VU | Leak is real in code; **not** proven as a latency failure in this `.jtl`. |

**Stop condition met.** Next gate is P13 (continuous testing), using these classifications — do not put Redis/HPA in the CI proposal as if the logs required them.
