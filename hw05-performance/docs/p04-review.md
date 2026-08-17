# P04 — Review and fix (P00–P03)

**Gate:** P04 only. No JMeter XML.  
**Role:** performance tester who has read `Repo/eshop-sut/backend/server.js` and `database.js`.  
**This file is Task 1 “Review and fix.”** Apply the **Fix in P05–P08** column when generating plans. Student may edit any row.

**Current lock (after first `-n`):** Load **20** / Stress **100** / Spike **5→80→5** / CSV **100** — see [`p01-parameters.md`](./p01-parameters.md). Hunt bodies below are the **P04-time** review (first guess 20/50/5→40). Do not copy 50 / 5→40 into a new plan.

Checked all seven hunt items. Several design choices are fine; the issues below are still real.

---

## Hunt 1 — Ramp-up / think-time copied across scenarios?

**Verdict:** think-time bands are **not** copied (Load 1–3 s, Stress 0.2–0.5 s, Spike 0–0.2 s). Ramp-ups differ (40 s / 15 s / 2 s jump). Keep that.

| | |
|--|--|
| **(a) What is wrong** | Two leftovers. (1) P00 still lists **per-step** Load bands (login 1–2 s, search 1–3 s, …). P01 then says **one Uniform Random Timer on every sampler**. P05 could mix both and double-pause. (2) Stress **15 s ramp × 50 threads** is a login burst at the start of a “sustained stress” test. If P10 includes those first seconds, Stress looks like a spike. |
| **(b) Why the model missed it** | Vague prompt stacked two think-time stories (P00 sequence vs P01 table). Generic Stress tables use “short ramp 10–20 s” without saying **exclude ramp from the Stress comparison**. |
| **(c) Fix in P05–P08** | One timer per plan, P01 numbers only (Load 1000–3000 ms, Stress **0–100 ms** locked, Spike 0–200 ms). Do **not** add five different Constant Timers from P00. In P10, compute Stress p95 **after ramp-up** (drop samples with `timeStamp` in the first **25 s** of the locked Stress plan; first-run Stress 50 used 15 s). |

---

## Hunt 2 — Thread counts too weak, too strong, or only lockout?

**Verdict (at review):** 20 / 50 / 5→40 is laptop-scale; Stress > Load; Spike is not “Load but longer”; valid passwords so we are **not** designing a lockout hammer. Keep the shape. **Now locked:** 20 / **100** / **5→80→5**.

| | |
|--|--|
| **(a) What is wrong** | (1) **50 is a guess**, not a measured knee. Five seed products and `LIKE` on `name` are cheap (`server.js` L141–151). Stress may stay **green** (only checkout `INSERT` + same-host JMeter hurt) **or** Java may pin the CPU while `node` is idle — then we measured the injector. (2) Spike peak **40 < Stress 50** is intentional for *shape*, but a reader can call Spike “weaker Stress.” (3) Standard Thread Group **cannot** do 5→40→5. |
| **(b) Why the model missed it** | Generic prior “Stress ≈ 2.5× Load.” No run yet, so it stated 50 as if SQLite will definitely fail. It named Ultimate Thread Group in prose and never made the **plugin** a hard P07 dependency. |
| **(c) Fix in P05–P08** | P06: 50 threads as **first** Stress; if error% stays ~0 and p95 ≈ Load, raise threads and/or cut think-time (document the change). **Applied:** first `-n` was 0% at 50 → P01 locked **100 VU** + think **0–100 ms** (not the 70 contingency). Watch Task Manager: if `java` is pinned and `node` is not, **lower** threads rather than claiming SUT failure. P07: **jp@gc Ultimate Thread Group** with stages **5 / 80 / 5** (first emit was 5/40/5) — **not** a flat peak-thread group. If the plugin is missing, install it; do not silently emit a normal Thread Group. |

---

## Hunt 3 — Assertions HTTP 200 only?

**Verdict:** P00 already requires `token`, JSON array, `name` / not `{}`, `Added to cart`, `orderId`. That part is **not** 200-only. Gaps remain that P05 will still implement wrong if it copies P00 loosely.

| | |
|--|--|
| **(a) What is wrong** | (1) Search still allows an **empty array** (`[]` is a valid JSON array). After P02, keywords match seed **names**; empty `[]` is now a **fail** (wrong `search` or empty catalog), not “maybe OK.” (2) CSV has **no `name` column**. README cart body is `{ product_id, quantity, name, price }`. Cart `push(req.body)` (`server.js` L293) still returns 200 `Added to cart` with a nameless body — assertion would pass a thin payload. (3) Detail: “Not Contains `{}`” is a bad JMeter test (`{"id":2,...}` can still be argued); even `id` stringify `price` (`server.js` L162) so a numeric `price` assertion would fail **real** products 2 and 4. (4) No HTTP **response timeout** — hung Stress samples never become errors. |
| **(b) Why the model missed it** | P00 was written **before** CSV existed, so it left search-empty as a hedge. Cart `name` came from the group README, not from the frozen CSV header. Generic JMeter “Contains `{}`” / “price is a number.” Timeouts are rarely in homework prompts. |
| **(c) Fix in P05–P08** | Every sampler: **status + JSON field**. Search: JSON Path `$[0].id` exists (non-empty). Detail: JSON Path `$.name` matches `.+` (and `$.id`); **do not** assert `price` type; **do not** use “body equals `{}`” as the only check — fail when `name` is absent. Cart: JSON Extractor `$.name` on detail → POST body `product_id,quantity,name,price`. Checkout: `$.orderId` present. Connect/response timeout **10 s** on HTTP Request Defaults. Login: `$.token` present. |

---

## Hunt 4 — Lockout spec vs implementation?

**Verdict:** `+= 2`, lock at `>= 3`, **180 s**, HTTP **403** is documented and Stress/Spike stay on **valid** passwords. Good. Still incomplete as a *test* of lockout.

| | |
|--|--|
| **(a) What is wrong** | (1) Lockout is **paper-only**. Nothing in P00–P03 empirically checks that two bad passwords lock. (2) `database.js` `initDatabase()` **DROP**s `users` on **every** `node server.js` start. Restarting Node to “clear lockout” **deletes `tram01`–`tram100`**. SQL reset (`reset-lockout.sql`) is correct only if Node **stays up**. (3) Double `--register` is dangerous: `email` is **not UNIQUE**; `SELECT * WHERE email = ?` (`server.js` L35) may bind the wrong row. |
| **(b) Why the model missed it** | The skill text still talks like FR-02 “3 fails.” The model read `server.js` for `+= 2` but did not read that `initDatabase()` runs on load (wipe). Register-once was added only after the student asked. |
| **(c) Fix in P05–P08 / P09** | **No** failed-login sampler inside Load/Stress/Spike (would measure lockout, not checkout). **P09 preflight (manual, one throwaway account):** two wrong passwords → 401 then 401; third login 403; then SQL reset. Keep Node **running** across Load → SQL reset → Stress → SQL reset → Spike. **Do not stop Node to run SQL** — P02’s “if database is locked, stop Node first” is a trap: the next `node server.js` runs `initDatabase()` and **DROP**s `tramNN`. After JMeter exits, run `reset-lockout.sql` with Node still up. If Node *does* restart, **`--register` again** before the next `.jmx`. Do not run `--register` twice on the same DB without checking `SELECT email, COUNT(*) FROM users GROUP BY email`. |

---

## Hunt 5 — CSV one-row recycle / Recycle vs Stop mismatch?

**Verdict:** **100** unique `tramNN` emails (≥ Stress 100), Recycle=true, Stop=false, Share=All threads is the right **pattern**. Not a single `test@eshop.com` row. (P04-time file had 50; CSV was grown after the 0% Stress-50 run.)

| | |
|--|--|
| **(a) What is wrong** | (1) Filename `23127271_users.csv` with no directory **fails** if JMeter cwd is not `test-plans/`. (2) “Variable names empty **or** filled” is ambiguous; Ignore first line=true with empty names can yield no `${email}`. (3) 100 rows + Recycle + All threads ⇒ two VUs can share one `user.id`; `userCarts[userId]` is shared (`server.js` L14). Checkout ignores the cart, so orders still insert — but login/cart labels can look “weird” under Stress. |
| **(b) Why the model missed it** | Generic “put CSV next to the plan.” It never ran `jmeter -n` from another folder. Sharing-mode collision is a JMeter iterator detail, not a REST one. |
| **(c) Fix in P05–P08** | CSV Data Set: **variable names** = the eight headers, **Ignore first line = true**, Allow quoted data = true, Recycle true, Stop false, All threads. Path: same folder as `.jmx` **and** P09 `cd` into `test-plans` (or set filename to an absolute path). Do **not** switch to Current thread (all VUs would get `tram01`). |

---

## Hunt 6 — Workflow drift (Khoa / Nguyên / Thịnh / Bảo)?

**Verdict:** sequence is still login → **search** → detail → cart → checkout. No `GET /api/products` without query, no categories, no coupon, no my-orders. **Keep.**

| | |
|--|--|
| **(a) What is wrong** | Only a foot-gun: P00’s optional `$[0].id` **replacing** CSV `product_id` is fine if it matches; using it blindly is still Search-to-buy. Drift risk is **adding** `GET /api/categories` or skipping search because “detail+CSV id is enough.” |
| **(b) Why the model missed it** | N/A for current docs; generic shop flows often list-all then buy. |
| **(c) Fix in P05–P08** | Samplers **exactly** those five paths. Search sampler must send `?search=${search}`. Do not add categories / apply-coupon / my-orders “for coverage.” |

---

## Hunt 7 — Soak confused with Spike?

**Verdict:** soak is constant **15** threads × **12 min** × Load think-time; Spike is **5→80→5** with recover. **Not the same.**

| | |
|--|--|
| **(a) What is wrong** | No soak `.jmx` name in frozen scope. P03 says soak may “reuse Load’s Tree.” Easy to run Load for 12 min and call it soak **or** run Spike’s schedule for 12 min. Soak also needs Node **not** restarted mid-run (`userCarts` growth is the point). |
| **(b) Why the model missed it** | P01 was asked for “starting guesses,” not a plan file. Generic “endurance = longer load.” |
| **(c) Fix in P05–P08 / P09** | Do **not** put soak into P05–P07. P09: clone Load, threads=15, duration=12 min, think-time 1–3 s, filename e.g. `23127271_Soak_20260814.jmx` (or `-Jthreads=15 -Jduration=720`). Never use Ultimate Thread Group for soak. |

---

## Extra issues (not in the seven, still apply)

### E1 — Aggregate Report cannot show jump vs recover

| | |
|--|--|
| **(a)** | P03’s **Unique** bullet claims Spike Aggregate shows p95 **jumping on the hold and falling on recover**. Aggregate is **one percentile table for the whole run**. It cannot split baseline / peak / recover. (P03 later already says HTML `-e -o` is the time-series evidence — the overclaim is that Unique bullet, not the whole listener pick.) |
| **(b)** | Generic pairing “Spike → Aggregate → percentiles” without knowing the listener has **no time axis**. |
| **(c)** | Keep Aggregate as the **required GUI listener**. Tell jump vs recover from **HTML `-e -o`** (Response Times Over Time) and from P10 splitting `.jtl` by timestamp (first 30 s vs hold vs last 90 s). Screenshot Aggregate **and** the HTML over-time graph. |

### E2 — `initDatabase()` wipe vs in-memory cart

Restarting Node drops tables **and** clears `userCarts`. SQL lockout reset does **not** clear carts: after Stress, Spike inherits a large heap. Prefer: Node stays up + SQL unlock between scenarios; optional Node restart **only after** Stress `.jtl` is saved, then `--register`, then Spike (cleaner heap, extra register step). Pick one in P09 and stick to it.

### E3 — Search `[]` vs teammate README `Laptop`

P02 correctly refused `Laptop`. If P05 copies the **group README example CSV**, search returns `[]` and (with the Hunt 3 fix) the plan fails closed. Keep `iPhone` / `Samsung` / `MacBook` / `AirPods` / `Keychron`.

---

## What to keep (brief)

- Paths and coverage sentences (Search-to-buy ≠ Khoa list-all).
- Laptop-scale **20 / 100 / 5→80→5**; three think-time bands (Load 1–3 s, Stress 0–0.1 s, Spike 0–0.2 s).
- **100** unique emails; valid passwords; Recycle=true / Stop=false / All threads.
- Listeners: Tree / Summary / Aggregate, one each; filenames `23127271_{Load\|Stress\|Spike}_20260814`.
- Detail `200 {}` quirk; even-id `price` string; lockout `+= 2` / 180 s / 403 on paper.
- Register **100** accounts **before** any run (`BEFORE-RUN.md`).

---

## P05–P08 fix checklist (do these)

1. Five samplers only; search query present; no teammate APIs.  
2. Assertions: `token`, `$[0].id`, `$.name` (not `{}`), `Added to cart`, `$.orderId`.  
3. Extract `token` then `name`/`price` from detail into cart body.  
4. HTTP timeouts 10 s; Header Manager **after** login (`Authorization: Bearer ${token}`).  
5. CSV config unambiguous + launch from `test-plans/`.  
6. Timers = P01 bands only.  
7. Load: 20 / 40 s / 8 min / Tree. Stress: **100** / **25 s** / 5 min / Summary. Spike: Ultimate TG **5→80→5** / Aggregate.  
8. No failed-login sampler; lockout = P09 manual probe + SQL reset; never stop Node just to unlock; never restart Node without `--register`.

---

## Student verdict (2026-08-14 ~19:35 ICT)

**ACCEPT** — seven hunts checked against `server.js` / `database.js` / CSV. No row rejected. Two wording nits applied above (no parameter changes):

1. **Hunt 4:** never stop Node to run lockout SQL (restart = DROP `tramNN`).
2. **E1:** P03 already caveats HTML for shape; we still treat the Aggregate “jump vs recover” Unique bullet as overclaim.

**Keep (at P04 time):** 20 / 50 / 5→40→5; three think-time bands; 50 unique emails; JSON-field asserts (tightened to `$[0].id` + no numeric `price`); Search-to-buy ≠ Khoa; soak ≠ Spike (soak stays P09).

**After first `-n` (0% at Stress 50):** P01 re-locked to Load **20** / Stress **100** / Spike **5→80→5**, CSV **100** emails — see [`p01-parameters.md`](./p01-parameters.md). Hunt 2’s “50 may stay green” was confirmed.

**Stop condition met:** issue list with what / why / fix. Next gate is P05 (Load `.jmx` only), using this list.
