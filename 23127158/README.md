# HW05 AI Performance Testing - 23127158

## Student Information

| Item | Value |
|---|---|
| Student name | Nguyễn Thanh Gia Bảo |
| Student ID | 23127158 |
| SUT | EShop backend API |
| Backend base URL during test | `http://localhost:3000` |
| Performance tool | Apache JMeter 5.6.3 |
| Main report | `reports/HW05_Main_Report.md` |
| AI Audit Report | `reports/AI_Audit_Report.md` |
| GitHub repository | `https://github.com/trngnneee/eshop-sut/tree/HW5-Bao` |

## Demo Video Links

| Clip | Content | YouTube link |
|---|---|---|
| Clip 1 | Load/Stress/Spike execution evidence with Vietnamese narration | `https://youtu.be/DMInJLsW32o` |
| Clip 2 | Agent Skill demonstration with Vietnamese narration | `https://youtu.be/_uB7Mj2IpRg` |

## Self-Assessment

| No. | Criteria | Grade | Self-Assessed Grade |
|---:|---|---:|---:|
| 1 | Task 1 - Load testing | 20 | 20 |
| 2 | Task 1 - Stress testing | 20 | 20 |
| 3 | Task 1 - Spike testing | 20 |  20 |
| 4 | Task 2 - AI analysis + misinterpretation hunt | 10 |  10 |
| 5 | Task 3 - Continuous Performance Testing proposal | 10 | 10 |
| 6 | Agent Skills | 10 | 10 |
|  | Total | 100 | 100 |

## Test Summary

| Scenario | Test plan | Raw JTL | HTML report | Evidence screenshot | Result summary |
|---|---|---|---|---|---|
| Load | `test-plans/23127158_Load_20260815.jmx` | `results/load_result.jtl` | `reports/html-report/load-profile/` | `screenshots/load-test-and-resource-usage.png` | 16.714 samples, error rate 0,0%, p95 6,0 ms, p99 9,0 ms, throughput 35,061 req/s. |
| Stress | `test-plans/23127158_Stress_20260816.jmx` | `results/stress_result.jtl` | `reports/html-report/stress-profile/` | `screenshots/stress-test-and-resource-usage.png` | 107.203 samples, error rate 0,0%, p95 8,0 ms, p99 13,0 ms, throughput 179,655 req/s. |
| Spike | `test-plans/23127158_Spike_20260816.jmx` | `results/spike_result.jtl` | `reports/html-report/spike-profile/` | `screenshots/spike-test-and-resource-usage.png` | 88.157 samples, error rate 0,0%, p95 10,0 ms, p99 16,0 ms, throughput 184,866 req/s; peak window p99 200,0 ms. |
| Soak / Endurance | `test-plans/23127158_Endurance_20260817.jmx` | `results/soak_result.jtl` | `reports/html-report/soak-profile/` | `screenshots/soak-test-and-resource-usage.png` | 189.818 samples, error rate 0,0%, p95 40,0 ms, p99 71,0 ms, throughput 218,751 req/s. |

## Endpoint Groups Covered

The same end-to-end workflow `Buy-then-history` was used across Load, Stress, Spike and Soak:

`Login -> browse product list -> view product detail -> add to cart -> checkout -> read My Orders`

| Endpoint group | Endpoint(s) covered | Workflow role |
|---|---|---|
| Auth-heavy | `POST /api/login` | Authenticate user and obtain JWT token. |
| Read-heavy | `GET /api/products`, `GET /api/products/:id` | Browse product list and view product detail. |
| Transactional | `POST /api/cart`, `POST /api/checkout`, `GET /api/orders/my-orders` | Add item to cart, create order and verify the newly created order. |

## Endurance Threshold

The empirical local endurance threshold was recorded at **300 concurrent users**, with approximately **238 stable RPS** during the sustained hold, **0,0% error rate**, **CPU peak 6,4%**, and **memory ceiling 73,0 MB**. The soak test completed 189.818 requests successfully, but p95/p99 latency should continue to be monitored because the HTML report recorded p95 40,0 ms and p99 71,0 ms.

## Performance Issues / Bugs

No functional bug was found in the accepted performance runs because Load, Stress, Spike and Soak all recorded 0,0% error rate. Three performance issues were documented for tracking:

| ID | Summary | Report file |
|---|---|---|
| PERF-001 | Spike peak 500 users creates strong tail latency across the workflow. | `performance-issues-bugs/PERF-001-spike-peak-tail-latency.md` |
| PERF-002 | Soak 300 users exceeds the proposed latency guardrail despite 0,0% errors. | `performance-issues-bugs/PERF-002-soak-latency-guardrail-exceeded.md` |
| PERF-003 | `My Orders` tail latency increases under high load and should be profiled when order data grows. | `performance-issues-bugs/PERF-003-my-orders-tail-latency.md` |

Number of bugs / performance issues: **3 performance issues, 0 confirmed functional bugs**.
