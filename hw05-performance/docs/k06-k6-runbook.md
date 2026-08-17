# K06 — k6 execution runbook (23127271 Search-to-buy)

**Gate:** K06 only. **Do not invent metrics.** JMeter P09 already ran; k6 is a second injector on the same SUT.

**Working dir:** `SoftwareTesting-HW/HW5/23127271/test-plans/`  
**k6:** v2.1.0 (`k6.exe`)  
**Hostname:** `DESKTOP-TCVI3HT` (same dxdiag)

---

## 1. Preflight

| # | Step | Done? | Note |
|---|------|-------|------|
| 1 | SUT `http://localhost:3000` | ☑ | 200 on `/api/products` |
| 2 | `tramNN` registered (do **not** double-register) | ☑ | `tram01` login → token |
| 3 | Task Manager: watch `node` vs `k6` (not `java`) | ☐ | screenshot if capturing |
| 4 | dxdiag already in `evidence/dxdiag.png` | ☑ | |

Node stays **up** across Load → Stress → Spike. SQL unlock between scenarios (`reset-lockout.sql`). Restart Node ⇒ `--register` again.

---

## 2. Order

```text
Load → SQL unlock → Stress → SQL unlock → Spike → SQL unlock → soak
```

Soak: `23127271_Soak_20260814.js` — 15 VU, 30s ramp, 720s hold, think 1–3s per request.

---

## 3. Commands (from `test-plans/`)

```bat
REM Tree-equivalent peek (NOT graded) — 1 VU 30s
k6 run --vus 1 --duration 30s --http-debug=full 23127271_Load_20260814.js

REM --- LOAD (graded) ---
k6 run --out json=../logs/23127271_Load_20260814.json 23127271_Load_20260814.js

REM --- STRESS ---
k6 run --out json=../logs/23127271_Stress_20260814.json 23127271_Stress_20260814.js

REM --- SPIKE ---
k6 run --out json=../logs/23127271_Spike_20260814.json 23127271_Spike_20260814.js

REM --- SOAK ---
k6 run --out json=../logs/23127271_Soak_20260814.json 23127271_Soak_20260814.js
```

`--vus`/`--duration` on the peek **override** stages — do not pass them on graded runs.

---

## 4. Evidence

| Artifact | Path |
|----------|------|
| JSON | `logs/23127271_{Load,Stress,Spike,Soak}_20260814.json` |
| Console summary | Stress screenshot optional; numbers from JSON |
| k6 + Task Manager | same frame if recording; Node memory UNKNOWN unless read off the screenshot |
| Demo | JMeter Task 1 video stays https://youtu.be/Nyvm0bxZxgA |

---

## 5. Soak blanks (fill after the real run)

| Observation | Value |
|-------------|-------|
| Overall error % | **0%** (5575 duration points, 0 failed) |
| Checkout p95 first 20% | **20.30 ms** |
| Checkout p95 last 20% | **19.84 ms** |
| Wall-clock http_reqs/s | **7.35** |

---

## 6. Leftover `userCarts`

JMeter P09 already pushed carts in this Node process. k6 Stress p95 may include a **warm heap**, not a k6-only defect. Say so in K09 if Node was not restarted between JMeter and k6.
