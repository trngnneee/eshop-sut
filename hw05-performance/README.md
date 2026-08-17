# HW05 — Performance Testing — 23127271

**Student:** Võ Ngọc Bích Trâm · `23127271`  
**Branch:** `HW5-Tram`  
**Workflow:** Search-to-buy (login → search → detail → cart → checkout)  
**Tool (required):** Apache JMeter 5.6.3  
**Tool (bonus):** k6 v2.1.0  
**SUT:** EShop backend `http://localhost:3000`

**Public GitHub folder:** https://github.com/trngnneee/eshop-sut/tree/HW5-Tram/hw05-performance/

---

## Folder layout

| Path | Contents |
|------|----------|
| `docs/` | Prompt plan, P00–P13, k6 K04–K09 |
| `test-plans/` | `{23127271}_{Load\|Stress\|Spike\|Soak}_20260814.jmx` + `.js` + CSV |
| `logs/` | Raw `.jtl`, HTML report folders, k6 JSON (Load/Spike/Soak) |
| `evidence/` | dxdiag + HTML dashboard/statistics screenshots |
| `audit/` | AI Audit Report |
| `submission/` | `git-commit-log.txt` (exported before zip) |

k6 Stress JSON (`23127271_Stress_20260814.json`, ~279 MB) is **not** in this repo (GitHub 100 MB file limit). Keep it in the Moodle zip / local workspace. Recomputed metrics: `docs/_k6_recompute_out.txt`.

---

## Test summary

- **Scenarios run:** Load (20 VU), Stress (100 VU), Spike (5→80→5), Soak (15 VU)
- **Endpoint groups covered:**
  - Auth-heavy: `POST /api/login`
  - Read-heavy: `GET /api/products?search=` → `GET /api/products/{id}`
  - Transactional: `POST /api/cart` → `POST /api/checkout`
- **Endurance / soak threshold:** ~7.27 rps, checkout p95 23 ms, 0% error (JMeter). Memory: UNKNOWN.
- **Bugs / performance issues logged:** 0 functional GitHub issues (0% HTTP error on graded runs; Stress knee is latency).
- **Demo video (Task 1, JMeter ≥6 min):** https://youtu.be/Nyvm0bxZxgA
- **Agent Skill demo:** TBD (second video, P16)

---

## Self-assessment

| No. | Criteria | Grade | Self-Assessed Grade |
|---|---|---|---|
| 1 | Task 1 — Load testing | 20 | |
| 2 | Task 1 — Stress testing | 20 | |
| 3 | Task 1 — Spike testing | 20 | |
| 4 | Task 2 — AI analysis + misinterpretation hunt | 10 | |
| 5 | Task 3 — Continuous Performance Testing proposal | 10 | |
| 6 | Agent Skills | 10 | |
| | **Total** | **100** | |
