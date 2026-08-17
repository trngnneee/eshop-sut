# HW05 Prompt Plan — Search-to-buy (23127271)

**Student:** Võ Ngọc Bích Trâm · `23127271`  
**SUT:** EShop backend `http://localhost:3000`  
**Tool (required):** Apache JMeter  
**Tool (bonus):** k6 — gated prompts **K01–K09** (after JMeter P08 freeze)  
**Workflow (frozen):** Search-to-buy  
**Date for filenames:** `20260814` (change if a plan is generated on a later day)

This file is the **prompt plan**, not the audit log. Copy one prompt per gate. After each AI reply, human-review before the next gate. Paste every interaction into `ai-audit-report.md` (tool, timestamp, prompt, output). Do **not** share these prompts with teammates — copying prompts scores 0 for both parties.

- Frozen scope (endpoints, CSV, lockout, VU sequence): [`frozen-scope.md`](./frozen-scope.md)
- Gate map (P00–P16 + K01–K09, Bloom, stop conditions): [`gate-map.md`](./gate-map.md)
- k6 bonus prompts: [`k6-prompt-plan.md`](./k6-prompt-plan.md)

---

## Why gated prompts

The brief forbids a single generic prompt such as *“run a load test and tell me whether performance is good.”* Drive the technique the way it was taught: map endpoints → justify parameters → CSV + lockout → distinct listeners → generate plans → human fix → execute with real evidence → AI analyses raw `.jtl` → hunt misreads → judge optimizations → continuous-testing proposal.

AI drafts. You own every number. Never ask AI to invent `.jtl` rows, screenshots, hardware specs, or soak thresholds.

---

## How to paste each prompt

1. Attach the files named in **Context**.
2. Stop at the **Stop condition**. Do not ask for the next gate in the same message.
3. After the reply: verdict (`ACCEPT` / `FIX` / `REJECT`) + one-line student note.
4. Log the interaction in the AI Audit Report.

Working folders (create when generating artifacts):

```
SoftwareTesting-HW/HW5/23127271/
  docs/           prompt-plan.md, frozen-scope.md, gate-map.md, prompt_log.md
  test-plans/     *.jmx + *.js + CSV
  logs/           *.jtl + HTML reports + k6 *.json
  evidence/       Task Manager + dxdiag
  report/         main report
  audit/          AI Audit + Critique
```

---

## P00 — Map workflow to real endpoints

**Stop condition:** endpoint table + 3 coverage sentences. No thread counts, no `.jmx`.

**Context:** `@Repo/eshop-sut/backend/server.js` · `@SoftwareTesting-HW/HW5/README.md` (section Trâm) · [`frozen-scope.md`](./frozen-scope.md).

```
You are assisting HW05 performance-test design for EShop. This is GATE P00 only.

Student 23127271. Workflow: Search-to-buy. Base URL: http://localhost:3000.

Do NOT invent REST paths. Confirm against server.js:

- Auth-heavy: POST /api/login
- Read-heavy: GET /api/products?search={q} then GET /api/products/{id}
- Transactional: POST /api/cart then POST /api/checkout

Produce:
1. A request sequence table: step, method, path, headers, body fields, extractors (JSON), think-time band, assertions (status AND JSON field — 200 with empty {} on product detail is a known SUT quirk).
2. Three short coverage sentences: which step is auth-heavy, which is read-heavy, which is transactional, and why this is not Khoa's browse-to-buy (he uses GET /api/products with no search).
3. SUT facts that will break a naive load test if ignored: login_attempts += 2 and 180s lock; in-memory cart; search LIKE interpolation; missing product id returns 200 {}.

Do not propose thread counts, CSV rows, listeners, or JMeter XML.
```

**You check:** paths match `server.js`; no categories/coupon/my-orders; detail assertion does not treat empty `{}` as a found product.

---

## P01 — Load / Stress / Spike parameters with justification

**Stop condition:** parameter table + rationale per scenario. No `.jmx`.

**Context:** P00 output · this machine is a student laptop (Windows, SUT + JMeter + Node on the same host).

```
GATE P01 only. Using the Search-to-buy sequence from P00, propose parameters for THREE scenarios that reuse the SAME workflow.

Constraints:
- This is a local demo Node + SQLite SUT on a student Windows laptop, not production. Do not copy AWS-scale numbers.
- Load = expected peak the laptop can likely hold with realistic think-time.
- Stress = beyond that, until errors or latency climb; still must complete the full login→search→detail→cart→checkout path.
- Spike = sudden jump then a short recover window (not a second Stress with a different name).
- Login: Load uses only valid credentials. Do not design Stress/Spike as “hammer failed logins” — that only measures lockout, not checkout capacity. Unique CSV users ≥ thread count.
- Think-time must differ by scenario (Load realistic 1–3s; Stress/Spike shorter) and you must say why.
- Give threads, ramp-up, duration (or schedule), think-time, expected outcome to observe.

Output a markdown table:

Scenario | Threads | Ramp-up | Duration / schedule | Think-time | What “success” means | Why these numbers for THIS SUT

Also state starting guesses for a later 10–15 min soak (constant threads, not Spike). Do not generate .jmx.
```

**You check:** Stress threads > Load; Spike is a jump+recover, not “Load but longer”; numbers are laptop-scale (e.g. Load ~10–30, not 5 000).

---

## P02 — CSV parameterization and lockout strategy

**Stop condition:** CSV files + lockout/reset policy. No `.jmx`.

**Context:** P01 table · seed users in SUT README · FR-02 vs actual `+= 2` / 180s.

```
GATE P02 only. Design data-driven input for Search-to-buy.

Need:
1. CSV header exactly:
   email,password,search,product_id,quantity,price,total_amount,shipping_address
2. At least as many unique emails as the highest thread count in P01. Prefix emails tram01@eshop.com, tram02@… — do not use test@eshop.com (shared seed).
3. search keywords that match seed product names (e.g. Laptop, iPhone) — no SQL metacharacters.
4. product_id / price / total_amount consistent with seed (or say “verify against DB after seed”).
5. JMeter CSV Data Set: delimiter, recycle on EOF vs stop-thread, sharing mode. Recommend recycle=true for Load duration > row count, but unique emails so parallel logins do not share one account.
6. Lockout policy:
   - Load: valid passwords only.
   - Stress/Spike: still valid passwords; document that 2 failed logins lock for 180s (implementation, not the spec’s “3 fails / 30s”).
   - Between Stress and Spike: numbered reset steps (wait locked_until, or sqlite UPDATE login_attempts=0, locked_until=NULL, or re-seed) with a place to write timestamps later.
7. How we will register the tramNN users before the first run.

Output the CSV contents (or a generator script) plus the recycle/lockout section. No .jmx.
```

**You check:** unique users ≥ max threads; no shared `test@eshop.com`; search terms are safe.

---

## P03 — Assign three distinct report views

**Stop condition:** listener assignment + why. No `.jmx`.

```
GATE P03 only. Across the three JMeter plans, assign THREE different listeners. Do not reuse a type.

Required pairing unless you justify a swap:
- 23127271_Load_20260814   → View Results Tree (inspect request/response while volume is still readable)
- 23127271_Stress_20260814 → Summary Report
- 23127271_Spike_20260814  → Aggregate Report

For each: what the listener shows that the other two do not, and what we will screenshot. Mention that GUI listeners are for evidence; the graded run still saves a .jtl via -l and HTML via -e -o.

No thread-group XML yet.
```

**You check:** three different types; filenames match `{StudentID}_{ScenarioType}_{YYYYMMDD}`.

---

## P04 — Human review of the AI design (before any `.jmx`)

**Stop condition:** issue list “what / why / fix”. You may disagree with the AI.

**Context:** P00–P03 outputs.

```
GATE P04 only. Critically review P00–P03 as a performance tester who has read EShop server.js. Do not generate JMeter XML.

Hunt specifically for:
1. Unrealistic ramp-up or think-time (same numbers copied across Load/Stress/Spike).
2. Thread counts that will not stress a local Node+SQLite app, or that will only lock accounts.
3. Assertions that check HTTP 200 only (product detail 200 {} ; checkout 200 without orderId).
4. Missing lockout handling (spec 3×30s vs code +=2 / 180s / 403).
5. CSV: one row recycled as many users; Recycle/Stop-thread mismatch.
6. Workflow drift toward a teammate’s flow (full list, categories, coupon, my-orders).
7. Soak confused with Spike.

For each issue: (a) what is wrong, (b) why the model missed it (vague prompt / no SUT knowledge / generic web-app prior), (c) the concrete fix I must apply in P05–P08.

If something is actually fine, say so briefly — but do not write “no issues found” without checking the seven items above.
```

**You write** the Task 1 “Review and fix” section from this gate (edit the AI’s list; keep genuine corrections).

---

## P05 — Generate Load plan only

**Stop condition:** one `.jmx` + matching CSV path. Not Stress/Spike.

**Context:** locked P00–P04 · `@SoftwareTesting-HW/HW5/23127271/test-plans/` (create if missing).

```
GATE P05 only. Generate the JMeter Load test plan for Search-to-buy.

Filename: 23127271_Load_20260814.jmx
CSV: 23127271_users.csv (from P02)

Must include:
- Test Plan + Thread Group named 23127271_Load_20260814 with P01 Load numbers (after P04 fixes): 20 threads, ramp 40 s.
- JMeter scheduler Duration INCLUDES ramp-up. P01 “8 min constant after ramp” ⇒ duration = 40 + 480 = **520** seconds, not 480.
- HTTP Request Defaults: http://localhost:3000; connect + response timeout 10 s.
- Content-Type: application/json only on POST samplers (login/cart/checkout). Do not put it on Thread Group so GET search/detail inherit it.
- Authorization: Bearer ${token} only as a child Header Manager of cart and checkout (not on login/search/detail).
- JSON Extractor on login for $.token only. Do not extract unused $.user.id.
- CSV Data Set Config as P02 (variableNames filled, Ignore first line=true, quotedData, recycle, All threads). Filename 23127271_users.csv.
- ONE Uniform Random Timer: offset 1000, range 2000 (1000–3000 ms). No per-step P00 timers.
- Response Assertion on every sampler: status AND JSON field ($.token / $[0].id / $.name+$.id / $.message=Added to cart / $.orderId). Do not assert price type.
- on_sample_error = startnextloop (failed detail must not POST cart with NAME_NOT_FOUND).
- ONE listener: View Results Tree. No Summary, no Aggregate on this plan.
- Cookie? not required if we use Bearer. Do not add unused Config Elements.

Output valid JMeter 5.x XML (.jmx). Do not emit Stress or Spike in this message.
```

**You check:** filename; duration **520**; only View Results Tree; JSON extractors; empty-detail assertion; Content-Type not on GETs.

---

## P06 — Generate Stress plan only

```
GATE P06 only. Same Search-to-buy workflow and same CSV as Load. Clone assertions, CSV config, Bearer-on-cart/checkout-only, timeouts, and startnextloop from the accepted Load plan.

Filename: 23127271_Stress_20260814.jmx
Thread Group uses P01 Stress numbers: **100** threads, ramp **25 s**, think Uniform **0–100 ms** (offset 0, range 100).
JMeter scheduler Duration INCLUDES ramp-up. P01 “5 min sustained at 100” ⇒ duration = 25 + 300 = **325** seconds.
ONE listener: Summary Report. Do not include View Results Tree or Aggregate Report.
No failed-login sampler.

Output only this .jmx.
```

**You check:** duration **325**; Summary only; think-time 0–100 ms; 100 threads; same five paths as Load.

---

## P07 — Generate Spike plan only

```
GATE P07 only. Same workflow and CSV as Load (assertions, Bearer, CSV, timeouts, startnextloop).

Filename: 23127271_Spike_20260814.jmx
Model a SPIKE, not another Stress. MUST use jp@gc Ultimate Thread Group (or an equivalent stepped schedule). Do NOT emit a flat Thread Group of 80.
P01 schedule: 30 s at 5 → jump to **80** in 2 s → hold 60 s → drop to 5 in 5 s → hold 90 s recover. Peak **80** (below Stress **100**).
Think-time Uniform 0–200 ms (offset 0, range 200).
ONE listener: Aggregate Report. Jump vs recover is NOT in that table — note in comments that HTML -e -o and .jtl time splits show the shape.

Output only this .jmx. Explain the schedule in a short comment inside the plan name or a sibling 23127271_Spike_20260814-notes.md.
```

**You check:** recover window exists; plugin/stepped group not a flat 80; listener is Aggregate Report.

---

## P08 — Apply human fixes

**Context:** P04 issue list + the three `.jmx` files.

```
GATE P08 only. Apply the accepted P04 fixes PLUS P05 review nits to the three existing .jmx files and CSV. Do not redesign the workflow. Do not add k6.

Must still be true after the patch:
- Load duration 520 (40+480); Stress duration **325** (25+300); Spike Ultimate TG **5→80→5**.
- Content-Type only on POSTs; Bearer only on cart/checkout; startnextloop; no unused user_id extractor.
- No failed-login sampler; CSV variableNames filled.

List each file touched and the exact change. Keep filenames 23127271_{Load|Stress|Spike}_20260814.
```

Commit after this gate: `test plans: Search-to-buy Load/Stress/Spike (23127271)`.

---

## P09 — Execution runbook (AI writes instructions; you run them)

**Stop condition:** commands + evidence checklist. No fake metrics.

```
GATE P09 only. Write the execution runbook for 23127271 Search-to-buy. Do NOT invent results.

Include:
1. Preflight: SUT up on :3000, seed/register tramNN users, Task Manager + JMeter visible for recording, dxdiag once (hostname must match previous HW).
2. Order: Load → reset/check unlock → Stress → reset lockout (document steps) → Spike → soak 10–15 min at the Load (or slightly below Load) constant level.
3. Non-GUI commands:

jmeter -n -t 23127271_Load_20260814.jmx -l 23127271_Load_20260814.jtl -e -o report_load/
(and Stress/Spike/soak equivalents)

4. Per-run evidence: tool + Task Manager in ONE screenshot; save .jtl AND HTML folder.
5. Soak: what to watch (error%, p95 trend, Node memory). Report later as max stable RPS, memory ceiling, elapsed time when latency starts climbing — leave blanks for me to fill from the real run.
6. Demo video: ≥6 minutes, Vietnamese narration, JMeter + resource monitor same frame; split per scenario allowed.
7. If a functional bug appears (crash, 200 {} on a real id, checkout without orderId), file GitHub Issue with screenshot — high latency alone is optional.

GUI mode is only for the demo video / Tree listener screenshots; timed numbers come from -n runs.
```

**You:** run P09; put real `.jtl` under `logs/`. Do not start P10 without files.

---

## P10 — Analyse raw `.jtl` (after real runs)

**Context:** attach `23127271_Load_20260814.jtl`, Stress, Spike, soak (or a large excerpt + how it was sampled). Optionally a pandas/python recompute you already ran.

```
GATE P10 only. Analyse the attached RAW JMeter .jtl files for Search-to-buy (23127271). Do not use a pre-computed summary as the source of truth.

For each scenario (Load, Stress, Spike, soak):
1. Sample count, error rate (success=false vs non-2xx — these can differ because of assertions).
2. elapsed: mean, median, p90, p95, p99, max — by label (login, search, detail, cart, checkout) and overall.
3. Throughput (req/s). State whether think-time is included in wall-clock.
4. Time trend: does p95 rise over the run (split first vs last 20% of timestamps)?
5. Propose thresholds for THIS SUT on a laptop (e.g. Load p95 checkout < X ms, error% < Y). Justify from the data, not from Google SLA folklore.
6. Call out lockout-shaped errors (401/403 on login) separately from 5xx/connection failures.

Cite label names and timestamp ranges. If a file is truncated, say what you could not compute.
Do not propose infrastructure that is not in this repo yet (that is P12).
```

**You:** recompute p95/error% yourself (script or spreadsheet) before trusting the table.

---

## P11 — Misinterpretation hunt

```
GATE P11 only. I will now treat P10 as untrusted. Here is my independent recompute from the raw .jtl:

<paste your pandas/Excel numbers: per-label p95, error%, throughput>

Compare P10 claims to these numbers. For every mismatch:
Claim → Correct value (with how I computed it: column elapsed, filter label=…) → Why the model erred (mean vs p95, success vs responseCode, think-time in RPS, warm-up included, lockout counted as system failure).

Do not invent extra mismatches. If a claim matches, say MATCH.
Output the table I will put in the report section 3.2.
```

If you want the AI to *suggest* likely mistakes before you recompute, ask it only for a **checklist**, then fill the table yourself. The grade is on **your** citations from raw logs.

---

## P12 — Judge optimization recommendations

**Context:** P10 suggestions · `@Repo/eshop-sut/backend/server.js` · package.json / SQLite usage.

```
GATE P12 only. From the P10 analysis, list each proposed optimization. For each, classify Feasible or Hallucinated for THIS SUT.

Stack facts:
- Node Express, better-sqlite/sqlite3 file DB, JWT, in-memory userCarts, no Redis, no connection pooler, search is string-interpolated LIKE, cart is process memory (lost on restart), orders go to SQLite.

A suggestion is Feasible only if (1) the component exists or can be added without rewriting the product, AND (2) the logs actually show that bottleneck.
Hallucinated examples: Redis cache, Postgres indexes, Nginx tuning, SQLite WAL if they never showed write-lock waits, Kubernetes HPA.

Output: Recommendation | Feasible/Hallucinated | Reasoning tied to a metric or a file:line in server.js.
```

---

## P13 — Continuous performance-testing proposal (G9.6)

```
GATE P13 only. Propose a continuous performance-testing model for eshop-sut that:
1. Watches commits and decides whether to run tests (path filter: backend/routes, server.js, DB schema, package.json — skip docs/frontend-only).
2. Tiers: cheap Load smoke on qualifying PRs vs full Load+Stress+Spike+soak on main/nightly.
3. Stores p95 + error% per commit; flags regression if p95 exceeds a concrete margin over a rolling baseline (pick a number, e.g. +20% vs last 7 green runs on the same runner class, AND error% above Load threshold). Use the soak numbers from my real run as the initial baseline once filled: <paste soak RPS / p95 / memory>.
4. Policy: warn on PR, block on main if it repeats — pick one and why.
5. Tooling: JMeter -n in CI is acceptable; mention k6 only as optional later, do not require it.
6. Mermaid flowchart: commit → filter → smoke/full/skip → compare baseline → pass/flag.
7. Trade-offs: CI minutes cost, false alarms on noisy laptops/shared CI, plan maintenance when APIs change.

This must be specific to Search-to-buy endpoints and this homework’s artifacts, not a generic “add Gatling to Jenkins” essay.
```

---

## P14 — AI Critique (200–300 English words)

```
GATE P14 only. Draft ONE paragraph, 200–300 words, critiquing the AI on THIS assignment.

Must answer: Where was it wrong, biased, or incomplete? Why did it fail (prompt quality, no SUT implementation knowledge, generic production priors)? What collaboration principle did I learn?

Ground it in P04 design misses AND P11 metric misreads AND P12 hallucinated fixes. No bullet list. No generic “AI is a useful assistant but humans must verify” without naming a Search-to-buy / JMeter / lockout / .jtl example.
```

**You:** count words; replace any claim you did not actually observe.

---

## P15 — Assemble the report (numbers from you)

**Context:** skill templates `report-template.md`, `readme-template.md`, `ai-audit-template.md` · real paths under `logs/` and `evidence/`.

```
GATE P15 only. Fill the HW05 main report markdown from templates. Use ONLY numbers I provide below. If a field is UNKNOWN, write UNKNOWN — do not estimate.

<paste: thread table, soak RPS, memory, p95 table, misinterpretation table, GitHub issue URLs, YouTube links when they exist>

Also draft README self-assessment table (do not default every row to 20/20). List zip contents checklist from the assignment Part 14.

Do not generate fake screenshots or .jtl.
```

---

## P16 — Agent Skill demo (second video, 10 points)

```
GATE P16 only. Write a 4–6 minute Vietnamese narration outline for the Agent Skill demo video (this is NOT the JMeter ≥6 min evidence video).

Show live: invoke the performance-testing skill → P00 map Search-to-buy → P01 parameters → open the generated Load plan. One complete endpoint group is enough (read-heavy search+detail, with auth+cart still in the same workflow).

List on-screen files the camera must show. Separate URL from the Task 1 demo.
```

---

## Bonus k6 (only if you run both tools)

Full copy-paste prompts (one gate per message, same rules as P05–P11): [`k6-prompt-plan.md`](./k6-prompt-plan.md).

Do **not** start K01 until JMeter P08 is frozen. Analyse k6 JSON in **K07** separately from P10; compare only in **K09**.

| Gate | Stop condition | AI may produce | You check |
|------|----------------|----------------|-----------|
| **K01** | One Load `.js` | `23127271_Load_20260814.js` — stages 40s→20 + 480s hold; per-request sleep 1–3s; Tree ≡ `--http-debug` peek | Same five paths + CSV as JMeter Load |
| **K02** | One Stress `.js` | 100 VUs, 25s+300s, sleep 0–100 ms; console summary | Not Stress-50; not failed-login |
| **K03** | One Spike `.js` | `stages` **5→80→5** + 90s recover; `--out json` ≡ Aggregate | Not a flat 80 |
| **K04** | Issue list | Parity hunt vs `.jmx` / P01 (think-time per request, tags, checks) | Genuine corrections; no “no issues found” |
| **K05** | Patch list | Fixes only | Filenames unchanged |
| **K06** | Runbook | `k6 run --out json=…` + soak 15 VU clone; evidence checklist | **You** run; no fake JSON |
| **K07** | Metrics from JSON | p95/error%/rps by `name` tag; Spike hold vs recover | Recompute before trusting |
| **K08** | Hunt table | Claim → correct value from JSON | Flag if K07 copied P10 |
| **K09** | Comparison table | JMeter vs k6 p95/error%/rps + footprint | UNKNOWN if not measured; no generic “k6 is faster” |

---

## Anti-cheat — never prompt for these

| Forbidden | Why |
|-----------|-----|
| “Generate a realistic .jtl” / fake HTML report | Part 11: raw logs must be from a real run |
| Invented dxdiag / Task Manager screenshots | Hardware hostname must match prior HW |
| “Generate a realistic k6 JSON” / fake console summary | Bonus track still needs a real `k6 run` |
| One prompt that designs + runs + analyses + writes the full report | Violates AI-first / human-review |
| Teammate’s browse / category / coupon / my-orders sequence | Duplicate workflow |
| Softening assertions so Stress “looks green” | You own correctness |

---

## Suggested git commits (one per step)

1. `docs: HW05 prompt plan (Search-to-buy)`  
2. `test-plans: CSV + Load jmx`  
3. `test-plans: Stress jmx`  
4. `test-plans: Spike jmx`  
5. `logs: Load/Stress/Spike jtl + HTML` (after real runs)  
6. `docs: AI log analysis + misinterpretation hunt`  
7. `docs: continuous performance-testing proposal`  
8. `report: HW05 main report + README self-assessment`  
9. `test-plans: k6 Load/Stress/Spike js` (bonus, after K05)  
10. `logs: k6 json` (after real `k6 run`)

---

## Execution checklist

- [ ] P00–P04 done; “Review and fix” notes exist **before** first `.jmx` run
- [ ] Three uniquely named plans + three listeners
- [ ] CSV unique `tramNN` users
- [ ] **Before first `-n` run:** SUT up + `node generate-tram-users.js --register` (**100** accounts; see `test-plans/BEFORE-RUN.md`)
- [x] Real `-n` runs + soak; screenshots + dxdiag
- [x] P10 on raw `.jtl`; independent recompute MATCH (`docs/p11-recompute.md`); P11 hunt table (`docs/p11-misinterpretations.md`)
- [x] P12 classifications vs `server.js`
- [x] P13 flowchart + cost/false-alarm
- [ ] P14 200–300 words
- [x] Task 1 demo video: https://youtu.be/Nyvm0bxZxgA
- [ ] Agent Skill demo (second YouTube; P16)
- [ ] Zip name: `23127271_HW05_AI_Performance_<grade>.zip`
- [x] **k6 bonus (optional):** K01–K05 scripts + K06 real JSON + K07/K08 + K09 comparison — [`k6-prompt-plan.md`](./k6-prompt-plan.md)
