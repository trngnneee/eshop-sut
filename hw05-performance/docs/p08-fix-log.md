# P08 — Apply P04 + P05-fix to plans (23127271)

**Gate:** P08 only. No k6. No workflow redesign.  
**Date:** 2026-08-15  
**Result:** Structural P04/P05-fix items were **already present** in Load (after P05-fix), Stress (cloned from Load), and Spike. P08 **verified** every must-still-be-true item and stamped TestPlan comments with `P08 freeze`. After the first `-n` run (Stress 50 / Spike peak 40, both 0% err), P01 re-locked and this file’s **current** table is Load **20** / Stress **100** / Spike **5→80→5** / CSV **100**.

Suggested commit message (when you ask): `test plans: Search-to-buy Load/Stress/Spike (23127271)`.

---

## Must-still-be-true (current lock — P01 after first `-n`)

| Check | Load | Stress | Spike |
|-------|------|--------|-------|
| Duration / schedule | 520 (40+480) | **325** (25+300) | Ultimate TG **5→80→5** (rows 5@187s + **75**@30/2/60/5) |
| Threads / ramp / think | 20 / 40s / 1000–3000 | **100** / **25s** / **0–100** | peak **80** / 0–200 |
| Content-Type only on POSTs | yes (login, cart, checkout) | yes | yes |
| Bearer only on cart/checkout | yes | yes | yes |
| `startnextloop` | yes | yes | yes |
| No `user_id` extractor | yes | yes | yes |
| No failed-login sampler | yes | yes | yes |
| CSV `variableNames` filled | yes | yes | yes |
| Listener | View Results Tree | Summary Report | Aggregate Report |
| Asserts (`token`, `$[0].id`, `$.name`/`$.id`, Added to cart, `orderId`) | yes | yes | yes |
| 10 s connect/response timeout | yes | yes | yes |

First freeze (before `-n`) was Stress 50 / 315 / think 200–500 and Spike 5→40→5. That freeze is **history**; do not copy it into a new plan.

---

## Files touched and exact change

| File | Exact change in P08 |
|------|---------------------|
| `test-plans/23127271_Load_20260814.jmx` | **Comment only:** TestPlan.comments stamped `P05+P08 freeze` and restates duration 520 / Content-Type / Bearer / startnextloop / no user_id. **No sampler/thread XML change** (already patched in P05-fix). |
| `test-plans/23127271_Stress_20260814.jmx` | **Comment only at first freeze:** TestPlan.comments stamped `P06+P08 freeze`. **Later retune:** 100 threads / 25 s / 325 / think 0–100 ms (see § P08 retune). |
| `test-plans/23127271_Spike_20260814.jmx` | **Comment only at first freeze:** Ultimate TG + Aggregate-vs-HTML caveat. **Later retune:** peak **80** (row2 **+75**). |
| `test-plans/23127271_users.csv` | First freeze: 50 unique `tramNN`. **Later:** **100** unique `tramNN`; no `test@eshop.com`; search ≠ `Laptop`; quoted addresses. |
| `test-plans/23127271_Spike_20260814-notes.md` | **None** (schedule already documented in P07). |
| `docs/p08-fix-log.md` | **Created** (this file). |

---

## P04 items applied earlier (not re-changed in P08)

Already in all three `.jmx` from P05-fix → P07:

1. One P01 Uniform timer (not P00 per-step bands).  
2. Search rejects empty `[]` via `$[0].id`.  
3. Cart `name` from detail `Extract product_name` (CSV has no `name` column).  
4. No numeric `price` assertion (even-id string quirk).  
5. HTTP Defaults timeouts 10 s.  
6. Relative CSV path + `variableNames` + ignoreFirstLine + quotedData + recycle + All threads.  
7. Spike = Ultimate Thread Group, not a flat peak (locked **5→80→5**).  
8. Valid passwords only (lockout probe stays P09).

**Stop condition met:** change list + filenames unchanged. Next gate is P09 (execution runbook).

---

## P08 retune (same day, after first `-n` run)

First Stress **50 / 0% err**. P01 then locked to **100 VU** (student):

| File | Change |
|------|--------|
| `23127271_Stress_20260814.jmx` | **100** threads; ramp **25** s; duration **325**; think **0–100 ms** |
| `23127271_Spike_20260814.jmx` | peak **80** (UTG row2 **+75**) |
| `23127271_Load_20260814.jmx` | **unchanged** (Load 0% is the correct outcome) |
| `23127271_users.csv` + generator | **100** unique `tramNN`; `--register` skips emails that already login |

Keep first-run `.jtl` as “guess was too low.” Re-run Stress/Spike after SUT up + `--register` (restart Node wipes users).
