# [PERF][Endurance] Soak 300 users vượt latency guardrail dù không có lỗi

## Found by Test Case

Endurance / Soak Test - `23127158_Endurance_20260817.jmx`

## Requirement liên quan

FR-02 Login, FR-05 Product listing/search, FR-06 Product detail view, FR-07 Shopping cart, FR-08 Checkout, FR-11 Order history view.

## Severity / Priority

Major / P1

## Environment

- **OS**: Windows 11 Pro 64-bit, Lenovo 83EG
- **Browser**: N/A - Backend API tested by Apache JMeter
- **URL**: `http://localhost:3000`
- **Build/Commit**: Local HW05 workspace, Node.js + Express + SQLite backend

## Steps to reproduce

1. Start the EShop backend at `http://localhost:3000`.
2. Run `23127158/test-plans/23127158_Endurance_20260817.jmx`.
3. Use the Soak profile: 300 concurrent users, ramp-up 90 seconds, sustained hold 720 seconds, ramp-down 60 seconds.
4. Generate and inspect `23127158/reports/html-report/soak-profile/statistics.json`.

## Expected result

For sustained non-spike workload, the system should maintain stable throughput and stay within the continuous testing latency guardrail: p95 <= 25 ms and p99 <= 50 ms.

## Actual result

The Soak run completed 189.818 requests with 0 failures and error rate 0,0%. However, the HTML report recorded overall p95 = 40,0 ms and p99 = 71,0 ms, exceeding the proposed sustained/stepped-load latency guardrail. Throughput remained strong: overall HTML throughput 218,751 req/s, and hold-phase throughput from raw JTL stayed around 238,5-239,5 req/s. CPU peak was only 6,4%, RAM peak was 73,0 MB, so this appears as a tail-latency issue rather than CPU/memory exhaustion.

## Link github issue
https://github.com/trngnneee/eshop-sut/issues/411#issue-5165904814

