# HW05 — Performance Testing — 23127271

**Student:** Võ Ngọc Bích Trâm · `23127271`  
**Branch:** `HW5-Tram`  
**Workflow:** Search-to-buy (login → search → detail → cart → checkout)  
**Tool:** Apache JMeter  
**SUT:** EShop backend `http://localhost:3000`

---

## Folder layout

| Path | Contents |
|------|----------|
| `docs/` | Design docs (endpoint map, scope) |
| `test-plans/` | `{23127271}_{Load\|Stress\|Spike}_{YYYYMMDD}.jmx` + CSV |
| `logs/` | Raw `.jtl` + HTML report folders (after real runs) |
| `submission/` | `git-commit-log.txt` (exported before zip) |

---

## Test summary

*(Fill after execution)*

- **Scenarios run:** Load, Stress, Spike
- **Endpoint groups covered:**
  - Auth-heavy: `POST /api/login`
  - Read-heavy: `GET /api/products?search=` → `GET /api/products/{id}`
  - Transactional: `POST /api/cart` → `POST /api/checkout`
- **Endurance / soak threshold:** TBD
- **Bugs / performance issues logged:** TBD
- **Demo video:** TBD
- **Agent Skill demo:** TBD

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
