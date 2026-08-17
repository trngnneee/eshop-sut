# P11 — Misinterpretation hunt (report §3.2)

**Gate:** P11 only. P10 treated as untrusted.  
**Independent numbers:** [`p11-recompute.md`](./p11-recompute.md) / [`_recompute_jtl.csv`](./_recompute_jtl.csv) — script `docs/_recompute_jtl.py` (column `elapsed`, filter `label=…`; error% from `success` **and** `responseCode`).  
**Rule:** do not invent extra mismatches. Arithmetic MATCH uses tolerance 0.51 ms / 0.02 rps.

Independent headline (linear percentile, index `(n−1)×p/100`):

| Scenario | N | `success=false` % | non-2xx % | p95 overall | p95 checkout | wall-clock rps |
|----------|--:|------------------:|----------:|------------:|-------------:|---------------:|
| Load | 4972 | 0 | 0 | 19 | 22 | 9.60 |
| Stress | 104397 | 0 | 0 | 476 | 534 | 321.43 |
| Spike | 24330 | 0 | 0 | 381 | 437 | 130.30 |
| Soak | 5439 | 0 | 0 | 18 | 23 | 7.27 |

---

## 3.2 Misinterpretations found

| # | AI's claim (source) | Correct value (raw log citation) | Why the error happened |
|---|---|---|---|
| 1 | Load login **max 223 ms is a warm-up outlier** (median 4 ms). **P10 §2 Load.** | Max `elapsed=223` on `label=login` is at `timeStamp = t0 + 123.24 s` (`23127271_Load_20260814.jtl`, n_login=1003). Median login **4.00 ms MATCH**. 223 ms is a **mid-run** tail, not the first samples. | Assumed **max = JVM/connection warm-up** without checking `timeStamp`. Warm-up would sit near t0, not +2 minutes. |
| 2 | Stress: **“Mean ≈ median (mild skew).”** **P10 §2 Stress.** | Overall `elapsed`: mean **242.23**, median **233.00** (gap is small), but p95 **476.00**, p99 **594.00**, max **1009**. **p95 / median = 2.04.** | Confused **mean–median** (robust to tail) with **tail weight**. An SLA on p95 is not “mild.” |
| 3 | Spike **baseline ~0–30 s** overall p95 **19** / checkout **27** as the designed **5 VU** floor. **P10 §4 phase table.** | Same window: `max(grpThreads)=13`, n=1255, rps=41.85. The **5 VU** floor is **recover ~97–end**: max thr **5**, overall p95 **18**, checkout p95 **23.65** (P10 printed 24). | Phases measured from **first HTTP sample**, not Ultimate TG t=0, so “baseline” already overlaps the jump. P10 noted thr=13 but still published that row as baseline. |
| 4 | JMeter HTML Stress **Total** p95 (`pct2ResTime`) **455 ms**, median **251**. **`logs/report_stress/statistics.json` + `evidence/Stress_html_statistics.png`.** | Sort **all** `elapsed` (n=104397): linear p95 **476**, median **233**. Mean **242.23 MATCH**es HTML mean — same file, different Total aggregator. | HTML **Total** is not the percentile of concatenated label rows (and not NIST R7). Pasting the screenshot into the report would understate Stress p95 by **21 ms**. |
| 5 | HTML Load **login** p95 **6.8 ms**. **`report_load/statistics.json`.** | `label=login`, sorted `elapsed`, linear p95 **6.00** (n=1003). R6 p95 **6.80** = HTML. | Per-label HTML uses a **different percentile estimator** (R6-like). P10’s 6.00 is the linear value; the dashboard is not a second measurement. |
| 6 | HTML Spike **Total** p99 **721 ms**. **`report_spike/statistics.json`.** | All Spike `elapsed`, linear p99 **925.84**, max **1651** (n=24330). | Same Total-row trap as #4; worse on a **bimodal** jump+recover mix. |

---

## MATCH (P10 claim checked — keep these)

| # | P10 claim | Independent result | Note |
|---|---|---|---|
| M1 | N = 4972 / 104397 / 24330 / 5439 | MATCH | Four graded `.jtl`, not the archive. |
| M2 | `success=false` % = 0 and non-2xx % = 0 (all four) | MATCH (0 and 0, counted separately) | Did **not** mix assertion fail with HTTP status. |
| M3 | login 401/403 = 0; no 5xx | MATCH | Did **not** invent lockout as system failure. |
| M4 | Linear p95 by label (Load checkout 22, Stress 534, Spike 437, Soak 23; overall 19 / 476 / 381 / 18) | MATCH | See `p11-recompute.md`. |
| M5 | Wall-clock rps 9.60 / 321.43 / 130.30 / 7.27 **includes think-time** | MATCH | Denominator = last−first `timeStamp`. |
| M6 | First vs last 20% p95 table (Load flat; Stress falls 533→456; Spike last-20% = recover 18; Soak 17→19 / checkout 20→24) | MATCH | |
| M7 | Spike **whole-run** p95 381 is a **blend**; cite hold vs recover | MATCH | Hold checkout p95 **464**, recover **23.65≈24**, hold rps **289.48**. |
| M8 | Stress after +25 s: overall p95 480, checkout 537, n=97544 / 19504 | MATCH | Ramp-aware cut does not change the story (full-run p95 already 476). |
| M9 | Soak checkout p99 **122.74** (P10 rounded to 123) | MATCH | Thin tail, still `success=true`, code 200. |

**Stop condition met.** Report §3.2 = the mismatch table above. Next gate is P12 (feasible vs hallucinated optimizations) — not this file.
