# Test Script Specification – EShop_Workload_Model.jmx

## 1. Purpose

This document specifies the design, configuration, and behavior of the JMeter test script `EShop_Workload_Model.jmx`, which models a realistic mixed-traffic workload against the **EShop** application. The script uses **Throughput Controllers** to simulate a weighted mix of user journeys (browsing, viewing products, purchasing, checking out) under two different load profiles (Baseline and Spike).

---

## 2. System Under Test (SUT)

| Parameter | Value |
|---|---|
| Protocol | HTTP |
| Host | `localhost` |
| Port | `3000` |
| Content Encoding | UTF-8 |
| HTTP Implementation | HttpClient4 |

---

## 3. Test Plan-Level Configuration

The following elements are configured at **Test Plan scope** (siblings of the Thread Groups) and therefore apply globally to **every sampler in every Thread Group**.

| Element | Type | Configuration | Purpose |
|---|---|---|---|
| HTTP Request Defaults | Config Element | domain=`localhost`, port=`3000`, protocol=`http` | Centralizes the base URL for all requests |
| HTTP Header Manager | Config Element | `Content-Type: application/json` | Applies JSON content type to all requests |
| HTTP Cookie Manager | Config Element | `clearEachIteration=false`, `controlledByThreadGroup=false` | Manages session cookies; cookies persist across loop iterations |
| Constant Timer | Timer | Delay = `1000 ms` | Adds 1-second think time before each sampler execution |
| Response Assertion – "HTTP 200" | Assertion | Field = Response Code, Pattern = `200`, Test Type = Equals | Validates that every sampled request returns HTTP status 200 |

**Test Plan properties:**

| Property | Value |
|---|---|
| Tear-down on shutdown | `true` |
| Functional test mode | `false` (raw response data not stored — suitable for load testing) |
| Serialize Thread Groups | `false` — Thread Groups execute **concurrently**, not sequentially |
| User-defined variables | None defined |

---

## 4. Load Profiles (Thread Groups)

The script defines **two Thread Groups**, representing two distinct load scenarios. Both share the same workload mix (Section 5) but differ in concurrency and duration.

| Thread Group |  Threads (Users) | Ramp-Up | Duration | Loop Count | Same User per Iteration | On Sample Error |
|---|---|---|---|---|---|---|
| **Thread Group 1 – Baseline Load Test** |  50 | 60 s | 180 s (3 min) | Infinite (bounded by duration) | true | Continue |
| **Thread Group 2 – Spike Load Test** |  500 | 30 s | 60 s (1 min) | Infinite (bounded by duration) | true | Continue |

---

## 5. Workload Model (Throughput Controllers)

Each Thread Group contains four **Throughput Controllers** configured with `style = Percent Executions`, distributing traffic across four user journeys. The percentages are identical in both Thread Groups.

| Scenario | Throughput Controller | Weight | Description |
|---|---|---|---|
| Browse Products | `Browse Products (60%)` | **60%** | Anonymous product listing |
| View Product Detail | `View Product Detail (25%)` | **25%** | Product listing + detail view with correlation |
| Customer Purchase | `Customer Purchase (10%)` | **10%** | Login + Add to Cart |
| Checkout | `Checkout (5%)` | **5%** | Login + Add to Cart + Checkout |
| **Total** | | **100%** | |

> `ThroughputController.perThread = false` means the percentage is calculated across **all threads collectively**, not per individual thread.

---

## 6. Request Specifications by Scenario

### 6.1 Scenario: Browse Products (60%)

| Step | Sampler Name | Method | Endpoint | Body | Notes |
|---|---|---|---|---|---|
| 1 | Get Product List | GET | `/api/products` | — | No parameters; returns product catalog |

**Sampler count per iteration:** 1

---

### 6.2 Scenario: View Product Detail (25%)

| Step | Sampler Name | Method | Endpoint | Body | Notes |
|---|---|---|---|---|---|
| 1 | Get Product List | GET | `/api/products` | — | Returns product catalog |
| 2 | *(Post-Processor)* Extract Product Id | — | — | — | JSON Extractor: `$[0].id` → `${productId}` |
| 3 | View Product Detail | GET | `/api/products/${productId}` | — | Uses `productId` extracted in Step 2 |

**Sampler count per iteration:** 2 HTTP requests + 1 extractor
**Correlation:** `productId` extracted from the first element (`$[0].id`) of the product list JSON response.

---

### 6.3 Scenario: Customer Purchase (10%)

| Step | Sampler Name | Method | Endpoint | Body | Notes |
|---|---|---|---|---|---|
| 1 | Login | POST | `/api/login` | `{"email": "test@eshop.com", "password": "Test1234!"}` | Hardcoded credentials |
| 2 | *(Post-Processor)* Extract JWT Token | — | — | — | JSON Extractor: `$.token` → `${token}` |
| 3 | Add Product to Cart | POST | `/api/cart` | `{"id": 1, "name": "San pham A", "price": 100000, "quantity": 2}` | Header: `Authorization: Bearer ${token}` |

**Sampler count per iteration:** 2 HTTP requests + 1 extractor
**Correlation:** `token` extracted from the login response and reused via an `Authorization` header on the Add to Cart request.

---

### 6.4 Scenario: Checkout (5%)

| Step | Sampler Name | Method | Endpoint | Body | Notes |
|---|---|---|---|---|---|
| 1 | Login | POST | `/api/login` | `{"email": "test@eshop.com", "password": "Test1234!"}` | Hardcoded credentials |
| 2 | *(Post-Processor)* Extract JWT Token | — | — | — | JSON Extractor: `$.token` → `${token}` |
| 3 | Add Product to Cart | POST | `/api/cart` | `{"id": 1, "name": "San pham A", "price": 100000, "quantity": 2}` | Header: `Authorization: Bearer ${token}` |
| 4 | Checkout | POST | `/api/checkout` | `{"total_amount": 200000, "shipping_address": "123 Le Loi, Q1, TP.HCM"}` | Header: `Authorization: Bearer ${token}` |

**Sampler count per iteration:** 3 HTTP requests + 1 extractor
**Correlation:** Same `token` variable is reused across the Add to Cart and Checkout requests within this scenario branch.

---

## 7. Variable Correlation Summary

| Variable | Source Sampler | Extraction Method | JSON Path / Expression | Used In | Default Value |
|---|---|---|---|---|---|
| `productId` | Get Product List | JSON Extractor | `$[0].id` | View Product Detail (`/api/products/${productId}`) | `NOT_FOUND` |
| `token` | Login | JSON Extractor | `$.token` | Authorization header (`Bearer ${token}`) on Add to Cart / Checkout | `NOT_FOUND` |

> Both extractors are configured with `match_numbers = 1` (first match only) and a fallback default value of `NOT_FOUND`, which will surface clearly in results if the API response shape changes or the correlation fails, rather than failing silently.

---

## 8. Test Data

| Field | Value | Scope | Risk |
|---|---|---|---|
| Login credentials | `test@eshop.com` / `Test1234!` | Hardcoded, shared by all threads | All virtual users authenticate as the same account — no data isolation between concurrent "customers" |
| Cart item | `id=1`, `name="San pham A"`, `price=100000`, `quantity=2` | Hardcoded, identical for all threads | Every simulated purchase adds the exact same product/quantity; does not reflect varied basket sizes |
| Checkout payload | `total_amount=200000`, fixed shipping address | Hardcoded, identical for all threads | No variation in order value or destination |

---

## 9. Assertions and Validation

| Assertion | Scope | Field Checked | Expected Value | Match Type |
|---|---|---|---|---|
| Response Assertion – "HTTP 200" | Global (Test Plan level, applies to all samplers) | Response Code | `200` | Equals |

No response body/content assertions (e.g., verifying `token` presence, cart total, or checkout confirmation) are configured. Functional correctness beyond the HTTP status code is not validated by this script.

---

## 10. Result Collection (Listeners)

Four listeners are configured at Test Plan level and apply to results from both Thread Groups:

| Listener | Type | Output File | Purpose |
|---|---|---|---|
| Aggregate Report | `StatVisualizer` | *(not set)* | Per-sampler statistics: Average, Min, Max, Percentiles, Error %, Throughput |
| Summary Report | `SummaryReport` | *(not set)* | Lightweight real-time summary during GUI execution |
| View Results Tree | `ViewResultsFullVisualizer` | *(not set)* | Detailed request/response inspection (debugging only) |
| Simple Data Writer | `SimpleDataWriter` | *(not set)* | Raw sample data persistence |

All listeners share the same `SampleSaveConfiguration`: response time, latency, connect time, success/failure, assertion results, thread counts, and byte counts are recorded; **raw response body, request headers, and response headers are NOT saved** (kept lightweight for load testing).

---

## 11. Test Plan Structure (Visual Summary)

```
EShop - Workload Model (Throughput Controllers)      [Test Plan]
│
├── HTTP Request Defaults                            (localhost:3000, http)
├── HTTP Header Manager                               (Content-Type: application/json)
├── HTTP Cookie Manager                                (persist across iterations)
├── Constant Timer                                     (1000 ms)
├── Response Assertion – HTTP 200                      (global, Equals)
│
├── Thread Group 1 – Baseline Load Test  [DISABLED]    (50 users / 60s ramp-up / 180s duration)
│   ├── Browse Products (60%)          → Get Product List
│   ├── View Product Detail (25%)      → Get Product List → Extract productId → View Product Detail
│   ├── Customer Purchase (10%)        → Login → Extract token → Add Product to Cart
│   └── Checkout (5%)                  → Login → Extract token → Add to Cart → Checkout
│
├── Thread Group 2 – Spike Load Test    [ENABLED]      (500 users / 30s ramp-up / 60s duration)
│   ├── Browse Products (60%)          → Get Product List
│   ├── View Product Detail (25%)      → Get Product List → Extract productId → View Product Detail
│   ├── Customer Purchase (10%)        → Login → Extract token → Add Product to Cart
│   └── Checkout (5%)                  → Login → Extract token → Add to Cart → Checkout
│
├── Aggregate Report
├── Summary Report
├── View Results Tree
└── Simple Data Writer
```

---

## 12. Recommended Execution Command

Non-GUI execution is recommended for accurate load measurement:

```
jmeter -n -t EShop_Workload_Model.jmx -l results.jtl -e -o report
```

| Flag | Purpose |
|---|---|
| `-n` | Run in Non-GUI mode |
| `-t EShop_Workload_Model.jmx` | Test plan file to execute |
| `-l results.jtl` | Explicitly define the results file (required — see Section 10 issue) |
| `-e -o report` | Generate an HTML Dashboard Report into the `report` folder after completion |

> Before execution, confirm whether **Thread Group 1 – Baseline Load Test** should be enabled. As currently configured, only the **Spike Load Test** will run.

---

## 13. Known Issues and Recommendations

| # | Observation | Recommendation |
|---|---|---|
| 1 | Thread Group 1 (Baseline) is disabled | Enable explicitly if a baseline load test is required, or run it as a separate, isolated execution rather than concurrently with the Spike test |
| 2 | Both Thread Groups run concurrently (`serialize_threadgroups=false`) | If Baseline is re-enabled, decide whether Baseline and Spike should run in parallel (combined load) or sequentially (isolated measurement); adjust `serialize_threadgroups` accordingly |
| 3 | All listener `filename` fields are empty | Always supply `-l <file>.jtl` on the command line for Non-GUI runs; do not rely on the listener's internal filename setting |
| 4 | View Results Tree is included in the script | Disable/remove before large-scale or CI-integrated execution to reduce memory overhead |
| 5 | Hardcoded login credentials and cart data | Externalize via CSV Data Set Config for realistic, non-duplicate test data across concurrent users |
| 6 | Global Response Assertion expects exactly HTTP 200 | Verify against actual EShop API responses (e.g., `POST` endpoints may correctly return `201`); adjust the assertion pattern if needed to avoid false failures |
| 7 | No functional/content assertions beyond status code | Consider adding assertions on key response fields (e.g., `token` present, `productId` non-null) to catch silent functional regressions during load testing |
| 8 | Spike Thread Group has no preceding warm-up | 500 users ramped in 30s with no prior baseline may stress the system from a cold start; consider a short warm-up phase before the spike if this reflects a production concern |

---

## 14. Traceability Matrix (Script vs. EShop API Endpoints)

| API Endpoint | Method | Exercised By | Coverage |
|---|---|---|---|
| `/api/products` | GET | Browse Products, View Product Detail |Covered |
| `/api/products/{id}` | GET | View Product Detail | Covered |
| `/api/login` | POST | Customer Purchase, Checkout |Covered |
| `/api/cart` | POST | Customer Purchase, Checkout | Covered |
| `/api/checkout` | POST | Checkout | Covered |

---

