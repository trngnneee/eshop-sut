# Stress - Phase 4: Result Analysis

## Source Evidence

- Raw JTL: `results/stress/result.jtl`
- Test plan: `test-plans/23127158_Stress_20260816.jmx`
- Scenario: Stress
- Workflow: Buy-then-history
- Run window from JTL timestamps: 2026-08-16 00:26:10 +07:00 to 2026-08-16 00:39:11 +07:00
- Analyzer: `.codex/skills/hw05-performance-testing/scripts/analyze_jtl.py`
- Evidence gap: `reports/html/stress/` is empty in the workspace, and no Stress resource-monitor screenshot was found during this analysis pass.

## Objective Metrics From Raw JTL

| Metric | Value | Source |
|---|---:|---|
| Total samples | 20,531 | `result.jtl` rows |
| Failures | 0 | `success` column |
| Error rate | 0.0% | `failures / samples` |
| Response code distribution | HTTP 200: 20,531 | `responseCode` column |
| Duration | 780.832 s | first-to-last `timeStamp` |
| Request throughput | 26.294 req/s | `samples / duration` |
| Approx. complete workflows | 3,375 | terminal sampler count, `06 My Orders Verify New Order` |
| Approx. workflow throughput | 4.322 workflows/s, 259.34 workflows/min | `3375 / 780.832 s` |
| Avg latency | 4.948 ms | `elapsed` column |
| Median latency | 3.0 ms | `elapsed` column |
| p90 latency | 10.0 ms | `elapsed` column |
| p95 latency | 15.0 ms | `elapsed` column |
| p99 latency | 31.0 ms | `elapsed` column |
| Max latency | 82.0 ms | `elapsed` column |

## Per-Sampler Metrics From Raw JTL

| Sampler / endpoint | Samples | Error % | Avg ms | p95 ms | p99 ms | Throughput req/s |
|---|---:|---:|---:|---:|---:|---:|
| 01 Login / `POST /api/login` | 3,473 | 0.0 | 4.191 | 11.0 | 24.0 | 4.448 |
| 02 Browse Product List / `GET /api/products?search=...` | 3,448 | 0.0 | 2.434 | 8.0 | 21.0 | 4.429 |
| 03 View Product Detail / `GET /api/products/:id` | 3,428 | 0.0 | 2.369 | 8.0 | 18.73 | 4.408 |
| 04 Add To Cart / `POST /api/cart` | 3,414 | 0.0 | 2.079 | 3.0 | 9.0 | 4.397 |
| 05 Checkout / `POST /api/checkout` | 3,393 | 0.0 | 6.495 | 11.0 | 22.0 | 4.371 |
| 06 My Orders Verify New Order / `GET /api/orders/my-orders` | 3,375 | 0.0 | 12.260 | 31.0 | 38.0 | 4.353 |

## AI Interpretation

The Stress run completed successfully from the raw JTL perspective. All 20,531 samples succeeded and all recorded responses were HTTP 200, so the selected 10/20/35/50-user stepped profile did not break the backend functionally. Overall latency stayed low on this local machine: p95 was 15 ms, p99 was 31 ms, and max latency was 82 ms. Request throughput rose to 26.294 req/s, and the terminal My Orders sampler shows approximately 3,375 complete workflows, or 4.322 workflows/s.

The clearest stress signal is endpoint skew, not failures. `GET /api/orders/my-orders` is the slowest sampler with avg 12.260 ms, p95 31 ms, and p99 38 ms. This is much higher than the other read/cart steps and higher than checkout p95 11 ms. This pattern is plausible because each completed workflow creates another order, and My Orders reads the user's order history at the end of every iteration.

Compared with the approved Load run, overall p95 increased from 8 ms to 15 ms while request throughput increased from 4.539 req/s to 26.294 req/s. This is a healthy scaling result for the tested local profile. However, it does not prove production capacity or resource headroom because the JTL does not include CPU, memory, disk I/O, event-loop delay, or SQLite lock-wait data. No resource-monitor screenshot or HTML report was found in the workspace, so hardware-saturation claims remain unsupported.

## AI-Proposed Thresholds

| Threshold | Proposed value | Rationale | Raw metric used |
|---|---:|---|---|
| Stress overall p95 warning | > 30 ms | Observed Stress p95 is 15 ms; 30 ms catches a 2x latency regression under the same profile while allowing local variance. | Overall p95 = 15 ms |
| Stress overall p95 fail / breakpoint | > 100 ms | Phase 1 identified sustained p95 above 100 ms as a stress degradation signal; this run stayed far below it. | Overall p95 = 15 ms |
| My Orders p95 warning | > 50 ms | My Orders is the slowest sampler at p95 31 ms; 50 ms would flag further order-history growth before it dominates the workflow. | My Orders p95 = 31 ms |
| Checkout p95 warning | > 50 ms | Checkout is the main write step and observed p95 is 11 ms; 50 ms would catch write-path contention without overreacting to small local noise. | Checkout p95 = 11 ms |
| Error-rate warning | > 0.5% | Observed error rate is 0.0%; any recurring failures with valid credentials during Stress should be investigated. | Error rate = 0.0% |
| Error-rate fail | >= 1.0% | At 1% failures, the stepped stress profile is no longer reliable enough for the selected E2E workflow. | Error rate = 0.0% |
| Complete workflow throughput floor | < 3.75 workflows/s | Observed workflow throughput is 4.322 workflows/s; 3.75 workflows/s gives about 13% tolerance while catching a meaningful regression. | Workflow throughput = 4.322 workflows/s |
| Request throughput floor | < 23 req/s | Observed request throughput is 26.294 req/s; below 23 req/s under the same profile suggests throughput degradation. | Request throughput = 26.294 req/s |

## AI-Proposed Optimizations

| Recommendation | Evidence category | Metric / observation used | Expected effect |
|---|---|---|---|
| Add an index for user order-history reads, for example `CREATE INDEX idx_orders_user_id_id ON orders(user_id, id DESC)`, then rerun Stress to verify. | Supported by raw evidence | My Orders is the slowest sampler: avg 12.260 ms, p95 31 ms, p99 38 ms; backend query filters by `user_id` and orders by `id DESC`; schema shows no index on `orders.user_id`. | Reduce My Orders latency and keep order-history verification stable as the orders table grows. |
| Add pagination or a `LIMIT` to `/api/orders/my-orders` for the performance workflow if the UI only needs recent orders. | Supported by raw evidence | Stress creates 3,375 completed workflows and repeatedly reads My Orders; My Orders has the highest avg and p95 latency. | Reduce response size and database work per verification request, especially after many created orders. |
| Keep the checkout implementation unchanged for now; do not claim write-path saturation from this run. | Supported by raw evidence | Checkout p95 is 11 ms, p99 22 ms, max 82 ms, with 0 failures and no recorded SQLite lock errors. | Avoid premature optimization; focus investigation on order-history read growth first. |
| Generate the missing JMeter HTML report and copy real Stress resource-monitor screenshots into the evidence folder. | Supported by raw evidence | Raw JTL exists, but `reports/html/stress/` is empty and no Stress screenshot was found in the workspace. | Completes assignment evidence and allows latency/resource correlation during human review. |
| Use per-thread or per-user test accounts instead of the repeated `test@eshop.com` account. | Plausible but not proven | CSV repeats one account, and all orders accumulate under one user's My Orders history; the JTL shows My Orders is slowest, but it does not prove shared-user data is the only cause. | Improve realism, reduce shared cart/order-history interference, and make assertions cleaner under heavier tests. |
| Enable SQLite WAL mode and configure a busy timeout only if later Spike/endurance runs show lock errors or checkout tail latency growth. | Plausible but not proven | This Stress JTL has 0 failures and no lock-related response codes/messages; checkout p95 is only 11 ms. | May improve concurrent read/write behavior under heavier tests, but this run does not prove it is needed. |
| Claim that the stress test reached the local hardware limit. | Unsupported / possible hallucination | The JTL has no CPU, memory, disk, or process evidence, and no resource-monitor screenshot was found. | Do not include this claim unless backed by real resource-monitor evidence. |
| Claim that a normal B-tree index on `products(name)` will fix a product-search bottleneck in this run. | Unsupported / possible hallucination | Product list p95 is 8 ms, and the backend search uses a leading-wildcard `LIKE '%term%'` query; no search bottleneck is shown. | Avoid unsupported database-index claims; validate query plans before proposing this as a performance fix. |

## Human Review Questions

- Confirm whether the Stress interpretation should be marked as healthy scaling rather than a discovered breakpoint.
- Review whether the My Orders index and pagination recommendations should be classified as supported, feasible, or only plausible.
- Verify whether the missing Stress HTML report and resource-monitor screenshot exist outside the workspace and should be copied into the submission evidence.
- Check whether the proposed p95 and throughput thresholds match your hardware and course expectations.

Status: Pending Human Review.
