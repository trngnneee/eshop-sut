# [PERF][Spike] Tail latency tăng mạnh trong peak 500 users

## Found by Test Case

Spike Test - `23127158_Spike_20260816.jmx`

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
2. Run `23127158/test-plans/23127158_Spike_20260816.jmx`.
3. Use the Spike profile: baseline 50 users, spike to peak 500 users.
4. Inspect `23127158/results/spike_result.jtl` with window analysis for the peak 500-user hold window.

## Expected result

The system should absorb the short spike without errors and keep peak-window tail latency within the proposed Spike guardrail: p95 <= 60 ms and p99 <= 250 ms. Latency should recover after the spike.

## Actual result

The system produced no HTTP/assertion errors, but the Spike run showed clear tail latency under high concurrency. Values visible in the JMeter HTML report include:

| HTML report metric | Value |
|---|---:|
| Total samples | 88.157 |
| Total error rate | 0,0% |
| Total max response time | 464,0 ms |
| `01 Login` p95 / p99 / max | 34,0 ms / 153,990 ms / 457,0 ms |
| `05 Checkout` p95 / p99 / max | 36,0 ms / 166,230 ms / 440,0 ms |
| `06 My Orders Verify New Order` p95 / p99 / max | 32,0 ms / 148,0 ms / 419,0 ms |

Additional raw JTL window analysis shows the issue is concentrated in the peak 500-user window: overall peak-window p95 reached 57,0 ms and p99 reached 200,0 ms. Endpoint-level peak p99 values were also high: Checkout 227,940 ms, Login 218,080 ms, and My Orders 205,090 ms. The issue is performance-related, not a functional failure, because recovery returned near baseline after spike ramp-down.

## Link github issue
https://github.com/trngnneee/eshop-sut/issues/410#issue-5165886300

