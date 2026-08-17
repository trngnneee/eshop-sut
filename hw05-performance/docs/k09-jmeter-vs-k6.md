# K09 — JMeter vs k6 (23127271 Search-to-buy)

**Sources only:** P11 linear `.jtl` vs `_recompute_k6.py` on `--out json`. Same host `DESKTOP-TCVI3HT`, SUT `localhost:3000`, CSV `23127271_users.csv`, P01 VUs.  
**Double-check (2026-08-17):** all four k6 JSON files — `http_req_duration` n = `http_reqs`; every duration tag `status=200`; five `name` tags equal (Load 1005×5, Stress 19938×5, Spike 4945×5, Soak 1115×5); `http_req_failed` value=true **0**. JMeter Spike windows re-run from first `.jtl` sample: hold checkout p95 **464**, recover **23.65** (MATCH P10/P11).  
**Node memory:** UNKNOWN (not read off Task Manager).  
**Confound:** Node was **not** restarted between JMeter P09 and this k6 session — in-memory `userCarts` may already be populated.

## Setup parity

| Item | JMeter | k6 | Delta |
|------|--------|-----|-------|
| Paths | login→search→detail→cart→checkout | same | MATCH |
| VUs | 20 / 100 / 5→80→5 / soak 15 | same stages | MATCH (`startVUs: 5` on Spike) |
| Think-time | Uniform timer **per sampler** | `sleep` **per request** | Same bands; RNG not identical |
| Duration | Load 520, Stress 325, Spike ~187, Soak 750 | stages 40+480, 25+300, 187, 30+720 | MATCH |
| Assertions | JSONPath + status | `check()` same fields | MATCH |
| CSV | shareMode.all | `(__VU-1+__ITER)%n` after K05 | Concurrent uniqueness MATCH |
| Error% | 0 all four `.jtl` | 0 all four JSON (`http_req_failed`) | MATCH |

## Metric table (checkout p95 is the fair label)

| Scenario | Metric | JMeter | k6 | k6 − JMeter |
|----------|--------|-------:|---:|------------:|
| Load | checkout p95 (ms) | 22.00 | 21.29 | **−3.2%** |
| Load | overall p95 | 19.00 | 18.29 | −3.7% |
| Load | wall req/s | 9.60 | 9.51 | −0.9% |
| Stress | checkout p95 | 534.00 | 598.56 | **+12.1%** |
| Stress | overall p95 | 476.00 | 522.30 | +9.7% |
| Stress | wall req/s | 321.43 | 305.55 | −4.9% |
| Spike | whole-run overall p95 | 381.00 | 320.83 | blend — **do not use** |
| Spike | **hold** checkout p95 | 464.00 | 369.44 | **−20.4%** |
| Spike | **recover** checkout p95 | 23.65 | 22.78 | **−3.7%** |
| Soak | checkout p95 | 23.00 | 20.66 | −10.2% |
| Soak | last / first checkout p95 | 24 / 20 | 19.84 / 20.30 | JMeter slight climb; k6 flat |
| Soak | rps | 7.27 | 7.35 | +1.1% |

**How to read it:** Load and Spike **recover** agree within ~4% — same SUT, same think-time band. Stress k6 is **slower** (+12% checkout p95), not faster; Spike **hold** k6 is **faster** (−20%). That split is not “k6 is faster than JMeter.” Likely mix of Go vs Java client, no JVM injector, and a dirty in-memory cart from the JMeter session still running in Node. **Do not** merge `.jtl` and JSON into one CI baseline (P13).

## Tool footprint

| | JMeter | k6 |
|--|--------|-----|
| Injector | JVM (`java`) | Go binary `k6.exe` v2.1.0 |
| Graded log | `.jtl` + HTML folder | NDJSON `--out json` (Stress JSON **279 MB**) |
| RAM of injector | UNKNOWN this k6 session | UNKNOWN |
| CI (P13) | nightly full `-n` | optional sub-minute smoke; **separate** store |

## CI

Keep P13: PR smoke can be **k6 Load** later if a runner has `k6`; nightly stays JMeter `.jmx` already frozen. Never average JMeter p95 with k6 p95.

**Stop condition met.** Report §4 can use this table.
