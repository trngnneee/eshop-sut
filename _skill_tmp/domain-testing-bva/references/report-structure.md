# HW02 Report Structure

## File: report.md (Main Report)

```markdown
# HW02 – Domain Testing Report
**Student ID**: <ID>  
**Feature**: <FR-xx> — <Name>  
**Date**: <YYYY-MM-DD>

---

## 1. Feature Overview
Brief description of the feature and why it was selected.

## 2. Domain Testing

### 2.1 Input Variables Identified
(Table of variables and constraints)

### 2.2 Equivalence Classes
(EP tables per variable)

### 2.3 Test Cases — Domain Testing
(Full TC table: TC-FRxx-DT-001 … )

### 2.4 Execution Results
(Fill Actual Result + Status after execution)

## 3. Boundary Value Analysis

### 3.1 Variables with Boundaries
(Which variables have numeric/length bounds)

### 3.2 BVA Point Tables
(ON/OFF/IN/OUT per boundary)

### 3.3 Test Cases — BVA
(Full TC table: TC-FRxx-BVA-001 … )

### 3.4 Execution Results
(Fill Actual Result + Status after execution)

## 4. Bug Reports
(One subsection per bug, using BUG-<FR>-<seq> format)

## 5. AI Gap Analysis
(See gap-analysis-template.md)

## 6. Test Summary

| Metric | Value |
|--------|-------|
| Feature | FR-xx |
| DT test cases designed | |
| BVA test cases designed | |
| Total test cases | |
| Passed | |
| Failed | |
| Not executed | |
| Bugs found | |

---

## Appendix A — AI Audit Report
(One entry per AI session, see SKILL.md Step 8)

## Appendix B — AI Critique
(200–300 words, see gap-analysis-template.md)
```

---

## File: README.md

```markdown
# HW02 – Domain Testing

## Self-Assessment Table

| No. | Criteria | Max | Self-Assessed |
|-----|----------|-----|--------------|
| 1 | Feature A (DT + BVA) | 25 | |
| 2 | Feature B (DT + BVA) | 25 | |
| 3 | Feature C (DT + BVA) | 25 | |
| 4 | Feature D – Mobile (DT + BVA) | 15 | |
| 5 | Agent Skills | 10 | |
| | **Total** | 100 | |

## Test Summary Report

| Feature | TC Designed | TC Executed | Passed | Failed | Not Exec | Bugs |
|---------|-------------|-------------|--------|--------|----------|------|
| FR-xx   | | | | | | |
| FR-xx   | | | | | | |
| FR-xx   | | | | | | |
| FR-xx   | | | | | | |
| **Total** | | | | | | |

## Demo Videos
- Feature A: <YouTube link>
- Feature B: <YouTube link>
- Feature C: <YouTube link>
- Feature D: <YouTube link>
- Agent Skill demo: <YouTube link>
```

---

## Submission Checklist

```
<StudentID>_HW02_AI_DomainTesting_<Grade>.zip
├── report.md               ← Main report (Markdown)
├── report.pdf              ← Main report (PDF export)
├── test-cases-DT.md        ← DT test case tables
├── test-cases-BVA.md       ← BVA test case tables
├── bug-report.md           ← Bug reports with GitHub Issue links
├── ai-audit.md             ← AI Audit Report (Markdown)
├── ai-audit.pdf            ← AI Audit Report (PDF)
├── ai-critique.md          ← 200–300 word critique
├── git-log.txt             ← Git commit log
├── README.md               ← Self-assessment + test summary
└── screenshots/            ← Bug screenshots
    ├── bug-FR01-001.png
    └── ...
```

## Git Commit Convention

One commit per major step, per feature:

```
git commit -m "FR01: identify input variables and constraints"
git commit -m "FR01: DT equivalence class table"  
git commit -m "FR01: DT test cases TC-FR01-DT-001 to TC-FR01-DT-012"
git commit -m "FR01: BVA point tables"
git commit -m "FR01: BVA test cases TC-FR01-BVA-001 to TC-FR01-BVA-010"
git commit -m "FR01: execute test cases, record results"
git commit -m "FR01: bug report BUG-FR01-001"
git commit -m "FR01: AI gap analysis and audit log"
```
