# User Guide - Performance Testing with k6 and AI-Assisted Scenario Generation

> Note: This is a draft User Guide skeleton. Screenshots, actual command outputs, and benchmark results will be added after executing the test scenarios on the EShop system.

## 1. Introduction
This guide provides developers and testers with step-by-step instructions on setting up, writing, and executing performance tests on EShop using k6. It also outlines how to leverage AI tools (ChatGPT/Claude) to accelerate script development while keeping audits manual and secure.

## 2. Installation

### Prerequisites
- Node.js (for EShop runtime if applicable)
- Go / Docker (depending on EShop container setup)

### k6 Installation
- **Windows (Chocolatey)**: `choco install k6`
- **macOS (Homebrew)**: `brew install k6`
- **Linux (Debian/Ubuntu)**: Follow official Debian repository instructions.

### EShop Setup
- Instructions on starting EShop locally:
  `[Insert actual EShop run command here]`

### Verification
Verify k6 installation by running:
```bash
k6 version
```
*Expected output*: `k6 vX.Y.Z (date, goX.Y.Z, platform)` `[Insert actual k6 output here]`

`[Insert installation screenshot here]`

## 3. First Test on EShop
1. **Start EShop** locally on your machine.
2. **Select user flow**: e.g., view homepage and access a product.
3. **Capture scenario guidelines**: Define endpoint path and workload specifications.
4. **Draft the script**: Write or generate the initial script file `baseline.js`.
5. **Run test**:
   ```bash
   k6 run baseline.js
   ```
6. **Read summary metrics**: Review HTTP request durations and error rates in the console.
7. **Save evidence**: Save console output logs.

`[Insert baseline test execution screenshot here]`

## 4. Advanced Usage
- **Thresholds**: Defining SLA limits (e.g., `http_req_duration: ['p(95)<500']`).
- **Scenarios**: Mixing browse flow with checkout flow in a single run.
- **Ramping VUs**: Implementing stages to increase load smoothly.
- **Custom Metrics**: Using Trend or Counter metrics to track specific application events.
- **Environment Variables**: Passing configuration options into tests.

## 5. Troubleshooting
| Problem | Possible Cause | Fix | Evidence |
|---|---|---|---|
| `connection refused` | EShop is not running | Start the EShop instance before running k6 | `[Link evidence here]` |
| High HTTP 500 error rates | Database lock / limit reached | Check EShop container log for SQLite locks | `[Link evidence here]` |
| `threshold failed` | Latency exceeded p95 limit | Analyze response time bottleneck or optimize DB queries | `[Link evidence here]` |

## 6. Failure Modes
Below are critical performance testing failure modes mapped to triggers, symptoms, detection, and mitigations:

| Failure Mode | Trigger | Symptom | Detection | Mitigation |
| :--- | :--- | :--- | :--- | :--- |
| **1. Unrealistic Workload Distribution** | Writing a script that hammers the checkout endpoint with 100% of VUs. | High checkout error rate, DB lockups instantly. | Check k6 request distribution stats; checkout requests match VUs exactly. | Refactor script using Scenarios or random weights to match the 60/25/10/5 funnel. |
| **2. Missing Think Time** | VUs requesting pages continuously with zero delay between requests. | Unnaturally high throughput (RPS) and CPU exhaustion on SUT. | Lack of `sleep()` functions inside the script logic. | Add realistic pauses (`sleep(Math.random() * 2 + 1)`) between user actions. |
| **3. Missing Session/Token Correlation** | Replaying hardcoded session cookies or order IDs in multiple parallel VUs. | HTTP 401 Unauthorized or duplicate order errors. | High error rates on authenticated endpoints. | Extract dynamic CSRF/Auth tokens from initial login responses and pass them in subsequent headers. |
| **4. Only Looking at Average Latency** | Reporting average latency instead of distribution percentiles. | Hidden poor user experiences (e.g., 5% of users waiting >10 seconds). | The average response time is low (e.g. 200ms) but p95 or p99 is high (e.g. 5000ms). | Define and monitor strict thresholds on `p(95)` and `p(99)` metrics in k6 configurations. |
| **5. Local Bottlenecks (SQLite/Hardware)** | Running k6 and EShop on the same weak local machine. | CPU spikes to 100% instantly, disk I/O bottlenecks skewing latencies. | System monitoring tools show test runner machine CPU/Disk usage is maxed out. | Run test runner on a separate network node, or limit VUs to avoid local hardware bottlenecks. |
| **6. AI Script Using Invalid Endpoints** | Using AI-generated k6 scripts containing hallucinated or deprecated EShop routes. | High HTTP 404 Not Found error rate. | k6 console log shows a flood of 404 status codes. | Perform a manual code audit of the generated URLs against actual EShop route controllers. |

## 7. References
- **k6 Documentation**: [https://k6.io/docs/](https://k6.io/docs/)
- **JMeter User Manual**: [https://jmeter.apache.org/usermanual/](https://jmeter.apache.org/usermanual/)
- **Artillery Docs**: [https://www.artillery.io/docs](https://www.artillery.io/docs)
- **EShop Repository**: [Insert repository link]

---
**Evidence / Project Management References**:
- Installation Verification: `[Insert installation screenshot here]`
- First Test Output: `[Insert actual k6 output here]`
- User Guide Tasks: `[Insert Jira task screenshot here]`
