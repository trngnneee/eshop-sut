# Independent recompute — p95 / error% from raw `.jtl`

**Purpose:** do **not** trust `p10-analysis.md` until these numbers are checked.
**Script:** `docs/_recompute_jtl.py` (stdlib `csv` only; does not import `_p10_analyze.py`).
**Columns:** `elapsed`, `success`, `responseCode`, `label`, `timeStamp`.
**p95 linear:** sorted `elapsed`, index `(n−1)×0.95`, interpolate — same formula P10 claimed.
**p95 R6:** index `(n+1)×0.95` (1-based interpolate). Matches some HTML *per-label* `pct2` rows (Load login 6.8, Spike search 332.8). Does **not** explain HTML Stress **Total** p95 **455** (raw linear and R6 are both **476**).
**error%:** `success=false` count / N **and** non-2xx / N, separately.
**Not used as input:** HTML dashboards, Interaction 15 console, archive-first-guess.

## Verdict vs P10

Every P10 **linear-p95**, **N**, **error%**, **rps** (±0.02), and **first/last 20% p95** cell **MATCH**es this recompute (tolerance 0.51 ms). Do **not** treat JMeter HTML `pct2ResTime` as the same estimator — see per-label `vs HTML`.

## Per-scenario tables

### Load

File `23127271_Load_20260814.jtl` · N=4972 · wall=517.803s · rps=9.6021 · `success=false`=0 (0.0000%) · non-2xx=0 (0.0000%) · login 401/403=0 · codes={'200': 4972}

| Label | n | mean | median linear | p95 linear | p95 R6 | p95 nearest | P10 p95 | HTML pct2 (p95) | vs P10 | vs HTML |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| overall | 4972 | 5.66 | 2.00 | **19.00** | 19.00 | 19.00 | 19.00 | 19.0 | MATCH | linear MATCH; R6 MATCH |
| login | 1003 | 4.36 | 4.00 | **6.00** | 6.80 | 6.00 | 6.00 | 6.7999999999999545 | MATCH | linear diff; R6 MATCH |
| search | 1000 | 2.51 | 2.00 | **3.00** | 3.00 | 3.00 | 3.00 | 3.0 | MATCH | linear MATCH; R6 MATCH |
| detail | 994 | 2.40 | 2.00 | **4.00** | 4.00 | 4.00 | 4.00 | 4.0 | MATCH | linear MATCH; R6 MATCH |
| cart | 988 | 1.61 | 2.00 | **3.00** | 3.00 | 3.00 | 3.00 | 3.0 | MATCH | linear MATCH; R6 MATCH |
| checkout | 987 | 17.53 | 17.00 | **22.00** | 22.00 | 22.00 | 22.00 | 22.0 | MATCH | linear MATCH; R6 MATCH |

First-20% n=841 overall p95=20.00 checkout p95=23.90 · Last-20% n=1036 overall p95=19.00 checkout p95=21.60 · trend vs P10: MATCH
Headline vs P10: N MATCH · error% MATCH · rps MATCH (computed 9.6021 vs P10 9.6) · overall median linear=2.00 vs P10 2.0 vs HTML 2.0

### Stress

File `23127271_Stress_20260814.jtl` · N=104397 · wall=324.785s · rps=321.4342 · `success=false`=0 (0.0000%) · non-2xx=0 (0.0000%) · login 401/403=0 · codes={'200': 104397}

| Label | n | mean | median linear | p95 linear | p95 R6 | p95 nearest | P10 p95 | HTML pct2 (p95) | vs P10 | vs HTML |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| overall | 104397 | 242.23 | 233.00 | **476.00** | 476.00 | 476.00 | 476.00 | 455.0 | MATCH | linear diff; R6 diff |
| login | 20923 | 294.70 | 287.00 | **506.00** | 506.00 | 506.00 | 506.00 | 509.0 | MATCH | linear diff; R6 diff |
| search | 20898 | 248.57 | 238.00 | **447.00** | 447.00 | 447.00 | 447.00 | 451.0 | MATCH | linear diff; R6 diff |
| detail | 20869 | 254.70 | 243.00 | **462.00** | 462.00 | 462.00 | 462.00 | 464.0 | MATCH | linear diff; R6 diff |
| cart | 20857 | 104.08 | 93.00 | **217.00** | 217.00 | 217.00 | 217.00 | 219.0 | MATCH | linear diff; R6 diff |
| checkout | 20850 | 308.91 | 299.00 | **534.00** | 534.00 | 534.00 | 534.00 | 537.0 | MATCH | linear diff; R6 diff |

First-20% n=19818 overall p95=533.00 checkout p95=603.30 · Last-20% n=20709 overall p95=456.00 checkout p95=481.00 · trend vs P10: MATCH
Headline vs P10: N MATCH · error% MATCH · rps MATCH (computed 321.4342 vs P10 321.43) · overall median linear=233.00 vs P10 233.0 vs HTML 251.0

### Spike

File `23127271_Spike_20260814.jtl` · N=24330 · wall=186.716s · rps=130.3048 · `success=false`=0 (0.0000%) · non-2xx=0 (0.0000%) · login 401/403=0 · codes={'200': 24330}

| Label | n | mean | median linear | p95 linear | p95 R6 | p95 nearest | P10 p95 | HTML pct2 (p95) | vs P10 | vs HTML |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| overall | 24330 | 126.66 | 73.00 | **381.00** | 381.00 | 381.00 | 381.00 | 383.0 | MATCH | linear diff; R6 diff |
| login | 4898 | 175.13 | 128.00 | **437.15** | 438.00 | 438.00 | 437.15 | 438.0 | MATCH | linear diff; R6 MATCH |
| search | 4883 | 109.18 | 71.00 | **332.00** | 332.80 | 332.00 | 332.00 | 332.8000000000002 | MATCH | linear diff; R6 MATCH |
| detail | 4865 | 108.23 | 67.00 | **354.00** | 354.00 | 354.00 | 354.00 | 354.0 | MATCH | linear MATCH; R6 MATCH |
| cart | 4846 | 51.23 | 28.00 | **163.00** | 163.00 | 163.00 | 163.00 | 163.0 | MATCH | linear MATCH; R6 MATCH |
| checkout | 4838 | 189.34 | 152.00 | **437.00** | 437.05 | 437.00 | 437.00 | 437.0500000000002 | MATCH | linear MATCH; R6 MATCH |

First-20% n=3432 overall p95=371.00 checkout p95=437.95 · Last-20% n=1633 overall p95=18.00 checkout p95=25.40 · trend vs P10: MATCH
Headline vs P10: N MATCH · error% MATCH · rps MATCH (computed 130.3048 vs P10 130.3) · overall median linear=73.00 vs P10 73.0 vs HTML 78.0

### Soak

File `23127271_Soak_20260814.jtl` · N=5439 · wall=748.334s · rps=7.2681 · `success=false`=0 (0.0000%) · non-2xx=0 (0.0000%) · login 401/403=0 · codes={'200': 5439}

| Label | n | mean | median linear | p95 linear | p95 R6 | p95 nearest | P10 p95 | HTML pct2 (p95) | vs P10 | vs HTML |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| overall | 5439 | 5.95 | 2.00 | **18.00** | 18.00 | 18.00 | 18.00 | 18.0 | MATCH | linear MATCH; R6 MATCH |
| login | 1093 | 4.44 | 4.00 | **6.00** | 6.30 | 6.00 | 6.00 | 6.2999999999999545 | MATCH | linear MATCH; R6 MATCH |
| search | 1092 | 2.31 | 2.00 | **4.00** | 4.00 | 4.00 | 4.00 | 4.0 | MATCH | linear MATCH; R6 MATCH |
| detail | 1088 | 2.21 | 2.00 | **4.00** | 4.00 | 4.00 | 4.00 | 4.0 | MATCH | linear MATCH; R6 MATCH |
| cart | 1087 | 1.91 | 2.00 | **3.00** | 3.00 | 3.00 | 3.00 | 3.0 | MATCH | linear MATCH; R6 MATCH |
| checkout | 1079 | 19.01 | 16.00 | **23.00** | 23.00 | 23.00 | 23.00 | 23.0 | MATCH | linear MATCH; R6 MATCH |

First-20% n=1004 overall p95=17.00 checkout p95=20.00 · Last-20% n=1110 overall p95=19.00 checkout p95=24.00 · trend vs P10: MATCH
Headline vs P10: N MATCH · error% MATCH · rps MATCH (computed 7.2681 vs P10 7.27) · overall median linear=2.00 vs P10 2.0 vs HTML 2.0

## How to read this for P11

- Cite **p95 linear** when checking P10 claims (same formula).
- Cite **HTML pct2** only as a *different* aggregator. Biggest gap: Stress **Total** HTML p95 **455** / median **251** vs raw-all-`elapsed` p95 **476** / median **233**. That is **not** a P10 arithmetic bug.
- Spike HTML overall median **78** vs raw median **73**; HTML p99 Total **721** vs linear p99 **926** — same Total-row issue.
- Machine-readable copy: `_recompute_jtl.csv`.

