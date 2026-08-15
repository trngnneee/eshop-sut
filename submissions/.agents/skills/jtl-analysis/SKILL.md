---
name: jtl-analysis
description: >-
  Use this skill when the user wants to analyze raw JMeter .jtl log files for
  HW05 Performance Testing (Task 2). Guides the agent to: (1) parse and
  summarize key metrics from the .jtl CSV logs, (2) prompt AI to suggest
  performance thresholds, (3) identify where AI misinterprets the metrics,
  (4) prompt AI to propose optimizations and classify them as feasible or
  hallucinated, and (5) update Report.md Task 2 sections with the analysis
  results. Human review of misinterpretations and feasibility judgments is
  NOT handled by this skill.
---

# HW05 – JTL Log Analysis Skill

**Student:** Phan Quốc Thịnh | **MSSV:** 23127486  
**Submissions dir:** `c:\Users\Public\Projects\Testing_HCMUS\HW5\eshop-sut\submissions\`

> **Task 2 Goal:** Use AI to analyse the `.jtl` logs and suggest performance
> thresholds, then present the raw AI output for human review.
>
> **This skill does NOT perform human review** — misinterpretation hunting and
> feasibility classification require human judgment.

---

## Prerequisites

Ensure the following files exist in `submissions/` before running this skill:
- `23127486_Load_{YYYYMMDD}.jtl`
- `23127486_Stress_{YYYYMMDD}.jtl`
- `23127486_Spike_{YYYYMMDD}.jtl`

If they do not exist, run the tests first using `hw5-test-plan-design` and
JMeter before proceeding.

---

## Step 1 — Parse the .jtl Files and Extract Key Metrics

JMeter `.jtl` files are CSV format. Read the header and data rows from each
file. The standard columns are:

```
timeStamp,elapsed,label,responseCode,responseMessage,threadName,
dataType,success,failureMessage,bytes,sentBytes,grpThreads,
allThreads,URL,Latency,IdleTime,Connect
```

For each `.jtl` file, compute and record the following metrics:

| Metric | Formula / Column |
|:-------|:----------------|
| **Total Requests** | Count of all rows |
| **Error Count** | Count where `success == false` |
| **Error Rate (%)** | `(Error Count / Total Requests) × 100` |
| **Throughput (RPS)** | `Total Requests / Total Duration (seconds)` |
| **Avg Response Time (ms)** | Mean of `elapsed` column |
| **Median Response Time (ms)** | Median of `elapsed` |
| **90th Percentile (ms)** | 90th percentile of `elapsed` |
| **95th Percentile (ms)** | 95th percentile of `elapsed` |
| **99th Percentile (ms)** | 99th percentile of `elapsed` |
| **Min / Max Response Time** | Min/Max of `elapsed` |
| **Total Duration (s)** | `(max(timeStamp) - min(timeStamp)) / 1000` |

Produce a summary table for each scenario (Load, Stress, Spike).

---

## Step 2 — Prompt AI to Analyse the Results

Use the following structured prompt sequence (NOT a single generic prompt):

### Prompt 2a — Context Setting
```
I am performing performance testing on an EShop REST API using JMeter.
The SUT is a Vietnamese e-commerce demo application with SQLite database.
I have three test scenarios: Load (normal traffic), Stress (above-normal
until breaking point), and Spike (sudden burst).

Here are the raw metrics I extracted from the .jtl logs:

[Paste the metrics tables from Step 1]

Please analyse these results and tell me:
1. Is the system's performance acceptable under Load conditions?
2. At what point does it degrade under Stress?
3. How does it recover from the Spike?
```

### Prompt 2b — Threshold Suggestions
```
Based on the metrics above, suggest appropriate performance thresholds
for this EShop API:
- Maximum acceptable average response time (ms)
- Maximum acceptable 95th percentile response time (ms)
- Maximum acceptable error rate (%)
- Recommended maximum concurrent users before degradation

Justify each threshold value with industry standards or the SUT's
observed behavior.
```

### Prompt 2c — Bottleneck Identification
```
Looking at the per-endpoint breakdown from the .jtl data:
[Paste per-label metrics if available]

Which endpoints are the bottlenecks? Which HTTP response codes appear
most frequently during stress/spike? What do you think causes the
degradation?
```

### Prompt 2d — Optimization Recommendations
```
Given the bottlenecks you identified, propose 5–8 specific optimizations
that could improve performance. For each optimization, describe:
- What it is
- How it addresses the bottleneck
- Whether it requires application code changes, database changes,
  infrastructure changes, or JMeter configuration changes
```

Record all AI outputs verbatim. They will be presented in `Report.md`
for human review.

---

## Step 3 — Update Report.md (Task 2 Sections)

After collecting the AI analysis output, update `Report.md`:

### Section 5.1 — AI Analysis of Results
Fill in with:
- The metrics tables from Step 1 (your own computation)
- The prompts used (verbatim, in order)
- The AI's responses (verbatim or clearly attributed quotes)

### Section 5.2 — Misinterpretation Hunt (Scaffold only)
Create a table with the AI's claims pre-populated, but leave the
"Correct Value" and "Error Explanation" columns blank — these require
human review:

```markdown
| # | AI Claim | Correct Value (from .jtl) | Error Explanation |
|:--|:---------|:--------------------------|:------------------|
| 1 | [AI stated X] | _[Human to fill]_ | _[Human to fill]_ |
| 2 | [AI stated Y] | _[Human to fill]_ | _[Human to fill]_ |
```

### Section 5.3 — Feasibility of AI Recommendations (Scaffold only)
Pre-populate with the AI's optimization suggestions, leave the verdict
and reasoning for human judgment:

```markdown
| # | AI Recommendation | Feasible / Hallucinated | Reasoning |
|:--|:-----------------|:-----------------------|:----------|
| 1 | [AI suggestion 1] | _[Human to fill]_ | _[Human to fill]_ |
| 2 | [AI suggestion 2] | _[Human to fill]_ | _[Human to fill]_ |
```

---

## Step 4 — Update AI_Audit.md

Record the AI interactions from Steps 2a–2d in `AI_Audit.md`:
- Prompt 2a (context + analysis request)
- Prompt 2b (threshold suggestions)
- Prompt 2c (bottleneck identification)
- Prompt 2d (optimization recommendations)

See the `hw5-ai-audit-update` skill for the detailed procedure.

---

## Validation

- [ ] Metrics tables filled for all 3 scenarios in Report.md Section 5.1
- [ ] AI prompts and responses documented in Section 5.1
- [ ] Section 5.2 table scaffolded with AI claims (awaiting human review)
- [ ] Section 5.3 table scaffolded with AI recommendations (awaiting human review)
- [ ] AI_Audit.md updated with this session's interactions
