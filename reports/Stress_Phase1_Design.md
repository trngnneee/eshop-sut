# Stress - Phase 1: Design

## Source Context

- StudentID: `23127158`
- Scenario: Stress
- Planned test-plan name: `23127158_Stress_20260816`
- Workflow: Buy-then-history
- Backend base URL: `http://localhost:3000`
- Existing CSV files: `data/stress_auth_users.csv`, `data/product_inputs.csv`, `data/checkout_inputs.csv`
- Previous approved Load baseline: 10 users, 60 s ramp-up, 300 s hold, 30 s shutdown, Summary Report listener

## Proposed Stress Design

### Workload Model

Use a closed-model JMeter stress test with the Ultimate Thread Group plugin. The workload gradually increases concurrent virtual users across multiple steps until the local backend starts to degrade. This keeps the same Buy-then-history request sequence as the Load scenario while increasing pressure on authentication, product reads, cart mutation, checkout writes, and My Orders readback.

### VU / Thread Count

Use a stepped profile with four stress levels:

| Step | Users | Ramp-up | Hold | Shutdown |
|---|---:|---:|---:|---:|
| 1 | 10 | 30 s | 120 s | 15 s |
| 2 | 20 | 30 s | 120 s | 15 s |
| 3 | 35 | 45 s | 120 s | 20 s |
| 4 | 50 | 60 s | 180 s | 30 s |

The peak is 50 concurrent users. This is intentionally higher than the approved Load baseline and should expose the first local threshold without making the run excessively long for a Node.js + Express + SQLite SUT.

### Duration

Total planned schedule is about 765 seconds, or 12.75 minutes:

- 165 s for step 1
- 165 s for step 2
- 185 s for step 3
- 270 s for step 4

The run is long enough to observe trend changes across stress levels while still remaining manageable for local execution and evidence capture.

### Think Time

Use a Uniform Random Timer between 500 and 1500 ms between business steps. This is shorter than the Load plan's 1000-3000 ms range so the same number of users produces stronger pressure while preserving a realistic user-paced workflow.

### CSV Usage

Reuse the three existing data-driven CSV files:

- `data/stress_auth_users.csv`: `email,password` with 50 distinct valid Stress users
- `data/product_inputs.csv`: `search,product_id,product_name,price,quantity`
- `data/checkout_inputs.csv`: `shipping_address,total_amount`

Rows should recycle during the stress run. All credentials should remain valid to avoid accidental login lockout. The Stress authentication CSV uses distinct users so shared cart and order-history state does not collapse into a single account during the 50-user peak.

### Correlation

- Extract `$.token` from `POST /api/login` into `${token}`.
- Send `Authorization: Bearer ${token}` on cart, checkout, and My Orders requests.
- Extract `$.orderId` from `POST /api/checkout` into `${orderId}`.
- Verify `GET /api/orders/my-orders` contains `${orderId}`.

### Assertions

Use the same assertions as the Load plan so results are comparable:

- HTTP 200 for all six samplers.
- Login response contains a JWT token.
- Product list response contains the selected product context.
- Product detail response contains the selected product ID/name/price.
- Add-to-cart response contains `Added to cart`.
- Checkout response contains `Checkout successful` and `orderId`.
- My Orders response contains the newly created `${orderId}`.

### JMeter Structure

- Test Plan: `23127158_Stress_20260816`
- Thread Group: Ultimate Thread Group
- HTTP Request Defaults: `http://localhost:3000`
- CSV Data Set Configs: auth, product, checkout
- Header Managers: JSON content type; dynamic authorization for protected endpoints
- Samplers:
  1. `POST /api/login`
  2. `GET /api/products?search=${search}`
  3. `GET /api/products/${product_id}`
  4. `POST /api/cart`
  5. `POST /api/checkout`
  6. `GET /api/orders/my-orders`
- Post-processors: JSON extractors for `${token}` and `${orderId}`
- Listener/report view: Aggregate Report, saving raw results to `results/stress/23127158_Stress_20260816.jtl`
- HTML report folder after execution: `reports/html/stress/`

### Stress Exit / Breakpoint Criteria

During analysis, treat any of these as stress degradation signals:

- Overall p95 exceeds 100 ms for a sustained stress step.
- Checkout or My Orders p95 exceeds 150 ms.
- Error rate reaches or exceeds 1%.
- HTTP 500, 401/403 from valid credentials, SQLite busy/locked errors, or assertion failures appear.
- Backend CPU stays near saturation or memory grows continuously during the peak step.

### Execution Evidence Needed Later

Phase 3 must collect real evidence, not generated evidence:

- Raw `.jtl` at `results/stress/23127158_Stress_20260816.jtl`
- JMeter HTML report under `reports/html/stress/`
- Screenshot showing JMeter and backend resource monitor together
- Notes on any backend crash, lockout, SQLite lock, or functional failure

## Design Summary

The Stress scenario will reuse the exact approved Buy-then-history workflow and the same CSV-driven business data as Load. The only intended changes are the workload profile, shorter think time, and a distinct Aggregate Report listener. The Ultimate Thread Group will step from 10 to 20 to 35 to 50 users over about 12.75 minutes to find where latency, errors, or local resource usage begins to degrade.

Status: Pending Human Review.
