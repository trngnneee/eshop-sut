# Load - Phase 4: Result Analysis

## Source Evidence

- Raw JTL: `results/load/result.jtl`
- Test plan: `test-plans/23127158_Load_20260815.jmx`
- Scenario: Load
- Workflow: Buy-then-history
- Run window from JTL timestamps: 2026-08-15 23:37:54 +07:00 to 2026-08-15 23:44:14 +07:00
- Execution evidence gap: `reports/html/load/` is currently empty, and no resource-monitor screenshot was found in the workspace during this analysis pass.

## Objective Metrics From Raw JTL

Computed with `.codex/skills/hw05-performance-testing/scripts/analyze_jtl.py`.

| Metric | Value | Source |
|---|---:|---|
| Total samples | 1,727 | `result.jtl` rows |
| Failures | 0 | `success` column |
| Error rate | 0.0% | `failures / samples` |
| Response code distribution | HTTP 200: 1,727 | `responseCode` column |
| Duration | 380.446 s | first-to-last `timeStamp` |
| Request throughput | 4.539 req/s | `samples / duration` |
| Approx. complete workflows | 283 | minimum terminal sampler count, `06 My Orders Verify New Order` |
| Approx. workflow throughput | 0.744 workflows/s, 44.63 workflows/min | `283 / 380.446 s` |
| Avg latency | 2.871 ms | `elapsed` column |
| Median latency | 2.0 ms | `elapsed` column |
| p90 latency | 5.0 ms | `elapsed` column |
| p95 latency | 8.0 ms | `elapsed` column |
| p99 latency | 9.0 ms | `elapsed` column |
| Max latency | 46.0 ms | `elapsed` column |

## Per-Sampler Metrics From Raw JTL

| Sampler / endpoint | Samples | Error % | Avg ms | p95 ms | p99 ms | Throughput req/s |
|---|---:|---:|---:|---:|---:|---:|
| 01 Login / `POST /api/login` | 292 | 0.0 | 3.051 | 4 | 4 | 0.784 |
| 02 Browse Product List / `GET /api/products?search=...` | 291 | 0.0 | 1.567 | 2 | 3.1 | 0.784 |
| 03 View Product Detail / `GET /api/products/:id` | 289 | 0.0 | 1.519 | 2 | 2 | 0.776 |
| 04 Add To Cart / `POST /api/cart` | 286 | 0.0 | 1.916 | 3 | 3 | 0.768 |
| 05 Checkout / `POST /api/checkout` | 286 | 0.0 | 6.563 | 9 | 10 | 0.769 |
| 06 My Orders Verify New Order / `GET /api/orders/my-orders` | 283 | 0.0 | 2.640 | 3 | 4 | 0.785 |

## AI Interpretation

The Load run completed successfully from the raw JTL perspective. All 1,727 recorded samples succeeded, and every response code was HTTP 200. Overall latency was low in this local environment: p95 was 8 ms, p99 was 9 ms, and max latency was 46 ms. The measured request throughput was 4.539 req/s.

The checkout sampler is the slowest step in the workflow, with average latency 6.563 ms and p95 9 ms. This is expected because checkout performs an order insert, while the product list/detail endpoints are read-heavy and stayed around 2 ms p95. The My Orders verification step stayed low at p95 3 ms even after repeated order creation, so the raw Load evidence does not show order-history read degradation at this scale.

Sampler counts are uneven: 292 logins were recorded, but only 283 final My Orders checks completed. For business-flow reporting, the safer completed workflow count is therefore 283, not 292. This likely reflects Ultimate Thread Group ramp-down/stopped iterations near the end of the schedule, but the JTL alone cannot prove the exact stopping cause.

This result is a healthy baseline, not proof of production capacity. The JTL does not include CPU, memory, disk, SQLite lock waits, or server-side profiling. Because no resource-monitor screenshot or HTML report output was found in the workspace, any claim about hardware saturation would be unsupported.

## AI-Proposed Thresholds

| Threshold | Proposed value | Rationale | Raw metric used |
|---|---:|---|---|
| Overall p95 latency warning | > 50 ms | The observed p95 is 8 ms. A 50 ms warning catches a >6x regression while allowing normal local variance. | Overall p95 = 8 ms |
| Overall p95 latency fail | > 100 ms | A 100 ms p95 would be >12x this baseline and should fail the Load baseline unless explained by hardware or environment changes. | Overall p95 = 8 ms |
| Checkout p95 warning | > 75 ms | Checkout is the slowest business-critical sampler at p95 9 ms; 75 ms allows write variance but flags a major regression. | Checkout p95 = 9 ms |
| Error-rate warning | > 0.5% | The observed error rate is 0.0%; any recurring failures under valid-user Load are worth investigating. | Error rate = 0.0% |
| Error-rate fail | >= 1.0% | A 1% failure rate in a modest local Load scenario indicates unstable behavior or test-data contamination. | Error rate = 0.0% |
| Request throughput floor | < 4.0 req/s | Observed throughput is 4.539 req/s; dropping below 4.0 req/s under the same profile suggests regression. | Request throughput = 4.539 req/s |
| Complete workflow throughput floor | < 0.65 workflows/s | Observed completed workflow throughput is 0.744 workflows/s; this catches material slowdown while allowing noise. | Workflow throughput = 0.744 workflows/s |

## AI-Proposed Optimizations

| Recommendation | Evidence category | Metric / observation used | Expected effect |
|---|---|---|---|
| Keep the current implementation as the Load baseline and do not optimize solely from this run. | Supported by raw evidence | 0 failures, 0.0% error rate, all 1,727 responses HTTP 200, overall p95 8 ms | Avoid unnecessary code churn; preserve this run as the baseline for Stress/Spike comparison. |
| Add per-thread or per-user test accounts instead of reusing only `test@eshop.com` for all load threads. | Plausible but not proven | The original Load run used repeated credentials in `auth_users.csv`; workflow uses cart and orders tied to `user_id`; sampler counts are uneven from 292 login to 283 My Orders. This has been addressed for reruns by `data/load_auth_users.csv`. | Reduce shared-user state interference, make order-history assertions cleaner, and improve repeatability for higher Stress/Spike loads. |
| Generate the JMeter HTML report after execution and capture backend resource monitor evidence beside JMeter. | Supported by raw evidence | `results/load/result.jtl` exists, but `reports/html/load/` is empty and no resource-monitor screenshot was found | Improves assignment evidence quality; enables correlation of latency with CPU/memory/disk behavior. |
| Add an index for order-history lookup, for example `CREATE INDEX idx_orders_user_id_id ON orders(user_id, id DESC)`, if Stress/Spike or endurance tests show My Orders latency growth. | Plausible but not proven | My Orders query filters by `user_id` and sorts by `id DESC`; current Load My Orders p95 is only 3 ms, so the bottleneck is not proven | May keep order-history reads stable as the orders table grows; should be validated with larger data volume. |
| Consider SQLite WAL mode and a configured busy timeout if later Stress/Spike tests show checkout write contention or lock errors. | Plausible but not proven | Checkout is the slowest sampler at avg 6.563 ms and p95 9 ms, but this Load run has 0 failures and no lock errors | Could improve concurrent write/read behavior under heavier workloads; not necessary based on this Load run alone. |
| Parameterize `/api/products?search=...` SQL instead of interpolating the search term directly. | Plausible but not proven | Backend source shows `LIKE '%${searchQuery}%'`; product search p95 is 2 ms, so this is not a performance bottleneck in the JTL | Improves safety and query correctness; performance impact is likely small for this dataset. |
| Add a normal B-tree index on `products(name)` and expect it to speed up the current `LIKE '%term%'` search. | Unsupported / possible hallucination | Product search p95 is already 2 ms; the query pattern has a leading wildcard, which commonly prevents normal index use | Do not claim this as a proven optimization unless the query pattern changes or database query plans confirm benefit. |

## Human Review Questions

- Confirm whether the uneven sampler counts should be explained as expected ramp-down behavior from the Ultimate Thread Group.
- Review the optimization evidence categories, especially which items should be treated as feasible, plausible but not proven, unsupported, or hallucinated.
- Verify whether the missing HTML report and resource-monitor screenshot exist outside the workspace and should be copied into the evidence folder.
- Review whether the proposed thresholds are reasonable for your hardware and course expectations.

Status: Pending Human Review.
