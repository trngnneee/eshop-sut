# Report – HW05 Performance Testing

**Student:** Phan Quốc Thịnh  
**MSSV:** 23127486  
**Course:** CS423 / CSC13003 – Software Testing (AI-augmented · 2026)  
**Assignment:** HW05 – Performance Testing  
**Date:** _(Fill in date)_

---

## 1. Introduction

> _(Briefly describe the purpose of this performance testing assignment and the SUT – EShop.)_

## 2. System Under Test (SUT)

- **Application:** EShop – Vietnamese e-commerce demo
- **Repository:** https://github.com/ttbhanh/eshop-sut
- **Environment:** _(Fill in your local environment details: OS, RAM, CPU)_

## 3. Scope – Endpoint Selection

### 3.1 Selected Endpoint Groups

| Group | Endpoint(s) | Justification |
|:------|:------------|:--------------|
| Auth-heavy | _(e.g., POST /api/auth/login)_ | _(Justify your selection)_ |
| Read-heavy | _(e.g., GET /api/products, GET /api/products/{id})_ | _(Justify your selection)_ |
| Transactional | _(e.g., POST /api/cart, POST /api/orders)_ | _(Justify your selection)_ |

### 3.2 End-to-End Workflow

> _(Describe the end-to-end workflow that a virtual user will follow, e.g.:_  
> _1. Login (auth-heavy)_  
> _2. Browse/search products (read-heavy)_  
> _3. Add item to cart (transactional)_  
> _4. Checkout / create order (transactional))_

---

## 4. Task 1 – AI-Assisted Test Design and Execution

### 4.1 AI-Assisted Test Plan Design

> _(Describe how you used AI step-by-step to design the three test plans. Include the prompts you used and the AI's responses.)_

#### 4.1.1 Load Test Plan

- **File:** `23127486_Load_YYYYMMDD.jmx`
- **Scenario:** _(Describe the load scenario)_
- **Parameters:**
  - Thread count: 
  - Ramp-up: 
  - Duration: 
  - Think time: 
- **Report view used:** _(e.g., View Results Tree)_

#### 4.1.2 Stress Test Plan

- **File:** `23127486_Stress_YYYYMMDD.jmx`
- **Scenario:** _(Describe the stress scenario)_
- **Parameters:**
  - Thread count: 
  - Ramp-up: 
  - Duration: 
  - Think time: 
- **Report view used:** _(e.g., Summary Report)_

#### 4.1.3 Spike Test Plan

- **File:** `23127486_Spike_YYYYMMDD.jmx`
- **Scenario:** _(Describe the spike scenario)_
- **Parameters:**
  - Thread count (spike): 
  - Ramp-up: 
  - Duration: 
  - Think time: 
- **Report view used:** _(e.g., Aggregate Report)_

### 4.2 CSV Data-Driven Workflow

- **CSV file(s):** `test_data.csv`
- **Parameters:** _(Describe what is parameterized, e.g., credentials, product IDs, order payloads)_

### 4.3 Human Review – AI Corrections

> _(Critically review what the AI got wrong or missed in the test plans. For each issue, explain:_  
> _- What the AI generated_  
> _- What was wrong or missing_  
> _- How you fixed it_  
> _- Why the AI missed it (prompt quality, model limitations, endpoint characteristics))_

| # | Issue Found | AI Output | Correction Made | Why AI Missed It |
|:--|:------------|:----------|:----------------|:-----------------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

### 4.4 Test Execution

#### 4.4.1 Hardware Report

> _(Insert dxdiag/screenfetch screenshot and spec table here)_

| Spec | Value |
|:-----|:------|
| CPU | |
| RAM | |
| OS | |
| Hostname | |

#### 4.4.2 Load Test Results

- **Screenshot:** _(Insert screenshot of JMeter + Task Manager/htop in same frame)_
- **Key Metrics:**
  | Metric | Value |
  |:-------|:------|
  | Throughput (RPS) | |
  | Avg Response Time | |
  | 90th Percentile | |
  | Error Rate | |

#### 4.4.3 Stress Test Results

- **Screenshot:** _(Insert screenshot)_
- **Account Lockout Reset Steps:** _(Describe steps to reset 3-fail login lockout between runs)_
- **Key Metrics:**
  | Metric | Value |
  |:-------|:------|
  | Throughput (RPS) | |
  | Avg Response Time | |
  | 90th Percentile | |
  | Error Rate | |

#### 4.4.4 Spike Test Results

- **Screenshot:** _(Insert screenshot)_
- **Key Metrics:**
  | Metric | Value |
  |:-------|:------|
  | Throughput (RPS) | |
  | Avg Response Time | |
  | 90th Percentile | |
  | Error Rate | |

### 4.5 Endurance / Soak Test

- **Duration:** ~10–15 minutes
- **Load:** _(Sustained load configuration)_
- **Maximum Stable RPS:** 
- **Memory Ceiling:** 
- **Screenshot:** _(Insert resource monitor screenshot)_

### 4.6 Demo Video

- **YouTube (unlisted):** _(Link here)_

---

## 5. Task 2 – AI Analysis and Misinterpretation Hunt

### 5.1 AI Analysis of Results

> _(Describe how you prompted AI to analyse the .jtl logs and suggest performance thresholds. Include the prompts and AI responses.)_

### 5.2 Misinterpretation Hunt

> _(For each misinterpretation found, cite the correct value from your raw .jtl log and explain the error.)_

| # | AI Claim | Correct Value (from .jtl) | Error Explanation |
|:--|:---------|:--------------------------|:------------------|
| 1 | | | |
| 2 | | | |
| 3 | | | |

### 5.3 Feasibility of AI Recommendations

> _(Have the AI propose optimizations and classify each as feasible or hallucinated, with reasoning.)_

| # | AI Recommendation | Feasible / Hallucinated | Reasoning |
|:--|:-----------------|:-----------------------|:----------|
| 1 | | | |
| 2 | | | |
| 3 | | | |

---

## 6. Task 3 – Continuous Performance Testing Proposal (Disrupt / G9.6)

### 6.1 Proposal Overview

> _(Propose a continuous performance-testing model that:_  
> _- Watches SUT commits_  
> _- Decides whether to run performance tests_  
> _- Flags p95 regressions)_

### 6.2 Flow Chart

> _(Insert Mermaid or image flow chart here)_

```
[ Placeholder for flowchart ]
```

### 6.3 Trade-off Discussion

> _(Discuss the trade-offs of the proposed model: cost, false alarms, etc.)_

---

## 7. Bug Report

> _(Log any genuine bugs or performance issues found during testing. Include GitHub Issues links.)_

| # | Issue | Type | Severity | GitHub Issue |
|:--|:------|:-----|:---------|:-------------|
| 1 | | | | |

---

## 8. Conclusion

> _(Summarize your findings from all three tasks.)_

---

## References

- ISTQB Foundation Level Syllabus (latest edition).
- Hardman, P. (2025). A Post-AI Learning Taxonomy.
- Fuster Rabella, M. (2025). OECD Education Working Paper No. 338.
- Anthropic (2025). Building Reliable AI Test Agents — engineering blog.
- DeepEval & Promptfoo documentation — LLM testing frameworks.
