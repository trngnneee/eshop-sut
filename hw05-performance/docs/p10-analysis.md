# P10 — Raw `.jtl` analysis (23127271 Search-to-buy)

**Gate:** P10 only. Source of truth = CSV rows in `logs/*.jtl`, **not** HTML Summary/Aggregate dashboards.  
**Recompute:** `docs/_p10_analyze.py` (linear interpolation percentile on sorted `elapsed`: index `(n-1)*p/100`).  
**Not used:** `logs/archive-first-guess-20260815/` (Stress 50 / Spike 40, 0% error — first guess).  
**Not used:** Interaction 15 console lines as p95.

**Files:**

| Scenario | File | Bytes | Samples | Wall-clock (first→last `timeStamp`) | Max `grpThreads` |
|----------|------|-------|---------|--------------------------------------|------------------|
| Load | `logs/23127271_Load_20260814.jtl` | 630 443 | 4 972 | 517.803 s · 2026-08-15 20:52:22.647–21:01:00.450 ICT | 20 |
| Stress | `logs/23127271_Stress_20260814.jtl` | 14 017 038 | 104 397 | 324.785 s · 21:07:37.010–21:13:01.795 ICT | 100 |
| Spike | `logs/23127271_Spike_20260814.jtl` | 3 151 443 | 24 330 | 186.716 s · 21:13:44.841–21:16:51.557 ICT | 80 |
| Soak | `logs/23127271_Soak_20260814.jtl` | 688 797 | 5 439 | 748.334 s · 21:17:34.731–21:30:03.065 ICT | 15 |

No file was truncated (header + complete last row; sample counts match a finished `-n` run). Labels present: `login`, `search`, `detail`, `cart`, `checkout` only.

**Throughput note:** `req/s = sample_count / (last_timeStamp − first_timeStamp)`. That **includes think-time and idle** in the denominator. It is **not** “service time only.” Load think-time 1–3 s/sampler therefore yields ~10 rps; Stress 0–100 ms yields ~321 rps on the same five-step workflow.

---

## 1. Sample count and error rate

`success` is JMeter assertion pass/fail. `non-2xx` is `responseCode` not in 200–299. They **can** differ (200 + failed JSON assertion). In **this** run they do not: every row is `success=true` and `responseCode=200`.

| Scenario | N | `success=false` | `success=false` % | non-2xx | non-2xx % | login 401/403 |
|----------|---|-----------------|-------------------|---------|-----------|---------------|
| Load | 4 972 | 0 | **0.0000%** | 0 | 0.0000% | **0** |
| Stress | 104 397 | 0 | **0.0000%** | 0 | 0.0000% | **0** |
| Spike | 24 330 | 0 | **0.0000%** | 0 | 0.0000% | **0** |
| Soak | 5 439 | 0 | **0.0000%** | 0 | 0.0000% | **0** |

Per-label counts are slightly uneven (Load login 1003 vs checkout 987) because the scheduler stops mid-iteration (`startnextloop` + duration). That is not truncation of the file.

**Lockout vs 5xx:** zero `401`/`403` on `login`; zero `5xx`; zero connection-class `responseCode` (no `Non HTTP response code`). Capacity loss, where it exists, is **latency**, not lockout and not crashes.

---

## 2. `elapsed` (ms) — overall and by label

### Load (20 VU)

| Label | n | mean | median | p90 | p95 | p99 | max |
|-------|---|------|--------|-----|-----|-----|-----|
| **overall** | 4972 | 5.66 | 2.00 | 17.00 | **19.00** | 23.00 | 223 |
| login | 1003 | 4.36 | 4.00 | 5.00 | 6.00 | 19.00 | 223 |
| search | 1000 | 2.51 | 2.00 | 3.00 | 3.00 | 16.01 | 169 |
| detail | 994 | 2.40 | 2.00 | 3.00 | 4.00 | 16.07 | 66 |
| cart | 988 | 1.61 | 2.00 | 2.00 | 3.00 | 3.13 | 12 |
| checkout | 987 | 17.53 | 17.00 | 21.00 | **22.00** | 32.14 | 178 |

Checkout is the slowest step (SQLite `INSERT`). Login max 223 ms is a warm-up outlier (median 4 ms).

### Stress (100 VU)

| Label | n | mean | median | p90 | p95 | p99 | max |
|-------|---|------|--------|-----|-----|-----|-----|
| **overall** | 104397 | 242.23 | 233.00 | 416.00 | **476.00** | 594.00 | 1009 |
| login | 20923 | 294.70 | 287.00 | 454.00 | 506.00 | 613.00 | 1009 |
| search | 20898 | 248.57 | 238.00 | 394.00 | 447.00 | 558.00 | 975 |
| detail | 20869 | 254.70 | 243.00 | 406.00 | 462.00 | 593.00 | 991 |
| cart | 20857 | 104.08 | 93.00 | 185.40 | 217.00 | 294.00 | 544 |
| checkout | 20850 | 308.91 | 299.00 | 475.00 | **534.00** | 637.00 | 991 |

After dropping the first **25 s** of timestamps (P04 ramp-aware Stress): overall p95 **480** ms; checkout p95 **537** ms (n=97 544 / checkout n=19 504). Still **0%** error. Mean ≈ median (mild skew). Max elapsed **1009** ms — no 10 s timeout hits.

### Spike (peak 80)

| Label | n | mean | median | p90 | p95 | p99 | max |
|-------|---|------|--------|-----|-----|-----|-----|
| **overall** | 24330 | 126.66 | 73.00 | 315.00 | **381.00** | 925.84 | 1651 |
| login | 4898 | 175.13 | 128.00 | 366.30 | 437.15 | 1106.51 | 1651 |
| search | 4883 | 109.18 | 71.00 | 263.00 | 332.00 | 741.48 | 1637 |
| detail | 4865 | 108.23 | 67.00 | 277.00 | 354.00 | 507.52 | 1635 |
| cart | 4846 | 51.23 | 28.00 | 127.00 | 163.00 | 236.55 | 1267 |
| checkout | 4838 | 189.34 | 152.00 | 375.00 | **437.00** | 1204.89 | 1638 |

Whole-run Spike p95 **mixes** baseline + hold + recover (P04 E1 / P03). Do **not** treat 381 ms as “the spike.” Phase split is §4.

### Soak (15 VU)

| Label | n | mean | median | p90 | p95 | p99 | max |
|-------|---|------|--------|-----|-----|-----|-----|
| **overall** | 5439 | 5.95 | 2.00 | 17.00 | **18.00** | 25.00 | 385 |
| login | 1093 | 4.44 | 4.00 | 5.00 | 6.00 | 20.00 | 156 |
| search | 1092 | 2.31 | 2.00 | 3.00 | 4.00 | 7.00 | 141 |
| detail | 1088 | 2.21 | 2.00 | 3.00 | 4.00 | 14.00 | 34 |
| cart | 1087 | 1.91 | 2.00 | 3.00 | 3.00 | 4.00 | 247 |
| checkout | 1079 | 19.01 | 16.00 | 20.00 | **23.00** | 122.74 | 385 |

Soak p95 matches Load. Checkout **p99 123 ms / max 385 ms** is a thin tail, not a new error class (`success` still true, code 200).

---

## 3. Throughput (req/s)

| Scenario | req/s (wall-clock) | Think-time in denominator? | How to read it |
|----------|--------------------|----------------------------|----------------|
| Load | **9.60** | **Yes** (1–3 s/sampler) | Offered shopper load, not Node’s max. |
| Stress | **321.43** | Yes, but think is 0–100 ms | ~33× Load; this is the capacity probe. |
| Spike | **130.30** | Yes (0–200 ms) | **Average over the whole shape** — not hold rps. Hold phase ≈ **289 rps** (§4). |
| Soak | **7.27** | **Yes** (1–3 s, 15 VU) | Slightly below Load, as designed. |

---

## 4. Time trend (first vs last 20% of `timeStamp` span)

Split: samples with `timeStamp ≤ t0 + 0.2*(t1−t0)` vs `≥ t1 − 0.2*(t1−t0)`.

| Scenario | First-20% n | First overall p95 | First checkout p95 | Last-20% n | Last overall p95 | Last checkout p95 | Trend |
|----------|-------------|-------------------|--------------------|------------|------------------|-------------------|-------|
| Load | 841 | 20.00 | 23.90 | 1036 | 19.00 | 21.60 | **Flat** (slightly faster later) |
| Stress | 19818 | 533.00 | 603.30 | 20709 | 456.00 | 481.00 | **Falls** after ramp/warm-up — not a soak-style climb |
| Spike | 3432 | 371.00 | 437.95 | 1633 | 18.00 | 25.40 | Last 20% is **recover @5 VU** — p95 collapse is the shape, not “got healthier under peak” |
| Soak | 1004 | 17.00 | 20.00 | 1110 | 19.00 | 24.00 | **Nearly flat** (+4 ms checkout p95 over ~12 min) |

### Spike phases (relative to **first sample**, not JMeter test-start)

Windows: 0–30 s baseline, 30–32 jump, 32–92 hold, 92–97 drop, 97–end recover. Because `t0` is the first HTTP sample, the “baseline” window can overlap the start of the jump (`max grpThreads` in 0–30 s was 13, not 5). Hold/recover are still usable.

| Phase | n | max thr | rps | overall p95 | checkout p95 | login p95 | error% |
|-------|---|---------|-----|-------------|--------------|-----------|--------|
| baseline ~0–30 s | 1255 | 13 | 41.85 | 19 | 27 | 20 | 0 |
| jump ~30–32 s | 565 | 80 | 284.63 | 209 | 211 | 215 | 0 |
| **hold ~32–92 s** | 17363 | **80** | **289.48** | **414** | **464** | **480** | 0 |
| drop ~92–97 s | 1208 | 76 | 242.04 | 206 | 218 | 247 | 0 |
| **recover ~97–end** | 3939 | **5** | **43.92** | **18** | **24** | **16** | 0 |

Hold checkout p95 **464 ms** vs recover **24 ms** (Load-like). The SUT **did recover**. Whole-run Spike p95 381 ms is a blend; cite hold vs recover for the shape.

---

## 5. Thresholds for **this** laptop SUT (justified from these logs)

Not Google “p95 < 200 ms” folklore. Node + SQLite + JMeter share one Windows host; catalog is five `LIKE` rows.

| Gate | Proposed threshold | Why this number |
|------|--------------------|-----------------|
| Load error% | **< 0.1%** (`success=false`) | Observed **0 / 4972**. Any non-zero here is setup (unregistered `tramNN`, empty search, `200 {}`), not “load.” |
| Load checkout p95 | **< 50 ms** | Observed **22 ms**; 50 ms is ~2× with room for laptop noise, still far below Stress. |
| Load overall p95 | **< 40 ms** | Observed **19 ms**. |
| Stress “we found a knee” | checkout p95 **≥ 10× Load** **or** error% **> 1%** | Observed checkout p95 **534 vs 22 ms (~24×)** with **0%** error. Latency is the signal; do not require 5xx to call Stress a success. |
| Stress error% (valid CSV) | login **401/403 still ≈ 0** | Observed 0. If 403 appears, that is lockout contamination, not SQLite capacity. |
| Spike recover | recover checkout p95 **return to < 2× Load** (~44 ms) | Observed **24 ms**. If recover stayed near hold (464 ms), call “no recover.” |
| Soak | checkout p95 last-20% **< 2× first-20%** and error% **< 0.1%** | Observed 24 vs 20 ms, 0% error. A climb to e.g. 100 ms+ would be `userCarts`/orders growth. |
| Soak RPS | treat **~7 rps @ 15 VU** as the measured endurance offered load | Not a production SLA. |

**Do not** set Load p95 to Stress’s 476 ms — that would hide the 20 VU baseline.

---

## 6. Lockout-shaped vs system failures

| Class | Count in graded `.jtl` |
|-------|-------------------------|
| login `401` / `403` | **0** (all four files) |
| other 4xx | 0 |
| 5xx | 0 |
| connection / timeout codes | 0 |
| assertion-fail on HTTP 200 | 0 |

Stress/Spike were **valid passwords only**. Zero lockout errors is expected if CSV/`--register` worked. Do not interpret 0% error as “Stress failed to stress”: checkout p95 went **22 → 534 ms**.

---

## What P10 does **not** claim (P12)

No Redis, Nginx, Postgres, WAL, or Kubernetes recommendations here. Observations only: checkout and login dominate Stress `elapsed`; cart stays cheapest (in-memory `push`); search `LIKE` on five rows is not the Stress limiter; Spike recovered when threads returned to 5.

**Stop condition met.** Independent recompute (`docs/_recompute_jtl.py` → [`p11-recompute.md`](./p11-recompute.md)): every P10 linear p95 / N / error% / rps / first–last 20% cell **MATCH**es raw `elapsed`+`success`. Hunt table: [`p11-misinterpretations.md`](./p11-misinterpretations.md). Do not substitute JMeter HTML `pct2` for these cells (Stress Total HTML p95 **455** vs raw **476**).
