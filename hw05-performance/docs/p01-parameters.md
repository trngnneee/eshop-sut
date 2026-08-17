# P01 — Load / Stress / Spike parameters (23127271)

**Gate:** P01 (locked after first `-n` run).  
**Workflow:** Search-to-buy from [`p00-endpoint-map.md`](./p00-endpoint-map.md) — same five steps every scenario.  
**Host:** student Windows laptop; **Node + SQLite SUT, JMeter, and the OS share one machine.** Loopback `http://localhost:3000`.  
**Login policy (all three):** valid credentials only. Unique CSV emails **≥ max threads = 100** (P02). Do **not** hammer failed logins — that measures the `+= 2` / 180s lockout (`server.js` L54–57), not checkout capacity.

Think-time is a **Uniform Random Timer on every sampler** (five samplers per iteration). Bands differ by scenario on purpose.

First guess was Load 20 / Stress 50 / Spike 5→40→5. The 2026-08-15 `-n` run was **0% error** at Stress 50 (~137 rps, avg ~6 ms) and Spike peak 40. Catalog is five `LIKE` rows — 50 VU never reached a knee. **Locked numbers below** replace that guess. Load 20 stays: a green Load is the baseline, not a failure.

---

## Parameter table

| Scenario | Threads | Ramp-up | Duration / schedule | Think-time | What “success” means | Why these numbers for THIS SUT |
|----------|---------|---------|---------------------|------------|----------------------|--------------------------------|
| **Load** | **20** | **40 s** (~2 s/thread) | **8 min** constant after ramp (scheduler duration **520** = 40+480) | **Uniform 1000–3000 ms** per sampler | Almost all samples **assertion-pass**. Error% ≈ 0. **No 401/403.** Node and JMeter stay usable. | Unchanged. First run confirmed 20 + 1–3 s think ≈ **9.6 rps, 0% err** — this *is* expected peak on the laptop, not a stress. |
| **Stress** | **100** | **25 s** | **5 min** sustained at 100 (scheduler duration **325** = 25+300) | **Uniform 0–100 ms** per sampler | Observe **capacity loss** vs Load: p95 climb and/or non-zero errors (timeout, SQLite busy, connection reset). Full login→checkout still runs. 401/403 ≈ 0 if CSV is valid. | **100 > 20.** First Stress **50 / 200–500 ms stayed 0% / avg 6 ms**. P04 Hunt 2: raise threads and/or cut think-time. Student lock: **100 VU** + short think (0–100 ms). 25 s ramp avoids a 100-login burst that would look like Spike. Watch Task Manager: if `java` is pinned and `node` is idle, **lower** threads (injector, not SUT). |
| **Spike** | **5 → 80 → 5** (peak **80**) | **Near-instant jump:** 2 s from 5→80; **recover:** 5 s from 80→5 | **Stepped schedule:** (1) **30 s** at 5, (2) jump to 80 in **2 s**, **hold 60 s**, (3) drop to 5 in **5 s**, **hold 90 s recover**. Total ~3.5 min. Ultimate Thread Group — **not** a flat 80-thread group. | **Uniform 0–200 ms** | Hold: error%/p95 **jump** vs 5-thread baseline. Recover: trend back. If they stay high at 5, SUT did not recover. | Peak **80** is **above Load (20)** and **below Stress (100)** so Spike is shape, not “Stress renamed.” First peak 40 did not perturb (0% err). Recover 90 s < 180 s lockout. |

---

## Think-time (why the three bands are different)

| Scenario | Band | Why |
|----------|------|-----|
| Load | 1–3 s | Shopper pacing. Keeps Load in the **stable** zone measured at ~9.6 rps. |
| Stress | 0–0.1 s | 50 VU with 0.2–0.5 s never stressed this SUT. Short think + 100 VU raises offered load without 500 threads on the same laptop. |
| Spike | 0–0.2 s | Burst. Recovery must be visible **while traffic continues** at 5 threads. |

Do **not** copy Load’s 1–3 s into Stress/Spike.

---

## Login / CSV implication for P02

| Rule | Value |
|------|--------|
| Load / Stress / Spike passwords | Valid only (`Test1234!`). No dedicated “fail login” sampler. |
| Unique emails | **≥ 100** (`tram01@eshop.com` … `tram100@…`). Stress is the high-water mark. |
| Recycle | Allowed for duration > row count **only if** each row is a distinct account. Never one shared `test@eshop.com`. |
| Between Stress and Spike | Reset lockout (SQL while Node stays up). |

---

## Soak starting guesses (not a fourth “Spike”)

Soak is **constant** threads for **10–15 min**, after Load/Stress/Spike, using the **same Search-to-buy path** and **Load think-time**.

| Guess | Value | Why |
|-------|--------|-----|
| Threads | **15** (slightly **below** Load 20) | `userCarts` never clears. First soak at 15 was 0% / ~7.3 rps for 12 min — still the endurance profile, not a second Stress. |
| Ramp-up | **30 s** | Gentle; not a spike. |
| Duration | **12 min** (scheduler **750** = 30+720) | Inside 10–15. |
| Think-time | **Uniform 1000–3000 ms** (same as Load) | “Does Load stay stable over time?” |

---

## Explicitly rejected (generic priors)

| Rejected | Why not for this SUT |
|----------|----------------------|
| Load 100 / Stress 500 / Spike 2000 | AWS-scale; injector and SUT share one laptop. **Load 100** would erase the baseline (Stress is the 100 VU plan). |
| Spike = “Load for 20 min” | Duration ≠ spike. Spike needs jump **and** recover. |
| Stress = failed-login hammer | Measures 403 lockout after two bad passwords, not Search-to-buy capacity. |
| Same think-time on all three | Would make Stress/Spike only a thread-count rename. |
| Keep Stress 50 after a 0% run | First `-n` proved 50 is not a knee on this 5-product SQLite shop. |

**Stop condition met:** parameter table + rationale. Plans and CSV must match this table.
