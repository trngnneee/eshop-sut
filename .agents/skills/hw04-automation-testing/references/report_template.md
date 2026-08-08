# HW04 — Automation Testing Report

**Student ID:** {{STUDENT_ID}}
**Repository:** {{GITHUB_REPO_URL}}
**Tool stack:** Playwright | {{Chromium/Firefox/WebKit or Chrome/Edge/Firefox}} | {{Allure or Playwright HTML reporter}}

## 1. Feature Selection

| Pool | Feature | Reused from HW02? |
|---|---|---|
| A | FR-xx — ... | Yes / No (state reason if No) |
| B | FR-xx — ... | |
| C | FR-xx — ... | |

---

## 2. Feature A — FR-xx <name>

### 2.1 Test Cases (≥12)
| ID | Type (positive/negative/edge) | Description | Expected Result |
|---|---|---|---|
| TC-A-01 | positive | ... | ... |
| ... | | | |

### 2.2 Test Data
Location: `data/feature-a.csv` (or `.json`) — link/describe schema briefly.

### 2.3 AI-Driven Generation Process
Summarize the step-by-step prompting sequence used (link to the relevant AI Audit
Report entries by number, don't duplicate full prompts here).

### 2.4 Assertion Patterns Used
List the ≥3 distinct patterns used across this feature's spec (e.g. `toHaveText`,
`toHaveURL`, custom API check) with one example each.

### 2.5 Human Review — What the AI Got Wrong / Missed
| Issue | Category (selector/assertion/edge case/wait) | Fix applied | Likely cause |
|---|---|---|---|
| ... | ... | ... | prompt quality / model limitation / feature characteristic |

### 2.6 Execution Results
| Browser | Pass | Fail | HTML report link |
|---|---|---|---|
| Chromium | | | reports/feature-a-chromium/index.html |
| Firefox | | | |
| WebKit | | | |

### 2.7 Bugs Found (if any)
| Bug ID | Found by TC | Requirement | Severity/Priority | GitHub Issue |
|---|---|---|---|---|
| BUG-xxx | TC-xxx | FR-xx | e.g. Major/P1 | {{link}} |

Full details (steps, expected/actual, evidence) live in the linked GitHub Issue,
filed with `.github/ISSUE_TEMPLATE/bug_report.md` — don't duplicate the full write-up here.

### 2.8 Test Cases Not Automated (if any)
List and explain why.

---

## 3. Feature B — FR-xx <name>
(same structure as §2)

## 4. Feature C — FR-xx <name>
(same structure as §2)

---

## 5. Overall Summary

- Total features automated: 3
- Total test cases automated: {{n}} (min 36 across 3 features)
- Total browser runs: {{n}} (min 9)
- Total bugs filed: {{n}}
- Test cases not automated: {{n}}

## 6. AI Critique (200–300 words)
See `docs/ai-critique.md` (or paste inline here — check word count).

## 7. Appendix
- AI Audit Report: `docs/ai-audit-report.md`
- Bug Report: `docs/bug-report.md`
- Git commit log: `docs/commit-log.txt`
- Demo video: {{YouTube unlisted link}}