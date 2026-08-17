# P03 — Listener assignment (23127271)

**Gate:** P03 only (no thread-group XML, no `.jmx`).  
**Rule:** one listener type per plan; **do not reuse** a type across Load / Stress / Spike.  
**Pairing:** frozen scope — no swap.

GUI listeners are for **screenshots / demo video** (Task Manager in the same frame). Graded numbers come from **non-GUI**:

```text
jmeter -n -t <plan>.jmx -l logs/<plan>.jtl -e -o logs/report_<scenario>/
```

`-l` writes the raw `.jtl`. `-e -o` builds the HTML dashboard. Do **not** treat the GUI table as the source of p95/error%.

---

## Assignment

| Plan filename | Scenario | Listener (exactly one) | Why this pairing |
|---------------|----------|------------------------|------------------|
| `23127271_Load_20260814.jmx` | Load (20 threads, 8 min, think 1–3 s) | **View Results Tree** | Volume is still small enough to open request/response bodies and catch Search-to-buy assertion bugs (`200 {}` on detail, login without `token`, checkout without `orderId`). |
| `23127271_Stress_20260814.jmx` | Stress (**100** threads, 5 min, think 0–0.1 s; P01 locked after first 50 VU run stayed 0% err) | **Summary Report** | Tree would freeze the laptop; we need a compact #samples / error% / throughput view while capacity breaks. |
| `23127271_Spike_20260814.jmx` | Spike (**5→80→5**, peak below Stress 100) | **Aggregate Report** | Need **percentiles** (90/95/99) for the jump vs recover window; Summary does not show p90/p95/p99. |

No Graph Results, no Backend Listener, no second listener “just in case.” P05–P07 attach **only** the row above.

---

## What each listener shows that the other two do not

### Load — View Results Tree

- **Unique:** per-sample **Request / Response data** (headers, JSON body, assertion failure message). You can see `{"token":...}` vs 401, search `[]` vs an array, detail `{}` vs `name`, cart `Added to cart`, checkout `orderId`.
- **Summary Report cannot** show a body. **Aggregate Report cannot** show why a sample failed.
- **Screenshot:** JMeter GUI with Tree expanded on (1) a passing login (body has `token`) and (2) if any fail, a detail/`{}` or checkout-without-`orderId` row — plus Task Manager in the same frame. Keep the Tree **disabled or unused** during the long `-n` run; GUI Tree on 8 min × 20 threads × 5 samplers will eat RAM on this laptop.

### Stress — Summary Report

- **Unique:** running **totals** in one table: `# Samples`, `Average`, `Min`, `Max`, `Std. Dev.`, `Error %`, `Throughput`, `Received/Sent KB/sec`, `Avg Bytes` — cheap to keep open while **100** threads hammer checkout `INSERT`.
- **Tree** would be unreadably huge and can stall the injector (same host as Node). **Aggregate** adds percentiles but is heavier; Stress’s first question is “are errors/throughput collapsing?”, not p99.
- **Screenshot:** Summary table with **per-label** rows (`login`, `search`, `detail`, `cart`, `checkout`) and **TOTAL**, next to Task Manager (CPU/memory of `node` vs `java`). Capture near the **end** of the 5 min so Error% has settled.

### Spike — Aggregate Report

- **Unique:** **90% / 95% / 99% / 99.9%** (and median) **per label**. Aggregate is **one table for the whole run** — it does **not** plot p95 jumping on the 80-thread hold and falling on recover. Summary has average/max only. Tree cannot summarize the recover window.
- **Screenshot:** Aggregate table after the run (or near the end of recover): labels + TOTAL, with 95% column visible. Same-frame Task Manager. For the **shape** (baseline → jump → recover) the HTML dashboard from `-e -o` is the time-series evidence; the GUI Aggregate is the percentile snapshot required by the brief.

---

## GUI vs graded run (do not mix)

| Artifact | When | What it is for |
|----------|------|----------------|
| GUI + the one listener | Demo video (≥6 min, Vietnamese) and evidence PNGs | Show the assigned report view beside Task Manager |
| `jmeter -n … -l *.jtl` | Timed Load / Stress / Spike / soak | Raw log for P10; **source of truth** for error% and percentiles |
| `-e -o report_*/` | After each `-n` run | HTML graphs (over-time) that Tree/Summary/Aggregate GUI do not replace |

Listeners in the `.jmx` must stay **one type each** so opening the plan in GUI matches the assignment. The `-n` run still writes `.jtl` even if the listener is present; we will not add extra listeners to “get more reports.”

Soak (later, 15 threads × 12 min) is **not** a fourth distinct listener requirement. It can reuse Load’s Tree only for a short GUI peek, then `-n` + `.jtl` for the 12 min numbers.

---

## Filename check (`{StudentID}_{ScenarioType}_{YYYYMMDD}`)

| File | Listener |
|------|----------|
| `23127271_Load_20260814` | View Results Tree |
| `23127271_Stress_20260814` | Summary Report |
| `23127271_Spike_20260814` | Aggregate Report |

**Stop condition met:** listener assignment + why. Next gate is P04 (human review of P00–P03), still no `.jmx`.
