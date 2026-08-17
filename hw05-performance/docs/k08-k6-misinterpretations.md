# K08 — k6 misinterpretation hunt (23127271)

**Independent recompute:** `docs/_recompute_k6.py` on raw `--out json` (`http_req_duration`, tag `name`). Tolerance 0.51 ms / 0.02 rps vs K07.

Independent headline:

| Scenario | n | failed% | p95 overall | p95 checkout | rps |
|----------|--:|--------:|------------:|-------------:|----:|
| Load | 5025 | 0 | 18.29 | 21.29 | 9.51 |
| Stress | 99690 | 0 | 522.30 | 598.56 | 305.55 |
| Spike | 24725 | 0 | 320.83 | 354.84 | 131.99 |
| Soak | 5575 | 0 | 17.41 | 20.66 | 7.35 |

---

## 3.2-style mismatches

| # | Claim | Correct value | Why |
|---|-------|---------------|-----|
| 1 | k6 **console** Stress `http_req_duration` p95 **522.3 ms** is checkout latency | Checkout tag p95 **598.56 ms** (n=19938). 522.30 is **all five names mixed**. | Same trap as JMeter HTML Total vs label. Console = overall. |
| 2 | Spike console p95 **320.83 ms** is “the spike” | Hold checkout p95 **369.44**; recover checkout **22.78**. Whole-run 320.83 mixes phases. | k6 end-of-run trend has no stage split (K03 notes). |
| 3 | K07 copied JMeter P10 (Load checkout 22, Stress 534) | k6 Load checkout **21.29**, Stress checkout **598.56** — different files. | Did **not** happen. MATCH that K07 used JSON. |

---

## MATCH

| # | K07 claim | Recompute |
|---|-----------|-----------|
| M1 | failed 0 on all four JSON files | MATCH |
| M2 | Load overall p95 18.29, checkout 21.29, rps 9.51 | MATCH (console p95 18.29 too) |
| M3 | Stress overall p95 522.30, n=99690, rps 305.55 | MATCH |
| M4 | Spike hold checkout 369.44, recover 22.78 | MATCH |
| M5 | Soak checkout p95 20.66; first20% 20.30 last20% 19.84 | MATCH |
| M6 | Equal per-label counts (k6 finishes iterations) | MATCH |
| M7 | login 401/403 = 0 | MATCH |

No extra mismatches invented. Console vs per-tag is the one to put in the report if someone pastes the Stress summary screenshot as checkout p95.
