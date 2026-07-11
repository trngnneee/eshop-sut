# Performance Test Report - EShop

Student: `23127438 - Đặng Trường Nguyên`

## 1. Objective

Evaluate `k6` as the main performance testing tool for the EShop seminar demo. The test simulates realistic e-commerce behavior so the team can measure response time, throughput, latency percentiles, error rate, and application stability during both normal load and sudden traffic spikes.

## 2. Test Environment

| Item | Value |
| --- | --- |
| Application | EShop backend |
| Base URL | `http://localhost:3000` |
| Backend stack | Node.js, Express, SQLite |
| Test data | Seeded database from `backend/database.js` |
| Test user | `test@eshop.com` |
| Tool | `k6 v2.0.0` |
| Execution date | 2026-07-11 |

## 3. Workload Model

Each k6 iteration randomly selects one user action according to the target e-commerce funnel distribution below.

| User action | Target mix | Endpoint behavior |
| --- | ---: | --- |
| Browse/Search Products | 60% | `GET /api/products` or `GET /api/products?search=...` |
| View Product Details | 25% | `GET /api/products/:id` |
| Add to Cart | 10% | `POST /api/cart` with JWT |
| Checkout Flow | 5% | `POST /api/checkout` with JWT |

Reusable script:

```text
tests/performance_testing/scripts/eshop.k6.js
```

## 4. Baseline Test Profile

Command:

```bash
cd tests/performance_testing
npm run k6:baseline
```

Profile:

| Setting | Value |
| --- | --- |
| Target virtual users | 50 VUs |
| Ramp-up | 1 minute |
| Steady state | 3 minutes |
| Ramp-down | 1 minute |
| Purpose | Measure baseline latency and throughput under normal operating load |

Result:

| Metric | Value |
| --- | --- |
| Total requests | 12,036 |
| Completed iterations | 12,034 |
| Interrupted iterations | 0 |
| Throughput | 40.04 req/s |
| Average response time | 1.09 ms |
| Median response time | 0.78 ms |
| p95 latency | 3.80 ms |
| p99 latency | 4.65 ms |
| Error rate | 0.00% |
| Check pass rate | 100.00% |

Observed workload distribution:

| User action | Target mix | Observed count | Observed mix |
| --- | ---: | ---: | ---: |
| Browse/Search Products | 60% | 7,241 | 60.17% |
| View Product Details | 25% | 2,976 | 24.73% |
| Add to Cart | 10% | 1,202 | 9.99% |
| Checkout Flow | 5% | 615 | 5.11% |

Evidence:

- `tests/performance_testing/reports/k6-baseline-summary.json`
- `tests/performance_testing/reports/k6-baseline-summary.html`
- Baseline execution screenshot: `[Insert baseline test execution screenshot here]`

## 5. Spike Test Profile

Command:

```bash
cd tests/performance_testing
npm run k6:spike
```

Profile:

| Setting | Value |
| --- | --- |
| Initial traffic | 50 VUs |
| Spike ramp-up | 50 to 500 VUs in 30 seconds |
| Peak load | 500 VUs for 1 minute |
| Ramp-down | 30 seconds |
| Purpose | Evaluate whether EShop crashes, locks SQLite, or drops requests during a sudden traffic burst |

Result:

| Metric | Value |
| --- | --- |
| Total requests | 45,943 |
| Completed iterations | 45,941 |
| Interrupted iterations | 0 |
| Throughput | 378.43 req/s |
| Average response time | 1.15 ms |
| Median response time | 0.70 ms |
| p95 latency | 3.73 ms |
| p99 latency | 5.95 ms |
| Error rate | 0.00% |
| Check pass rate | 100.00% |

Observed workload distribution:

| User action | Target mix | Observed count | Observed mix |
| --- | ---: | ---: | ---: |
| Browse/Search Products | 60% | 27,558 | 59.99% |
| View Product Details | 25% | 11,605 | 25.26% |
| Add to Cart | 10% | 4,448 | 9.68% |
| Checkout Flow | 5% | 2,330 | 5.07% |

Evidence:

- `tests/performance_testing/reports/k6-spike-summary.json`
- `tests/performance_testing/reports/k6-spike-summary.html`
- Spike execution screenshot: `[Insert spike test execution screenshot here]`

## 6. Analysis

The observed action mix closely matched the intended workload model in both profiles. The baseline test stayed stable at 50 concurrent VUs with 0.00% error rate and p95 latency of 3.80 ms. The spike test increased traffic to 500 VUs and still completed without failed HTTP requests or interrupted iterations.

System CPU and memory were not separately monitored during this run. Application stability was checked through k6 results and a post-spike `GET /api/products` smoke check, which returned HTTP `200`. No backend crash, visible SQLite lock failure, or request drop was observed during these executions.

## 7. Conclusion

`k6` is suitable as the main tool for the EShop performance testing demo. It supports realistic weighted user behavior, concurrent virtual users, spike profiles, threshold-based pass/fail checks, and reusable summary outputs. Under the tested local workload, EShop remained stable in both baseline and spike scenarios, with 0.00% error rate and 100.00% check pass rate.
