# Stress - Phase 2: Generate Test Plan

## Generated Artifacts

- Test plan: `test-plans/23127158_Stress_20260816.jmx`
- Existing CSV inputs reused:
  - `data/auth_users.csv`
  - `data/product_inputs.csv`
  - `data/checkout_inputs.csv`
- Planned raw JTL path: `results/stress/23127158_Stress_20260816.jtl`
- Planned HTML report folder: `reports/html/stress/`

## Applied Human Feedback

The Stress Phase 1 design was approved without corrections. Phase 2 generated the Stress `.jmx` using the approved Buy-then-history workflow, StudentID `23127158`, Ultimate Thread Group, and Aggregate Report listener.

One arithmetic note was corrected during generation: the approved step schedule sums to approximately 785 seconds, not 765 seconds:

- Step 1: 10 users, 30 s ramp-up, 120 s hold, 15 s shutdown = 165 s
- Step 2: 20 users, 30 s ramp-up, 120 s hold, 15 s shutdown = 165 s
- Step 3: 35 users, 45 s ramp-up, 120 s hold, 20 s shutdown = 185 s
- Step 4: 50 users, 60 s ramp-up, 180 s hold, 30 s shutdown = 270 s
- Total: 785 s

## Test Plan Summary

- Scenario: Stress
- Workflow: Buy-then-history
- Test Plan name: `23127158_Stress_20260816`
- Backend target: `http://localhost:3000`
- Thread model: Ultimate Thread Group stepped profile
- Stress profile:
  - 10 users: initial delay 0 s, ramp-up 30 s, hold 120 s, shutdown 15 s
  - 20 users: initial delay 165 s, ramp-up 30 s, hold 120 s, shutdown 15 s
  - 35 users: initial delay 330 s, ramp-up 45 s, hold 120 s, shutdown 20 s
  - 50 users: initial delay 515 s, ramp-up 60 s, hold 180 s, shutdown 30 s
- Think time: Uniform Random Timer, 500 ms base delay plus 0-1000 ms random range
- Request sequence:
  1. `POST /api/login`
  2. `GET /api/products?search=${search}`
  3. `GET /api/products/${product_id}`
  4. `POST /api/cart`
  5. `POST /api/checkout`
  6. `GET /api/orders/my-orders`
- CSV variables:
  - `email,password`
  - `search,product_id,product_name,price,quantity`
  - `shipping_address,total_amount`
- Correlation:
  - Extract `$.token` as `${token}`
  - Reuse `${token}` as `Authorization: Bearer ${token}`
  - Extract `$.orderId` as `${orderId}`
  - Verify My Orders contains `"id":${orderId}`
- Listener/report view: Aggregate Report - Stress

## Validation Results

| Check | Result |
|---|---|
| XML parse | Passed |
| Naming convention | Passed: `23127158_Stress_20260816.jmx` |
| Scenario date | Passed: generated on 2026-08-16 local time |
| Endpoint sequence | Passed: same Buy-then-history sequence as Load |
| Backend base URL | Passed: `${protocol}://${host}:${port}` = `http://localhost:3000` |
| CSV configuration | Passed: three CSV Data Set Configs with recyclable rows |
| Correlation | Passed: JWT token and checkout orderId extractors present |
| Assertions | Passed: 12 ResponseAssertion elements present |
| Thread group | Passed: one Ultimate Thread Group, zero standard Thread Groups |
| Stress schedule | Passed: 10, 20, 35, and 50 user steps configured |
| Think time | Passed: 500-1500 ms |
| Listener uniqueness | Passed: Stress uses Aggregate Report; Load used Summary Report |
| Local plugin availability | Passed: `E:\apache-jmeter-5.6.3\lib\ext\jmeter-plugins-casutg-3.1.1.jar` exists |

## Review Notes

- The test plan has not been executed in Phase 2.
- Before Phase 3 execution, open the `.jmx` in JMeter and confirm the Ultimate Thread Group renders correctly.
- Use valid login data only; the shared `test@eshop.com` account avoids lockout because all rows use the correct password, but it remains a known limitation for user isolation.
- During execution, capture the real `.jtl`, HTML report, and screenshot showing JMeter together with backend resource usage.

## Revision - Continuous Incremental Stress Schedule

The Stress `.jmx` was revised after human review because the original Ultimate Thread Group rows behaved like independent total targets and could drop close to 0 users between stages. The E2E workflow, CSV configuration, correlation, assertions, think time, Aggregate Report listener, and output path were kept unchanged.

Updated Ultimate Thread Group schedule:

| Start Threads Count | Initial Delay | Startup Time | Hold Load For | Shutdown Time |
|---:|---:|---:|---:|---:|
| 10 | 0 | 30 | 675 | 30 |
| 10 | 150 | 30 | 525 | 30 |
| 15 | 300 | 45 | 360 | 30 |
| 15 | 465 | 60 | 180 | 30 |

Preview validation by schedule math:

| Time window | Expected concurrent users |
|---|---:|
| 0-30 s | Ramp 0 -> 10 |
| 30-150 s | Hold 10 |
| 150-180 s | Ramp 10 -> 20 |
| 180-300 s | Hold 20 |
| 300-345 s | Ramp 20 -> 35 |
| 345-465 s | Hold 35 |
| 465-525 s | Ramp 35 -> 50 |
| 525-705 s | Hold 50 |
| 705-735 s | Graceful shutdown 50 -> 0 |

Revision validation:

| Check | Result |
|---|---|
| XML parse after revision | Passed |
| Ultimate Thread Group rows | Passed: incremental rows 10, 10, 15, 15 |
| Continuous staircase preview | Passed: 10 -> 20 -> 35 -> 50 with no near-0 drop between stages |
| Request sequence unchanged | Passed |
| CSV configuration unchanged | Passed |
| Correlation/extractors unchanged | Passed |
| Assertions unchanged | Passed |
| Think time unchanged | Passed |
| Listener/output path unchanged | Passed |

Status: Pending Human Review.
