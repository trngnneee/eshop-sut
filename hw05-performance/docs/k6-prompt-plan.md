# HW05 k6 bonus — Prompt plan (23127271 Search-to-buy)

**Student:** Võ Ngọc Bích Trâm · `23127271`  
**SUT:** `http://localhost:3000`  
**Required track:** JMeter (P00–P16) — already frozen at P08; graded `.jtl` exist.  
**This file:** copy-paste prompts for **k6 only**. Parent: [`prompt-plan.md`](./prompt-plan.md). Scope: [`frozen-scope.md`](./frozen-scope.md).

Do **not** start K01 until JMeter P08 is frozen. Do **not** one-shot “write Load+Stress+Spike k6 and tell me if it is fast.” One prompt per gate. After each reply: `ACCEPT` / `FIX` / `REJECT` + log in `ai-audit-report.md`. Never invent k6 JSON, console totals, or Task Manager %.

Reuse (do not regenerate): [`p01-parameters.md`](./p01-parameters.md) · [`p02-csv-lockout.md`](./p02-csv-lockout.md) · `test-plans/23127271_users.csv` · [`p03-listeners.md`](./p03-listeners.md) · [`p09-runbook.md`](./p09-runbook.md).

**Filenames:** `23127271_{Load|Stress|Spike|Soak}_20260814.js` (same date as `.jmx`).  
**JSON:** `logs/23127271_{Scenario}_20260814.json`

| JMeter plan | JMeter view | k6 script | Graded k6 output |
|-------------|-------------|-----------|------------------|
| Load | View Results Tree | `23127271_Load_20260814.js` | Short `--http-debug` peek **or** `console.log` on failed `check`; numbers from `--out json=` |
| Stress | Summary Report | `23127271_Stress_20260814.js` | End-of-run **console summary** + `--out json=` |
| Spike | Aggregate Report | `23127271_Spike_20260814.js` | `--out json=` (p95 by `name` tag). Console is not the percentile source |

---

## K01 — Generate Load script only

**Stop condition:** one `.js` + CSV path. Not Stress/Spike/soak.

**Context:** locked P00–P08 · `test-plans/23127271_users.csv` · `test-plans/23127271_Load_20260814.jmx`

```
GATE K01 only. Generate the k6 Load script for Search-to-buy. Parity with the accepted JMeter Load plan. Do NOT emit Stress or Spike.

Filename: 23127271_Load_20260814.js
CSV: same folder, 23127271_users.csv (header email,password,search,product_id,quantity,price,total_amount,shipping_address). Load with SharedArray + papaparse from jslib.k6.io (quoted fields). Recycle by __ITER % length. Unique emails — do not hardcode test@eshop.com.

Must include:
- Base URL http://localhost:3000. Timeout 10s on every request.
- options.stages matching P01 Load: 40s ramp to 20 VUs, then 480s hold at 20 (JMeter duration 520 includes ramp). Do not use a flat 20 with no ramp.
- VU sequence: POST /api/login → GET /api/products?search=${search} → GET /api/products/${product_id} → POST /api/cart (Bearer) → POST /api/checkout (Bearer).
- Extract token from login JSON. Authorization only on cart and checkout. Content-Type application/json only on POSTs.
- check() on every step: status 200 AND body (login token; search first element id; detail name+id, reject empty {}; cart "Added to cart"; checkout orderId). Do not check price type.
- If detail check fails, return (skip cart/checkout) — same idea as JMeter startnextloop.
- Think-time: sleep after EACH of the five requests, Uniform 1–3s (sleep(1 + Math.random()*2)). Not one sleep per iteration.
- Tag every request name: login, search, detail, cart, checkout (so JSON can be split like JMeter labels).
- No failed-login request. No categories/coupon/my-orders.
- Comment at top: graded numbers come from k6 run --out json=../logs/23127271_Load_20260814.json ; --http-debug is Tree-equivalent for a short peek only.

Output valid k6 JS. No Stress/Spike in this message.
```

**You check:** 20 VUs; stages 40s+480s; five sleeps 1–3s; Bearer only on cart/checkout; CSV SharedArray.

---

## K02 — Generate Stress script only

```
GATE K02 only. Same Search-to-buy workflow, CSV, checks, tags, timeouts, skip-on-failed-detail, Bearer-on-cart/checkout-only as the accepted Load k6 script.

Filename: 23127271_Stress_20260814.js
options.stages: 25s ramp to 100 VUs, then 300s hold at 100 (JMeter duration 325 includes ramp).
Think-time: sleep after EACH request, Uniform 0–100 ms (sleep(Math.random()*0.1)).
No failed-login. Peak 100, not 50 (P01 locked after first JMeter Stress-50 stayed 0% err).

Output only this .js. Comment: graded view = console summary + --out json=../logs/23127271_Stress_20260814.json
```

**You check:** 100 VUs; think 0–100 ms; same five paths; no extra endpoints.

---

## K03 — Generate Spike script only

```
GATE K03 only. Same workflow/CSV/checks/tags/Bearer/timeouts/skip-on-failed-detail as Load k6.

Filename: 23127271_Spike_20260814.js
Model a SPIKE, not another Stress. MUST use options.stages (ramping-vus). Do NOT export a constant 80 VUs.

P01 schedule (same as JMeter Ultimate TG):
- 30s at 5
- 2s jump to 80
- 60s hold at 80
- 5s drop to 5
- 90s recover at 5

Peak 80 (below Stress 100). Think-time Uniform 0–200 ms after EACH request (sleep(Math.random()*0.2)).

Comment: jump vs recover is NOT in the end-of-run http_req_duration p95 (that mixes phases). Split JSON by time like JMeter HTML. Graded file: --out json=../logs/23127271_Spike_20260814.json

Output only this .js plus a short 23127271_Spike_20260814-k6-notes.md explaining the stages vs JMeter Ultimate TG.
```

**You check:** recover window exists; stages not a flat 80; think 0–200 ms.

---

## K04 — Human review vs JMeter parity (before any `k6 run`)

**Stop condition:** issue list “what / why / fix”. You may disagree.

**Context:** K01–K03 scripts · JMeter `.jmx` · `p01-parameters.md` · `p04-review.md`

```
GATE K04 only. Critically review the three k6 scripts against the frozen JMeter Search-to-buy plans. Do not generate new scripts in this message.

Hunt specifically for:
1. VU/stage mismatch vs P01 (Load 20/40s+480s; Stress 100/25s+300s; Spike 5→80→5 with recover). k6 stages duration is NOT “JMeter duration minus ramp” by accident.
2. Think-time: one sleep per iteration instead of per request (would under-offer vs JMeter Uniform timer on every sampler). Same band copied across Load/Stress/Spike.
3. Checks that only test status 200 (detail 200 {}; checkout 200 without orderId).
4. Bearer on login/search/detail, or Content-Type on GETs.
5. CSV: one row for all VUs; ignoring quoted shipping_address; using test@eshop.com.
6. Failed-login sampler; lockout ignored between Stress and Spike.
7. Spike as constant-vus 80, or soak mixed into Spike stages.
8. Missing name tags (cannot compare to JMeter labels login/search/detail/cart/checkout).
9. Workflow drift (categories, coupon, my-orders, list-all without search).

For each issue: (a) what is wrong, (b) why the model missed it (k6 prior / no JMeter XML / generic cloud k6 example), (c) the concrete fix for K05.

If something matches JMeter, say MATCH — but do not write “no issues found” without checking the nine items.
```

**You write** the k6 “Review and fix” notes (edit the AI list; keep genuine corrections).

---

## K05 — Apply human fixes

**Context:** K04 issue list + the three `.js` files.

```
GATE K05 only. Apply the accepted K04 fixes to the three existing k6 scripts and CSV path. Do not redesign the workflow. Do not add Redis. Do not emit JMeter XML.

Must still be true after the patch:
- Load stages 40s→20 + 480s hold; Stress 25s→100 + 300s hold; Spike stages 5→80→5 with 90s recover.
- Per-request think-time bands 1–3s / 0–100ms / 0–200ms.
- Bearer only on cart/checkout; skip cart if detail check fails; CSV SharedArray; tags login|search|detail|cart|checkout.

List each file touched and the exact change. Keep filenames 23127271_{Load|Stress|Spike}_20260814.js.
```

Commit after this gate: `test-plans: Search-to-buy k6 Load/Stress/Spike (23127271)`.

---

## K06 — Execution runbook (AI writes instructions; you run them)

**Stop condition:** commands + evidence checklist. No fake metrics.

```
GATE K06 only. Write the k6 execution runbook for 23127271 Search-to-buy. Do NOT invent results. JMeter P09 already ran; k6 is a second injector on the SAME SUT — reset lockout and do not treat leftover userCarts as a k6-only finding without saying so.

Include:
1. Preflight: k6 version; SUT :3000; tramNN already registered (do not double-register — email is not UNIQUE); Task Manager visible (watch node vs k6, not java); same dxdiag hostname DESKTOP-TCVI3HT.
2. Order: Load → SQL unlock (Node stays up) → Stress → unlock → Spike → soak clone of Load at 15 VUs / 30s ramp / 720s hold / think 1–3s per request. Filename 23127271_Soak_20260814.js.
3. Commands (from test-plans/):

k6 run --out json=../logs/23127271_Load_20260814.json 23127271_Load_20260814.js
k6 run --out json=../logs/23127271_Stress_20260814.json 23127271_Stress_20260814.js
k6 run --out json=../logs/23127271_Spike_20260814.json 23127271_Spike_20260814.js
k6 run --out json=../logs/23127271_Soak_20260814.json 23127271_Soak_20260814.js

Load Tree-equivalent: a SHORT k6 run --http-debug=full with VUs=1, duration=30s — not the graded 520s (debug will drown the laptop).
Stress: capture console summary screenshot + Task Manager.
Spike: JSON + optional k6-reporter HTML; split hold vs recover in K07.

4. Per-run evidence: k6 window + Task Manager same frame; save JSON. Do not invent Node memory.
5. Soak blanks: error%, checkout p95 first vs last 20% of JSON time, rps — leave empty for the real run.
6. Demo: k6 may be a short extra clip; the ≥6 min Vietnamese video is still the JMeter Task 1 video (https://youtu.be/Nyvm0bxZxgA). Do not replace it.
```

**You:** run K06; put real JSON under `logs/`. Do not start K07 without files.

---

## K07 — Analyse raw k6 JSON (after real runs)

**Context:** attach `logs/23127271_Load_20260814.json` (and Stress/Spike/soak) or a sampled excerpt + how it was sampled. Do **not** attach JMeter `.jtl` as the source of truth for this gate.

```
GATE K07 only. Analyse the attached RAW k6 JSON (--out json) for Search-to-buy (23127271). Do not use the console summary as the source of truth. Do not copy P10 JMeter numbers into this table.

k6 JSON is NDJSON Point samples. Filter metric == "http_req_duration" and extra_tags.name in {login,search,detail,cart,checkout}. Failed checks: metric http_req_failed or check status.

For each scenario (Load, Stress, Spike, soak):
1. Sample count per name tag; error rate (failed checks vs http_req_failed — they can differ).
2. http_req_duration: mean, median, p90, p95, p99, max — by name and overall.
3. Throughput (iterations/s and http_reqs/s). State that sleep() is in wall-clock.
4. Time trend: first vs last 20% of timestamps; Spike split hold vs recover using stage windows from t=0 (k6 stages start at test start — unlike JMeter first-HTTP t0). Say if you used t=0 or first sample.
5. Propose thresholds for THIS SUT on a laptop from THIS k6 data, not from the JMeter table and not from Google SLA folklore.
6. Call out login 401/403 separately.

Cite tag names. If the JSON is truncated, say what you could not compute.
Do not write the JMeter-vs-k6 comparison (that is K09). Do not propose Redis (P12 already judged that).
```

**You:** recompute p95/error% with a script on the JSON before trusting K07.

---

## K08 — Misinterpretation hunt (k6)

```
GATE K08 only. I will now treat K07 as untrusted. Here is my independent recompute from the raw k6 JSON:

<paste per-tag p95, error%, http_reqs/s>

Compare K07 claims to these numbers. For every mismatch:
Claim → Correct value (how: metric=http_req_duration, extra_tags.name=checkout, …) → Why (mean vs p95; checks vs http_req_failed; sleep in RPS; mixing all tags as one p95; Spike whole-run vs hold).

Do not invent extra mismatches. If a claim matches, say MATCH.
Also flag if K07 silently used JMeter P10 figures.
```

---

## K09 — JMeter vs k6 comparison (only after K07 + P10 both exist)

**Context:** [`p10-analysis.md`](./p10-analysis.md) · K07 output · evidence screenshots (java vs k6 vs node in Task Manager)

```
GATE K09 only. Compare JMeter Search-to-buy vs k6 on THIS laptop. Use only numbers from P10/P11 (JMeter .jtl) and K07/K08 (k6 JSON). If a cell is UNKNOWN, write UNKNOWN.

Table per scenario (Load, Stress, Spike, soak):

Scenario | Metric | JMeter | k6 | Notes
Load | checkout p95 | | |
Load | error% | | |
Load | wall-clock req/s | | |
… Stress / Spike (hold checkout p95 + recover) / soak …

Then:
1. Setup parity: same five paths, CSV, VU counts, think-time bands — list any deliberate difference (e.g. k6 sleep vs JMeter Uniform timer).
2. Tool footprint: from screenshots, java vs k6 vs node CPU/RAM. Do not invent memory if UNKNOWN.
3. Why small gaps are expected (Go HTTP client vs JMeter Java; connection reuse). Investigate large gaps (wrong stages, missing sleep, checks not tagged).
4. CI: k6 smoke vs JMeter nightly — align with P13 (k6 optional sub-minute probe; do not mix JSON and .jtl into one baseline).

No generic “k6 is faster than JMeter” without these run’s numbers.
```

**You:** fill the table from your recomputes; this becomes report §4.

---

## Anti-cheat (k6)

| Forbidden | Why |
|-----------|-----|
| “Generate a realistic k6 JSON” / fake console summary | Bonus still needs a real `k6 run` |
| Copy P10 JMeter p95 into K07 | Separate logs, then K09 |
| Flat 80 VUs named Spike | Must be stages jump+recover |
| Double `--register` before k6 | `email` is not UNIQUE |

## Suggested commits

1. `test-plans: k6 Load js`  
2. `test-plans: k6 Stress js`  
3. `test-plans: k6 Spike js`  
4. `logs: k6 json` (after real runs)  
5. `docs: k6 analysis + JMeter comparison`
