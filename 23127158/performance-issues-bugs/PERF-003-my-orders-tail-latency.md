# [PERF][Orders] My Orders tail latency tăng dưới tải cao

## Found by Test Case

Spike Test - `23127158_Spike_20260816.jmx`; Endurance / Soak Test - `23127158_Endurance_20260817.jmx`

## Requirement liên quan

FR-11 Order history view (user)

## Severity / Priority

Minor / P2

## Environment

- **OS**: Windows 11 Pro 64-bit, Lenovo 83EG
- **Browser**: N/A - Backend API tested by Apache JMeter
- **URL**: `http://localhost:3000`
- **Build/Commit**: Local HW05 workspace, Node.js + Express + SQLite backend

## Steps to reproduce

1. Start the EShop backend at `http://localhost:3000`.
2. Run the Buy-then-history workflow under high concurrency using the Spike or Soak test plan.
3. In each workflow iteration, execute checkout and then call `GET /api/orders/my-orders` to verify the new order.
4. Inspect My Orders metrics in the Spike window analysis and Soak HTML report.

## Expected result

`GET /api/orders/my-orders` should remain stable as orders accumulate, especially because it is the final read-after-write verification step of the workflow. Under non-spike sustained load, My Orders should stay within the read-after-write guardrail: p95 <= 30 ms.

## Actual result

No functional failure was observed, but My Orders showed elevated tail latency under high load. In the Spike peak 500-user window, My Orders p99 reached 205,090 ms. In the Soak 300-user HTML report, My Orders p95/p99 reached 23,0 ms / 51,0 ms. This does not prove a database-index issue yet, but it suggests the order-history endpoint should be monitored and profiled as test data grows.

## Link github issue
https://github.com/trngnneee/eshop-sut/issues/412#issue-5165913188
