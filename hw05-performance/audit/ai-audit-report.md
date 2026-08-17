# AI Audit Report

**Student:** Võ Ngọc Bích Trâm · `23127271`  
**Workflow:** Search-to-buy (EShop `http://localhost:3000`)  
**Tool:** Cursor Agent (Grok 4.6 / Composer) driving gated prompts in `docs/prompt-plan.md`  
**Principle:** AI drafts; the student owns every number. Raw `.jtl` come from real `-n` runs, not from the model.

**Locked design (after first run + student re-lock):** Load **20** · Stress **100** (think 0–100 ms) · Spike **5→80→5** · CSV **100** unique `tramNN`. Load `.jmx` never changed. First-run logs (Stress 50 / Spike peak 40, all 0% error) stay under `logs/` as evidence the first guess was too low.

Verbatim gate prompts live in [`docs/prompt-plan.md`](../docs/prompt-plan.md). One-line log: [`docs/prompt_log.md`](../docs/prompt_log.md).

I use AI tools for the following tasks:

## Task 1 — Test design (JMeter)

### Interaction 1 — GATE P00 (endpoint map)

- **Tool:** Cursor Agent (Grok 4.6)
- **Date/time:** 2026-08-14 ~18:25 ICT
- **Prompt:** GATE P00 only (`prompt-plan.md`): map Search-to-buy to real `server.js` paths; sequence table; three coverage sentences; SUT facts (lockout `+= 2` / 180 s, in-memory cart, LIKE interpolation, `200 {}` on missing product). No thread counts, CSV, listeners, or JMeter XML.
- **Output:** `docs/p00-endpoint-map.md` — login → `GET /api/products?search=` → detail → cart → checkout. Coverage: not Khoa’s list-all (`GET /api/products` with no search). Fact: **`Laptop` is a category**, so `?search=Laptop` returns `[]`.
- **Student verdict:** ACCEPT

### Interaction 2 — GATE P01 (parameters — first guess)

- **Tool:** Cursor Agent (Grok 4.6)
- **Date/time:** 2026-08-14 ~18:41 ICT
- **Prompt:** GATE P01 only: Load / Stress / Spike on the same workflow; laptop-scale Node+SQLite+JMeter on one Windows host; valid logins only; distinct think-time; soak starting guesses. No `.jmx`.
- **Output:** `docs/p01-parameters.md` (first table): Load **20** / 40 s / 8 min / think 1–3 s; Stress **50** / 15 s / 5 min / think 0.2–0.5 s; Spike **5→40→5**; soak **15** × 12 min. Unique emails ≥ 50. Rejected AWS-scale and failed-login hammer.
- **Student verdict:** ACCEPT at the time. **Later superseded** (Interactions 16–17) after a 0% Stress run. The first table is kept as the guess that P04 already warned might stay green.

### Interaction 3 — GATE P02 (CSV + lockout)

- **Tool:** Cursor Agent (Grok 4.6)
- **Date/time:** 2026-08-14 ~18:46 ICT
- **Prompt:** GATE P02 only: unique `tramNN` emails ≥ max threads; seed-safe search keywords; recycle/sharing; lockout reset; register-before-run. No `.jmx`.
- **Output:** `docs/p02-csv-lockout.md`; `test-plans/23127271_users.csv` (then 50 rows); `generate-tram-users.js`; `reset-lockout.sql`. Keywords `iPhone` / `Samsung` / `MacBook` / `AirPods` / `Keychron` — not category `Laptop`. Recycle=true, Stop=false, Share=All threads.
- **Student verdict:** ACCEPT (then 50 rows; later expanded to 100 in Interaction 17)

### Interaction 4 — P02 follow-up: register first?

- **Tool:** Cursor Agent (Grok 4.6)
- **Date/time:** 2026-08-14 ~18:55 ICT
- **Prompt:** `50 account need register first to test?`
- **Output:** Yes. Seed only has `admin@eshop.com` and `test@eshop.com`. Skip `--register` → every login **401**. `initDatabase()` DROP on Node restart wipes `tramNN`.
- **Student verdict:** ACCEPT

### Interaction 5 — P02 follow-up: write it down

- **Tool:** Cursor Agent (Grok 4.6)
- **Date/time:** 2026-08-14 ~18:57 ICT
- **Prompt:** `Note it before run test`
- **Output:** `test-plans/BEFORE-RUN.md` plus the same warning on P02, the generator, `reset-lockout.sql`, and the prompt-plan checklist.
- **Student verdict:** ACCEPT

### Interaction 6 — GATE P03 (listeners)

- **Tool:** Cursor Agent (Grok 4.6)
- **Date/time:** 2026-08-14 ~19:00 ICT
- **Prompt:** GATE P03 only: three distinct listeners — Load Tree, Stress Summary, Spike Aggregate. GUI for screenshots; graded numbers from `-n -l .jtl -e -o`.
- **Output:** `docs/p03-listeners.md`. No swap. Filenames `23127271_{Load|Stress|Spike}_20260814`.
- **Student verdict:** ACCEPT. Later (P04 E1): Aggregate is a **whole-run** table — jump vs recover comes from HTML Over Time and `.jtl` time splits, not from that table.

### Interaction 7 — GATE P04 (human review)

- **Tool:** Cursor Agent (Grok 4.6)
- **Date/time:** 2026-08-14 ~19:16 ICT
- **Prompt:** GATE P04 only: hunt copied think-time, weak/strong threads, 200-only asserts, lockout spec vs code, CSV recycle, teammate drift, soak vs Spike. What / why / fix. No `.jmx`.
- **Output:** `docs/p04-review.md`. Keep: distinct think-times; then-current 20/50/5→40; JSON-field asserts in P00; Search-to-buy ≠ Khoa; soak ≠ Spike. Must-fix: one P01 timer (not P00 per-step); Stress 50 **may stay green**; Spike needs Ultimate Thread Group; search `$[0].id`; cart `name` from detail; no numeric `price`; 10 s timeout; no fail-login sampler; Node restart DROPs users; CSV variableNames + `cd test-plans`.
- **Student verdict:** ACCEPT + two nits (never stop Node just to SQL-unlock; Aggregate cannot show jump vs recover). Hunt 2 (“50 may stay green”) was **confirmed by the first `-n` run**.

### Interaction 8 — P04 double-check vs SUT

- **Tool:** Cursor Agent (Grok 4.6)
- **Date/time:** 2026-08-14 ~19:35 ICT
- **Prompt:** Double-check P04 against P00–P03, CSV, `server.js`, `database.js`; write ACCEPT + nits.
- **Output:** All seven hunts matched code. Nits written into `p04-review.md`; `frozen-scope.md` assertions aligned (`$[0].id`, no numeric `price`, cart name from detail, 10 s timeout, one P01 timer).
- **Student verdict:** ACCEPT — P05 may generate Load `.jmx`.

### Interaction 9 — GATE P05 (Load `.jmx`)

- **Tool:** Cursor Agent (Grok 4.6)
- **Date/time:** 2026-08-14 ~19:40 ICT
- **Prompt:** GATE P05 only: `23127271_Load_20260814.jmx`; P01 Load numbers; CSV; Bearer; JSON extractors; Uniform timer; status **and** JSON field; Tree only. No Stress/Spike.
- **Output:** Load plan with 20 / 40 s / **480 s** (wrong: JMeter duration includes ramp), Thread-Group Content-Type on GETs, `continue` on error, unused `user_id` extractor.
- **Student verdict:** FIX (see Interaction 10)

### Interaction 10 — P05-fix

- **Tool:** Cursor Agent
- **Date/time:** 2026-08-14 ~19:49 ICT
- **Prompt:** Patch Load only: duration **520**; Content-Type on POSTs only; `startnextloop`; drop `user_id` extractor.
- **Output:** Patched `23127271_Load_20260814.jmx`. This file is still the Load plan (20 VU) after the later Stress re-lock.
- **Student verdict:** ACCEPT

### Interaction 11 — GATE P06 (Stress `.jmx`, first version)

- **Tool:** Cursor Agent
- **Date/time:** 2026-08-15 ~10:14 ICT
- **Prompt:** GATE P06 only: clone Load workflow; **50** / 15 s / 315 s / think 200–500 ms; Summary Report only; no failed-login.
- **Output:** `23127271_Stress_20260814.jmx` at those first-guess numbers.
- **Student verdict:** ACCEPT then. **Replaced** after the 0% run (Interactions 16–17). First-run `.jtl` still reflects this 50 VU plan.

### Interaction 12 — GATE P07 (Spike `.jmx`, first version)

- **Tool:** Cursor Agent
- **Date/time:** 2026-08-15 ~10:29 ICT
- **Prompt:** GATE P07 only: Ultimate Thread Group (not flat 40); 30 s @5 → jump 40 in 2 s → hold 60 s → drop to 5 in 5 s → recover 90 s; think 0–200 ms; Aggregate only.
- **Output:** `23127271_Spike_20260814.jmx` + `23127271_Spike_20260814-notes.md`. Plugin `jpgc-casutg` required.
- **Student verdict:** ACCEPT then. **Replaced** peak 40 → 80 in Interaction 17. First-run `.jtl` still reflects peak 40.

### Interaction 13 — GATE P08 (freeze before first run)

- **Tool:** Cursor Agent
- **Date/time:** 2026-08-15 ~10:35 ICT
- **Prompt:** GATE P08 only: apply P04 + P05-fix nits; list files touched; no k6; no workflow redesign.
- **Output:** `docs/p08-fix-log.md`. No sampler/thread XML change — nits already in P05-fix→P07. Comment stamps only.
- **Student verdict:** ACCEPT (honest freeze). A **second** P08 pass after the run is Interactions 16–17, not this freeze.

### Interaction 14 — GATE P09 (runbook)

- **Tool:** Cursor Agent
- **Date/time:** 2026-08-15 ~10:41 ICT
- **Prompt:** GATE P09 only: execution runbook; do **not** invent results. Preflight, order, `-n` commands, evidence, soak blanks, demo video, GitHub Issue for functional bugs.
- **Output:** `docs/p09-runbook.md`. Soak clone: 15 threads / 750 s. Metric table left blank.
- **Student verdict:** ACCEPT (later profile rows updated to match locked P01)

## Task 1 — Execution support

### Interaction 15 — First real `-n` runs

- **Tool:** Cursor Agent
- **Date/time:** 2026-08-15 ~11:01–11:44 ICT
- **Prompt:** `Chạy cho t đi`
- **Output:** Installed JMeter 5.6.3 at `C:\DiskD\Tools\apache-jmeter-5.6.3` + `jpgc-casutg`; started SUT; registered 50 `tramNN`; wrote `23127271_Soak_20260814.jmx`; ran Load → Stress → Spike → Soak.

  Console totals (**not** P10; P10 must recompute from raw `.jtl`):

  | Scenario        | Samples | Approx. throughput | Error %                           |
  | --------------- | ------- | ------------------ | --------------------------------- |
  | Load (20)       | 4972    | ~9.6/s             | **0%**                            |
  | Stress (50)     | 43045   | ~136.6/s           | **0%**                            |
  | Spike (peak 40) | 22492   | ~120.2/s           | **0%** (5→40→5 visible on Active) |
  | Soak (15)       | 5474    | ~7.3/s             | **0%**                            |

  Artifacts: `logs/*.jtl` + `logs/report_{load,stress,spike,soak}/`. Task 1 demo: https://youtu.be/Nyvm0bxZxgA. dxdiag: `evidence/dxdiag.png` (hostname `DESKTOP-TCVI3HT`). HTML dashboard/statistics PNGs in `evidence/`. Agent Skill demo (separate video, P16) still owed.
- **Student verdict:** Load 0% = expected. Stress/Spike 0% = first guess too low (P04 Hunt 2). Keep these logs; do not delete them.

### Interaction 16 — Raise VUs after 0% Stress (intermediate)

- **Tool:** Cursor Agent
- **Date/time:** 2026-08-15 ~19:09 ICT
- **Prompt:** `Fix the plan: increase number of VUs. Explain why there's no error`
- **Output:** Explained Load 0% is correct. Draft retune: Stress **80** / think 0–100 ms; Spike **5→70→5**; CSV **80**. Registered `tram51`–`tram80` while SUT was still up.
- **Student verdict:** FIX — student then asked to lock **from P01** at Stress **100**, not stop at 80.

### Interaction 17 — Re-lock P01 at Stress 100 VU

- **Tool:** Cursor Agent
- **Date/time:** 2026-08-15 ~19:15 ICT
- **Prompt:** `Fix the plan from P01, stress 100VUs`
- **Output:** Rewrote `docs/p01-parameters.md` as the locked table: Load **20** / Stress **100** (25 s ramp, duration 325, think 0–100 ms) / Spike **5→80→5**. Updated Stress + Spike `.jmx`, generator `COUNT=100`, CSV `tram01`–`tram100`, P02/P09/P08/prompt-plan. Load `.jmx` unchanged. `--register` now skips emails that already login (schema `email` is not UNIQUE).
- **Student verdict:** ACCEPT as current design. Graded `.jtl` later replaced the first guess: Stress **100** (104397 samples) / Spike peak **80** (24330 samples). Archive of Stress-50 / Spike-40 is `logs/archive-first-guess-20260815/`.

## Task 1 — Test design (k6, bonus)

Not started (JMeter-only unless asked).

## Task 2 — Log analysis

### Interaction 18 — GATE P10 (raw `.jtl`)

- **Tool:** Cursor Agent
- **Date/time:** 2026-08-16 ~19:43 ICT
- **Prompt:** GATE P10 only — analyse attached raw JMeter `.jtl` for Load/Stress/Spike/soak; sample count; `success=false` vs non-2xx; elapsed mean/median/p90/p95/p99/max by label; throughput and think-time; first vs last 20% p95; laptop thresholds from data; 401/403 vs 5xx. No P12 infra.
- **Output:** `docs/p10-analysis.md` + `docs/_p10_analyze.py`. Graded files: Load 4972 / 9.60 rps / checkout p95 **22 ms** / 0% err; Stress 104397 / 321.43 rps / checkout p95 **534 ms** / 0% err; Spike 24330 / whole-run p95 381 ms but **hold checkout p95 464 vs recover 24**; Soak 5439 / 7.27 rps / checkout p95 23 ms, last-20% 24 vs first 20. Zero 401/403/5xx. Throughput includes think-time in wall-clock. Archive first-guess not used.
- **Student verdict:** ACCEPT after independent recompute (Interaction 19). Linear p95/error%/N/rps MATCH. Do not quote HTML Stress Total p95 455 as the raw value.

### Interaction 19 — Independent p95 / error% recompute (before trusting P10)

- **Tool:** Cursor Agent
- **Date/time:** 2026-08-16 ~21:07 ICT
- **Prompt:** `recompute p95/error% yourself (script or spreadsheet) before trusting the table of P10`
- **Output:** `docs/_recompute_jtl.py` (does not import `_p10_analyze.py`), `docs/p11-recompute.md`, `docs/_recompute_jtl.csv`. Sorted `elapsed`; `success=false` vs non-2xx counted separately. All four graded `.jtl`: error% **0** both ways. P10 linear p95 MATCH (tol 0.51 ms). HTML dashboard Total row disagrees on Stress (p95 455 vs raw 476; median 251 vs 233) and Spike (median 78 vs 73; p99 721 vs 926).
- **Student verdict:** Trust P10 **linear** tables. Do not trust HTML **Total** percentiles as the same statistic. Hunt table: Interaction 20.

### Interaction 20 — GATE P11 (claim → correct value)

- **Tool:** Cursor Agent
- **Date/time:** 2026-08-16 ~21:57 ICT
- **Prompt:** `Claim and correct value` (GATE P11: treat P10 as untrusted; independent recompute already in `p11-recompute.md`)
- **Output:** `docs/p11-misinterpretations.md` (report §3.2). Six mismatches: (1) Load login max 223 is mid-run not warm-up (`t0+123.24s`); (2) Stress “mild skew” vs p95/median=2.04; (3) Spike “baseline” window already at 13 VU; (4–6) HTML Total/login percentiles ≠ raw linear. Nine MATCH rows for N, dual error%, lockout 0, linear p95, think-time rps, trends, hold vs recover, after-ramp, soak p99.
- **Student verdict:** ACCEPT as §3.2. Did not invent arithmetic bugs in P10’s linear tables.

### Interaction 21 — GATE P12 (feasible vs hallucinated)

- **Tool:** Cursor Agent
- **Date/time:** 2026-08-16 ~22:01 ICT
- **Prompt:** GATE P12 only — from P10, classify each optimization Feasible vs Hallucinated for Express + sqlite3 + JWT + in-memory cart. Feasible only if the component exists/can be added without rewrite AND logs show that bottleneck.
- **Output:** `docs/p12-optimizations.md`. P10 proposed no Redis/WAL/K8s. **Feasible:** checkout `INSERT` as the Stress hot path (`server.js` L297–308); clear `userCarts` after checkout as leak hygiene (not the 534 ms cause). **Hallucinated as perf:** wait-for-login-`UPDATE` (would add latency; L47–51 is a correctness smell), parameterized LIKE, Redis, Postgres, Nginx, HPA, WAL (no SQLITE_BUSY), connection pool, products.name index, orders.user_id index, cluster/PM2, lockout tuning (0× 401/403).
- **Student verdict:** FIX then ACCEPT (Interaction 22).

### Interaction 22 — Human check of P12 vs `server.js`

- **Tool:** Cursor Agent
- **Date/time:** 2026-08-16 ~22:05 ICT
- **Prompt:** `Check p12`
- **Output:** Re-read `server.js` L14 / L35 / L47–51 / L144 / L290–308, `database.js` L5 / users `email TEXT` (no UNIQUE), `package.json` `sqlite3` only. Reclassified login fire-and-forget UPDATE from Feasible → **Hallucinated as a performance fix**. Line numbers in the remaining rows MATCH the repo.
- **Student verdict:** ACCEPT. Two Feasible rows remain: checkout INSERT hot path; cart-clear hygiene.

## Task 3 — Continuous-testing proposal

### Interaction 23 — GATE P13

- **Tool:** Cursor Agent
- **Date/time:** 2026-08-16 ~22:26 ICT
- **Prompt:** GATE P13 only — continuous model for eshop-sut: path filter, PR Load smoke vs main/nightly full suite, p95 +20% vs last 7 green, soak baseline, warn-on-PR / block-if-repeats, JMeter -n, mermaid, trade-offs. Search-to-buy specific.
- **Output:** `docs/p13-continuous.md`. Filter `server.js`/`database.js`/`package.json` (no `backend/routes/` in this SUT). Smoke = Load 20. Full = P09 order. Seed: soak **7.27 rps**, checkout p95 **23 ms**, error% **0**, memory **UNKNOWN**. Flag: +20% vs last-7 median **and** checkout p95 > 50 ms; 401/403 = setup fail. Warn PR; block main on second consecutive fail. k6 optional, not required. Do not gate Spike on whole-run p95.
- **Student verdict:** FIX then ACCEPT (Interaction 24).

### Interaction 24 — Human check of P13

- **Tool:** Cursor Agent
- **Date/time:** 2026-08-16 ~22:40 ICT
- **Prompt:** `check p13`
- **Output:** Confirmed 7/7 P13 bullets, soak seed vs P11, no Redis/HPA CI “fix”, Spike not gated on whole-run p95, memory left UNKNOWN. Patched path filter (`hw05-performance/**`, `package-lock.json`) and CI recompute note (`_recompute_jtl.py` hardcodes homework `.jtl` names).
- **Student verdict:** ACCEPT.

## Task 1 — Test design (k6, bonus)

### Interaction 25 — K01–K09 executed

- **Tool:** Cursor Agent
- **Date/time:** 2026-08-16 23:07–23:43 ICT
- **Prompt:** `Tự run từng step trong prompt plan k6 và tự double check qua từng step`
- **Output:** Scripts in `test-plans/` (`_k6_workflow.js` + Load/Stress/Spike/Soak). K04 found CSV `__ITER%n` would collide on `tram01` → K05 `(__VU-1+__ITER)%n`. Smoke 1 VU 30s: 44/44 checks. Graded `k6 run --out json` Load→Stress→Spike→Soak, all **0%** `http_req_failed`. Recompute: Load checkout p95 **21.29** / 9.51 rps; Stress **598.56** / 305.55 rps; Spike hold checkout **369.44** recover **22.78**; Soak **20.66** / 7.35 rps. Docs: `k04`–`k09`. Node not restarted after JMeter (possible warm `userCarts`). Memory UNKNOWN.
- **Student verdict:** ACCEPT bonus track. Do not mix JSON with `.jtl` baselines.

## Other

Prompt plan, frozen scope, and gate map were authored before P00. This log is P00–P13 plus k6 K01–K09.
