# K07 — Raw k6 JSON analysis (23127271 Search-to-buy)

**Gate:** K07 only. Source = `logs/23127271_*_20260814.json` (`type=Point`, `metric=http_req_duration`, tag `name`).  
**Recompute:** `docs/_recompute_k6.py` (linear percentile, same formula as P11).  
**Not used as truth:** k6 console summary (cross-check only). **Not copied:** P10 JMeter tables.

k6 duration `value` is **milliseconds**. `sleep()` is in wall-clock rps. All four runs: `http_req_failed` **0**. Checks 100% on console (Load 11055, Stress 219318, Spike 54395, Soak 12265).

| Scenario | Duration points | Failed | Wall span | http rps (sleep in) | t0–t1 ICT |
|----------|----------------:|-------:|----------:|--------------------:|-----------|
| Load | 5025 | 0 | 528.3 s | **9.51** | 23:12:38–23:21:26 |
| Stress | 99690 | 0 | 326.3 s | **305.55** | 23:21:30–23:26:56 |
| Spike | 24725 | 0 | 187.3 s | **131.99** | 23:26:58–23:30:06 |
| Soak | 5575 | 0 | 758.9 s | **7.35** | 23:30:07–23:42:46 |

Per-label counts are **equal** (Load 1005×5, Stress 19938×5, Spike 4945×5, Soak 1115×5): k6 finishes iterations; JMeter scheduler can stop mid-loop.

login **401/403:** 0 (no `status` other than 200 on duration points; smoke + graded checks 100%).

---

## elapsed (ms) by `name` tag

### Load (20 VU)

| Label | n | mean | p50 | p90 | p95 | p99 | max |
|-------|--:|-----:|----:|----:|----:|----:|----:|
| overall | 5025 | 5.16 | 2.16 | 16.47 | **18.29** | 21.49 | 223.17 |
| login | 1005 | 2.94 | 2.78 | 3.68 | 4.34 | 12.97 | 33.26 |
| search | 1005 | 2.23 | 1.95 | 2.75 | 3.18 | 13.24 | 57.28 |
| detail | 1005 | 2.08 | 1.95 | 2.65 | 2.99 | 9.22 | 51.65 |
| cart | 1005 | 1.59 | 1.62 | 2.16 | 2.48 | 3.57 | 14.79 |
| checkout | 1005 | 16.98 | 16.43 | 19.82 | **21.29** | 28.11 | 223.17 |

### Stress (100 VU)

| Label | n | mean | p50 | p90 | p95 | p99 | max |
|-------|--:|-----:|----:|----:|----:|----:|----:|
| overall | 99690 | 263.61 | 250.98 | 461.87 | **522.30** | 646.45 | 868.69 |
| login | 19938 | 317.27 | 309.18 | 489.76 | 540.32 | 658.44 | 864.35 |
| search | 19938 | 265.48 | 254.59 | 422.77 | 479.70 | 584.85 | 797.87 |
| detail | 19938 | 271.55 | 257.00 | 442.82 | 504.29 | 620.23 | 868.69 |
| cart | 19938 | 115.20 | 103.70 | 206.54 | 246.63 | 323.93 | 515.09 |
| checkout | 19938 | 348.54 | 336.75 | 536.47 | **598.56** | 731.85 | 858.02 |

Checkout still slowest. Max 869 ms — no 10 s timeout. **0%** error: knee is latency, not 5xx.

### Spike (5→80→5)

| Label | n | mean | p50 | p90 | p95 | p99 | max |
|-------|--:|-----:|----:|----:|----:|----:|----:|
| overall | 24725 | 131.76 | 104.43 | 277.49 | **320.83** | 725.33 | 1800.47 |
| checkout | 4945 | 174.77 | 164.99 | 310.93 | **354.84** | 1023.02 | 1779.67 |

Whole-run p95 **mixes** hold+recover. Do **not** treat 321 ms as “the spike.”

Phases vs **first duration sample** (k6 stages start at test start; first HTTP ≈ +1 s):

| Phase | n | overall p95 | checkout p95 |
|-------|--:|------------:|-------------:|
| baseline ~0–30 s | 1468 | 17.27 | 22.02 |
| jump ~30–32 s | 529 | 152.52 | 156.07 |
| **hold ~32–92 s** | 17356 | **336.77** | **369.44** |
| drop ~92–97 s | 1080 | 328.84 | 343.61 |
| **recover ~97–end** | 4292 | **17.40** | **22.78** |

SUT **did recover** (22.78 ≈ Load checkout 21.29).

### Soak (15 VU)

| Label | n | mean | p50 | p95 | p99 | max |
|-------|--:|-----:|----:|----:|----:|----:|
| overall | 5575 | 5.11 | 2.06 | **17.41** | 22.23 | 245.47 |
| checkout | 1115 | 16.77 | 15.72 | **20.66** | 35.07 | 245.47 |

---

## Time trend (first vs last 20% of timestamp span)

| Scenario | First p95 / checkout | Last p95 / checkout | Trend |
|----------|----------------------|---------------------|-------|
| Load | 18.23 / 22.09 | 18.08 / 20.70 | Flat |
| Stress | 424.27 / 447.92 | 508.83 / 595.72 | **Rises** after ramp (unlike JMeter Stress which fell) |
| Spike | 273.56 / 285.02 | 16.71 / 19.23 | Last 20% = recover @5 VU |
| Soak | 17.32 / 20.30 | 16.19 / 19.84 | Flat (slightly faster later) |

Node was **not** restarted after JMeter P09 — `userCarts` may already be large. Stress climb is **not** proven as a k6-only defect.

---

## Thresholds from **this** k6 run (laptop)

| Gate | Proposed | Why |
|------|----------|-----|
| Load error% | **< 0.1%** | Observed 0/5025 failed. |
| Load checkout p95 | **< 50 ms** | Observed **21.29 ms**. |
| Stress knee | checkout p95 **≥ 10× Load** or error% **> 1%** | 598.56 / 21.29 ≈ **28×**, 0% err. |
| Spike recover | checkout p95 **< 2× Load** (~43 ms) | Observed **22.78 ms**. |
| Soak | last-20% checkout p95 **< 2×** first-20% | 19.84 / 20.30 ≈ 1.0. |

**Stop.** Next: K08 (do not trust this table blindly) then K09 vs JMeter.
