---
name: performance-test-plan-design
description: >-
  Use this skill when the user wants to design and generate JMeter test plans
  for Performance Testing. Guides the agent step-by-step to: (1) explore
  the current project (EShop SUT) API endpoints, (2) design a single end-to-end workflow covering
  three API endpoint groups (auth-heavy, read-heavy, transactional), (3)
  generate three JMeter test plans (Load, Stress, Spike) as .jmx files with
  CSV parameterization, (4) name files following the convention
  {StudentID}_{ScenarioType}_{YYYYMMDD}, and (5) update the Report.md in the
  submissions folder with Task 1 design documentation.
---

# HW05 – Test Plan Design Skill

**Student:** Phan Quốc Thịnh | **MSSV:** 23127486  
**Submissions dir:** `c:\Users\Public\Projects\Testing_HCMUS\HW5\eshop-sut\submissions\`  
**SUT repo:** https://github.com/ttbhanh/eshop-sut

> **Scope (Lecturer Note):** Perform Load, Stress, and Spike testing on a
> **single end-to-end workflow** that covers **three API endpoint groups**:
> auth-heavy, read-heavy, and transactional.

---

## Step 0 — Discover the SUT's API

Before designing any test plan, inspect the SUT to identify the exact
endpoints, ports, and request/response schemas.

1. Check the SUT repository structure (README, `docker-compose.yml`, config
   files) to find the **base URL** and **port** of the backend REST API.
2. Look for an OpenAPI/Swagger spec (`swagger.json`, `/api/docs`, etc.) or
   review the frontend source to discover available endpoints.
3. Record these in `Report.md` under **Section 3 – Scope**.

Verify each endpoint with a quick `curl` or HTTP request before proceeding.

---

## Step 1 — Confirm the Workflow with the User (REQUIRED)

> ⚠️ **STOP — Do NOT proceed until the user has explicitly specified the workflow.**

The workflow/features to be tested **must be specified by the user**, not
chosen by the AI. Ask the user the following questions before continuing:

1. **Which end-to-end user workflow should be tested?**  
   (e.g., "Login → Browse products → Add to cart → Checkout")
2. **Which SUT features map to each endpoint group?**  
   Confirm which steps are auth-heavy, read-heavy, and transactional.
3. **Are there any constraints or special behaviors to handle?**  
   (e.g., account lockout after 3 failed logins, JWT token expiry, required headers)

**Wait for the user's answers before proceeding to any further steps.**

Once the user confirms the workflow, record it in this structured format (For each specified feature, you need to map to ít HTTP method + path):

```
[Auth]          <HTTP method> <endpoint>  — <brief description>
[Read]          <HTTP method> <endpoint>  — <brief description>
[Read]          <HTTP method> <endpoint>  — <brief description>
[Transactional] <HTTP method> <endpoint>  — <brief description>
[Transactional] <HTTP method> <endpoint>  — <brief description>
```

Then — and only then — use the AI to suggest realistic **think times**
(typically 1–3 s) between steps, with justification based on typical
e-commerce UX research.

**Update `Report.md`** → Section 3.2 "End-to-End Workflow" with the
user-confirmed workflow and the endpoint mapping table.

---

## Step 2 — Create the CSV Data File

> ⚠️ **Only proceed after the workflow is confirmed by the user in Step 1.**

Based on the user-confirmed workflow, determine which request fields vary
per virtual user and create the CSV accordingly.

For each request step in the workflow:
- Identify fields that differ between users (credentials, resource IDs, payloads)
- Add one CSV column for each varying field
- Do **not** invent columns for fields that are constant across users

Ask the user if there are **existing test accounts or data** already seeded
in the SUT's database. Use those real IDs/credentials if available; otherwise
use realistic-looking placeholder data (never real emails or passwords).

**File path:** `submissions\test_data.csv`

Generate at least 20 rows to ensure each virtual user gets unique data.


---

## Step 3 — Design the Three Test Scenarios with AI

For each scenario, prompt the AI step-by-step (not a single generic prompt).
Follow this pattern:

### 3.1 Load Test

**Goal:** Simulate normal, expected production load. The system should handle
this without degradation.

Prompt the AI to suggest:
- Thread count (virtual users) for "normal load" based on a small Vietnamese
  e-commerce site (e.g., 10–50 concurrent users)
- Ramp-up period (e.g., 60 seconds)
- Test duration (e.g., 5–10 minutes)
- Think time between requests

**Report listener:** Use **View Results Tree** (do NOT reuse for other tests).

**Output file naming:** `23127486_Load_{YYYYMMDD}.jmx`  
(Replace `{YYYYMMDD}` with today's actual date, e.g., `23127486_Load_20260815.jmx`)

### 3.2 Stress Test

**Goal:** Push beyond normal load until the system degrades or breaks. Identify
the breaking point.

Prompt the AI to suggest:
- Thread count significantly higher than load test (e.g., step up: 50→100→200)
- Ramp-up aggressive enough to stress the system
- Account lockout handling: stress login with intentionally wrong passwords may
  trigger 3-fail lockout. In the test plan, use diverse credentials from CSV
  so lockout affects only individual accounts, not all.

**Report listener:** Use **Summary Report** (different from Load test).

**Output file naming:** `23127486_Stress_{YYYYMMDD}.jmx`

### 3.3 Spike Test

**Goal:** Simulate a sudden burst of traffic (spike), then return to normal.

Prompt the AI to suggest:
- Baseline threads (low, e.g., 5–10)
- Spike threads (very high, e.g., 5× or 10× baseline, achieved instantly)
- Spike duration (short)
- Recovery period (return to baseline)

Consider using **Ultimate Thread Group** plugin or a stepping approach to
model the spike shape accurately.

**Report listener:** Use **Aggregate Report** (different from both above).

**Output file naming:** `23127486_Spike_{YYYYMMDD}.jmx`

---

## Step 4 — Generate the .jmx Files

For each of the three test plans, generate the full JMeter `.jmx` XML content.
Each `.jmx` file must include:

- [ ] **Test Plan** with name `{StudentID}_{ScenarioType}_{YYYYMMDD}`
- [ ] **CSV Data Set Config** pointing to `test_data.csv`
- [ ] **HTTP Request Defaults** (base URL, port, protocol)
- [ ] **HTTP Header Manager** (Content-Type: application/json, Authorization if needed)
- [ ] **ThreadGroup** with the scenario-specific parameters
- [ ] For each workflow step:
  - HTTP Sampler with correct method, path, and request body
  - Response Assertion (check HTTP 200/201)
  - JSON Extractor (to extract token from login response, product data, etc.)
  - Constant Timer (think time)
- [ ] **The correct Listener** (View Results Tree / Summary Report / Aggregate Report)
  - Set the filename to `{StudentID}_{ScenarioType}_{YYYYMMDD}.jtl`
- [ ] **EnduranceTest ThreadGroup** (for the soak test, separate thread group
  within the Load test plan or a 4th separate plan):
  - Duration: 600–900 seconds (10–15 minutes)
  - Moderate load (below breaking point found in stress test)

Save each file to:
```
c:\Users\Public\Projects\Testing_HCMUS\HW5\eshop-sut\submissions\
```

---

## Step 5 — Update Report.md (Task 1 Documentation)

After generating all test plans, update `Report.md` with the following:

### Section 4.1 — AI-Assisted Test Plan Design
- Document the AI prompts used (verbatim or summarized)
- For each scenario, fill in the parameters table (thread count, ramp-up, duration, think time)
- Explain how the workflow covers each endpoint group

### Section 4.2 — CSV Data-Driven Workflow
- Describe what parameters are in `test_data.csv` and why each was chosen

**DO NOT fill in:**
- Section 4.3 (Human Review – AI Corrections) — requires human judgment
- Section 4.4 (Test Execution Results) — requires running the tests
- Section 4.5 (Endurance Threshold) — requires running the soak test

---

## Validation

After completing the steps above, verify:

- [ ] 3 `.jmx` files exist in `submissions/` with correct naming convention
- [ ] `test_data.csv` exists with ≥ 20 rows
- [ ] Each `.jmx` uses a **different** listener type
- [ ] Report.md Sections 3.1, 3.2, 4.1, 4.2 are filled in
