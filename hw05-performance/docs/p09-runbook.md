# P09 — Execution runbook (23127271 Search-to-buy)

**Gate:** P09 only. **Do not invent metrics.** Fill blanks from real runs.  
**Student:** 23127271 · **SUT:** `http://localhost:3000` · **Tool:** Apache JMeter (non-GUI for numbers)  
**Working dir for all `-n` commands:** `SoftwareTesting-HW/HW5/23127271/test-plans/`  
**Artifacts:** `.jtl` + HTML under `../logs/` · screenshots under `../evidence/`

Related: [`BEFORE-RUN.md`](../test-plans/BEFORE-RUN.md) · [`reset-lockout.sql`](../test-plans/reset-lockout.sql) · [`p01-parameters.md`](./p01-parameters.md) · [`23127271_Spike_20260814-notes.md`](../test-plans/23127271_Spike_20260814-notes.md)

---

## 0. Anti-cheat / honesty

| Never | Why |
|-------|-----|
| Invent `.jtl` rows, HTML report numbers, or Task Manager % | Part 11: raw logs from a real run |
| Invent dxdiag / hostname | Must match prior HW evidence |
| Treat GUI listener tables as graded p95 | Graded numbers = `-n` + `.jtl` / HTML |
| Restart Node “to unlock” without re-register | `initDatabase()` DROP wipe `tramNN` |

---

## 1. Preflight

Do this **once** before Load (and again after any SUT re-seed).

| # | Step | Done? | Timestamp / note |
|---|------|-------|------------------|
| 1 | Start EShop backend so `http://localhost:3000` responds | ☑ | Graded `-n` logs exist (Load/Stress/Spike/Soak all HTTP 200) |
| 2 | Open **Task Manager** (CPU + Memory; show `node` + `java` if possible) and leave it visible for screenshots | ☑ | Same-frame in Task 1 demo video; HTML dashboards also in `evidence/` |
| 3 | Confirm **JMeter** on PATH (`jmeter -v`) and **jpgc-casutg** installed (needed for Spike Ultimate Thread Group) | ☑ | Spike `.jtl` maxAllThreads **80** (Ultimate TG ran) |
| 4 | `cd` to `test-plans/` and register **100** users: `node generate-tram-users.js --register` → expect 100× 200 (or SKIP if already registered) | ☑ | Stress `.jtl` reached **100** concurrent threads |
| 5 | Spot-check: `POST /api/login` with `tram01@eshop.com` / `Test1234!` → 200 + `token` | ☑ | All four `.jtl`: login `responseCode=200`, `success=true` |
| 6 | Optional lockout **probe** (throwaway once, not inside Load/Stress/Spike): two wrong passwords on a spare account → then 403; then run `reset-lockout.sql`. Do **not** stop Node unless SQLite is locked | ☐ | Optional; not required — graded runs had **0** login 401/403 |
| 7 | Capture **dxdiag** once → save under `evidence/` (hostname must match previous HW) | ☑ | file: `evidence/dxdiag.png` (`DESKTOP-TCVI3HT`) |
| 8 | Create folders if missing: `../logs/`, `../evidence/` | ☑ | |

**Do not** use `test@eshop.com` in JMeter.

**Node policy for the whole day:** keep Node **running** across Load → Stress → Spike when possible. Prefer SQL unlock over restart. If Node must restart → re-run `--register` before the next plan.

---

## 2. Run order

```text
Load  →  reset/check unlock  →  Stress  →  reset lockout  →  Spike  →  reset if needed  →  soak
```

| Order | Plan | Profile (reminder) | Listener (GUI only) |
|-------|------|--------------------|---------------------|
| 1 | `23127271_Load_20260814.jmx` | 20 thr / 40 s ramp / **520** s / think 1–3 s | View Results Tree |
| 2 | Reset | SQL preferred — see §4 | — |
| 3 | `23127271_Stress_20260814.jmx` | **100** / 25 / **325** / think 0–0.1 s (P01 locked) | Summary Report |
| 4 | Reset | SQL preferred — see §4 | — |
| 5 | `23127271_Spike_20260814.jmx` | Ultimate TG **5→80→5** (~187 s) / think 0–0.2 s | Aggregate Report |
| 6 | Reset if login 401/403 appeared | | |
| 7 | Soak | **15** thr / 30 s ramp / **750** s (30+720) / think 1–3 s — see §6 | optional short Tree peek |

---

## 3. Non-GUI commands (graded runs)

From `test-plans/`:

```bat
REM --- LOAD ---
jmeter -n -t 23127271_Load_20260814.jmx -l ../logs/23127271_Load_20260814.jtl -e -o ../logs/report_load/

REM --- STRESS (after lockout reset) ---
jmeter -n -t 23127271_Stress_20260814.jmx -l ../logs/23127271_Stress_20260814.jtl -e -o ../logs/report_stress/

REM --- SPIKE (after lockout reset; needs Ultimate Thread Group plugin) ---
jmeter -n -t 23127271_Spike_20260814.jmx -l ../logs/23127271_Spike_20260814.jtl -e -o ../logs/report_spike/

REM --- SOAK (after cloning Load → see §6) ---
jmeter -n -t 23127271_Soak_20260814.jmx -l ../logs/23127271_Soak_20260814.jtl -e -o ../logs/report_soak/
```

If `jmeter` is not on PATH, use the full path to `jmeter.bat`.

**GUI mode:** only for demo video and listener screenshots (Tree / Summary / Aggregate). Do not quote GUI averages as the report’s p95.

---

## 4. Lockout reset (between scenarios)

Fill timestamps when you run. Prefer **B**. Never stop Node just to unlock if SQL works (restart → DROP users).

### After Load → before Stress

1. Stop Load JMeter; confirm `.jtl` flushed. **Time:** Load `.jtl` span **517.8 s**, 4972 samples, flushed  
2. Any login **401/403** in Load? yes / no: **no** (4972× HTTP 200)  
3. Reset: **not needed** (no lockout in Load).  
   - **A** wait ≥180 s if locked. **Until:** n/a  
   - **B (preferred):**  
     ```bat
     sqlite3 ..\..\..\..\Repo\eshop-sut\backend\database.sqlite < reset-lockout.sql
     ```  
     (Adjust path to your `database.sqlite`. Or paste SQL in DB Browser.) **SQL time:** n/a — skipped  
   - **C last resort:** re-seed Node → **must** `--register` again. **Time:** n/a  
4. Stress start: after Load `.jtl` closed; Stress `.jtl` maxAllThreads **100**, span **324.8 s**  

### After Stress → before Spike

Same checklist. **Stopped:** Stress `.jtl` flushed (104397 samples) · **403?** **no** (all 200) · **Reset:** not needed · **Spike start:** Spike `.jtl` maxAllThreads **80**, span **186.7 s**  

### After Spike → before soak

**Stopped:** Spike `.jtl` flushed (24330 samples) · **Reset:** not needed (0× 401/403) · **Soak start:** Soak `.jtl` maxAllThreads **15**, span **748.3 s**  

---

## 5. Per-run evidence checklist

For **each** of Load / Stress / Spike / soak:

| Evidence | Path / note | Done? |
|----------|-------------|-------|
| Raw `.jtl` | `logs/23127271_{Scenario}_20260814.jtl` | ☑ Load 4972 / Stress 104397 / Spike 24330 / Soak 5439 |
| HTML report folder | `logs/report_{load\|stress\|spike\|soak}/` | ☑ |
| HTML dashboard + Statistics screenshots | `evidence/{Load,Stress,Spike,Soak}_html_{dashboard,statistics}.png` | ☑ |
| Hardware | `evidence/dxdiag.png` (`DESKTOP-TCVI3HT`) | ☑ |
| JMeter + Task Manager same frame | Task 1 demo video (not separate `*_tool_taskmgr.png`) | ☑ video |
| Optional: Spike HTML “Response Times Over Time” (jump vs recover) | `evidence/Spike_html_dashboard.png` + `logs/report_spike/` | ☑ |

Hostname on dxdiag / screenshots must match prior HW submissions.

---

## 6. Soak (constant load — not Spike)

Soak is **not** in the three graded listener plans. Build once before running:

1. Copy `23127271_Load_20260814.jmx` → `23127271_Soak_20260814.jmx`  
2. Edit Thread Group:  
   - Threads = **15** (slightly below Load 20; P01 guess)  
   - Ramp-up = **30** s  
   - Duration = **750** s (30 + 12×60; scheduler includes ramp)  
   - Keep Load think-time 1000–3000 ms, same CSV/asserts  
3. Rename Thread Group / Test Plan to `23127271_Soak_20260814`  
4. Listener: optional Tree for a short GUI peek; **numbers from `-n`**

### Watch during soak (fill after the run — leave blank now)

| Observation | Value (fill from real run) |
|-------------|----------------------------|
| Overall error % | **0%** (5439 samples, all `success=true`, HTTP 200) |
| Checkout p95 — first ~20% of timestamps | **19.8 ms** (n=206 checkout samples) |
| Checkout p95 — last ~20% of timestamps | **24.0 ms** (n=219) |
| Node memory start → end (Task Manager) | UNKNOWN as a number (see demo video; not written from a screenshot) |
| Max stable RPS (req/s from HTML or `.jtl`) | **7.27 req/s** (HTML Total throughput; think-time 1–3 s included in wall-clock) |
| Memory ceiling observed | UNKNOWN as a number |
| Elapsed time when latency starts climbing (if it does) | **stable full ~12.5 min** (span 748.3 s). Checkout p95 19.8 → 24.0 ms is a small drift, not a climb. HTML checkout p95 (pct2) = **23 ms**; p99 (pct3) = 137 ms (outlier max 385 ms). |

---

## 7. Demo video (≥6 minutes)

| Rule | Detail |
|------|--------|
| Length | ≥ **6** minutes (may split by scenario) |
| Language | Vietnamese narration |
| Frame | JMeter **and** resource monitor (Task Manager) visible together |
| Content | Show at least one Load / Stress / Spike segment; soak optional if time |
| GUI vs numbers | GUI for visuals; say that graded numbers come from `-n` `.jtl` |
| Upload | Unlisted YouTube: https://youtu.be/Nyvm0bxZxgA (README) |
| **Not** this video | Agent Skill demo (P16) is a **second** video |

Recording outline (optional): 0:00 preflight → Load Tree peek → cut to `-n` end → Stress Summary → Spike Aggregate + mention HTML shape → Task Manager memory.

---

## 8. Bugs → GitHub Issue

File an Issue (with screenshot) if you see **functional** SUT bugs, e.g.:

- Process crash / hang  
- `GET /api/products/{id}` returns **200 `{}`** for a **real** seed id used in CSV  
- Checkout **200** without `orderId`  
- Search always `[]` for a known name substring after seed verify  

High latency / high error% under Stress alone is a **performance** finding for the report — Issue optional, not required.

---

## 9. After all runs (hand-off to P10)

- [x] Four `.jtl` files under `logs/` (Load, Stress, Spike, soak)  
- [x] Four HTML report folders  
- [x] Screenshots + dxdiag in `evidence/`  
- [x] Lockout reset timestamps filled in §4  
- [x] Soak blanks in §6 filled from **your** numbers (memory left UNKNOWN)  
- [x] Raw `.jtl` exist — **P09 closed; next gate is P10**

**Log generations:** first `-n` (Load 20 / Stress **50** / Spike peak **40** / Soak 15) is archived under `logs/archive-first-guess-20260815/`. Current `logs/*.jtl` are the **locked P01** runs: Load **20** / Stress **100** / Spike peak **80** / Soak **15** (all 0% err, all HTTP 200). P10 must analyse **these** files, not the archive.

**Stop condition met:** commands + evidence checklist. You run the tests; AI does not fabricate logs.
