# HW05 – Performance Testing

**Student:** Phan Quốc Thịnh  
**MSSV:** 23127486  
**Course:** CS423 / CSC13003 – Software Testing (AI-augmented · 2026)  
**Assignment:** HW05 – Performance Testing

---

## Self-Assessment Table

| No. | Criteria | Grade | Self-Assessed Grade |
|:----|:---------|:-----:|:-------------------:|
| 1 | Task 1 — Load testing | 20 | |
| 2 | Task 1 — Stress testing | 20 | |
| 3 | Task 1 — Spike testing | 20 | |
| 4 | Task 2 — AI analysis + misinterpretation hunt (with correct values from raw logs) | 10 | |
| 5 | Task 3 — Continuous Performance Testing proposal (G9.6) | 10 | |
| 6 | Agent Skills | 10 | |
| | **Total** | **100** | |

---

## Test Summary Report

### Scenarios Run

| Scenario | Test Plan File | Status |
|:---------|:--------------|:-------|
| Load Test | `23127486_Load_YYYYMMDD.jmx` | |
| Stress Test | `23127486_Stress_YYYYMMDD.jmx` | |
| Spike Test | `23127486_Spike_YYYYMMDD.jmx` | |

### Endpoint Groups Covered

| Group | Endpoints | Description |
|:------|:----------|:------------|
| Auth-heavy | `POST /api/auth/login`, ... | Login, account lockout |
| Read-heavy | `GET /api/products`, `GET /api/products/{id}`, ... | Product listing, search, detail |
| Transactional | `POST /api/cart`, `POST /api/orders`, ... | Add-to-cart, checkout |

### End-to-End Workflow

> _(Describe the workflow here: e.g., virtual user logs in → browses products → adds to cart → checks out)_

### Endurance Threshold

| Metric | Value |
|:-------|:------|
| Maximum Stable RPS | |
| Memory Ceiling | |
| Endurance Test Duration | ~10–15 minutes |
| Hardware | _(See hardware spec screenshot)_ |

### Bug / Performance Issues

| # | Issue | Type | GitHub Issue Link |
|:--|:------|:-----|:-----------------|
| 1 | | | |

### Demo Video

- YouTube (unlisted): _(Link here)_

---

## Repository

- GitHub: _(Link to public repository)_

---

## File Index

| File | Description |
|:-----|:------------|
| `Report.md` | Main performance testing report |
| `AI_Audit.md` | AI Audit Report (Mandatory Appendix) |
| `AI_Critique.md` | AI Critique (200–300 words) |
| `git_commit_log.txt` | Git commit log |
| `23127486_Load_YYYYMMDD.jmx` | JMeter Load test plan |
| `23127486_Stress_YYYYMMDD.jmx` | JMeter Stress test plan |
| `23127486_Spike_YYYYMMDD.jmx` | JMeter Spike test plan |
| `test_data.csv` | CSV input data for parameterized requests |
| `23127486_Load_YYYYMMDD.jtl` | Raw JTL log – Load test |
| `23127486_Stress_YYYYMMDD.jtl` | Raw JTL log – Stress test |
| `23127486_Spike_YYYYMMDD.jtl` | Raw JTL log – Spike test |
| `bug_report.md` | Bug report with screenshots |
| `screenshots/` | Resource monitor & hardware spec screenshots |
| `html_reports/` | HTML report folders for each scenario |
